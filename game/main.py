#!/usr/bin/env python3
"""Point d'entree CLI : ./ilearn play|dashboard|hint|solution|goto|reset|doctor"""

import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import __version__  # noqa: E402
from game import certs, engine, levels, progress, ui  # noqa: E402


def cmd_play(_args):
    progress.ensure_dirs()
    engine.play_loop()


def cmd_dashboard(_args):
    progress.ensure_dirs()
    ui.banner()
    ui.dashboard(progress.load(), levels.total(), levels.max_day())


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
    if not 1 <= args.n <= levels.total():
        ui.error("le niveau doit etre entre 1 et {}.".format(levels.total()))
        return
    prog["current"] = args.n
    progress.save(prog)
    ui.success("Prochain niveau : {} (pratique libre, l'XP compte quand meme !).".format(args.n))


def cmd_certs(_args):
    progress.ensure_dirs()
    prog = progress.load()
    ui.banner()
    print()
    ui.title("MES CERTIFICATS")
    earned = prog.get("certs", {}) or {}
    if not earned:
        ui.info("Aucun certificat pour l'instant : termine un bloc complet (ex : niveaux 1-10) !")
    for cid in sorted(earned):
        rec = earned[cid]
        cert = certs.get_cert(cid)
        slug = cert["slug"] if cert else cid.lower()
        svg = os.path.join(progress.BASE_DIR, "certificats", "{}-{}.svg".format(cid, slug))
        print(ui.paint("  [X] {} ({})".format(rec.get("title", cid), cid), ui.C.GREEN + ui.C.BOLD))
        print("      Delivre le {} a {} — code {}".format(rec.get("at", "?"), rec.get("name", "?"),
                                                          rec.get("code", "?")))
        print("      {}".format(svg if os.path.isfile(svg) else "(fichier regenere a la prochaine remise)"))
    print()
    ui.title("EN ROUTE VERS")
    for cert, n, total in certs.next_certificates(prog, limit=5):
        bar = ui.progress_bar(n, total, size=12)
        print("  {} {} — {}/{} {}".format(cert["id"], cert["title"], n, total, bar))
    print()
    ui.info("Astuce : ./ilearn profil \"Ton Nom\" pour personnaliser tes certificats.")


def cmd_profile(args):
    progress.ensure_dirs()
    prog = progress.load()
    if args.name:
        name = certs.set_profile_name(prog, args.name)
        ui.success("Nom enregistre : {} (il figurera sur tes certificats).".format(name))
    else:
        name = certs.profile_name(prog)
        if name:
            ui.info("Nom sur les certificats : {}".format(name))
        else:
            ui.info("Aucun nom defini : ./ilearn profil \"Ton Nom\" (ou il sera demande au 1er certificat).")


def cmd_verify(args):
    prog = progress.load()
    cert, name = certs.verify_code(prog, args.code)
    if cert is None:
        ui.error("Code inconnu sur cette machine.")
        return
    ui.success("Code valide : {} ({}) delivre a {}.".format(cert["title"], cert["id"], name or "?"))


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
    check("Bash", shutil.which("bash") is not None)
    errors = levels.validate()
    check("{} niveaux valides".format(levels.total()), not errors, errors[0] if errors else "aucune erreur")
    if errors:
        ok = False
        for err in errors[:10]:
            print("       - {}".format(err))
    check("Dossier de progression", os.path.isdir(progress.BASE_DIR), progress.BASE_DIR)
    check("Missions accessibles en ecriture", os.access(progress.ARENA_DIR, os.W_OK), progress.ARENA_DIR)
    # Outils systeme utilises par les missions (vraies commandes !).
    tools = ["tar", "gzip", "find", "grep", "sort", "ps", "ping", "ip", "ss",
             "getent", "curl", "ssh", "ssh-keygen", "scp", "top", "free", "lscpu",
             "lsblk", "du", "df", "wc", "cut", "tr", "tee", "nohup", "pgrep",
             "journalctl", "systemctl", "dmesg", "ln", "file", "strings",
             "md5sum", "sha256sum", "base64"]
    missing = [t for t in tools if shutil.which(t) is None]
    check("Outils systeme", not missing,
          "tous presents" if not missing else "manquants : {} (ex: sudo apt install ...)".format(", ".join(missing)))
    # Cibles simulees (fournies par le jeu, zero installation).
    fakebin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakebin")
    sims = ["nmap", "ssh", "john"]
    sims_ok = all(os.access(os.path.join(fakebin, s), os.X_OK) for s in sims)
    check("Simulateurs (nmap/ssh/john)", sims_ok, "inclus dans le jeu, prets" if sims_ok else "verifie game/fakebin")
    prog = progress.load()
    check("Progression", True, "niveau {}, {} XP, serie {} j".format(
        prog.get("current", 1), prog.get("xp", 0), prog.get("streak", {}).get("current", 0)))
    print()
    if ok:
        ui.success("Tout est pret : lance ./ilearn play (v{}) et deviens agent !".format(__version__))
    else:
        ui.error("Des problemes bloquent le jeu : corrige-les puis relance ./ilearn doctor.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ilearn",
        description="ILearnLinux — du terminal a Agent Cyber, en jouant avec de vraies commandes.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("play", help="Jouer (terminal de mission interactif)").set_defaults(func=cmd_play)
    sub.add_parser("dashboard", help="Tableau de bord : XP, serie, badges").set_defaults(func=cmd_dashboard)
    sub.add_parser("stats", help="Alias de dashboard").set_defaults(func=cmd_dashboard)
    sub.add_parser("hint", help="Indice pour le niveau courant").set_defaults(func=cmd_hint)
    sub.add_parser("solution", help="Solution du niveau courant").set_defaults(func=cmd_solution)
    sub.add_parser("mission", help="Reafficher la mission courante").set_defaults(func=cmd_mission)
    goto = sub.add_parser("goto", help="Aller a un niveau (pratique libre)")
    goto.add_argument("n", type=int, help="numero du niveau")
    goto.set_defaults(func=cmd_goto)
    sub.add_parser("certificats", help="Voir mes certificats + progression").set_defaults(func=cmd_certs)
    sub.add_parser("certs", help="Alias de certificats").set_defaults(func=cmd_certs)
    prof = sub.add_parser("profil", help="Voir/definir le nom des certificats")
    prof.add_argument("name", nargs="?", default="", help="nom a faire figurer")
    prof.set_defaults(func=cmd_profile)
    ver = sub.add_parser("verifier", help="Verifier un code de certificat")
    ver.add_argument("code", help="code ILEARN-XXXX-XXXX")
    ver.set_defaults(func=cmd_verify)
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
