"""Moteur de jeu : affiche le niveau et surveille l'arene en continu.

Principe : le jeu tourne dans un onglet, le joueur joue dans un autre.
Le moteur prepare l'arene, puis verifie les objectifs chaque seconde
jusqu'a reussite (validation automatique, facon Duolingo).
"""

import os
import shutil
import sys
import time

from . import checker, levels, progress, ui

try:
    import select as _select
    _HAS_SELECT = hasattr(_select, "select")
except ImportError:
    _select = None
    _HAS_SELECT = False


def prepare_arena(level):
    """(Re)cree l'arene du niveau et applique le setup. Retourne le chemin."""
    ws = progress.arena_path(level["id"])
    base = os.path.realpath(progress.ARENA_DIR)
    target = os.path.realpath(ws)
    # Securite : on ne nettoie que DANS le dossier d'arene.
    if os.path.commonpath([base, target]) != base:
        raise RuntimeError("chemin d'arene refuse : {}".format(ws))
    if os.path.isdir(ws):
        shutil.rmtree(ws)
    os.makedirs(ws, exist_ok=True)
    checker.apply_setup(level.get("setup", []), ws)
    return ws


def _stdin_has_data(timeout):
    if not _HAS_SELECT:
        return False
    try:
        r, _, _ = _select.select([sys.stdin], [], [], timeout)
        return bool(r)
    except (OSError, ValueError):
        return False


def _read_stdin_line():
    try:
        return sys.stdin.readline()
    except (OSError, ValueError):
        return ""


def _needs_commands(level):
    return any(c.get("type") in ("command", "cwd") for c in level.get("checks", []))


def play_level(level, prog):
    """Boucle de surveillance d'un niveau. Retourne 'done', 'quit' ou 'skip'."""
    ws = prepare_arena(level)
    total_xp = prog.get("xp", 0)
    streak = prog.get("streak", {}).get("current", 0)
    ui.level_card(level, ws, total_xp, streak)

    _, offset = progress.read_new_log_lines(0)
    try:
        offset = os.path.getsize(progress.COMMANDS_LOG)
    except OSError:
        offset = 0
    new_commands, new_pwds = [], []
    hints_used = 0
    solution_used = False
    assists = progress.get_assists(prog, level["id"])
    hints_used = assists.get("hints", 0)
    solution_used = assists.get("solution", False)

    start = time.time()
    last_hook_warning = 0.0
    states = [False] * len(level.get("checks", []))
    print(ui.paint("  Je surveille ton onglet JOUEUR... a toi de jouer !", ui.C.DIM))
    time.sleep(0.4)

    while True:
        if _stdin_has_data(1.0):
            line = _read_stdin_line()
            if line == "":
                print()
                ui.info("Entree fermee : pause du jeu. Relance avec ./ilearn play.")
                return "quit"
            cmd = line.strip().lower()
            if cmd in ("h", "hint", "aide", "indice"):
                if ui.show_hint(level.get("hints", []), hints_used):
                    hints_used += 1
                    progress.record_assist(prog, level["id"], "hint")
            elif cmd in ("s", "solution", "sol"):
                ui.show_solution(level.get("solution", ""))
                if not solution_used:
                    solution_used = True
                    progress.record_assist(prog, level["id"], "solution")
            elif cmd in ("m", "mission"):
                ui.mission_recap(level)
            elif cmd in ("q", "quit", "exit", "quitter"):
                return "quit"
            elif cmd == "":
                pass
            else:
                ui.info("Commandes du jeu : h (indice), s (solution), m (mission), q (quitter).")
        # Lire les nouvelles commandes du joueur.
        lines, offset = progress.read_new_log_lines(offset)
        for ln in lines:
            pwd, cmd = progress.parse_log_line(ln)
            if cmd.strip():
                new_commands.append(cmd)
                new_pwds.append(pwd)
        # Evaluer les objectifs.
        states = checker.eval_all(level.get("checks", []), ws, new_commands, new_pwds)
        ui.tick(states)
        if all(states):
            elapsed = time.time() - start
            xp = level.get("xp", 10) - 2 * hints_used
            if solution_used:
                xp = 2
            xp = max(2, xp)
            progress.record_completion(prog, level["id"], xp, len(new_commands), hints_used, solution_used)
            print()
            ui.celebrate(level, xp, prog.get("xp", 0), elapsed, len(new_commands),
                         prog.get("streak", {}).get("current", 0))
            return "done"
        # Rappel hook si aucune commande detectee sur un niveau qui en attend.
        if _needs_commands(level) and not new_commands:
            now = time.time()
            if now - start > 25 and now - last_hook_warning > 60:
                last_hook_warning = now
                print()
                ui.info("Astuce : aucune commande detectee. Dans l'onglet JOUEUR, as-tu active "
                        "le hook ? (source tools/hook.sh — voir README)")
                print(ui.paint("  Je continue de surveiller...", ui.C.DIM))


def play_loop(start_level=None):
    """Enchaine les niveaux jusqu'a quitter ou finir le jeu."""
    prog = progress.load()
    if start_level is None:
        current = prog.get("current", 1)
    else:
        current = start_level
    if current > 1000:
        ui.banner()
        ui.success("Tu as termine les 1000 niveaux ! Tu es ADMIN SYS LINUX. Legende.")
        return
    ui.banner()
    while current <= 1000:
        level = levels.get_level(current)
        if level is None:
            ui.error("niveau {} introuvable.".format(current))
            return
        result = play_level(level, prog)
        if result == "quit":
            ui.info("Partie sauvegardee au niveau {}. A demain pour la serie !".format(level["id"]))
            return
        current = progress.load().get("current", current + 1)
        if current > 1000:
            ui.success("1000/1000. Tu es officiellement ADMIN SYS LINUX. Chapeau !")
            return
        try:
            answer = input(ui.paint("Entree = niveau suivant  |  q = pause : ", ui.C.YELLOW))
        except (EOFError, KeyboardInterrupt):
            print()
            ui.info("Partie sauvegardee. A bientot !")
            return
        if answer.strip().lower() in ("q", "quit", "exit"):
            ui.info("Partie sauvegardee au niveau {}. A demain pour la serie !".format(current))
            return
