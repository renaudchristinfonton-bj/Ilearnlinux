"""Jour 1 (niveaux 1-10) : Bienvenue dans le terminal."""

from .common import L, F, D, C_cmd, C_fe, C_fc, C_nempty

LEVELS = [
    L(1, "Premier contact",
      lesson="Le terminal est une fenetre ou tu parles a Linux avec des commandes. "
             "La commande 'echo' repete simplement ce que tu lui donnes. Essaie : elle ne mord pas.",
      mission="Tape ta premiere commande, juste en dessous :  echo je-suis-pret",
      checks=[C_cmd(r"\becho\b.*je-suis-pret")],
      hints=["Tape la commande juste en dessous, dans le terminal du jeu.",
             "Tape exactement : echo je-suis-pret  puis Entree."],
      solution="echo je-suis-pret",
      story="An 2026. Ton clavier vibre. Une voix robotique murmure : 'Humain... tape ta premiere commande, et ton aventure commence.'"),

    L(2, "Ou suis-je ? (pwd)",
      lesson="'pwd' signifie Print Working Directory : il affiche le dossier ou tu te trouves. "
             "Sous Linux, tout est organise en dossiers qui partent de la racine '/'.",
      mission="Tape, juste en dessous :  pwd",
      checks=[C_cmd(r"(^|[;&|]\s*)\bpwd\b")],
      hints=["3 lettres : p, w, d.", "Tape 'pwd' puis Entree."],
      solution="pwd",
      story="Tu te reveilles dans un labyrinthe de dossiers. Premier reflexe d'un explorateur : regarder ou il est."),

    L(3, "Qui suis-je ? (whoami)",
      lesson="'whoami' affiche ton nom d'utilisateur. Linux est multi-utilisateurs : chacun a son compte, "
             "ses droits, son dossier personnel (~).",
      mission="Tape, juste en dessous :  whoami",
      checks=[C_cmd(r"(^|[;&|]\s*)\bwhoami\b")],
      hints=["C'est de l'anglais : who am i = qui suis-je ?", "Tape 'whoami' puis Entree."],
      solution="whoami"),

    L(4, "Echo, l'ami fidele",
      lesson="'echo' affiche du texte. C'est LA commande pour tester, afficher des messages, "
             "et plus tard ecrire dans des fichiers.",
      mission="Tape, juste en dessous :  echo linux-cest-cool",
      checks=[C_cmd(r"\becho\b.*linux-cest-cool")],
      hints=["echo suivi de ton texte.", "Tape : echo linux-cest-cool"],
      solution="echo linux-cest-cool"),

    L(5, "Quelle heure est-il ? (date)",
      lesson="'date' affiche la date et l'heure du systeme. Les serveurs Linux tournent grace a une horloge precise : "
             "logs, sauvegardes, taches planifiees, tout en depend.",
      mission="Affiche la date du systeme avec la commande date.",
      checks=[C_cmd(r"(^|[;&|]\s*)\bdate\b")],
      hints=["4 lettres, en anglais.", "Tape : date"],
      solution="date"),

    L(6, "Faire le menage (clear)",
      lesson="'clear' nettoie l'ecran du terminal (ou Ctrl+L). Quand ton terminal ressemble a un champ de bataille, "
             "un petit clear et on repart zen.",
      mission="Nettoie ton terminal avec la commande clear.",
      checks=[C_cmd(r"(^|[;&|]\s*)\bclear\b")],
      hints=["En anglais, 'clear' = nettoyer, effacer.", "Tape : clear"],
      solution="clear"),

    L(7, "La memoire du terminal (history)",
      lesson="'history' affiche les commandes que tu as deja tapees. Astuce de pro : la fleche HAUT rejoue "
             "la derniere commande, Ctrl+R cherche dans l'historique.",
      mission="Affiche ton historique de commandes avec history.",
      checks=[C_cmd(r"(^|[;&|]\s*)\bhistory\b")],
      hints=["Le mot anglais pour 'historique'.", "Tape : history"],
      solution="history"),

    L(8, "Demander de l'aide (--help)",
      lesson="Presque chaque commande explique comment l'utiliser avec '--help'. Exemple : 'ls --help'. "
             "C'est ton mode d'emploi integre, gratuit, sans pub.",
      mission="Affiche l'aide de la commande ls :  ls --help",
      checks=[C_cmd(r"\bls\b.*--help")],
      hints=["ls, espace, tiret-tiret, help.", "Tape : ls --help"],
      solution="ls --help"),

    L(9, "Ecrire dans un fichier (>)",
      lesson="Le symbole '>' redirige la sortie d'une commande vers un fichier. "
             "'echo salut > bonjour.txt' cree le fichier bonjour.txt contenant 'salut'. Magique, non ?",
      mission="Ici meme, cree un fichier bonjour.txt contenant le mot 'salut' avec :  echo salut > bonjour.txt",
      checks=[C_fe("bonjour.txt"), C_fc("bonjour.txt", text="salut")],
      hints=["Tu es deja dans le dossier de mission : tape directement.",
             "Tape : echo salut > bonjour.txt"],
      solution="echo salut > bonjour.txt",
      story="Tu viens de decouvrir un super-pouvoir : creer des fichiers sans editeur, d'une seule ligne."),

    L(10, "BOSS du jour : carte d'identite",
      lesson="Revision express : echo affiche, '>' ecrit dans un fichier. Un admin automatise tout, et tout commence par ca.",
      mission="Ici meme, cree un fichier moi.txt contenant ton prenom (ou pseudo), en UNE commande echo avec redirection.",
      checks=[C_fe("moi.txt"), C_nempty("moi.txt")],
      hints=["Modele : echo TON_PRENOM > moi.txt",
             "Remplace TON_PRENOM par ton vrai prenom, sans espaces."],
      solution="echo ton-prenom > moi.txt",
      story="Le gardien du niveau 10 te bloque le passage : 'Prouve que tu sais ecrire dans un fichier, humain.'",
      xp=25, boss=True),
]
