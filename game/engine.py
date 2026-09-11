"""Moteur de jeu : UN terminal, des VRAIES commandes, un mentor qui guide.

Le joueur tape de vraies commandes Linux, executees pour de vrai dans le
dossier de la mission. Le mentor reagit aux erreurs, donne des indices,
et valide les objectifs en continu (facon Duolingo).
"""

import json
import os
import re
import shutil
import sys

from . import certs, checker, levels, progress, ui
from .terminal import Terminal

# Commandes du jeu (interceptees, jamais executees par bash).
GAME_HELP = ("aide", "help", "?")
GAME_MISSION = ("mission",)
GAME_COURSE = ("cours", "lecon", "leçon")
GAME_HINT = ("indice", "hint", "aide-moi")
GAME_SOLUTION = ("solution", "sol")
GAME_QUIT = ("quitter", "quit", "exit", "logout", "q")


def prepare_mission(level):
    """(Re)cree le dossier de mission. Retourne (chemin, scenario_path ou None)."""
    ws = progress.arena_path(level["id"])
    base = os.path.realpath(progress.ARENA_DIR)
    target = os.path.realpath(ws)
    if os.path.commonpath([base, target]) != base:
        raise RuntimeError("chemin de mission refuse : {}".format(ws))
    if os.path.isdir(ws):
        shutil.rmtree(ws)
    os.makedirs(ws, exist_ok=True)
    checker.apply_setup(level.get("setup", []), ws)
    scenario_path = None
    if level.get("scenario"):
        scenario_path = os.path.join(ws, "scenario.json")
        with open(scenario_path, "w", encoding="utf-8") as fh:
            json.dump(level["scenario"], fh, indent=2)
    return ws, scenario_path


def display_path(cwd, root):
    cwd = os.path.realpath(cwd)
    root = os.path.realpath(root)
    if cwd == root:
        return "~"
    if cwd.startswith(root + os.sep):
        return "~/" + os.path.relpath(cwd, root)
    return cwd


# -- garde-fous --------------------------------------------------------
def blocked_command(cmd):
    """Detecte les commandes dangereuses ou inutilisables ici.

    Retourne un message du mentor si la commande est refusee, None sinon.
    """
    s = cmd.strip()
    if re.match(r"^\s*sudo(\s|;|&&|\|\||$)", s) and "-n" not in s:
        return ("'sudo' demanderait un mot de passe ici : refuse. Bonne nouvelle : "
                "aucune mission n'a besoin de sudo ! (Et 'sudo -n ...' reste autorise.)")
    if re.match(r"^\s*su(\s|;|&&|\|\||$)", s):
        return "'su' changerait d'utilisateur : inutile ici, tout se passe en agent."
    if re.match(r"^\s*passwd(\s|;|$)", s):
        return "Pas touche aux mots de passe du systeme ! Ici, on s'entraine sans risque."
    if re.search(r":\s*\(\s*\)\s*\{", s):
        return "Oh non, une fork-bomb ! Refuse, evidemment. (Et ne tape jamais ca ailleurs.)"
    if re.search(r"\brm\s+[^\n;|&]*-[a-zA-Z]*r[a-zA-Z]*f\s+/(?:\s|;|$)", s):
        return "REFUSE : 'rm -rf /' effacerait tout le systeme. Retiens : on ne tape JAMAIS ca."
    if re.search(r"\brm\s+[^\n;|&]*-[a-zA-Z]*r[a-zA-Z]*f\s+~(?:\s|;|/|$)", s):
        return "REFUSE : ca effacerait ton dossier personnel ! 'rm -rf' + chemin douteux = danger."
    if re.match(r"^\s*mkfs\b", s):
        return "REFUSE : mkfs formate un disque. Pas dans ce jeu, pas comme ca !"
    if re.search(r"\bdd\b[^\n;|&]*of=/dev/", s):
        return "REFUSE : 'dd' vers /dev/... peut detruire un disque. Dangereux, meme pour de vrai."
    if re.search(r"\bchmod\s+-R\b[^\n;|&]*\s/(?:\s|;|$)", s):
        return "REFUSE : 'chmod -R' sur / casserait tout le systeme. On reste dans la mission !"
    return None


def interactive_warning(cmd):
    """Programmes interactifs qui ne marchent pas dans ce terminal. Message ou None."""
    s = cmd.strip()
    first = s.split()[0] if s.split() else ""
    base = os.path.basename(first)
    if base in ("python3", "python", "ipython", "node", "irb") and s.strip() == base:
        return ("'{}' seul ouvrirait un interpreteur interactif : utilise plutot {} -c '...'.".format(base, base))
    if base in ("vim", "vi", "nano", "emacs", "pico", "ne"):
        return ("Pas d'editeur interactif ici : fabrique tes fichiers avec echo/printf et les redirections !")
    if base in ("htop", "telnet", "ftp", "mysql", "psql", "sqlite3") and s.strip() == base:
        return "'{}' est interactif : indisponible dans ce terminal de mission.".format(base)
    if base == "top" and "-b" not in s:
        return "Utilise 'top -b -n 1' (mode non-interactif) au lieu de 'top' seul."
    return None


