"""Jour 2 (niveaux 11-20) : Explorer avec ls."""

from .common import L, F, D, C_cmd, C_fe, C_fc

SETUP_LS = (
    D("docs"),
    F("rapport.txt", "Rapport annuel : tout va bien.\n"),
    F("photo.jpg", "fausse image, chut\n"),
    F(".secret", "fichier cache !\n"),
    F("docs/notes.txt", "des notes\n"),
    F("docs/todo.txt", "des choses a faire\n"),
)

LEVELS = [
    L(11, "Lister (ls)",
      lesson="'ls' (list) affiche le contenu du dossier courant : fichiers et sous-dossiers. "
             "C'est la commande que tu taperas des milliers de fois dans ta vie d'admin.",
      mission="Tape, juste en dessous :  ls",
      setup=SETUP_LS,
      checks=[C_cmd(r"(^|[;&|]\s*)\bls\b")],
      hints=["2 lettres : l, s.", "Tape : ls"],
      solution="ls",
      story="On t'a parachute dans un dossier inconnu. Avant de toucher a quoi que ce soit : regarder ce qu'il y a."),

    L(12, "Les details (ls -l)",
      lesson="'ls -l' (long) montre les details : permissions, proprietaire, taille, date. "
             "Un admin lit ca comme un medecin lit une radio.",
      mission="Affiche le contenu detaille de l'arene avec :  ls -l",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b.*-[a-zA-Z]*l")],
      hints=["ls, espace, tiret, L minuscule.", "Tape : ls -l"],
      solution="ls -l"),

    L(13, "Les caches (ls -a)",
      lesson="'ls -a' (all) montre aussi les fichiers caches, ceux qui commencent par un point. "
             "Sous Linux, pas de case 'fichier cache' : un point devant le nom suffit.",
      mission="Affiche TOUT, y compris les caches, avec :  ls -a",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b.*-[a-zA-Z]*a")],
      hints=["Le 'a' de all (tout).", "Tape : ls -a"],
      solution="ls -a",
      story="Il parait qu'un fichier secret se cache ici... Les options de ls vont le denicher."),

    L(14, "Tailles lisibles (ls -lh)",
      lesson="'ls -lh' combine -l (details) et -h (human : tailles en K, M, G au lieu d'octets). "
             "On peut combiner les options : -lh = -l -h.",
      mission="Affiche les details avec tailles lisibles :  ls -lh",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b.*-[a-zA-Z]*h")],
      hints=["Ajoute h a ton ls -l.", "Tape : ls -lh"],
      solution="ls -lh"),

    L(15, "Tout voir, partout (ls -R)",
      lesson="'ls -R' (recursif) descend dans les sous-dossiers et affiche tout l'arbre. "
             "Pratique pour une vue d'ensemble... mais a eviter a la racine / (trop de monde !).",
      mission="Affiche l'arene et ses sous-dossiers avec :  ls -R",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b.*-[a-zA-Z]*R")],
      hints=["R comme Recursif (majuscule !).", "Tape : ls -R"],
      solution="ls -R"),

    L(16, "Trier par date (ls -lt)",
      lesson="'ls -lt' trie par date de modification (le plus recent d'abord). "
             "Ideal pour retrouver 'le fichier que je viens de toucher' ou le dernier log.",
      mission="Liste l'arene triee par date avec :  ls -lt",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b.*-[a-zA-Z]*t")],
      hints=["t comme time (temps).", "Tape : ls -lt"],
      solution="ls -lt"),

    L(17, "Lister un autre dossier",
      lesson="'ls' accepte un chemin en argument : 'ls docs' liste le dossier docs sans y entrer. "
             "La plupart des commandes marchent comme ca : commande + cible.",
      mission="Liste le contenu du sous-dossier docs (sans y entrer) avec :  ls docs",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b[^\n;|&]*\bdocs\b")],
      hints=["ls suivi du nom du dossier.", "Tape : ls docs"],
      solution="ls docs"),

    L(18, "Le joker * (glob)",
      lesson="L'etoile '*' est un joker : 'ls *.txt' liste tous les fichiers finissant par .txt. "
             "On appelle ca le 'globbing'. Ton shell remplace * avant meme que ls ne s'execute.",
      mission="Liste uniquement les fichiers .txt de l'arene avec :  ls *.txt",
      setup=SETUP_LS,
      checks=[C_cmd(r"\bls\b[^\n;|&]*\*\.txt")],
      hints=["L'etoile remplace 'n'importe quoi'.", "Tape : ls *.txt"],
      solution="ls *.txt",
      story="Le dossier est plein. Heureusement, ton shell sait filtrer : demande seulement les .txt."),

    L(19, "Un par ligne, dans un fichier",
      lesson="'ls -1' (chiffre un) affiche un fichier par ligne : parfait pour rediriger vers un fichier "
             "ou enchainer avec d'autres commandes.",
      mission="Enregistre la liste des fichiers (un par ligne) dans liste.txt :  ls -1 > liste.txt",
      setup=SETUP_LS,
      checks=[C_fe("liste.txt"), C_fc("liste.txt", text="rapport.txt")],
      hints=["Combine ls -1 et la redirection >.", "Tape : ls -1 > liste.txt"],
      solution="ls -1 > liste.txt"),

    L(20, "BOSS du jour : inventaire complet",
      lesson="Revision : -a voit les caches, -l detaille, '>' sauvegarde. Un bon admin garde toujours une trace ecrite.",
      mission="Cree un inventaire COMPLET (caches inclus, en details) de l'arene dans inventaire.txt en une commande.",
      setup=SETUP_LS,
      checks=[C_fe("inventaire.txt"), C_fc("inventaire.txt", text=".secret")],
      hints=["Il faut -l, -a, et rediriger vers inventaire.txt.",
             "Tape : ls -la > inventaire.txt"],
      solution="ls -la > inventaire.txt",
      story="Le dragon de l'inventaire exige la liste de TOUT, meme les caches. Sinon, pas de niveau 21.",
      xp=25, boss=True),
]
