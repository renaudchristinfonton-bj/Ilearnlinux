"""Sauvegarde de progression : niveau courant, XP, serie quotidienne, historique."""

import datetime
import json
import os

BASE_DIR = os.environ.get("ILEARN_HOME", os.path.expanduser("~/.ilearnlinux"))
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")
ARENA_DIR = os.environ.get("ILEARN_ARENA", os.path.expanduser("~/IlearnLinux-arena"))


def ensure_dirs():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(ARENA_DIR, exist_ok=True)


def default_progress():
    return {
        "current": 1,
        "done": [],
        "xp": 0,
        "history": {},
        "streak": {"current": 0, "best": 0, "last_day": None},
        "profile": {},
        "certs": {},
        "assists": {},
        "started_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }


def load():
    ensure_dirs()
    if not os.path.exists(PROGRESS_FILE):
        return default_progress()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return default_progress()
    base = default_progress()
    base.update(data)
    return base


def save(progress):
    ensure_dirs()
    tmp = PROGRESS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(progress, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, PROGRESS_FILE)


def today_iso():
    return datetime.date.today().isoformat()


def record_completion(progress, level_id, xp_earned, n_commands, hints_used, solution_used):
    lid = str(level_id)
    if level_id not in progress["done"]:
        progress["done"].append(level_id)
    progress["xp"] += xp_earned
    progress["history"][lid] = {
        "xp": xp_earned,
        "at": datetime.datetime.now().isoformat(timespec="seconds"),
        "commands": n_commands,
        "hints": hints_used,
        "solution": bool(solution_used),
    }
    progress["assists"].pop(lid, None)
    # Serie quotidienne : 1+ niveau valide par jour.
    today = today_iso()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    streak = progress["streak"]
    if streak.get("last_day") == today:
        pass
    elif streak.get("last_day") == yesterday:
        streak["current"] = streak.get("current", 0) + 1
    else:
        streak["current"] = 1
    streak["best"] = max(streak.get("best", 0), streak["current"])
    streak["last_day"] = today
    # Avancer au niveau suivant non termine.
    done = set(progress["done"])
    nxt = level_id + 1
    while nxt in done:
        nxt += 1
    progress["current"] = nxt
    save(progress)
    return progress


def record_assist(progress, level_id, kind):
    """Memorise l'usage d'un indice/solution pour ajuster l'XP."""
    lid = str(level_id)
    assists = progress.setdefault("assists", {}).setdefault(lid, {"hints": 0, "solution": False})
    if kind == "hint":
        assists["hints"] = assists.get("hints", 0) + 1
    elif kind == "solution":
        assists["solution"] = True
    save(progress)
    return assists


def get_assists(progress, level_id):
    return progress.get("assists", {}).get(str(level_id), {"hints": 0, "solution": False})


def reset():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    return default_progress()


def arena_path(level_id):
    return os.path.join(ARENA_DIR, "niveau-{:04d}".format(level_id))
