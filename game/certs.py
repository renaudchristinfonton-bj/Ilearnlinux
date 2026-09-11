"""Certificats de maitrise : recompenses officielles par bloc de competences.

Quand le joueur termine TOUS les niveaux d'un bloc (ex : le systeme de
fichiers), le jeu lui remet un certificat personnalise (SVG + HTML, aux
couleurs de la communaute), avec un code de verification unique.

La charte graphique est centralisee dans THEME : une seule variable a
adapter pour changer les couleurs / l'organisme sur tous les certificats.
"""

import base64
import hashlib
import os
import uuid
from xml.sax.saxutils import escape

# ---------------------------------------------------------------------------
# Charte graphique.
# TODO(charte) : remplacer par les couleurs/logo exacts d'ESPRITROPIC COMMUNITY
# des reception de la charte (fichier PDF non parvenu au jeu). Tout le reste
# (mise en page, textes) suit deja et s'adaptera automatiquement.
# ---------------------------------------------------------------------------
THEME = {
    "org": "ESPRITROPIC COMMUNITY",
    "program": "ILEARNLINUX — Formation d'agents cybersecurite",
    "primary": "#123B2A",      # vert sombre (couleur principale)
    "secondary": "#C9A227",    # dore (filets, sceau)
    "background": "#FAF6EC",   # fond ivoire
    "ink": "#1E1E1E",          # texte courant
    "muted": "#6B6B6B",        # texte secondaire
    "seal_emoji": "★",
    # Chemin optionnel vers le logo (PNG/JPG) : il est integre au certificat.
    # Exemple : "/home/user/logo-espritropic.png" ou "assets/logo.png".
    "logo_path": "",
}

CERTS_DIRNAME = "certificats"

# id, slug, titre, (1er niveau, dernier niveau), competences validees.
CERTS = [
    {"id": "CERT-01", "slug": "fondamentaux-du-terminal",
     "title": "Fondamentaux du terminal", "range": (1, 10),
     "skills": ["Se reperer (pwd, whoami)", "Afficher du texte (echo)",
                "Consulter l'aide", "Rediriger une sortie (>)"]},
    {"id": "CERT-02", "slug": "systeme-de-fichiers",
     "title": "Systeme de fichiers", "range": (11, 60),
     "skills": ["Explorer avec ls", "Naviguer avec cd",
                "Creer dossiers et fichiers", "Lire (cat, head, tail)",
                "Ranger (mv, cp, rm)"]},
    {"id": "CERT-03", "slug": "texte-et-recherche",
     "title": "Texte & recherche", "range": (61, 100),
     "skills": ["Redirections et pipes", "Filtrer avec grep",
                "Retrouver avec find", "Transformer (sort, uniq, cut)"]},
    {"id": "CERT-04", "slug": "permissions-et-droits",
     "title": "Permissions & droits", "range": (101, 200),
     "skills": ["Lire les droits (ls -l)", "chmod numerique et symbolique",
                "Scripts executables", "Liens symboliques"]},
    {"id": "CERT-05", "slug": "utilisateurs-et-groupes",
     "title": "Utilisateurs & groupes", "range": (201, 300),
     "skills": ["Identites (id, groups)", "Lire /etc/passwd",
                "Delegation avec sudo"]},
    {"id": "CERT-06", "slug": "archives-et-sauvegardes",
     "title": "Archives & sauvegardes", "range": (301, 400),
     "skills": ["Archiver avec tar", "Compresser (gzip)",
                "Strategie de sauvegarde"]},
    {"id": "CERT-07", "slug": "systeme-et-materiel",
     "title": "Systeme & materiel", "range": (401, 500),
     "skills": ["Noyau et version", "Disques et partitions",
                "Memoire et processeur"]},
    {"id": "CERT-08", "slug": "processus",
     "title": "Gestion des processus", "range": (501, 600),
     "skills": ["Observer (ps, top)", "Jobs d'arriere-plan",
                "Arreter proprement (kill)", "Persistance (nohup)"]},
    {"id": "CERT-09", "slug": "reseau",
     "title": "Reseau", "range": (601, 700),
     "skills": ["Tester (ping)", "Adresses IP", "DNS",
                "Ports et services", "Requetes (curl)"]},
    {"id": "CERT-10", "slug": "ssh-et-transferts",
     "title": "SSH & transferts", "range": (701, 800),
     "skills": ["Cles SSH", "Empreintes", "Copies (scp)", "Configuration client"]},
    {"id": "CERT-11", "slug": "scripting-shell",
     "title": "Scripting shell", "range": (801, 900),
     "skills": ["Variables", "Boucles for/while", "Tests (if)",
                "Fonctions"]},
    {"id": "CERT-12", "slug": "administration-pro",
     "title": "Administration pro", "range": (901, 1000),
     "skills": ["Journaux systeme", "Depannage methodique",
                "Gestion d'incidents"]},
    {"id": "CERT-13", "slug": "cyber-reconnaissance-intrusion",
     "title": "Cyber — Reconnaissance & intrusion", "range": (1001, 1030),
     "skills": ["Chasse aux flags", "Empreintes (hash)",
                "Scans nmap", "Connexions SSH"]},
    {"id": "CERT-14", "slug": "cyber-flags-mots-de-passe",
     "title": "Cyber — Flags & mots de passe", "range": (1031, 1050),
     "skills": ["Recherche avancee (find, grep)", "Encodage base64",
                "Audit de mots de passe (john)"]},
    {"id": "CERT-15", "slug": "cyber-forensics-web",
     "title": "Cyber — Forensics & web", "range": (1051, 1070),
     "skills": ["Analyse de journaux", "Rapports d'incident",
                "Enumeration web"]},
    {"id": "CERT-16", "slug": "cyber-pivot-privesc",
     "title": "Cyber — Pivot & privilege", "range": (1071, 1090),
     "skills": ["Pivot reseau", "Binaires SUID",
                "Droits sudo", "Enumeration privesc"]},
    {"id": "CERT-17", "slug": "agent-cyber-certifie",
     "title": "Agent Cyber certifie", "range": (1091, 1100),
     "skills": ["Examen mini-CTF complet", "Scan + intrusion + craquage",
                "Forensics + web + rapport"]},
]


