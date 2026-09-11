"""Affichage du jeu : couleurs ANSI, panneaux de mission, mentor, celebrations."""

import os
import shutil
import textwrap


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def _color_enabled():
    return os.environ.get("NO_COLOR") is None and os.environ.get("TERM", "") != "dumb"


def paint(text, code):
    if not _color_enabled():
        return str(text)
    return "{}{}{}".format(code, text, C.RESET)


def width():
    try:
        cols = shutil.get_terminal_size((80, 24)).columns - 2
    except OSError:
        cols = 78
    return max(60, min(78, cols))


def hr(char="-"):
    print(paint(char * width(), C.DIM))


def wrap(text, prefix=""):
    return textwrap.fill(
        str(text), width=width(), initial_indent=prefix, subsequent_indent=prefix
    )


def title(t):
    print()
    print(paint(t, C.BOLD + C.CYAN))
    hr()


RANKS = [
    (1, "Curieux du terminal"),
    (51, "Explorateur"),
    (151, "Bidouilleur"),
    (301, "Power User"),
    (501, "Sorcier du shell"),
    (751, "Gardien du systeme"),
    (901, "Futur Admin Sys"),
    (1000, "ADMIN SYS LINUX"),
    (1001, "Agent Cyber stagiaire"),
    (1041, "Agent Cyber"),
    (1081, "Agent Cyber confirme"),
    (1100, "AGENT CYBER D'ELITE"),
]


def rank_for(level_id):
    rank = RANKS[0][1]
    for threshold, name in RANKS:
        if level_id >= threshold:
            rank = name
    return rank


def season_for(level_id):
    if level_id <= 1000:
        return "Saison 1 - Linux"
    return "Saison 2 - Agent Cyber"


BANNER = r"""
  ___  _                      _     _
 |_ _|| | ___  __ _ _ __ _ __| |   (_)_ __  _   ___  __
  | | | |/ _ \/ _` | '__| '_ \| |   | | '_ \| | | \ \/ /
  | | | |  __/ (_| | |  | | | | |___| | | | | |_| |>  <
 |___||_|\___|\__,_|_|  |_| |_|_____|_|_| |_|\__,_/_/\_\
"""


def banner():
    print(paint(BANNER, C.GREEN + C.BOLD))
    print(paint("  Saison 1 : deviens Admin Sys Linux - Saison 2 : deviens Agent Cyber.", C.BOLD))
    print(paint("  Un terminal, des vraies commandes, un mentor. Bon courage, futur agent !", C.DIM))


def progress_bar(done, total, size=30):
    if total <= 0:
        return "[{}]".format("." * size)
    filled = int(size * done / total)
    return "[{}{}] {}/{}".format("#" * filled, "." * (size - filled), done, total)


def mission_panel(level, mission_path, total_xp, streak, total):
    lid = level["id"]
    day = level["day"]
    n_checks = len(level.get("checks", []))
    print()
    hr("=")
    head = " NIVEAU {}/{} - JOUR {} - {} ".format(lid, total, day, rank_for(lid))
    if level.get("boss"):
        print(paint("*** NIVEAU BOSS ***" + head + "***", C.BOLD + C.YELLOW))
    else:
        print(paint(head, C.BOLD + C.MAGENTA))
    print(paint(season_for(lid), C.DIM))
    hr("=")
    print(paint("Titre : ", C.BOLD) + level["title"] + paint("   ({} XP)".format(level.get("xp", 10)), C.YELLOW))
    print(paint("Progression : ", C.DIM) + progress_bar(lid - 1, total)
          + paint("   |   Total XP : {}   |   Serie : {} jour(s)".format(total_xp, streak), C.DIM))
    hr()
    if level.get("story"):
        print(paint("Histoire", C.CYAN + C.BOLD))
        print(wrap(level["story"], prefix="  "))
        print()
    print(paint("Cours", C.CYAN + C.BOLD))
    print(wrap(level["lesson"], prefix="  "))
    print()
    print(paint("Ta mission", C.GREEN + C.BOLD))
    print(wrap(level["mission"], prefix="  >> "))
    print()
    print(paint("Dossier de mission : ", C.BOLD) + mission_path)
    print(paint("Objectifs : {}   |   aide = commandes du jeu (indice, solution, quitter...)".format(n_checks), C.DIM))
    hr()


