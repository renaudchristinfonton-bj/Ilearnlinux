"""Jour 8 (niveaux 71-80) : Chercher du texte avec grep."""

from .common import L, F, D, C_cmd, C_fe, C_fc, C_fnc, C_nempty

ELEVES = "marie\npaul\nmarie-line\njean\nsophie\n"
JOURNAL = (
    "2026-01-01 bonne annee\n"
    "2026-02-14 fete\n"
    "2025-12-25 Noel dernier\n"
    "2026-03-01 printemps\n"
)

LEVELS = [
    L(71, "Chercher un mot (grep)",
      lesson="'grep mot fichier' affiche les lignes contenant 'mot'. C'est le Ctrl+F du terminal, "
             "en 1000 fois plus puissant.",
      mission="Cherche 'marie' dans eleves.txt :  grep marie eleves.txt",
      setup=[F("eleves.txt", ELEVES)],
      checks=[C_cmd(r"\bgrep\b[^\n;|&]*marie")],
      hints=["grep, espace, mot, espace, fichier.", "Tape : grep marie eleves.txt"],
      solution="grep marie eleves.txt",
      story="La maitresse cherche tous les 'marie' de la classe. grep est son meilleur ami."),

    L(72, "Ignorer la casse (-i)",
      lesson="'grep -i' cherche sans distinguer majuscules/minuscules : 'MARIE', 'marie', 'Marie' matchent tous. "
             "Indispensable quand on ne connait pas la casse exacte.",
      mission="Cherche 'MARIE' (majuscules) dans eleves.txt avec :  grep -i MARIE eleves.txt",
      setup=[F("eleves.txt", ELEVES)],
      checks=[C_cmd(r"\bgrep\b[^\n;|&]*-i")],
      hints=["Ajoute -i a ton grep.", "Tape : grep -i MARIE eleves.txt"],
      solution="grep -i MARIE eleves.txt"),

    L(73, "Inverser la recherche (-v)",
      lesson="'grep -v mot' affiche les lignes qui ne contiennent PAS le mot. "
             "Pour exclure le bruit et ne garder que l'interessant.",
      mission="Garde les eleves presents (lignes SANS 'absent') dans presents.txt :  grep -v absent classe.txt > presents.txt",
      setup=[F("classe.txt", "marie\npaul absent\njean\nsophie absente\n")],
      checks=[C_fe("presents.txt"), C_fc("presents.txt", text="marie"), C_fnc("presents.txt", text="absent")],
      hints=["grep -v absent classe.txt > presents.txt", "-v = inverser (montrer ce qui ne matche pas)."],
      solution="grep -v absent classe.txt > presents.txt"),

    L(74, "Compter les matchs (-c)",
      lesson="'grep -c mot fichier' COMPTE les lignes qui matchent au lieu de les afficher. "
             "Combien d'erreurs dans ce log de 50 000 lignes ? grep -c te repond en 1 seconde.",
      mission="Compte les lignes contenant 'linux' dans doc.txt et sauve le resultat dans score.txt.",
      setup=[F("doc.txt", "linux est cool\nj'aime linux\nlinux partout\nwindows aussi\n")],
      checks=[C_fe("score.txt"), C_fc("score.txt", regex=r"3")],
      hints=["grep -c linux doc.txt > score.txt", "-c = count (compter)."],
      solution="grep -c linux doc.txt > score.txt",
      story="Le journaliste veut savoir combien de fois 'linux' apparait dans l'article. Compte vite."),

    L(75, "Numeros de ligne (-n)",
      lesson="'grep -n' affiche le NUMERO de chaque ligne qui matche. 'Erreur ligne 42' : tu sais ou regarder.",
      mission="Cherche 'jean' avec numeros de ligne :  grep -n jean eleves.txt",
      setup=[F("eleves.txt", ELEVES)],
      checks=[C_cmd(r"\bgrep\b[^\n;|&]*-n")],
      hints=["Ajoute -n a ton grep.", "Tape : grep -n jean eleves.txt"],
      solution="grep -n jean eleves.txt"),

    L(76, "Fouiller partout (-r)",
      lesson="'grep -r mot dossier' cherche dans TOUS les fichiers du dossier et ses sous-dossiers. "
             "'Ou ai-je mis ce mot de passe ?' -> grep -r le retrouve.",
      mission="Cherche 'tresor' dans toute l'arene avec :  grep -r tresor .",
      setup=[D("coffre"), F("coffre/carte.txt", "le tresor est ici\n"), F("rien.txt", "rien\n")],
      checks=[C_cmd(r"\bgrep\b[^\n;|&]*-r")],
      hints=["grep -r tresor . (le . = dossier courant).", "Tape : grep -r tresor ."],
      solution="grep -r tresor .",
      story="Un tresor est enterre quelque part dans l'arene. grep -r est ton detecteur de metaux."),

    L(77, "Filtrer une liste (| grep)",
      lesson="'ls -1 | grep txt' ne garde que les lignes contenant 'txt'. Le combo ls+grep filtre n'importe quelle liste : "
             "fichiers, processus, paquets...",
      mission="Liste les fichiers .txt via pipe :  ls -1 | grep txt > textes.txt (verifie que textes.txt contient 'notes.txt').",
      setup=[F("notes.txt", "n\n"), F("photo.jpg", "p\n"), F("doc.txt", "d\n")],
      checks=[C_fe("textes.txt"), C_fc("textes.txt", text="notes.txt")],
      hints=["ls -1 | grep txt > textes.txt", "ls produit la liste, grep filtre, > sauve."],
      solution="ls -1 | grep txt > textes.txt"),

    L(78, "Debut de ligne (^)",
      lesson="En regex, '^' signifie 'debut de ligne' : 'grep ^Marie' ne matche que les lignes COMMENCANT par Marie. "
             "Ton premier super-pouvoir regex !",
      mission="Affiche les lignes commencant par '2026' dans journal.txt :  grep ^2026 journal.txt",
      setup=[F("journal.txt", JOURNAL)],
      checks=[C_cmd(r"\bgrep\b[^\n]*\^2026")],
      hints=["grep ^2026 journal.txt", "^ = 'commence par'. Mets-le entre guillemets si besoin."],
      solution="grep ^2026 journal.txt"),

    L(79, "Enchainer grep et wc",
      lesson="Le grand classique de l'admin : 'grep erreur log.txt | wc -l' compte les erreurs. "
             "Filtrer PUIS compter : 90% de l'analyse de logs tient en ca.",
      mission="Compte les lignes 2026 du journal :  grep 2026 journal.txt | wc -l",
      setup=[F("journal.txt", JOURNAL)],
      checks=[C_cmd(r"\bgrep\b[^\n]*\|[^\n]*\bwc\b")],
      hints=["grep 2026 journal.txt | wc -l", "grep filtre, wc -l compte."],
      solution="grep 2026 journal.txt | wc -l"),

    L(80, "BOSS du jour : chasse aux erreurs",
      lesson="Revision : -i ignore la casse, '>' sauve. Extraire toutes les erreurs d'un log, proprement.",
      mission="Extrait TOUTES les lignes d'erreur (majuscules ou minuscules) de systeme.log vers erreurs.txt en une commande.",
      setup=[F("systeme.log", "demarrage ok\nERREUR disque plein\naudit ok\nerreur reseau\narret ok\n")],
      checks=[C_fe("erreurs.txt"), C_fc("erreurs.txt", text="disque"), C_fc("erreurs.txt", text="reseau"),
              C_fnc("erreurs.txt", text="demarrage")],
      hints=["grep -i erreur systeme.log > erreurs.txt", "-i attrape ERREUR et erreur d'un coup."],
      solution="grep -i erreur systeme.log > erreurs.txt",
      story="Le serveur tousse. Le medecin-chef veut TOUTES les erreurs du log, et vite. A toi de jouer.",
      xp=25, boss=True),
]