def mentor_react(cmd, output, rc):
    """Message du mentor apres une commande en echec. Retourne le texte."""
    out = output or ""
    low = out.lower()
    if "no such file or directory" in low:
        if cmd.strip().startswith("cd"):
            return ("Ce dossier n'existe pas (ou tu n'es pas au bon endroit). "
                    "Essaie 'ls' pour voir, 'pwd' pour savoir ou tu es.")
        return ("Fichier ou dossier introuvable. Verifie le nom avec 'ls' (majuscules, fautes de frappe...).")
    if "permission denied" in low:
        if "publickey" in low:
            return ("Connexion refusee : mauvais utilisateur ? La forme est 'ssh UTILISATEUR@CIBLE'.")
        return ("Permission refusee : il manque un droit. 'ls -l' montre les droits ; "
                "si c'est un script a toi, pense a 'chmod +x'.")
    if "command not found" in out:
        return ("Commande inconnue : verifie l'orthographe. (Et 'aide' liste les commandes du JEU : "
                "indice, solution, mission, quitter...)")
    if "is a directory" in out:
        return "C'est un dossier, pas un fichier : explore-le avec 'ls' au lieu de le lire."
    if "not a directory" in out:
        return "Un morceau de ton chemin n'est pas un dossier : verifie chaque etape avec 'ls'."
    if "could not resolve" in low or "name or service not known" in low:
        return "Hote inconnu : verifie l'adresse IP ou le nom (une faute de frappe, vite arrivee !)."
    if "missing operand" in out or "missing destination" in out:
        return "Il manque un argument a ta commande. Relis la mission (tape 'mission')."
    if "omitting directory" in out:
        return "grep saute les dossiers : ajoute -r pour fouiller dedans (grep -r ...)."
    if "invalid option" in out or "unrecognized option" in out or "unknown option" in out:
        return "Option inconnue : 'TA-COMMANDE --help' liste les vraies options."
    if "fopen:" in out and "no such file" in low:
        return "Fichier introuvable : verifie le nom avec 'ls'."
    if rc != 0 and not out.strip() and cmd.strip().startswith("grep"):
        return ("grep n'a rien trouve (et le dit en se taisant). Verifie le mot cherche et le fichier vise.")
    if rc != 0 and not out.strip():
        return ("Cette commande a echoue sans message. Verifie chaque argument... ou tape 'indice'.")
    return ("Raté, mais c'est comme ca qu'on apprend ! Lis le message d'erreur : il dit souvent la solution. "
            "(Et 'indice' est la si tu bloques.)")


TIMEOUT_TIP = ("Commande interrompue : elle ne se terminait pas (ping sans -c ? programme interactif ?). "
               "Astuce d'agent : 'ping -c 2 ...', 'top -b -n 1', et Ctrl+C en vrai terminal.")


def stash_input(stash, prompt):
    """Lit une ligne : d'abord celles rendues par le relais clavier (collees
    en avance), sinon une vraie saisie. Les lignes rendues sont re-affichees
    comme si elles venaient d'etre tapees."""
    if stash:
        line = stash.pop(0)
        sys.stdout.write(prompt + line + "\n")
        sys.stdout.flush()
        return line
    return input(prompt)


