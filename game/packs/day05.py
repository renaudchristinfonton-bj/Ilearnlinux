"""Jour 5 (niveaux 41-50) : Lire des fichiers."""

from .common import L, F, C_cmd, C_fe, C_fc, C_nempty

HISTOIRE = (
    "Chapitre 1 : il etait une fois un terminal.\n"
    "Chapitre 2 : le terminal repondait aux commandes.\n"
    "Chapitre 3 : l'humain apprenait vite.\n"
    "Chapitre 4 : l'humain devint admin.\n"
    "Chapitre 5 : et tout le monde vecut heureux.\n"
)

LEVELS = [
    L(41, "Tout afficher (cat)",
      lesson="'cat' affiche TOUT le contenu d'un fichier. Simple, direct. "
             "Parfait pour les petits fichiers ; pour les gros, on verra mieux.",
      mission="Affiche le contenu de histoire.txt avec :  cat histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\bcat\b[^\n;|&]*histoire")],
      hints=["cat, espace, nom du fichier.", "Tape : cat histoire.txt"],
      solution="cat histoire.txt",
      story="Un vieux manuscrit traine dans l'arene. Lis-le."),

    L(42, "Le debut (head)",
      lesson="'head' affiche les 10 premieres lignes. 'head -n 3' n'affiche que les 3 premieres. "
             "Ideal pour jeter un oeil sans tout lire.",
      mission="Affiche les 3 premieres lignes de histoire.txt avec :  head -n 3 histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\bhead\b[^\n;|&]*histoire")],
      hints=["head -n 3 suivi du fichier.", "Tape : head -n 3 histoire.txt"],
      solution="head -n 3 histoire.txt"),

    L(43, "La fin (tail)",
      lesson="'tail' affiche les 10 dernieres lignes. Les admins vivent avec 'tail' : les erreurs recentes "
             "sont TOUJOURS a la fin des fichiers de log.",
      mission="Affiche les 2 dernieres lignes de histoire.txt avec :  tail -n 2 histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\btail\b[^\n;|&]*histoire")],
      hints=["tail -n 2 suivi du fichier.", "Tape : tail -n 2 histoire.txt"],
      solution="tail -n 2 histoire.txt",
      story="Les dernieres lignes d'un journal contiennent toujours les secrets les plus frais."),

    L(44, "Compter (wc)",
      lesson="'wc' compte : lignes (-l), mots (-w), octets (-c). 'wc -l fichier' dit combien de lignes. "
             "Indispensable pour mesurer des logs.",
      mission="Compte les lignes de histoire.txt avec :  wc -l histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\bwc\b[^\n;|&]*histoire")],
      hints=["wc -l suivi du fichier.", "Tape : wc -l histoire.txt"],
      solution="wc -l histoire.txt"),

    L(45, "Lire page par page (less)",
      lesson="'less' affiche un fichier page par page : ESPACE pour avancer, 'q' pour quitter. "
             "Obligatoire pour les fichiers de 10 000 lignes (ne JAMAIS cat un gros log !).",
      mission="Ouvre histoire.txt avec less, jette un oeil, puis quitte avec la touche q.",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"(^|[;&|]\s*)\bless\b")],
      hints=["Tape : less histoire.txt", "Puis appuie sur ESPACE, puis sur q pour quitter."],
      solution="less histoire.txt puis q"),

    L(46, "Numeroter les lignes (cat -n)",
      lesson="'cat -n' affiche le contenu avec des numeros de ligne. Pratique pour dire 'l'erreur est ligne 42' "
             "sans compter sur ses doigts.",
      mission="Affiche histoire.txt avec numeros de ligne :  cat -n histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\bcat\b[^\n;|&]*-n[^\n;|&]*histoire|\bcat\b[^\n;|&]*histoire[^\n;|&]*-n")],
      hints=["Ajoute -n a ton cat.", "Tape : cat -n histoire.txt"],
      solution="cat -n histoire.txt"),

    L(47, "Tout compter (wc)",
      lesson="Sans option, 'wc fichier' donne lignes, mots ET octets d'un coup. Trois infos pour le prix d'une.",
      mission="Affiche les stats completes de histoire.txt avec :  wc histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\bwc\b[^\n;|&]*histoire")],
      hints=["wc tout seul, suivi du fichier.", "Tape : wc histoire.txt"],
      solution="wc histoire.txt"),

    L(48, "Fusionner deux fichiers",
      lesson="'cat' accepte plusieurs fichiers : 'cat a.txt b.txt' les affiche bout a bout. "
             "Avec '>', on sauvegarde la fusion : 'cat a.txt b.txt > total.txt'.",
      mission="Fusionne partie1.txt et partie2.txt dans total.txt en une commande cat + redirection.",
      setup=[F("partie1.txt", "Il etait une fois...\n"), F("partie2.txt", "...un admin heureux.\n")],
      checks=[C_fe("total.txt"), C_fc("total.txt", text="Il etait une fois"), C_fc("total.txt", text="admin heureux")],
      hints=["cat partie1.txt partie2.txt > total.txt", "cat colle les fichiers bout a bout."],
      solution="cat partie1.txt partie2.txt > total.txt",
      story="Le manuscrit a ete dechire en deux. Recolle les morceaux."),

    L(49, "Lire a l'envers (tac)",
      lesson="'tac' (cat a l'envers !) affiche le fichier en commencant par la derniere ligne. "
             "Les blagueurs de Linux ont de l'humour, et parfois c'est utile.",
      mission="Affiche histoire.txt a l'envers avec :  tac histoire.txt",
      setup=[F("histoire.txt", HISTOIRE)],
      checks=[C_cmd(r"\btac\b[^\n;|&]*histoire")],
      hints=["C'est 'cat' ecrit a l'envers.", "Tape : tac histoire.txt"],
      solution="tac histoire.txt"),

    L(50, "BOSS du jour : le resume",
      lesson="Revision : tail lit la fin, '>' sauvegarde. Extraire l'essentiel et le garder : le quotidien de l'admin.",
      mission="Enregistre les 2 dernieres lignes de journal.txt dans resume.txt en une commande.",
      setup=[F("journal.txt", "lundi : pluie\nmardi : soleil\nmercredi : nuages\njeudi : orage\nvendredi : arc-en-ciel\n")],
      checks=[C_fe("resume.txt"), C_fc("resume.txt", text="arc-en-ciel")],
      hints=["tail -n 2 journal.txt > resume.txt", "tail extrait, > sauvegarde."],
      solution="tail -n 2 journal.txt > resume.txt",
      story="Ton chef veut 'juste la fin' du journal. Livre-lui un resume.txt nickel en une ligne.",
      xp=25, boss=True),
]
