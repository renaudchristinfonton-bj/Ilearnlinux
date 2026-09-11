#!/usr/bin/env python3
"""Auto-test : valide les niveaux + simule des parties (sans toucher au home reel)."""

import os
import shutil
import stat
import sys
import tempfile

TMP = tempfile.mkdtemp(prefix="ilearn-test-")
os.environ["ILEARN_HOME"] = os.path.join(TMP, "home")
os.environ["ILEARN_ARENA"] = os.path.join(TMP, "arena")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import checker, levels, progress  # noqa: E402

PASS = 0


def ok(name, cond):
    global PASS
    assert cond, "ECHEC : {}".format(name)
    PASS += 1
    print("  [ok] {}".format(name))


def main():
    print("== validation des niveaux ==")
    errors = levels.validate()
    ok("1000 niveaux valides", not errors)
    if errors:
        print(errors[:5])
        sys.exit(1)
    all_lv = levels.all_levels()
    ok("ids 1..1000", [lv["id"] for lv in all_lv] == list(range(1, 1001)))
    ok("boss final = 1000", all_lv[-1]["id"] == 1000 and all_lv[-1]["boss"])

    print("== primitives du checker ==")
    ws = os.path.join(TMP, "ws")
    os.makedirs(ws)
    with open(os.path.join(ws, "a.txt"), "w") as fh:
        fh.write("bonjour monde\n")
    os.makedirs(os.path.join(ws, "d"))
    os.chmod(os.path.join(ws, "a.txt"), 0o644)
    os.symlink("a.txt", os.path.join(ws, "lien"))

    def ev(c, cmds=(), pwds=()):
        return checker.eval_check(c, ws, list(cmds), list(pwds))[0]

    ok("file_exists", ev({"type": "file_exists", "path": "a.txt"}))
    ok("dir_exists", ev({"type": "dir_exists", "path": "d"}))
    ok("not_exists", ev({"type": "not_exists", "path": "zzz"}))
    ok("file_contains", ev({"type": "file_contains", "path": "a.txt", "text": "jour"}))
    ok("file_contains regex", ev({"type": "file_contains", "path": "a.txt", "regex": r"bon\w+"}))
    ok("file_not_contains", ev({"type": "file_not_contains", "path": "a.txt", "text": "zzz"}))
    ok("file_equals", ev({"type": "file_equals", "path": "a.txt", "expected": "bonjour monde\n"}))
    ok("file_not_empty", ev({"type": "file_not_empty", "path": "a.txt"}))
    ok("perm", ev({"type": "perm", "path": "a.txt", "mode": "644"}))
    ok("symlink", ev({"type": "symlink", "path": "lien", "target": "a.txt"}))
    ok("command", ev({"type": "command", "pattern": r"\bls\b"}, cmds=["ls -la"]))
    ok("command negatif", not ev({"type": "command", "pattern": r"\bls\b"}, cmds=["echo hi"]))
    ok("cwd", ev({"type": "cwd", "path": "{ws}/d"}, pwds=[ws + "/d"]))
    ok("dir_count", ev({"type": "dir_count", "path": "{ws}", "count": 3}))

    print("== simulation de niveaux ==")
    progress.ensure_dirs()
    # Niveau 9 : echo + redirection.
    lv9 = levels.get_level(9)
    ws9 = os.path.join(TMP, "arena", "niveau-0009")
    os.makedirs(ws9)
    with open(os.path.join(ws9, "bonjour.txt"), "w") as fh:
        fh.write("salut\n")
    ok("niveau 9 reussi", all(checker.eval_all(lv9["checks"], ws9, ["echo salut > bonjour.txt"], [ws9])))
    ok("niveau 9 echoue si vide", not all(checker.eval_all(lv9["checks"], TMP, [], [])))
    # Niveau 91 : sort exact.
    lv91 = levels.get_level(91)
    ws91 = os.path.join(TMP, "arena", "niveau-0091")
    os.makedirs(ws91)
    with open(os.path.join(ws91, "tries.txt"), "w") as fh:
        fh.write("marie\npaul\nzoe\n")
    ok("niveau 91 reussi", all(checker.eval_all(lv91["checks"], ws91, [], [])))
    # Niveau genere 150 (permissions) : setup + resolution.
    lv150 = levels.get_level(150)
    ws150 = os.path.join(TMP, "arena", "niveau-0150")
    os.makedirs(ws150)
    checker.apply_setup(lv150.get("setup", []), ws150)
    ok("niveau 150 : setup applicable", True)
    # Niveau 1000 : scenario final simule.
    lv1000 = levels.get_level(1000)
    wsM = os.path.join(TMP, "arena", "niveau-1000")
    os.makedirs(os.path.join(wsM, "projet-final"))
    app = os.path.join(wsM, "projet-final", "app.sh")
    with open(app, "w") as fh:
        fh.write("#!/bin/bash\necho en-ligne\n")
    os.chmod(app, os.stat(app).st_mode | stat.S_IXUSR)
    with open(os.path.join(wsM, "projet-final", "statut.txt"), "w") as fh:
        fh.write("en-ligne\nversion:1.0\n")
    with open(os.path.join(wsM, "projet-final.tar.gz"), "wb") as fh:
        fh.write(b"fake-archive")
    with open(os.path.join(wsM, "preuve.txt"), "w") as fh:
        fh.write("projet-final/app.sh\n")
    ok("niveau 1000 reussi", all(checker.eval_all(lv1000["checks"], wsM, [], [])))

    print("== progression ==")
    prog = progress.load()
    progress.record_completion(prog, 9, 10, 3, 0, False)
    prog2 = progress.load()
    ok("sauvegarde + avancement", 9 in prog2["done"] and prog2["current"] == 10 and prog2["xp"] == 10)

    shutil.rmtree(TMP, ignore_errors=True)
    print("\nTOUT EST VERT : {} tests reussis.".format(PASS))


if __name__ == "__main__":
    main()