def game_help():
    print()
    print(paint("Commandes du jeu (a taper a la place d'une commande Linux) :", C.CYAN + C.BOLD))
    print("  aide      afficher ce message")
    print("  mission   revoir la mission en cours")
    print("  cours     revoir le cours du niveau")
    print("  indice    demander un indice (-2 XP)")
    print("  solution  voir la solution (XP reduits)")
    print("  quitter   faire une pause (progression sauvegardee)")
    print(paint("Tout le reste est execute comme une VRAIE commande Linux. Amuse-toi !", C.DIM))


def lesson_card(level):
    print()
    print(paint("Cours - {}".format(level["title"]), C.CYAN + C.BOLD))
    print(wrap(level["lesson"], prefix="  "))


def mission_recap(level):
    print()
    print(paint("Rappel de mission :", C.GREEN + C.BOLD))
    print(wrap(level["mission"], prefix="  >> "))


def mentor(text):
    print(paint("  [MENTOR] ", C.MAGENTA + C.BOLD) + text)


def objectives(states):
    symbols = []
    for ok in states:
        symbols.append(paint("OK", C.GREEN + C.BOLD) if ok else paint(".", C.DIM))
    print("  Objectifs : [{}]".format("][".join(symbols)))


def prompt_str(display_path):
    return "{}@{}:{}$ ".format(
        paint("agent", C.GREEN + C.BOLD),
        paint("cyber", C.CYAN + C.BOLD),
        paint(display_path, C.BLUE + C.BOLD))


def celebrate(level, xp_earned, total_xp, elapsed_s, n_commands, streak, faults=0):
    print()
    hr("*")
    art = [
        "   \\   *   /      BRAVO !  NIVEAU {} REUSSI  +{} XP      \\   *   /".format(level["id"], xp_earned),
        "    \\  \\ /  /",
        "     \\  V  /",
        "      \\ | /",
        "       \\|/",
        "        V",
    ]
    for line in art:
        print(paint(line, C.YELLOW + C.BOLD))
    mins, secs = divmod(int(elapsed_s), 60)
    print(paint("  Temps : {}m {:02d}s   |   Commandes : {}   |   Fautes : {}   |   Total XP : {}   |   Serie : {} j".format(
        mins, secs, n_commands, faults, total_xp, streak), C.CYAN))
    if faults == 0:
        print(paint("  SANS FAUTE ! Precision d'agent d'elite.", C.GREEN + C.BOLD))
    if level["id"] % 10 == 0:
        print(paint("  JOUR {} TERMINE ! Demain, on continue.".format(level["day"]), C.GREEN + C.BOLD))
    if level["id"] == 1000:
        print()
        print(paint("  SAISON 1 TERMINEE : tu es ADMIN SYS LINUX. La Saison 2 (Agent Cyber) t'attend !",
                    C.BOLD + C.MAGENTA))
    hr("*")


def cert_celebrate(cert, code, svg_path):
    from . import certs as certs_mod
    print()
    print(paint("  +" + "=" * 72 + "+", C.YELLOW + C.BOLD))
    print(paint("  |" + "  CERTIFICAT DE MAITRISE DECERNE !  ".center(72) + "|", C.YELLOW + C.BOLD))
    print(paint("  +" + "=" * 72 + "+", C.YELLOW + C.BOLD))
    print(paint("   {} ({})".format(cert["title"], cert["id"]), C.BOLD + C.CYAN))
    print("   Competences : {}".format(", ".join(cert["skills"][:4])))
    print("   {}".format(certs_mod.level_label(cert)))
    print(paint("   Code de verification : {}".format(code), C.GREEN + C.BOLD))
    print("   Document : {}".format(svg_path))
    print("   (Ouvre le .html du meme nom pour imprimer / enregistrer en PDF.)")


def show_hint(hints, used):
    if used < len(hints):
        print()
        print(paint("Indice {}/{} : ".format(used + 1, len(hints)), C.YELLOW + C.BOLD) + hints[used])
        print(paint("  (-2 XP sur ce niveau)", C.DIM))
        return True
    print(paint("  Plus d'indices pour ce niveau. Tu peux demander la solution (tape 'solution').", C.DIM))
    return False


def show_solution(solution):
    print()
    print(paint("Solution : ", C.RED + C.BOLD) + (solution or "(pas de solution courte, relis la mission)"))
    print(paint("  Ce niveau ne rapportera presque plus d'XP. Prochain niveau sans filet !", C.DIM))


