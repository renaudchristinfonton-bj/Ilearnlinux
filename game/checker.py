"""Moteur de verification des niveaux.

Chaque niveau declare une liste de "checks" que le moteur evalue en continu
en observant :
  - l'arene (le dossier de travail du niveau, cote onglet JOUEUR),
  - le journal des commandes tapees par le joueur (via tools/hook.sh).

Types de checks supportes :
  command        : une commande tapee correspond a la regex "pattern"
  cwd            : le dossier courant du joueur correspond au chemin "path"
  file_exists    : le fichier existe
  dir_exists     : le dossier existe
  not_exists     : le chemin n'existe pas (ou plus)
  file_contains  : le fichier contient "text" (ou la regex "regex")
  file_not_contains : le fichier ne contient PAS "text"/"regex"
  file_equals    : contenu exact du fichier == "expected"
  file_not_empty : le fichier existe et n'est pas vide
  dir_count      : le dossier contient exactement "count" entrees
  dir_count_min  : le dossier contient au moins "min" entrees
  perm           : permissions exactes "mode" (ex: "755")
  executable     : le fichier est executable
  symlink        : le chemin est un lien symbolique (option "target" : sous-chaine de la cible)
"""

import os
import re
import stat


CHECK_TYPES = {
    "command", "cwd", "file_exists", "dir_exists", "not_exists",
    "file_contains", "file_not_contains", "file_equals", "file_not_empty",
    "dir_count", "dir_count_min", "perm", "executable", "symlink",
}


def resolve(path, ws):
    """Resout un chemin de niveau : {ws} = arene du niveau, ~ = home, relatif = arene."""
    if path is None:
        return ws
    p = str(path).replace("{ws}", ws)
    p = os.path.expanduser(p)
    if not os.path.isabs(p):
        p = os.path.join(ws, p)
    return os.path.normpath(p)


def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (OSError, UnicodeError):
        return None


def eval_check(check, ws, new_commands, new_pwds):
    """Evalue UN check. Retourne (ok: bool, detail: str)."""
    t = check.get("type")
    if t == "command":
        pattern = check.get("pattern", "")
        try:
            rx = re.compile(pattern)
        except re.error:
            return False, "regex invalide"
        for cmd in new_commands:
            if rx.search(cmd):
                return True, "vu: {}".format(cmd[:60])
        return False, "en attente de la commande"
    if t == "cwd":
        expected = resolve(check.get("path", ""), ws)
        needle = re.escape(expected)
        for pwd in new_pwds:
            if re.search(needle, pwd):
                return True, "vu: {}".format(pwd)
        return False, "en attente de navigation"
    if t == "file_exists":
        p = resolve(check.get("path", ""), ws)
        return (os.path.isfile(p), p if os.path.isfile(p) else "fichier manquant")
    if t == "dir_exists":
        p = resolve(check.get("path", ""), ws)
        return (os.path.isdir(p), p if os.path.isdir(p) else "dossier manquant")
    if t == "not_exists":
        p = resolve(check.get("path", ""), ws)
        return ((not os.path.lexists(p)), "supprime" if not os.path.lexists(p) else "existe encore")
    if t == "file_contains":
        p = resolve(check.get("path", ""), ws)
        content = _read_text(p)
        if content is None:
            return False, "fichier illisible"
        if "regex" in check:
            try:
                ok = re.search(check["regex"], content) is not None
            except re.error:
                return False, "regex invalide"
            return ok, "regex trouvee" if ok else "regex absente"
        needle = check.get("text", "")
        ok = needle in content
        return ok, "texte trouve" if ok else "texte absent"
    if t == "file_not_contains":
        p = resolve(check.get("path", ""), ws)
        content = _read_text(p)
        if content is None:
            return False, "fichier illisible"
        if "regex" in check:
            try:
                ok = re.search(check["regex"], content) is None
            except re.error:
                return False, "regex invalide"
            return ok, "ok" if ok else "regex encore presente"
        needle = check.get("text", "")
        ok = needle not in content
        return ok, "ok" if ok else "texte encore present"
    if t == "file_equals":
        p = resolve(check.get("path", ""), ws)
        content = _read_text(p)
        if content is None:
            return False, "fichier illisible"
        expected = check.get("expected", "")
        ok = content == expected
        return ok, "contenu exact" if ok else "contenu different"
    if t == "file_not_empty":
        p = resolve(check.get("path", ""), ws)
        try:
            ok = os.path.isfile(p) and os.path.getsize(p) > 0
        except OSError:
            ok = False
        return ok, "non vide" if ok else "vide ou manquant"
    if t == "dir_count":
        p = resolve(check.get("path", ""), ws)
        try:
            n = len(os.listdir(p))
        except OSError:
            return False, "dossier illisible"
        want = int(check.get("count", 0))
        return n == want, "{}/{} entrees".format(n, want)
    if t == "dir_count_min":
        p = resolve(check.get("path", ""), ws)
        try:
            n = len(os.listdir(p))
        except OSError:
            return False, "dossier illisible"
        want = int(check.get("min", 1))
        return n >= want, "{} entrees (min {})".format(n, want)
    if t == "perm":
        p = resolve(check.get("path", ""), ws)
        try:
            mode = oct(stat.S_IMODE(os.stat(p).st_mode))[2:]
        except OSError:
            return False, "chemin illisible"
        want = str(check.get("mode", ""))
        return mode == want, "mode {}".format(mode)
    if t == "executable":
        p = resolve(check.get("path", ""), ws)
        ok = os.path.isfile(p) and os.access(p, os.X_OK)
        return ok, "executable" if ok else "pas executable"
    if t == "symlink":
        p = resolve(check.get("path", ""), ws)
        if not os.path.islink(p):
            return False, "pas un lien symbolique"
        target = check.get("target")
        if target:
            real = os.readlink(p)
            ok = target in real
            return ok, "-> {}".format(real)
        return True, "lien ok"
    return False, "type de check inconnu: {}".format(t)


def eval_all(checks, ws, new_commands, new_pwds):
    """Evalue tous les checks. Retourne une liste de bool."""
    return [eval_check(c, ws, new_commands, new_pwds)[0] for c in checks]


def apply_setup(actions, ws):
    """Prepare l'arene du niveau (dossiers/fichiers de depart)."""
    for action in actions or []:
        if "mkdir" in action:
            os.makedirs(resolve(action["mkdir"], ws), exist_ok=True)
        elif "file" in action:
            p = resolve(action["file"], ws)
            parent = os.path.dirname(p)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(action.get("content", ""))
            if action.get("mode"):
                os.chmod(p, int(str(action["mode"]), 8))
        elif "chmod" in action:
            p = resolve(action["chmod"], ws)
            if os.path.lexists(p):
                os.chmod(p, int(str(action.get("mode", "644")), 8))
        elif "symlink" in action:
            p = resolve(action["symlink"], ws)
            parent = os.path.dirname(p)
            if parent:
                os.makedirs(parent, exist_ok=True)
            if not os.path.lexists(p):
                os.symlink(action.get("target", ""), p)
