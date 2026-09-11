"""Chargement et validation des niveaux (Saison 1 + Saison 2...)."""

from .checker import CHECK_TYPES
from .packs import day01, day02, day03, day04, day05, day06, day07, day08, day09, day10
from .packs import days11_20, days21_30, days101_110
from .packs import generated

_CACHE = None


def all_levels():
    global _CACHE
    if _CACHE is None:
        levels = []
        for pack in (day01, day02, day03, day04, day05, day06, day07, day08, day09, day10):
            levels.extend(pack.LEVELS)
        levels.extend(days11_20.LEVELS)
        levels.extend(days21_30.LEVELS)
        # Blocs generes de Saison 1 non encore enrichis (jours 31-100).
        levels.extend(lv for lv in generated.build() if not 101 <= lv["id"] <= 300)
        levels.extend(days101_110.LEVELS)
        levels.sort(key=lambda lv: lv["id"])
        _CACHE = levels
    return _CACHE


def total():
    return len(all_levels())


def max_day():
    return max(lv["day"] for lv in all_levels())


def get_level(level_id):
    for lv in all_levels():
        if lv["id"] == level_id:
            return lv
    return None


def validate():
    """Verifie l'integrite des niveaux. Retourne une liste d'erreurs (vide = ok)."""
    errors = []
    levels = all_levels()
    ids = [lv.get("id") for lv in levels]
    if sorted(ids) != list(range(1, len(ids) + 1)):
        errors.append("les ids doivent couvrir 1..{} sans trou ni doublon".format(len(ids)))
    required = ("id", "day", "title", "lesson", "mission", "checks", "hints", "solution", "xp")
    for lv in levels:
        lid = lv.get("id", "?")
        for key in required:
            if key not in lv:
                errors.append("niveau {} : cle manquante '{}'".format(lid, key))
        if not lv.get("checks"):
            errors.append("niveau {} : aucun check".format(lid))
        if not lv.get("hints"):
            errors.append("niveau {} : aucun indice".format(lid))
        if lv.get("day") != (lid - 1) // 10 + 1:
            errors.append("niveau {} : jour incoherent ({})".format(lid, lv.get("day")))
        for c in lv.get("checks", []):
            if c.get("type") not in CHECK_TYPES:
                errors.append("niveau {} : type de check inconnu '{}'".format(lid, c.get("type")))
        for s in lv.get("setup", []):
            if not any(k in s for k in ("mkdir", "file", "chmod", "symlink")):
                errors.append("niveau {} : action setup inconnue {}".format(lid, s))
        if "scenario" in lv and not isinstance(lv["scenario"], dict):
            errors.append("niveau {} : scenario invalide".format(lid))
    return errors