def get_cert(cert_id):
    for cert in CERTS:
        if cert["id"] == cert_id:
            return cert
    return None


def _covered(cert, done_set):
    first, last = cert["range"]
    return all(n in done_set for n in range(first, last + 1))


def range_progress(cert, done_set):
    """Retourne (niveaux reussis, total) dans la plage du certificat."""
    first, last = cert["range"]
    total = last - first + 1
    n = sum(1 for n in range(first, last + 1) if n in done_set)
    return n, total


def newly_earned(progress):
    """Certificats couverts mais pas encore remis. Liste de definitions."""
    done_set = set(progress.get("done", []))
    issued = set(progress.get("certs", {}).keys())
    return [c for c in CERTS if c["id"] not in issued and _covered(c, done_set)]


def next_certificates(progress, limit=3):
    """Prochains certificats non termines, avec (reussis, total). Tries."""
    done_set = set(progress.get("done", []))
    upcoming = []
    for cert in CERTS:
        if _covered(cert, done_set):
            continue
        n, total = range_progress(cert, done_set)
        upcoming.append((cert, n, total))
    upcoming.sort(key=lambda item: (-(item[1] / item[2]), item[0]["id"]))
    return upcoming[:limit]


# -- profil & codes ---------------------------------------------------------
def profile_name(progress):
    return (progress.get("profile", {}) or {}).get("name", "")


def set_profile_name(progress, name):
    from . import progress as progress_mod
    prof = progress.setdefault("profile", {})
    prof["name"] = name.strip()
    if not prof.get("secret"):
        prof["secret"] = uuid.uuid4().hex
    progress_mod.save(progress)
    return prof["name"]


def ask_profile_name(progress, ask_fn=None):
    """Demande le nom une seule fois (pour les certificats). Jamais bloquant."""
    name = profile_name(progress)
    if name:
        return name
    ask = ask_fn or (lambda prompt: input(prompt))
    try:
        answer = (ask("Ton nom pour les certificats ( MEMOIRE : affiche tel quel) : ") or "").strip()
    except (EOFError, KeyboardInterrupt):
        answer = ""
    return set_profile_name(progress, answer or "Agent")


