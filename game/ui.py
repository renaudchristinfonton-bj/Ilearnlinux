"""Affichage du jeu : couleurs ANSI, cartes de niveaux, celebrations. (stdlib uniquement)"""

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
]


def rank_for(level_id):
    rank = RANKS[0][1]
    for threshold, name in RANKS:
        if level_id >= threshold:
            rank = name
    return rank


BANNER = r"""
  ___  _                      _     _
 |_ _|| | ___  __ _ _ __ _ __| |   (_)_ __  _   ___  __
  | | | |/ _ \/ _` | '__| '_ \| |   | | '_ \| | | \ \/ /
  | | | |  __/ (_| | |  | | | | |___| | | | | |_| |>  <
 |___||_|\___|\__,_|_|  |_| |_|_____|_|_| |_|\__,_/_/\_\
"""


def banner():
    print(paint(BANNER, C.GREEN + C.BOLD))
    print(paint("  Deviens Admin Sys Linux en 100 jours - 1000 niveaux, 100% pratique.", C.BOLD))
    print(paint("  Le jeu regarde, toi tu tapes. Bon courage, futur admin !", C.DIM))


def progress_bar(done, total, size=30):
    if total <= 0:
        return "[{}]".format("." * size)
    filled = int(size * done / total)
    return "[{}{}] {}/{}".format("#" * filled, "." * (size - filled), done, total)


def level_card(level, ws_path, total_xp, streak):
    lid = level["id"]
    day = level["day"]
    n_checks = len(level.get("checks", []))
    print()
    hr("=")
    head = " NIVEAU {}/1000  -  JOUR {}/100  -  {} ".format(lid, day, rank_for(lid))
    if level.get("boss"):
        print(paint("*** NIVEAU BOSS ***" + head + "***", C.BOLD + C.YELLOW))
    else:
        print(paint(head, C.BOLD + C.MAGENTA))
    hr("=")
    print(paint("Titre : ", C.BOLD) + level["title"] + paint("   ({} XP)".format(level.get("xp", 10)), C.YELLOW))
    print(paint("Progression : ", C.DIM) + progress_bar(lid - 1, 1000)
          + paint("   |   Total XP : {}   |   Serie : {} jour(s)".format(total_xp, streak), C.DIM))
    hr()
    if level.get("story"):
        print(paint("Histoire", C.CYAN + C.BOLD))
        print(wrap(level["story"], prefix="  "))
        print()
    print(paint("Lecon", C.CYAN + C.BOLD))
    print(wrap(level["lesson"], prefix="  "))
    print()
    print(paint("Ta mission", C.GREEN + C.BOLD))
    print(wrap(level["mission"], prefix="  >> "))
    print()
    print(paint("Arene (onglet JOUEUR) :", C.BOLD))
    print(paint("  cd {}".format(ws_path), C.YELLOW))
    print(paint("Objectifs a valider : {}   |   (h + Entree = indice, s + Entree = solution, q + Entree = quitter)".format(n_checks), C.DIM))
    hr()


def mission_recap(level):
    print()
    print(paint("Rappel de mission :", C.GREEN + C.BOLD))
    print(wrap(level["mission"], prefix="  >> "))


def tick(states):
    symbols = []
    for ok in states:
        symbols.append(paint("OK", C.GREEN + C.BOLD) if ok else paint(".", C.DIM))
    line = "  Objectifs : [{}]".format("][".join(symbols))
    print("\r" + line + " ", end="", flush=True)


def celebrate(level, xp_earned, total_xp, elapsed_s, n_commands, streak):
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
    print(paint("  Temps : {}m {:02d}s   |   Commandes tapees : {}   |   Total XP : {}   |   Serie : {} jour(s)".format(
        mins, secs, n_commands, total_xp, streak), C.CYAN))
    if level["id"] % 10 == 0:
        print(paint("  JOUR {} TERMINE ! Tu progresses vite. Demain, on continue.".format(level["day"]), C.GREEN + C.BOLD))
    if level["id"] == 1000:
        print()
        print(paint("  TU ES OFFICIELLEMENT ADMIN SYS LINUX. CHAPEAU, LEGENDE.", C.BOLD + C.MAGENTA))
    hr("*")


def show_hint(hints, used):
    if used < len(hints):
        print()
        print(paint("Indice {}/{} : ".format(used + 1, len(hints)), C.YELLOW + C.BOLD) + hints[used])
        print(paint("  (-2 XP sur ce niveau)", C.DIM))
        return True
    print(paint("  Plus d'indices pour ce niveau. Tu peux demander la solution (s).", C.DIM))
    return False


def show_solution(solution):
    print()
    print(paint("Solution : ", C.RED + C.BOLD) + (solution or "(pas de solution courte, relis la mission)"))
    print(paint("  Ce niveau ne rapportera presque plus d'XP. Prochain niveau sans filet !", C.DIM))


def dashboard(progress, total_levels=1000):
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
    print(paint("  Carte des 100 jours (ligne = 10 jours) :", C.BOLD))
    done_set = set(done)
    for row in range(10):
        cells = []
        for col in range(10):
            day = row * 10 + col + 1
            ids = set(range((day - 1) * 10 + 1, day * 10 + 1))
            n = len(ids & done_set)
            if n == 10:
                cells.append(paint("#", C.GREEN + C.BOLD))
            elif n > 0:
                cells.append(paint("+", C.YELLOW + C.BOLD))
            else:
                cells.append(paint(".", C.DIM))
        print("    jours {:>3}-{:>3} : {}".format(row * 10 + 1, row * 10 + 10, " ".join(cells)))
    print()
    print(paint("  Badges :", C.BOLD))
    badges = compute_badges(done_set, streak, best)
    for icon, name, earned in badges:
        mark = paint("[X]", C.GREEN) if earned else paint("[ ]", C.DIM)
        print("    {} {} {}".format(mark, icon, name))
    nxt = progress.get("current", 1)
    print()
    print(paint("  Prochain niveau : {}  ->  ./ilearn play".format(nxt if nxt <= total_levels else "TERMINE !"), C.CYAN))


def compute_badges(done_set, streak, best):
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
        ("Legende", "1000 niveaux reussis", n >= 1000),
    ]


def error(msg):
    print(paint("Erreur : {}".format(msg), C.RED + C.BOLD))


def info(msg):
    print(paint(msg, C.CYAN))


def success(msg):
    print(paint(msg, C.GREEN + C.BOLD))
