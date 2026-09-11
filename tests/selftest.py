#!/usr/bin/env python3
"""Suite de tests ILearnLinux : niveaux, correcteur, moteur, terminal, simulateurs.

Lance avec :  python3 tests/selftest.py   (depuis la racine du depot)
"""

import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from game import checker, engine, levels, progress  # noqa: E402
from game.terminal import Terminal  # noqa: E402


def _ev(check, ws, cmds, pwds):
    return checker.eval_check(check, ws, cmds, pwds)[0]

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  [OK] {}".format(name))
    else:
        FAIL += 1
        print("  [ECHEC] {}{}".format(name, " — {}".format(detail) if detail else ""))


def tmpdir():
    return tempfile.mkdtemp(prefix="ilearn-test-")


# ---------- niveaux ------------------------------------------------------
def t_levels():
    all_lv = levels.all_levels()
    check("1100 niveaux au total", len(all_lv) == 1100, "trouve {}".format(len(all_lv)))
    ids = [lv["id"] for lv in all_lv]
    check("ids continus 1..1100", ids == list(range(1, 1101)))
    errs = levels.validate()
    check("validate() sans erreur", not errs, "; ".join(errs[:3]))
    check("10 niveaux par jour", all(lv["day"] == (lv["id"] - 1) // 10 + 1 for lv in all_lv))
    ok = all(lv.get("title") and lv.get("mission") and lv.get("checks") for lv in all_lv)
    check("tous : titre + mission + objectifs", ok)
    scen_ok = True
    for lv in all_lv:
        if "scenario" in lv:
            try:
                json.dumps(lv["scenario"])
            except (TypeError, ValueError):
                scen_ok = False
    check("scenarios serialisables en JSON", scen_ok)
    n_scen = sum(1 for lv in all_lv if "scenario" in lv)
    check("35 missions avec cibles simulees", n_scen == 35, "trouve {}".format(n_scen))


# ---------- correcteur ---------------------------------------------------
def t_checker():
    ws = tmpdir()
    with open(os.path.join(ws, "a.txt"), "w") as fh:
        fh.write("bonjour FLAG{test}\n")
    os.mkdir(os.path.join(ws, "sub"))
    check("file_exists", _ev({"type": "file_exists", "path": "a.txt"}, ws, [], []))
    check("file_exists negatif", not _ev({"type": "file_exists", "path": "zzz"}, ws, [], []))
    check("file_contains texte",
          _ev({"type": "file_contains", "path": "a.txt", "text": "FLAG{test}"}, ws, [], []))
    check("file_contains regex",
          _ev({"type": "file_contains", "path": "a.txt", "regex": r"FLAG\{[a-z]+\}"}, ws, [], []))
    check("file_contains negatif",
          not _ev({"type": "file_contains", "path": "a.txt", "text": "zzz"}, ws, [], []))
    check("file_equals",
          _ev({"type": "file_equals", "path": "a.txt", "expected": "bonjour FLAG{test}\n"}, ws, [], []))
    check("file_not_empty", _ev({"type": "file_not_empty", "path": "a.txt"}, ws, [], []))
    check("not_exists", _ev({"type": "not_exists", "path": "zzz"}, ws, [], []))
    check("dir_exists", _ev({"type": "dir_exists", "path": "sub"}, ws, [], []))
    check("command match",
          _ev({"type": "command", "pattern": r"\bgrep\b"}, ws, ["grep x a.txt"], [ws]))
    check("command negatif",
          not _ev({"type": "command", "pattern": r"\bgrep\b"}, ws, ["ls"], [ws]))
    check("cwd match", _ev({"type": "cwd", "path": "sub"}, ws, [], [os.path.join(ws, "sub")]))
    check("eval_all tout vert",
          checker.eval_all([{"type": "file_exists", "path": "a.txt"},
                            {"type": "command", "pattern": "grep"}], ws, ["grep x"], [ws]) == [True, True])
    # apply_setup
    ws2 = tmpdir()
    checker.apply_setup([{"mkdir": "d1"}, {"file": "d1/f.txt", "content": "hi\n"},
                         {"file": "x.sh", "content": "#!/bin/bash\n", "mode": "755"}], ws2)
    check("setup mkdir+file", os.path.isfile(os.path.join(ws2, "d1", "f.txt")))
    check("setup mode", bool(os.stat(os.path.join(ws2, "x.sh")).st_mode & 0o100))
    checker.apply_setup([{"chmod": "x.sh", "mode": "644"}], ws2)
    check("setup chmod", not (os.stat(os.path.join(ws2, "x.sh")).st_mode & 0o100))
    checker.apply_setup([{"file": "abs", "content": "x"}], ws2)
    check("setup securise (relatif ok)", os.path.isfile(os.path.join(ws2, "abs")))


# ---------- progression --------------------------------------------------
def t_progress():
    d = tmpdir()
    old_base, old_file = progress.BASE_DIR, progress.PROGRESS_FILE
    progress.BASE_DIR = d
    progress.PROGRESS_FILE = os.path.join(d, "progress.json")
    try:
        prog = progress.load()
        check("progression par defaut", prog["current"] == 1 and prog["xp"] == 0)
        progress.record_completion(prog, 1, 10, 3, 0, False)
        check("completion avance + XP", prog["current"] == 2 and prog["xp"] == 10 and 1 in prog["done"])
        check("serie a 1", prog["streak"]["current"] == 1)
        progress.record_completion(prog, 2, 8, 5, 1, False)
        check("2e niveau meme jour : serie stable", prog["streak"]["current"] == 1)
        check("historique memorise", prog["history"]["2"]["hints"] == 1)
        a = progress.record_assist(prog, 3, "hint")
        check("indice comptabilise", a["hints"] == 1)
        progress.record_assist(prog, 3, "solution")
        check("solution comptabilisee", progress.get_assists(prog, 3)["solution"] is True)
        check("sauvegarde relisible", progress.load()["xp"] == 18)
    finally:
        progress.BASE_DIR, progress.PROGRESS_FILE = old_base, old_file


# ---------- moteur : garde-fous + mentor ---------------------------------
def t_engine():
    for bad in ["rm -rf /", "rm -rf / --no-preserve-root", "rm -rf ~", "sudo apt update",
                "su -", "passwd", "mkfs.ext4 /dev/sda", "dd if=x of=/dev/sda",
                "chmod -R 777 /", ":(){ :|:& };:"]:
        check("bloque: {}".format(bad[:24]), engine.blocked_command(bad) is not None)
    for ok in ["sudo -n -l", "rm -rf dossier/", "echo coucou", "nmap 10.10.0.5", "chmod +x m.sh"]:
        check("autorise: {}".format(ok[:24]), engine.blocked_command(ok) is None)
    for prog in ["vim", "nano fichier", "python3", "node", "top", "htop"]:
        check("alerte interactif: {}".format(prog), engine.interactive_warning(prog) is not None)
    for ok in ["top -b -n 1", "python3 -c 'print(1)'", "echo top", "grep -r x ."]:
        check("pas d'alerte: {}".format(ok[:24]), engine.interactive_warning(ok) is None)
    check("mentor fichier introuvable", "introuvable" in engine.mentor_react("cat z", "cat: z: No such file or directory", 1).lower()
          or "verifie" in engine.mentor_react("cat z", "cat: z: No such file or directory", 1).lower())
    check("mentor commande inconnue", "orthographe" in engine.mentor_react("gреп", "bash: gреп: command not found", 127))
    check("mentor ssh refuse", "ssh" in engine.mentor_react("ssh root@h", "Permission denied (publickey).", 255).lower())
    check("mentor grep silencieux", "grep" in engine.mentor_react("grep x f", "", 1).lower())


# ---------- terminal bash persistant -------------------------------------
def t_terminal():
    ws = tmpdir()
    term = Terminal(ws)
    try:
        r = term.run("echo hello-test")
        check("terminal echo", r["output"].strip() == "hello-test" and r["rc"] == 0 and not r["timed_out"], repr(r))
        r = term.run("mkdir sous && cd sous && pwd")
        check("terminal cwd persistant", r["cwd"] == os.path.join(ws, "sous") and "sous" in r["output"])
        r = term.run("pwd")
        check("terminal se souvient du dossier", r["cwd"] == os.path.join(ws, "sous"))
        r = term.run("cat fichier-qui-nexiste-pas")
        check("terminal code retour erreur", r["rc"] != 0 and "No such file" in r["output"])
        r = term.run("exit")
        check("terminal survit a exit", term.alive and r["cwd"] == ws)
        t2 = Terminal(ws, extra_env={"ILEARN_SCENARIO": "/tmp/x.json"})
        try:
            r = t2.run("echo $ILEARN_SCENARIO")
            check("terminal propage ILEARN_SCENARIO", r["output"].strip() == "/tmp/x.json")
            r = t2.run("which nmap")
            check("terminal trouve fakebin/nmap", "fakebin" in r["output"], r["output"].strip())
        finally:
            t2.stop()
    finally:
        term.stop()


# ---------- simulateurs --------------------------------------------------
def run_fake(name, args, scenario=None, stdin_text=None):
    env = dict(os.environ)
    if scenario is not None:
        path = os.path.join(tmpdir(), "scen.json")
        with open(path, "w") as fh:
            json.dump(scenario, fh)
        env["ILEARN_SCENARIO"] = path
    else:
        env.pop("ILEARN_SCENARIO", None)
    proc = subprocess.run([os.path.join(ROOT, "game", "fakebin", name)] + args,
                          input=stdin_text, capture_output=True, text=True, env=env, timeout=30)
    return proc


def t_relay():
    # Cas reel du jeu : input() lit en avance, puis Terminal.run() relaie
    # le clavier vers un programme interactif (ici : le ssh simule).
    scen = {"hosts": {"10.10.0.5": {
        "os": "Linux 5.15",
        "ports": [{"port": 22, "service": "ssh", "version": "OpenSSH 8.9", "state": "open"}],
        "users": ["agent"],
        "fs": {"home": {"agent": {"bienvenue.txt": "bienvenue agent\n"}}}}}}
    d = tmpdir()
    scen_path = os.path.join(d, "scen.json")
    with open(scen_path, "w") as fh:
        json.dump(scen, fh)
    child = (
        "import sys; sys.path.insert(0, {root!r}); "
        "from game.terminal import Terminal; "
        "cmd = input('prompt$ '); "
        "t = Terminal({d!r}, extra_env={{'ILEARN_SCENARIO': {s!r}}}); "
        "r = t.run(cmd); print(r['output']); print('RC:', r['rc'], 'TIMEOUT:', r['timed_out']); "
        "print('PUSHBACK:', t.pushback); t.stop()"
    ).format(root=ROOT, d=d, s=scen_path)
    proc = subprocess.run([sys.executable, "-c", child],
                          input="ssh agent@10.10.0.5\nls\ncat bienvenue.txt\nexit\nLIGNE-POUR-LE-JEU\n",
                          capture_output=True, text=True, timeout=60)
    check("relais : session complete", "bienvenue agent" in proc.stdout and "logout" in proc.stdout,
          proc.stdout[:200] + proc.stderr[:200])
    check("relais : rc 0 sans timeout", "RC: 0 TIMEOUT: False" in proc.stdout)
    check("relais : ligne jeu rendue", "PUSHBACK: ['LIGNE-POUR-LE-JEU']" in proc.stdout, proc.stdout[-200:])


def t_nmap():
    scen = {"hosts": {"10.10.0.5": {
        "os": "Linux 5.15",
        "ports": [{"port": 22, "service": "ssh", "version": "OpenSSH 8.9p1", "state": "open"},
                  {"port": 23, "service": "telnet", "version": "", "state": "filtered"}]}}}
    p = run_fake("nmap", ["10.10.0.5"], scen)
    check("nmap host up + port 22", "Host is up" in p.stdout and "22/tcp" in p.stdout and "open" in p.stdout, p.stdout[:200])
    p = run_fake("nmap", ["-sV", "10.10.0.5"], scen)
    check("nmap -sV versions", "OpenSSH 8.9p1" in p.stdout)
    check("nmap filtered", "filtered" in run_fake("nmap", ["10.10.0.5"], scen).stdout)
    p = run_fake("nmap", ["-O", "10.10.0.5"], scen)
    check("nmap -O systeme", "Linux" in p.stdout)
    p = run_fake("nmap", ["10.10.0.99"], scen)
    check("nmap hote inconnu = down", "down" in p.stdout.lower())
    p = run_fake("nmap", ["10.10.0.5"])
    check("nmap sans scenario = erreur claire", p.returncode != 0 and "ILEARN" in (p.stdout + p.stderr))


def t_ssh():
    scen = {"hosts": {"10.10.0.5": {
        "os": "Linux 5.15",
        "ports": [{"port": 22, "service": "ssh", "version": "OpenSSH 8.9", "state": "open"}],
        "users": ["agent"],
        "banner": "Welcome to Ubuntu 22.04 LTS (GNU/Linux)",
        "fs": {"home": {"agent": {"flag.txt": "FLAG{ssh-1}\n", ".cache": {"n.txt": "x\n"}}}}}}}
    p = run_fake("ssh", ["root@10.10.0.5"], scen)
    check("ssh mauvais user refuse", p.returncode == 255 and "Permission denied" in p.stderr, p.stderr.strip())
    p = run_fake("ssh", ["agent@10.10.9.9"], scen)
    check("ssh hote inconnu refuse", p.returncode == 255)
    p = run_fake("ssh", ["nimportequoi"], scen)
    check("ssh sans @ = aide", p.returncode != 0 and "ssh" in (p.stdout + p.stderr).lower())
    p = run_fake("ssh", ["-i", "macle", "agent@10.10.0.5"], scen, stdin_text="whoami\npwd\ncat flag.txt\nexit\n")
    check("ssh session whoami/pwd/cat", "agent" in p.stdout and "FLAG{ssh-1}" in p.stdout, p.stdout[:300])
    check("ssh marqueur interactif", "__ILEARN_IX__" in p.stdout)
    check("ssh banniere", "Ubuntu" in p.stdout)
    p = run_fake("ssh", ["agent@10.10.0.5"], scen, stdin_text="ls -a\ncat .cache/n.txt\nexit\n")
    check("ssh fichiers caches distants", ".cache" in p.stdout)
    p = run_fake("ssh", ["agent@10.10.0.5"], scen, stdin_text="cd /tmp\nexit\n")
    check("ssh rc zero", p.returncode == 0)


def t_john():
    d = tmpdir()
    words = os.path.join(d, "mots.txt")
    with open(words, "w") as fh:
        fh.write("chat\nsoleil\nchien\n")
    h = os.path.join(d, "hash.txt")
    with open(h, "w") as fh:
        fh.write("admin:23206deb7eba65b3fbc80a2ffbc53c28\n")  # md5(soleil)
    p = run_fake("john", ["--wordlist=" + words, h])
    check("john craque md5(soleil)", "soleil" in p.stdout and "1 password hash cracked" in p.stdout, p.stdout[:300])
    h2 = os.path.join(d, "h2.txt")
    with open(h2, "w") as fh:
        fh.write("x:de05930dd46a984ca32aad9feac718e8\n")  # md5(supernova)
    p = run_fake("john", ["--wordlist=" + words, h2])
    check("john 0 cracked si absent", "0 password hashes cracked" in p.stdout)
    p = run_fake("john", [h])
    check("john exige --wordlist", p.returncode != 0 and "wordlist" in (p.stdout + p.stderr).lower())


def t_fakeremote_direct():
    from game import fakeremote  # noqa: E402
    fs = {"home": {"agent": {"flag.txt": "FLAG{x}\n", ".c": {"n": "w\n"}}}}
    sh = fakeremote.RemoteShell("10.10.0.5", "agent", fs)
    check("RemoteShell demarre au home", sh.execute("pwd").strip() == "/home/agent")
    check("RemoteShell ls cache les caches", ".c" not in sh.execute("ls").split())
    check("RemoteShell ls -a", ".c" in sh.execute("ls -a") and "flag.txt" in sh.execute("ls -a"))
    check("RemoteShell cat", sh.execute("cat flag.txt").strip() == "FLAG{x}")
    sh.execute("cd .c")
    check("RemoteShell cd+pwd", sh.execute("pwd").strip() == "/home/agent/.c")
    check("RemoteShell whoami/id", "agent" in sh.execute("whoami") and "uid=" in sh.execute("id"))
    check("RemoteShell exit", sh.execute("exit") == "__EXIT__")
    check("RemoteShell commande inconnue", "command not found" in sh.execute("nmap"))


def main():
    global PASS, FAIL
    print("== ILearnLinux : auto-tests ==")
    for func in (t_levels, t_checker, t_progress, t_engine, t_terminal, t_relay, t_nmap, t_ssh, t_john, t_fakeremote_direct):
        print("-- {} --".format(func.__name__))
        try:
            func()
        except Exception as exc:  # noqa: BLE001
            FAIL += 1
            import traceback
            traceback.print_exc()
            print("  [ECHEC] exception dans {} : {}".format(func.__name__, exc))
    print("== resultat : {} OK, {} ECHEC ==".format(PASS, FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