def issue_code(progress, cert_id, name):
    """Code de verification deterministe : ILEARN-XXXX-XXXX."""
    secret = ((progress.get("profile", {}) or {}).get("secret") or "ilearn")
    raw = hashlib.sha256("{}|{}|{}".format(secret, cert_id, name).encode("utf-8")).digest()
    token = base64.b32encode(raw[:5]).decode("ascii").rstrip("=")
    return "ILEARN-{}-{}".format(token[:4], token[4:8])


def verify_code(progress, code):
    """Retourne (cert, name) si le code correspond a un certificat remis."""
    code = (code or "").strip().upper()
    for cert_id, record in (progress.get("certs", {}) or {}).items():
        if str(record.get("code", "")).upper() == code:
            return get_cert(cert_id), record.get("name", "")
    return None, ""


# -- generation des documents -----------------------------------------------
def certs_dir(base_dir):
    path = os.path.join(base_dir, CERTS_DIRNAME)
    os.makedirs(path, exist_ok=True)
    return path


def issue(progress, cert, name, date_text):
    """Enregistre le certificat et genere les fichiers. Retourne (code, svg, html)."""
    from . import progress as progress_mod
    code = issue_code(progress, cert["id"], name)
    certs = progress.setdefault("certs", {})
    record = certs.get(cert["id"], {})
    record.update({"at": date_text, "code": code, "name": name, "title": cert["title"]})
    certs[cert["id"]] = record
    progress_mod.save(progress)
    directory = certs_dir(progress_mod.BASE_DIR)
    svg_path = os.path.join(directory, "{}-{}.svg".format(cert["id"], cert["slug"]))
    html_path = os.path.join(directory, "{}-{}.html".format(cert["id"], cert["slug"]))
    svg = render_svg(cert, name, code, date_text)
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(render_html(cert, name, code, date_text, svg))
    return code, svg_path, html_path


def level_label(cert):
    first, last = cert["range"]
    day_first = (first - 1) // 10 + 1
    day_last = (last - 1) // 10 + 1
    if day_first == day_last:
        days = "jour {}".format(day_first)
    else:
        days = "jours {} a {}".format(day_first, day_last)
    return "Niveaux {} a {} ({}, Saison {})".format(
        first, last, days, 1 if last <= 1000 else 2)


_LOGO_CACHE = {}


def logo_data_uri():
    """Logo encode en data-URI (mis en cache), ou chaine vide."""
    path = (THEME.get("logo_path") or "").strip()
    if not path or not os.path.isfile(path):
        return ""
    if path in _LOGO_CACHE:
        return _LOGO_CACHE[path]
    try:
        with open(path, "rb") as fh:
            raw = fh.read(512 * 1024)
    except OSError:
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext != ".jpg" and ext != ".jpeg" else "image/jpeg"
    if ext == ".svg":
        mime = "image/svg+xml"
    import base64 as _b64
    uri = "data:{};base64,{}".format(mime, _b64.b64encode(raw).decode("ascii"))
    _LOGO_CACHE[path] = uri
    return uri