def dashboard(progress, total_levels, max_day):
    done = sorted(progress.get("done", []))
    xp = progress.get("xp", 0)
    streak = progress.get("streak", {}).get("current", 0)
    best = progress.get("streak", {}).get("best", 0)
    title("TABLEAU DE BORD - {}".format(rank_for((done[-1] + 1) if done else 1)))
    print(paint("  Niveaux reussis : ", C.BOLD) + "{}/{}".format(len(done), total_levels))
    print("  " + progress_bar(len(done), total_levels))
    print(paint("  XP total : ", C.BOLD) + str(xp))
    print(paint("  Serie : ", C.BOLD) + "{} jour(s)  (record : {})".format(streak, best))
    hist = progress.get("history", {})
    if hist:
        cmds = sum(v.get("commands", 0) for v in hist.values())
        print(paint("  Commandes tapees depuis le debut : ", C.BOLD) + str(cmds))
    print()
    print(paint("  Carte des jours (ligne = 10 jours, # = termine, + = en cours) :", C.BOLD))
    done_set = set(done)
    day = 1
    while day <= max_day:
        cells = []
        for col in range(10):
            d = day + col
            if d > max_day:
                break
            ids = set(range((d - 1) * 10 + 1, d * 10 + 1))
            n = len(ids & done_set)
            if n == 10:
                cells.append(paint("#", C.GREEN + C.BOLD))
            elif n > 0:
                cells.append(paint("+", C.YELLOW + C.BOLD))
            else:
                cells.append(paint(".", C.DIM))
        print("    jours {:>3}-{:>3} : {}".format(day, min(day + 9, max_day), " ".join(cells)))
        day += 10
    print()
    print(paint("  Badges :", C.BOLD))
    for icon, name, earned in compute_badges(done_set, best):
        mark = paint("[X]", C.GREEN) if earned else paint("[ ]", C.DIM)
        print("    {} {} {}".format(mark, icon, name))
    earned = progress.get("certs", {}) or {}
    if earned:
        print(paint("  Certificats ({} — ./ilearn certificats pour le detail) :".format(len(earned)), C.BOLD))
        for cid in sorted(earned):
            print("    {} {}".format(paint("[X]", C.GREEN),
                                     earned[cid].get("title", cid)))
    else:
        print(paint("  Certificats : aucun pour l'instant — termine un bloc pour le premier !", C.DIM))
    from . import certs as certs_mod
    nxt_certs = certs_mod.next_certificates(progress, limit=2)
    if nxt_certs:
        print(paint("  En route vers :", C.BOLD))
        for cert, n, total in nxt_certs:
            print("    {} {} — {}/{} ({})".format(paint("->", C.YELLOW), cert["title"], n, total,
                                                  "./ilearn play pour avancer"))
    nxt = progress.get("current", 1)
    print()
    print(paint("  Prochain niveau : {}  ->  ./ilearn play".format(nxt if nxt <= total_levels else "TERMINE !"), C.CYAN))


def compute_badges(done_set, best):
    n = len(done_set)
    return [
        ("Premier pas", "Finir le niveau 1", 1 in done_set),
        ("Serie de 10", "10 niveaux reussis", n >= 10),
        ("Jour 1 termine", "Niveaux 1 a 10 reussis", set(range(1, 11)) <= done_set),
        ("Explorateur", "50 niveaux reussis", n >= 50),
        ("Centenaire", "100 niveaux reussis", n >= 100),
        ("Flamme", "Serie de 3 jours", best >= 3),
        ("Brasier", "Serie de 7 jours", best >= 7),
        ("Machine", "300 niveaux reussis", n >= 300),
        ("Sorcier", "500 niveaux reussis", n >= 500),
        ("Admin Sys", "1000 niveaux reussis (fin Saison 1)", n >= 1000),
        ("Agent stagiaire", "Premier niveau cyber (1001)", 1001 in done_set),
        ("Agent confirme", "1050 niveaux reussis", n >= 1050),
        ("Agent d'elite", "1100 niveaux reussis (fin Saison 2)", n >= 1100),
    ]


def error(msg):
    print(paint("Erreur : {}".format(msg), C.RED + C.BOLD))


def info(msg):
    print(paint(msg, C.CYAN))


def success(msg):
    print(paint(msg, C.GREEN + C.BOLD))
