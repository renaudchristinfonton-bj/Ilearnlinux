"""Jour 6 (niveaux 51-60) : Deplacer, renommer, supprimer."""

from .common import L, F, D, C_cmd, C_fe, C_de, C_ne, C_fc

LEVELS = [
    L(51, "Renommer (mv)",
      lesson="'mv ancien nouveau' RENOMME un fichier. En fait, renommer = deplacer au meme endroit avec un autre nom. "
             "Simple et redoutable.",
      mission="Renomme vieux.txt en nouveau.txt avec :  mv vieux.txt nouveau.txt",
      setup=[F("vieux.txt", "contenu precieux\n")],
      checks=[C_fe("nouveau.txt"), C_ne("vieux.txt"), C_fc("nouveau.txt", text="precieux")],
      hints=["mv, espace, ancien nom, espace, nouveau nom.", "Tape : mv vieux.txt nouveau.txt"],
      solution="mv vieux.txt nouveau.txt",
      story="Ce fichier porte un nom ridicule depuis 3 ans. Il est temps de le rebaptiser."),

    L(52, "Deplacer vers un dossier",
      lesson="'mv fichier dossier/' DEPLACE le fichier dans le dossier (qui doit exister). "
             "Contrairement a cp, l'original disparait : c'est un demenagement, pas une photocopie.",
      mission="Cree le dossier archives, puis deplaces-y rapport.txt.",
      setup=[F("rapport.txt", "a archiver\n")],
      checks=[C_de("archives"), C_fe("archives/rapport.txt"), C_ne("rapport.txt")],
      hints=["Etape 1 : mkdir archives", "Etape 2 : mv rapport.txt archives/"],
      solution="mkdir archives puis mv rapport.txt archives/"),

    L(53, "Deplacer en rafale",
      lesson="'mv' accepte plusieurs sources : 'mv a.txt b.txt archives/' demenage les deux d'un coup. "
             "La destination est TOUJOURS le dernier argument.",
      mission="Cree le dossier archives, puis demenages-y a.txt ET b.txt en une commande mv.",
      setup=[F("a.txt", "a\n"), F("b.txt", "b\n"), F("reste.txt", "je reste\n")],
      checks=[C_fe("archives/a.txt"), C_fe("archives/b.txt"), C_fe("reste.txt")],
      hints=["mkdir archives d'abord.", "Puis : mv a.txt b.txt archives/"],
      solution="mkdir archives puis mv a.txt b.txt archives/"),

    L(54, "Copier un dossier (-r)",
      lesson="'cp -r dossier copie' copie TOUT un dossier et son contenu. Le -r (recursif) dit a cp de descendre partout. "
             "Sans lui, cp refuse de copier les dossiers.",
      mission="Copie le dossier projet vers projet-copie avec :  cp -r projet projet-copie",
      setup=[F("projet/code.txt", "print('hello')\n"), F("projet/lisez-moi.txt", "lire d'abord\n")],
      checks=[C_fe("projet-copie/code.txt"), C_fe("projet-copie/lisez-moi.txt")],
      hints=["cp -r, espace, source, espace, destination.", "Tape : cp -r projet projet-copie"],
      solution="cp -r projet projet-copie"),

    L(55, "Supprimer un dossier vide (rmdir)",
      lesson="'rmdir' supprime un dossier... VIDE uniquement. C'est la suppression polie et prudente. "
             "S'il reste un fichier dedans, rmdir refuse.",
      mission="Supprime le dossier vide poubelle avec :  rmdir poubelle",
      setup=[D("poubelle"), F("garde.txt", "garde-moi\n")],
      checks=[C_ne("poubelle"), C_fe("garde.txt")],
      hints=["rmdir suivi du nom du dossier vide.", "Tape : rmdir poubelle"],
      solution="rmdir poubelle"),

    L(56, "Supprimer un fichier (rm)",
      lesson="'rm' supprime un fichier. DEFINITIVEMENT. Pas de corbeille, pas de 'annuler'. "
             "Les grands pouvoirs impliquent de grandes responsabilites.",
      mission="Supprime brouillon.txt avec rm (et garde important.txt !).",
      setup=[F("brouillon.txt", "brouillon\n"), F("important.txt", "important\n")],
      checks=[C_ne("brouillon.txt"), C_fe("important.txt")],
      hints=["rm suivi du fichier a supprimer.", "Tape : rm brouillon.txt"],
      solution="rm brouillon.txt",
      story="Un brouillon inutile encombre l'arene. Envoie-le dans le neant. Avec precaution."),

    L(57, "Supprimer avec le joker (*)",
      lesson="'rm *.tmp' supprime TOUS les .tmp d'un coup. Ultra-pratique, ultra-dangereux : verifie TOUJOURS "
             "avec 'ls *.tmp' AVANT de tirer.",
      mission="Liste d'abord les .tmp avec ls, puis supprime-les tous avec rm (garde garde.txt).",
      setup=[F("x.tmp", "x\n"), F("y.tmp", "y\n"), F("z.tmp", "z\n"), F("garde.txt", "garde\n")],
      checks=[C_cmd(r"\bls\b[^\n;|&]*\*\.tmp"), C_ne("x.tmp"), C_ne("y.tmp"), C_ne("z.tmp"), C_fe("garde.txt")],
      hints=["Etape 1 : ls *.tmp (verifier)", "Etape 2 : rm *.tmp (supprimer)"],
      solution="ls *.tmp puis rm *.tmp"),

    L(58, "Ranger par type",
      lesson="Combo gagnant : mkdir + mv avec joker. 'mv *.jpg images/' range toutes les images d'un coup. "
             "C'est comme ca qu'on nettoie 10 000 fichiers en 5 secondes.",
      mission="Cree le dossier images, puis demenages-y toutes les .jpg (a.jpg, b.jpg) en une commande.",
      setup=[F("a.jpg", "img\n"), F("b.jpg", "img\n"), F("notes.txt", "notes\n")],
      checks=[C_fe("images/a.jpg"), C_fe("images/b.jpg"), C_fe("notes.txt")],
      hints=["mkdir images d'abord.", "Puis : mv *.jpg images/"],
      solution="mkdir images puis mv *.jpg images/"),

    L(59, "Corbeille maison",
      lesson="Astuce de pro prudent : au lieu de 'rm', deplace vers un dossier 'Corbeille'. "
             "On peut se tromper... une fois. La corbeille pardonne, rm jamais.",
      mission="Cree un dossier Corbeille et deplaces-y supprime-moi.txt (sans utiliser rm !).",
      setup=[F("supprime-moi.txt", "oups\n")],
      checks=[C_de("Corbeille"), C_fe("Corbeille/supprime-moi.txt"), C_ne("supprime-moi.txt")],
      hints=["mkdir Corbeille", "Puis : mv supprime-moi.txt Corbeille/"],
      solution="mkdir Corbeille puis mv supprime-moi.txt Corbeille/"),

    L(60, "BOSS du jour : grand menage",
      lesson="Revision : mkdir, mv avec joker, rm avec joker. Ranger le salon ET sortir la poubelle.",
      mission="Dans bordel/ : deplace les .txt vers range/ (a creer) et supprime tous les .tmp. "
              "A la fin, bordel/ doit etre vide.",
      setup=[D("bordel"), F("bordel/a.txt", "a\n"), F("bordel/b.txt", "b\n"),
             F("bordel/x.tmp", "x\n"), F("bordel/y.tmp", "y\n")],
      checks=[C_fe("range/a.txt"), C_fe("range/b.txt"), C_ne("bordel/x.tmp"), C_ne("bordel/y.tmp"),
              C_ne("bordel/a.txt"), C_ne("bordel/b.txt")],
      hints=["1) mkdir range", "2) mv bordel/*.txt range/", "3) rm bordel/*.tmp"],
      solution="mkdir range && mv bordel/*.txt range/ && rm bordel/*.tmp",
      story="Le dossier bordel/ porte bien son nom. Range les .txt, brule les .tmp. Satisfaction garantie.",
      xp=25, boss=True),
]