def play_level(level, prog, stash):
    """Boucle interactive d'un niveau. Retourne 'done' ou 'quit'."""
    total = levels.total()
    ws, scenario_path = prepare_mission(level)
    total_xp = prog.get("xp", 0)
    streak = prog.get("streak", {}).get("current", 0)
    ui.mission_panel(level, ws, total_xp, streak, total)

    env = {"ILEARN_SCENARIO": scenario_path or ""}
    term = Terminal(ws, extra_env=env, pushback=stash)
    typed, pwds, history = [], [], []
    faults = 0
    assists = progress.get_assists(prog, level["id"])
    hints_used = assists.get("hints", 0)
    solution_used = assists.get("solution", False)
    auto_hint_stage = 0

    import time as _time
    start = _time.time()
    ui.info("A toi de jouer : tape de VRAIES commandes ci-dessous. ('aide' = commandes du jeu)")
    ui.objectives([False] * len(level.get("checks", [])))

    def show_next_hint(auto=False):
        nonlocal hints_used
        if auto:
            ui.mentor("Je vois que tu galeres... prends ceci :")
        if ui.show_hint(level.get("hints", []), hints_used):
            hints_used += 1
            progress.record_assist(prog, level["id"], "hint")

    try:
        while True:
            try:
                line = stash_input(stash, ui.prompt_str(display_path(term.current_dir, ws)))
            except EOFError:
                print()
                return "quit"
            except KeyboardInterrupt:
                print()
                ui.info("(Ctrl+C : tape 'quitter' pour faire une pause)")
                continue
            s = line.strip()
            if not s:
                continue
            low = s.lower()
            if low in GAME_HELP:
                ui.game_help()
                continue
            if low in GAME_MISSION:
                ui.mission_recap(level)
                continue
            if low in GAME_COURSE:
                ui.lesson_card(level)
                continue
            if low in GAME_HINT:
                show_next_hint()
                continue
            if low in GAME_SOLUTION:
                ui.show_solution(level.get("solution", ""))
                if not solution_used:
                    solution_used = True
                    progress.record_assist(prog, level["id"], "solution")
                continue
            if low in GAME_QUIT:
                return "quit"
            if low == "history":
                for i, h in enumerate(history, 1):
                    print("  {}  {}".format(i, h))
                typed.append(s)
                pwds.append(term.current_dir)
                history.append(s)
            elif low == "clear":
                print("\033[2J\033[H", end="")
                ui.info("NIVEAU {} - {} (tape 'mission' pour revoir l'objectif)".format(level["id"], level["title"]))
                typed.append(s)
                pwds.append(term.current_dir)
                history.append(s)
            else:
                refusal = blocked_command(s)
                if refusal:
                    ui.mentor(refusal)
                    continue
                warn = interactive_warning(s)
                if warn:
                    ui.mentor(warn)
                    continue
                try:
                    res = term.run(s, on_output=lambda chunk: (sys.stdout.write(chunk), sys.stdout.flush()))
                except KeyboardInterrupt:
                    print()
                    term.restart()
                    ui.mentor("Commande interrompue (Ctrl+C). A toi !")
                    continue
                if res["output"] and not res["output"].endswith("\n"):
                    print()
                typed.append(s)
                history.append(s)
                pwds.append(res["cwd"])
                if res["timed_out"]:
                    faults += 1
                    ui.mentor(TIMEOUT_TIP)
                elif res["rc"] != 0:
                    faults += 1
                    ui.mentor(mentor_react(s, res["output"], res["rc"]))
                # Le mentor aide automatiquement quand ca coince vraiment.
                if faults >= 4 and auto_hint_stage == 0 and hints_used < len(level.get("hints", [])):
                    auto_hint_stage = 1
                    show_next_hint(auto=True)
                elif faults >= 8 and auto_hint_stage == 1 and hints_used < len(level.get("hints", [])):
                    auto_hint_stage = 2
                    show_next_hint(auto=True)
            states = checker.eval_all(level.get("checks", []), ws, typed, pwds)
            ui.objectives(states)
            if all(states):
                elapsed = _time.time() - start
                xp = level.get("xp", 10) - faults - 2 * hints_used
                if solution_used:
                    xp = 2
                xp = max(2, xp)
                progress.record_completion(prog, level["id"], xp, len(typed), hints_used, solution_used)
                ui.celebrate(level, xp, prog.get("xp", 0), elapsed, len(typed),
                             prog.get("streak", {}).get("current", 0), faults)
                for cert in certs.newly_earned(prog):
                    name = certs.ask_profile_name(prog)
                    code, svg_path, _html = certs.issue(prog, cert, name, certs_today())
                    ui.cert_celebrate(cert, code, svg_path)
                return "done"
    finally:
        term.stop()


def certs_today():
    import datetime
    return datetime.date.today().strftime("%d/%m/%Y")


def play_loop(start_level=None):
    """Enchaine les niveaux jusqu'a quitter ou finir le jeu."""
    total = levels.total()
    prog = progress.load()
    stash = []
    current = prog.get("current", 1) if start_level is None else start_level
    if current > total:
        ui.banner()
        ui.success("Tu as termine les {} niveaux ! Tu es une legende.".format(total))
        return
    ui.banner()
    while current <= total:
        level = levels.get_level(current)
        if level is None:
            ui.error("niveau {} introuvable.".format(current))
            return
        result = play_level(level, prog, stash)
        if result == "quit":
            ui.info("Partie sauvegardee au niveau {}. A demain pour la serie !".format(level["id"]))
            return
        current = progress.load().get("current", current + 1)
        if current > total:
            ui.success("Mission accomplie : {}/{} niveaux. Respect, agent.".format(total, total))
            return
        try:
            answer = stash_input(stash, ui.paint("Entree = niveau suivant  |  q = pause : ", ui.C.YELLOW))
        except (EOFError, KeyboardInterrupt):
            print()
            ui.info("Partie sauvegardee. A bientot !")
            return
        if answer.strip().lower() in ("q", "quit", "exit"):
            ui.info("Partie sauvegardee au niveau {}. A demain pour la serie !".format(current))
            return
