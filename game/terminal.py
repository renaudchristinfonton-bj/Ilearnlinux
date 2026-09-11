"""Terminal de mission : un VRAI bash persistant, pilote par le jeu.

Le joueur tape de VRAIES commandes, executees par un VRAI bash dans le
dossier de la mission. Le jeu recupere la sortie, le code retour et le
dossier courant apres chaque commande.

Protocole : apres chaque commande, le jeu envoie une ligne sentinelle qui
affiche le code retour, le dossier courant, puis une marque de fin.
Les outils simules (nmap/ssh/john de game/fakebin) peuvent demander un
mode interactif (relais clavier) via une marque speciale.

Securite : le shell tourne en tant que simple utilisateur, et le moteur
bloque les commandes destructrices avant execution (voir engine.py).
"""

import os
import select
import shutil
import subprocess
import sys
import tempfile
import time

RC_PREFIX = "__ILEARN_RC__:"
END_MARK = "__ILEARN_END__"
IX_MARK = "__ILEARN_IX__"
TAIL_KEEP = 512


class Terminal:
    def __init__(self, cwd, extra_env=None, idle_timeout=20.0, relay_timeout=600.0,
                 pushback=None):
        # pushback : liste partagee (optionnelle) qui recoit les lignes lues
        # au clavier mais non relayees (destinees au jeu, collees en avance).
        self.root = os.path.abspath(cwd)
        self.extra_env = dict(extra_env or {})
        self.idle_timeout = idle_timeout
        self.relay_timeout = relay_timeout
        self.current_dir = self.root
        self.proc = None
        self._run_id = 0
        self._fifodir = tempfile.mkdtemp(prefix="ilearn-")
        self.pushback = pushback if pushback is not None else []
        self._spawn()

    # -- cycle de vie -------------------------------------------------
    def _spawn(self):
        env = dict(os.environ)
        fakebin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakebin")
        env["PATH"] = fakebin + os.pathsep + env.get("PATH", "")
        env["PS1"] = ""
        env["TERM"] = "dumb"
        env.pop("PROMPT_COMMAND", None)
        env.update(self.extra_env)
        self.proc = subprocess.Popen(
            ["bash", "--noprofile", "--norc"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            cwd=self.root, env=env, bufsize=0, start_new_session=True)
        os.set_blocking(self.proc.stdout.fileno(), False)
        self.current_dir = self.root

    @property
    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def stop(self):
        try:
            if self.alive:
                self.proc.kill()
                self.proc.wait(timeout=5)
        except Exception:
            pass
        try:
            shutil.rmtree(self._fifodir, ignore_errors=True)
        except Exception:
            pass

    def restart(self):
        self.stop()
        self._spawn()

    # -- execution ----------------------------------------------------
    def _send(self, data):
        try:
            self.proc.stdin.write(data.encode("utf-8", "replace"))
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError, ValueError):
            self._spawn()
            self.proc.stdin.write(data.encode("utf-8", "replace"))
            self.proc.stdin.flush()

    def run(self, command, on_output=None):
        """Execute une commande.

        on_output(chunk) est appele au fil de l'eau avec le texte affiche.
        Retourne {"output", "rc", "cwd", "timed_out"}.
        """
        if not self.alive:
            self._spawn()
        # Une SEULE ligne : bash analyse tout avant d'executer. Ainsi, un
        # programme interactif (ssh) ne mange jamais la sentinelle comme entree.
        # Le groupe { ...; } (pas un sous-shell) preserve cd/pwd.
        # Le stdin vient d'un tube jetable par commande : les lignes relayees
        # en trop (collees par erreur) y meurent au lieu de s'executer dans bash.
        self._run_id += 1
        fifo = os.path.join(self._fifodir, "in-{}".format(self._run_id))
        rfd = None
        try:
            os.mkfifo(fifo)
            rfd = os.open(fifo, os.O_RDWR | os.O_NONBLOCK)
        except OSError:
            fifo = None
            rfd = None
        line = command.strip() or ":"
        if fifo is not None:
            self._send("{{ {0}; }} <'{1}'; echo \"{2}$?\"; pwd; echo \"{3}\"\n".format(
                line, fifo, RC_PREFIX, END_MARK))
        else:  # Repli (improbable) : pas de relais sans tube jetable.
            self._send("{{ {0}; }}; echo \"{1}$?\"; pwd; echo \"{2}\"\n".format(
                line, RC_PREFIX, END_MARK))

        buf = b""
        printed = 0
        shown = 0
        interactive = False
        start = time.time()
        last_activity = start
        fwd_mark = 0
        last_fwd = 0.0
        pending = []
        done = False
        ending = False
        seen = -1
        out_fd = self.proc.stdout.fileno()
        result = None

        def emit(upto):
            nonlocal printed, shown
            if upto > printed and on_output is not None:
                chunk = buf[printed:upto].decode("utf-8", "replace")
                chunk = chunk.replace(IX_MARK, "").replace(END_MARK, "")
                if chunk:
                    on_output(chunk)
                    shown += len(chunk)
            printed = max(printed, upto)

        try:
            while True:
                if len(buf) != seen:
                    seen = len(buf)
                    done = self._finished(buf)
                if done:
                    break
                if not self.alive and END_MARK.encode() not in buf:
                    # Le shell est mort (ex: commande 'exit') : on le relance.
                    self._spawn()
                    break
                now = time.time()
                if interactive:
                    if now - last_activity > 180 or now - start > self.relay_timeout:
                        result = self._timeout(buf, shown, on_output)
                        break
                    wait = 0.05
                else:
                    if now - start > self.idle_timeout:
                        result = self._timeout(buf, shown, on_output)
                        break
                    wait = 0.2
                want_stdin = interactive and rfd is not None
                rlist = [out_fd] + ([sys.stdin] if want_stdin else [])
                try:
                    ready, _, _ = select.select(rlist, [], [], wait)
                except (OSError, ValueError):
                    ready = []
                if out_fd in ready:
                    try:
                        chunk = os.read(out_fd, 4096)
                    except (OSError, BlockingIOError):
                        chunk = b""
                    if chunk:
                        buf += chunk
                        last_activity = time.time()
                        if IX_MARK.encode() in buf:
                            interactive = True
                        if not ending and RC_PREFIX.encode() in buf:
                            # La sentinelle tourne : le programme interactif a
                            # QUITTE, il ne lira plus jamais. Ne plus relayer.
                            ending = True
                        # Afficher tout sauf une queue (marqueur peut-etre coupe).
                        if len(buf) > printed + TAIL_KEEP:
                            emit(len(buf) - TAIL_KEEP)
                    elif not self.alive:
                        break
                if want_stdin and sys.stdin in ready:
                    # readline() voit TOUT : les lignes deja lues par input()
                    # (collage multi-lignes) + le clavier. select a dit lisible,
                    # donc ca ne bloque pas (ligne complete ou EOF).
                    try:
                        line_in = sys.stdin.readline()
                    except OSError:
                        line_in = ""
                    if line_in:
                        if len(pending) < 10000:
                            pending.append(line_in)
                    else:
                        time.sleep(0.05)
                # Relais RYTHME : on n'envoie la ligne suivante que quand le
                # programme distant affiche un nouveau prompt ('$ ' = pret pour
                # la saisie), ou apres 0.8 s sans reponse (securite). Apres
                # 'exit' il n'y a jamais de nouveau prompt : les lignes
                # destinees au JEU ne partent donc jamais, elles lui sont rendues.
                if pending and interactive and not done and not ending:
                    tail = buf[fwd_mark:].decode("utf-8", "replace")
                    ready = tail.endswith("$ ")
                    patient = time.time() - last_fwd > 0.8
                    if ready or patient:
                        fwd_mark = len(buf)
                        last_fwd = time.time()
                        payload = pending.pop(0).encode("utf-8", "replace")
                        while payload:
                            if done or ending:
                                payload = b""
                                break
                            try:
                                written = os.write(rfd, payload)
                                payload = payload[written:]
                                last_activity = time.time()
                            except BlockingIOError:
                                # Tube plein : drainer la sortie (fin de session ?).
                                try:
                                    extra = os.read(out_fd, 4096)
                                except OSError:
                                    extra = b""
                                if extra:
                                    buf += extra
                                    last_activity = time.time()
                                    if not ending and RC_PREFIX.encode() in buf:
                                        ending = True
                                    if len(buf) > printed + TAIL_KEEP:
                                        emit(len(buf) - TAIL_KEEP)
                                    done = self._finished(buf)
                                else:
                                    time.sleep(0.02)
        finally:
            if rfd is not None:
                try:
                    os.close(rfd)
                except OSError:
                    pass
            if fifo is not None:
                try:
                    os.unlink(fifo)
                except OSError:
                    pass
        if pending:
            # Lignes lues mais jamais relayees : elles sont pour le JEU
            # (collees apres 'exit') -> on les lui rend, sans le \n final.
            self.pushback.extend(p.rstrip("\n") for p in pending)
        if result is not None:
            return result
        return self._finish(buf, shown, on_output)

    def _finished(self, buf):
        try:
            text = buf.decode("utf-8", "replace")
        except ValueError:
            return False
        return END_MARK in text and RC_PREFIX in text.split(END_MARK)[0]

    def _timeout(self, buf, shown, on_output):
        text = buf.decode("utf-8", "replace")
        clean = text.replace(IX_MARK, "")
        if on_output is not None:
            tail = clean[shown:]
            if tail:
                on_output(tail)
        self.restart()
        return {"output": clean, "rc": 124, "cwd": self.root, "timed_out": True}

    def _finish(self, buf, shown, on_output):
        text = buf.decode("utf-8", "replace")
        rc, cwd, output = 0, self.root, text
        if RC_PREFIX in text:
            before, _, after = text.partition(RC_PREFIX)
            rc_part, _, rest = after.partition("\n")
            try:
                rc = int(rc_part.strip())
            except ValueError:
                rc = 0
            cwd_line, _, _ = rest.partition("\n")
            cwd_line = cwd_line.strip()
            if cwd_line:
                cwd = cwd_line
            output = before.replace(IX_MARK, "")
            # Afficher la queue mise en attente (sans les lignes protocole).
            if on_output is not None:
                chunk = output[shown:]
                if chunk:
                    on_output(chunk)
        else:
            if on_output is not None:
                rest = text.replace(IX_MARK, "")[shown:]
                if rest:
                    on_output(rest)
        self.current_dir = cwd
        if not self.alive:
            self._spawn()
            cwd = self.root
            self.current_dir = cwd
        return {"output": output, "rc": rc, "cwd": cwd, "timed_out": False}
