"""Petits raccourcis pour ecrire les niveaux de facon compacte et lisible."""


def L(id, title, lesson, mission, checks, hints=(), solution="", story="", setup=(), xp=10, boss=False):
    """Construit un niveau. Le jour est deduit de l'id (10 niveaux par jour)."""
    return {
        "id": id,
        "day": (id - 1) // 10 + 1,
        "title": title,
        "story": story,
        "lesson": lesson,
        "mission": mission,
        "setup": list(setup),
        "checks": list(checks),
        "hints": list(hints),
        "solution": solution,
        "xp": xp,
        "boss": boss,
    }


# --- Actions de preparation de l'arene ---
def F(path, content="", mode=None):
    d = {"file": path, "content": content}
    if mode:
        d["mode"] = mode
    return d


def D(path):
    return {"mkdir": path}


def CH(path, mode):
    return {"chmod": path, "mode": mode}


# --- Checks ---
def C_cmd(pattern):
    return {"type": "command", "pattern": pattern}


def C_cwd(path):
    return {"type": "cwd", "path": path}


def C_fe(path):
    return {"type": "file_exists", "path": path}


def C_de(path):
    return {"type": "dir_exists", "path": path}


def C_ne(path):
    return {"type": "not_exists", "path": path}


def C_fc(path, text=None, regex=None):
    d = {"type": "file_contains", "path": path}
    if regex is not None:
        d["regex"] = regex
    else:
        d["text"] = text or ""
    return d


def C_fnc(path, text=None, regex=None):
    d = {"type": "file_not_contains", "path": path}
    if regex is not None:
        d["regex"] = regex
    else:
        d["text"] = text or ""
    return d


def C_eq(path, expected):
    return {"type": "file_equals", "path": path, "expected": expected}


def C_nempty(path):
    return {"type": "file_not_empty", "path": path}


def C_count(path, count):
    return {"type": "dir_count", "path": path, "count": count}


def C_countmin(path, min):
    return {"type": "dir_count_min", "path": path, "min": min}


def C_perm(path, mode):
    return {"type": "perm", "path": path, "mode": mode}


def C_exe(path):
    return {"type": "executable", "path": path}


def C_sym(path, target=None):
    d = {"type": "symlink", "path": path}
    if target:
        d["target"] = target
    return d