def render_svg(cert, name, code, date_text):
    t = THEME
    skills = "".join(
        "<text x=\"140\" y=\"{}\" font-family=\"Georgia, 'DejaVu Serif', serif\" font-size=\"21\" "
        "fill=\"{}\">✓ {}</text>".format(560 + i * 34, t["ink"], escape(skill))
        for i, skill in enumerate(cert["skills"][:6]))
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1122" height="794" viewBox="0 0 1122 794">
  <rect x="0" y="0" width="1122" height="794" fill="{bg}"/>
  <rect x="18" y="18" width="1086" height="758" fill="none" stroke="{primary}" stroke-width="6"/>
  <rect x="34" y="34" width="1054" height="726" fill="none" stroke="{secondary}" stroke-width="2"/>
  <rect x="34" y="34" width="1054" height="130" fill="{primary}"/>
{logo}
  <text x="561" y="88" text-anchor="middle" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="34" font-weight="bold" letter-spacing="4" fill="#FFFFFF">{org}</text>
  <text x="561" y="126" text-anchor="middle" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="17" letter-spacing="2" fill="{secondary}">{program}</text>
  <text x="561" y="228" text-anchor="middle" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="26" letter-spacing="6" fill="{muted}">CERTIFICAT DE MAITRISE</text>
  <text x="561" y="292" text-anchor="middle" font-family="Georgia, 'DejaVu Serif', serif" font-size="52" font-weight="bold" fill="{primary}">{title}</text>
  <text x="561" y="348" text-anchor="middle" font-family="Georgia, 'DejaVu Serif', serif" font-size="22" font-style="italic" fill="{muted}">decerne a</text>
  <text x="561" y="412" text-anchor="middle" font-family="'Snell Roundhand', 'DejaVu Serif', Georgia, serif" font-size="54" font-style="italic" fill="{ink}">{name}</text>
  <line x1="311" y1="436" x2="811" y2="436" stroke="{secondary}" stroke-width="2"/>
  <text x="140" y="508" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="19" font-weight="bold" letter-spacing="2" fill="{primary}">COMPETENCES VALIDEES</text>
{skills}
  <text x="982" y="610" text-anchor="middle" font-family="Georgia, serif" font-size="86" fill="{secondary}">{seal}</text>
  <text x="982" y="648" text-anchor="middle" font-family="Verdana, sans-serif" font-size="13" letter-spacing="2" fill="{primary}">{cert_id}</text>
  <text x="140" y="700" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="16" fill="{muted}">{level_label}</text>
  <text x="140" y="728" font-family="Verdana, 'DejaVu Sans', sans-serif" font-size="16" fill="{muted}">Delivre le {date} — Verification : {code}</text>
  <text x="982" y="700" text-anchor="middle" font-family="Georgia, serif" font-size="20" font-style="italic" fill="{ink}">L'agence ILearnLinux</text>
  <line x1="872" y1="716" x2="1092" y2="716" stroke="{muted}" stroke-width="1"/>
  <text x="982" y="736" text-anchor="middle" font-family="Verdana, sans-serif" font-size="12" fill="{muted}">formation pratique, 100% terminal</text>
</svg>
""".format(bg=t["background"], primary=t["primary"], secondary=t["secondary"],
           muted=t["muted"], ink=t["ink"], org=escape(t["org"]),
           program=escape(t["program"]), title=escape(cert["title"]),
           name=escape(name), skills=skills, seal=t["seal_emoji"],
           cert_id=escape(cert["id"]), level_label=escape(level_label(cert)),
           date=escape(date_text), code=escape(code), logo=logo_image_tag())


def logo_image_tag():
    uri = logo_data_uri()
    if not uri:
        return ""
    return ('  <image x="58" y="50" width="98" height="98" preserveAspectRatio="xMidYMid meet" '
            'href="{}"/>').format(escape(uri, {'"': "&quot;"}))


def render_html(cert, name, code, date_text, svg):
    t = THEME
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>{cid} — {title} — {name}</title>
<style>
  body {{ font-family: Verdana, 'DejaVu Sans', sans-serif; background: #222; color: #eee;
         margin: 0; padding: 24px; text-align: center; }}
  .sheet {{ display: inline-block; background: #fff; padding: 12px; border-radius: 8px;
           box-shadow: 0 0 40px rgba(0,0,0,.6); max-width: 1150px; }}
  svg {{ width: 100%; height: auto; display: block; }}
  .actions {{ margin: 16px; }}
  button {{ font-size: 16px; padding: 10px 22px; border-radius: 6px; border: none;
           background: {secondary}; color: #111; font-weight: bold; cursor: pointer; }}
  p.note {{ color: #bbb; font-size: 13px; }}
  @media print {{ body {{ background: #fff; padding: 0; }} .actions, p.note {{ display: none; }}
    .sheet {{ box-shadow: none; padding: 0; }} }}
</style>
</head>
<body>
<div class="sheet">{svg}</div>
<div class="actions"><button onclick="window.print()">Imprimer / Enregistrer en PDF</button></div>
<p class="note">Certificat {cid} delivre par {org} — Verification : {code}</p>
</body>
</html>
""".format(cid=escape(cert["id"]), title=escape(cert["title"]), name=escape(name),
           secondary=t["secondary"], svg=svg, org=escape(t["org"]), code=escape(code))
