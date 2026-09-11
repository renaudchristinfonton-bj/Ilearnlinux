"""Jour 4 (niveaux 31-40) : Creer fichiers et dossiers."""

from .common import L, F, D, C_cmd, C_fe, C_de, C_fc

LEVELS = [
    L(31, "Creer un fichier vide (touch)",
      lesson="'touch' cree un fichier vide (ou met a jour sa date s'il existe). "
             "C'est le carnet vierge de l'admin : on cree, on remplira plus tard.",
      mission="Dans l'arene, cree un fichier notes.txt avec :  touch notes.txt",
      checks=[C_fe("notes.txt")],
      hints=["touch, espace, nom du fichier.", "Tape : touch notes.txt"],
      solution="touch notes.txt",
      story="Un nouveau projet demarre toujours pareil : un fichier vide plein de promesses."),

    L(32, "Creer en rafale",
      lesson="'touch' accepte plusieurs noms d'un coup : 'touch a.txt b.txt c.txt'. "
             "Pourquoi taper 3 fois quand une suffit ?",
      mission="Cree en UNE commande les fichiers a.txt, b.txt et c.txt.",
      checks=[C_fe("a.txt"), C_fe("b.txt"), C_fe("c.txt")],
      hints=["Les noms se suivent, separes par des espaces.", "Tape : touch a.txt b.txt c.txt"],
      solution="touch a.txt b.txt c.txt"),

    L(33, "Creer un dossier (mkdir)",
      lesson="'mkdir' (make directory) cree un dossier. Les pros rangent leurs fichiers par dossiers : "
             "projets, sauvegardes, scripts... Le bazar, c'est fini.",
      mission="Cree un dossier travail avec :  mkdir travail",
      checks=[C_de("travail")],
      hints=["mkdir = MaKe DIRectory.", "Tape : mkdir travail"],
      solution="mkdir travail"),

    L(34, "Creer des dossiers imbriques (-p)",
      lesson="'mkdir -p a/b/c' cree toute la chaine d'un coup, meme si 'a' n'existe pas. "
             "Sans -p, mkdir rale des qu'un maillon manque.",
      mission="Cree l'arborescence projets/site/images en UNE commande avec mkdir -p.",
      checks=[C_de("projets/site/images")],
      hints=["mkdir -p cree les parents automatiquement.", "Tape : mkdir -p projets/site/images"],
      solution="mkdir -p projets/site/images",
      story="Ton futur site web a besoin de toute une arborescence. Un admin la dresse en une ligne."),

    L(35, "Creer un fichier dans un sous-dossier",
      lesson="Les commandes acceptent des chemins : 'touch projets/todo.txt' cree le fichier directement au bon endroit. "
             "Pas besoin d'entrer dans le dossier d'abord.",
      mission="Cree le dossier projets, puis le fichier projets/todo.txt (le dossier doit exister avant !).",
      checks=[C_de("projets"), C_fe("projets/todo.txt")],
      hints=["Etape 1 : mkdir projets", "Etape 2 : touch projets/todo.txt"],
      solution="mkdir projets puis touch projets/todo.txt"),

    L(36, "Copier un fichier (cp)",
      lesson="'cp source dest' copie un fichier. Exemple : 'cp rapport.txt copie.txt'. "
             "L'original reste en place : copier, ce n'est pas deplacer.",
      mission="Copie rapport.txt vers copie.txt avec :  cp rapport.txt copie.txt",
      setup=[F("rapport.txt", "Rapport annuel : tout va bien.\n")],
      checks=[C_fe("rapport.txt"), C_fe("copie.txt"), C_fc("copie.txt", text="tout va bien")],
      hints=["cp, espace, source, espace, destination.", "Tape : cp rapport.txt copie.txt"],
      solution="cp rapport.txt copie.txt"),

    L(37, "Copier vers un dossier",
      lesson="'cp fichier dossier/' copie le fichier DANS le dossier (qui doit exister). "
             "Pense a creer la destination avant.",
      mission="Cree le dossier sauvegarde, puis copies-y rapport.txt (le fichier doit s'appeler sauvegarde/rapport.txt).",
      setup=[F("rapport.txt", "donnees precieuses\n")],
      checks=[C_fe("sauvegarde/rapport.txt")],
      hints=["Etape 1 : mkdir sauvegarde", "Etape 2 : cp rapport.txt sauvegarde/"],
      solution="mkdir sauvegarde puis cp rapport.txt sauvegarde/"),

    L(38, "Le reflexe backup (.bak)",
      lesson="Avant de modifier un fichier important, les admins en gardent une copie '.bak'. "
             "Ca a sauve plus de carrieres que n'importe quel diplome.",
      mission="Fais une copie de securite de important.txt vers important.bak avec cp.",
      setup=[F("important.txt", "ne jamais perdre ceci\n")],
      checks=[C_fe("important.bak"), C_fc("important.bak", text="ne jamais perdre")],
      hints=["cp important.txt important.bak", "Le .bak, c'est la ceinture ET les bretelles."],
      solution="cp important.txt important.bak",
      story="Tu t'appretes a modifier un fichier critique. TOUT admin digne de ce nom fait un .bak d'abord."),

    L(39, "Verifier son travail (ls)",
      lesson="Cree, puis VERIFIE avec ls. Un admin ne suppose jamais : il controle. 'ls' est ton miroir : "
             "regarde-toi dedans apres chaque action.",
      mission="Cree le fichier verifie.txt, puis affiche le contenu de l'arene avec ls.",
      checks=[C_fe("verifie.txt"), C_cmd(r"(^|[;&|]\s*)\bls\b")],
      hints=["Etape 1 : touch verifie.txt", "Etape 2 : ls"],
      solution="touch verifie.txt puis ls"),

    L(40, "BOSS du jour : chantier express",
      lesson="Revision : mkdir -p, touch avec chemin, cp. Monter une structure propre en 3 commandes chrono.",
      mission="Cree defi/docs, defi/images, le fichier defi/lisez-moi.txt, puis copis-le en defi/docs/copie.txt.",
      checks=[C_de("defi/docs"), C_de("defi/images"), C_fe("defi/lisez-moi.txt"), C_fe("defi/docs/copie.txt")],
      hints=["1) mkdir -p defi/docs defi/images", "2) touch defi/lisez-moi.txt", "3) cp defi/lisez-moi.txt defi/docs/copie.txt"],
      solution="mkdir -p defi/docs defi/images && touch defi/lisez-moi.txt && cp defi/lisez-moi.txt defi/docs/copie.txt",
      story="Le chef de chantier veut une structure complete, hier. Toi, tu sais faire ca les yeux fermes.",
      xp=25, boss=True),
]
