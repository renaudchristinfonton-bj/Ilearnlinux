#!/usr/bin/env python3
"""Point d'entree CLI : ./ilearn play|dashboard|hint|solution|goto|reset|doctor"""

import argparse
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import __version__  # noqa: E402
from game import engine, levels, progress, ui  # noqa: E402


def cmd_play(_args):
    progress.ensure_dirs()
    engine.play_loop()


def cmd_dashboard(_args):
    progress.ensure_dirs()
    ui.banner()
    ui.dashboard(progress.load())


def cmd_hint(_args):
    prog = progress.load()
    level = levels.get_level(prog.get("current", 1))
    if level is None:
        ui.error("jeu termine ou niveau introuvable.")
        return
    assists = progress.get_assists(prog, level["id"])
    if ui.show_hint(level.get("hints", []), assists.get("hints", 0)):
        progress.record_assist(prog, level["id"], "hint")


def cmd_solution(_args):
    prog = progress.load()
    level = levels.get_level(prog.get("current", 1))
    if level is None:
        ui.error("jeu termine ou niveau introuvable.")
        return
    ui.show_solution(level.get("solution", ""))
    progress.record_assist(prog, level["id"], "solution")


def cmd_mission(_args):
    prog = progress.load()
    level = levels.get_level(prog.get("current", 1))
    if level is None:
        ui.error("jeu termine ou niveau introuvable.")
        return
    print(ui.paint("NIVEAU {} — {}".format(level["id"], level["title"]), ui.C.BOLD + ui.C.MAGENTA))
    print(ui.wrap(level["mission"], prefix="  >> "))


def cmd_goto(args):
    prog = progress.load()
    if not 1 <= args.n <= 1000:
        ui.error("le niveau doit etre entre 1 et 1000.")
        return
    prog["current"] = args.n
    progress.save(prog)
    ui.success("Prochain niveau : {} (pratique libre, l'XP compte quand meme !).".format(args.n))


def cmd_reset(_args):
    answer = input("Tout effacer et recommencer au niveau 1 ? (o/N) : ").strip().lower()
    if answer in ("o", "oui", "y", "yes"):
        progress.reset()
        ui.success("Progression effacee. Nouveau depart : ./ilearn play")
    else:
        ui.info("Annule : ta progression est gardee.")


def cmd_doctor(_args):
    progress.ensure_dirs()
    ui.banner()
    print()
    ui.title("DOCTEUR ILEARN — diagnostic")
    ok = True

    def check(name, good, detail=""):
        status = ui.paint("[OK]", ui.C.GREEN + ui.C.BOLD) if good else ui.paint("[!!]", ui.C.RED + ui.C.BOLD)
        print("  {} {}{}".format(status, name, " — {}".format(detail) if detail else ""))

    check("Python {}".format(sys.version.split()[0]), sys.version_info >= (3, 8))
    errors = levels.validate()
    check("1000 niveaux valides", not errors, errors[0] if errors else "aucune erreur")
    if errors:
        ok = False
        for err in errors[:10]:
            print("       - {}".format(err))
    check("Dossier de progression", os.path.isdir(progress.BASE_DIR), progress.BASE_DIR)
    check("Arene accessible en ecriture", os.access(progress.ARENA_DIR, os.W_OK), progress.ARENA_DIR)
    # Outils systeme utilises par certains niveaux (lecture seule / bac a sable).
    tools = ["tar", "gzip", "find", "grep", "sort", "ps", "ping", "ip", "ss",
             "getent", "curl", "ssh", "ssh-keygen", "scp", "top", "free", "lscpu",
             "lsblk", "du", "df", "wc", "cut", "tr", "tee", "nohup", "pgrep",
             "crontab", "journalctl", "systemctl", "dmesg", "ln"]
    missing = [t for t in tools if shutil.which(t) is None]
    check("Outils systeme", not missing,
          "tous presents" if not missing else "manquants : {} (sudo apt install ...)".format(", ".join(missing)))
    # Hook : journal recent ?
    try:
        age = time.time() - os.path.getmtime(progress.COMMANDS_LOG)
        fresh = age < 3600
        check("Hook joueur", fresh,
              "journal actif (derniere commande il y a {}s)".format(int(age)) if fresh
              else "aucune commande depuis 1h — pense a 'source tools/hook.sh' dans l'onglet JOUEUR")
    except OSError:
        check("Hook joueur", True, "journal pret (aucune commande encore)")
    prog = progress.load()
    check("Progression", True, "niveau {}, {} XP, serie {} j".format(
        prog.get("current", 1), prog.get("xp", 0), prog.get("streak", {}).get("current", 0)))
    print()
    if ok:
        ui.success("Tout est pret : ouvre 2 onglets et lance ./ilearn play (v{}) !".format(__version__))
    else:
        ui.error("Des problemes bloquent le jeu : corrige-les puis relance ./ilearn doctor.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ilearn",
        description="ILearnLinux — deviens Admin Sys Linux en 100 jours, 1000 niveaux de jeu.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("play", help="Jouer (surveillance continue de l'arene)").set_defaults(func=cmd_play)
    sub.add_parser("dashboard", help="Tableau de bord : XP, serie, badges").set_defaults(func=cmd_dashboard)
    sub.add_parser("stats", help="Alias de dashboard").set_defaults(func=cmd_dashboard)
    sub.add_parser("hint", help="Indice pour le niveau courant").set_defaults(func=cmd_hint)
    sub.add_parser("solution", help="Solution du niveau courant").set_defaults(func=cmd_solution)
    sub.add_parser("mission", help="Reafficher la mission courante").set_defaults(func=cmd_mission)
    goto = sub.add_parser("goto", help="Aller a un niveau (pratique libre)")
    goto.add_argument("n", type=int, help="numero du niveau (1-1000)")
    goto.set_defaults(func=cmd_goto)
    sub.add_parser("reset", help="Tout recommencer").set_defaults(func=cmd_reset)
    sub.add_parser("doctor", help="Verifier l'installation").set_defaults(func=cmd_doctor)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        cmd_play(args)
    else:
        func(args)


if __name__ == "__main__":
    main()
