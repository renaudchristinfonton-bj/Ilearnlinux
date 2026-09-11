"""Jour 9 (niveaux 81-90) : Retrouver des fichiers avec find."""

from .common import L, F, D, C_cmd, C_fe, C_ne, C_fc

SETUP_FIND = (
    D("grenier/boites"),
    D("cave"),
    F("grenier/tresor.txt", "le tresor !\n"),
    F("grenier/vieux-journal.txt", "poussiere\n"),
    F("grenier/boites/photo.jpg", "souvenir\n"),
    F("cave/vin.txt", "grand cru\n"),
    F("cave/vieux.bak", "bak1\n"),
    F("grenier/vieux.bak", "bak2\n"),
)

LEVELS = [
    L(81, "Chercher par nom (-name)",
      lesson="'find . -name '*.txt'' cherche tous les .txt depuis ici. Les guillemets protegent le * du shell : "
             "c'est find qui doit l'interpreter, pas le shell.",
      mission="Cherche tous les .txt de l'arene :  find . -name '*.txt'",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*-name")],
      hints=["find . -name '*.txt' (avec les guillemets).", "Le . = 'commencer ici'."],
      solution="find . -name '*.txt'",
      story="La maison est immense. find est ton chien truffier : il renifle les fichiers par leur nom."),

    L(82, "Chercher des fichiers (-type f)",
      lesson="'find . -type f' ne liste que les FICHIERS (pas les dossiers). 'f' comme file. "
             "Pratique pour compter ou traiter uniquement les vrais fichiers.",
      mission="Liste tous les fichiers de l'arene :  find . -type f",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*-type\s+f")],
      hints=["find . -type f", "f = file (fichier)."],
      solution="find . -type f"),

    L(83, "Chercher des dossiers (-type d)",
      lesson="'find . -type d' ne liste que les DOSSIERS. 'd' comme directory. "
             "Pour cartographier une arborescence sans le bruit des fichiers.",
      mission="Liste tous les dossiers de l'arene :  find . -type d",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*-type\s+d")],
      hints=["find . -type d", "d = directory (dossier)."],
      solution="find . -type d"),

    L(84, "Localiser le tresor",
      lesson="find + redirection = rapport de recherche. 'find . -name tresor.txt > cachette.txt' : "
             "l'emplacement du tresor est sauvegarde, preuve a l'appui.",
      mission="Localise tresor.txt et sauve son emplacement dans cachette.txt en une commande.",
      setup=SETUP_FIND,
      checks=[C_fe("cachette.txt"), C_fc("cachette.txt", text="tresor.txt")],
      hints=["find . -name tresor.txt > cachette.txt", "find cherche, > sauve le resultat."],
      solution="find . -name tresor.txt > cachette.txt"),

    L(85, "Chercher les gros fichiers (-size)",
      lesson="'find . -size +100k' trouve les fichiers de plus de 100 ko. '+100M' = plus de 100 Mo. "
             "Quand le disque est plein, c'est comme ca qu'on deniche les coupables.",
      mission="Trouve les fichiers de plus de 100 ko :  find . -size +100k",
      setup=[F("petit.txt", "minuscule\n"), F("gros.dat", "x" * 200000)],
      checks=[C_cmd(r"\bfind\b[^\n]*-size")],
      hints=["find . -size +100k", "+100k = plus de 100 kilo-octets."],
      solution="find . -size +100k",
      story="Le disque se remplit mysterieursement... Un gros fichier se cache ici. Trouve-le."),

    L(86, "Chercher les recents (-mtime)",
      lesson="'find . -mtime -1' trouve les fichiers modifies il y a MOINS d'1 jour. '+7' = il y a PLUS de 7 jours. "
             "'Qu'est-ce qui a change cette nuit ?' -> find -mtime.",
      mission="Trouve les fichiers modifies recemment :  find . -mtime -1",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*-mtime")],
      hints=["find . -mtime -1", "-1 = moins d'un jour."],
      solution="find . -mtime -1"),

    L(87, "Chercher les vides (-empty)",
      lesson="'find . -empty' trouve fichiers ET dossiers vides. Les fichiers vides oublies sont comme les miettes : "
             "partout, et personne ne les a mis la (officiellement).",
      mission="Trouve les fichiers vides de l'arene :  find . -empty",
      setup=[F("vide.txt", ""), F("plein.txt", "contenu\n")],
      checks=[C_cmd(r"\bfind\b[^\n]*-empty")],
      hints=["find . -empty", "Un fichier vide est un fichier de 0 octet."],
      solution="find . -empty"),

    L(88, "Supprimer via find (-delete)",
      lesson="'find . -name '*.bak' -delete' supprime tous les .bak trouves. find cherche ET agit. "
             "DANGER : teste TOUJOURS sans -delete d'abord (sinon, adieu les fichiers... et peut-etre ton week-end).",
      mission="D'abord liste les .bak (find . -name '*.bak'), VERIFIE, puis supprime-les avec -delete.",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*-delete"), C_ne("cave/vieux.bak"), C_ne("grenier/vieux.bak"),
              C_fe("cave/vin.txt")],
      hints=["Etape 1 : find . -name '*.bak' (verifier)", "Etape 2 : find . -name '*.bak' -delete"],
      solution="find . -name '*.bak' puis find . -name '*.bak' -delete",
      story="Des .bak trainent partout depuis des mois. find va les denicher et les liquider. Proprement."),

    L(89, "find + grep : le duo",
      lesson="'find . -type f | grep conf' : find liste les fichiers, grep filtre ceux qui parlent de 'conf'. "
             "Deux specialists valent mieux qu'un.",
      mission="Liste les fichiers puis filtre ceux contenant 'vin' :  find . -type f | grep vin",
      setup=SETUP_FIND,
      checks=[C_cmd(r"\bfind\b[^\n]*\|[^\n]*\bgrep\b")],
      hints=["find . -type f | grep vin", "find produit, grep filtre."],
      solution="find . -type f | grep vin"),

    L(90, "BOSS du jour : rapport de logs",
      lesson="Revision : find cherche par nom et type, '>' sauve. Produire un rapport precis en une ligne.",
      mission="Liste tous les FICHIERS .log de l'arene dans logs.txt en une commande (find ... -type f ...).",
      setup=[D("srv"), F("srv/a.log", "a\n"), F("srv/b.log", "b\n"), F("srv/readme.txt", "r\n"), D("srv/vieux.log")],
      checks=[C_fe("logs.txt"), C_fc("logs.txt", text="a.log"), C_fc("logs.txt", text="b.log")],
      hints=["find . -type f -name '*.log' > logs.txt", "Combine -type f et -name, puis redirige."],
      solution="find . -type f -name '*.log' > logs.txt",
      story="L'auditeur veut la liste EXACTE des fichiers .log. Pas les dossiers qui s'appellent .log, hein. Sois precis.",
      xp=25, boss=True),
]
