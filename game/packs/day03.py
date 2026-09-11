"""Jour 3 (niveaux 21-30) : Se deplacer avec cd."""

from .common import L, F, D, C_cmd, C_cwd, C_fe, C_fc

SETUP_HOME = (
    D("maison/cuisine"),
    D("maison/salon"),
    F("maison/cuisine/frigo.txt", "il reste du jus\n"),
    F("maison/salon/canape.txt", "tres confortable\n"),
)

LEVELS = [
    L(21, "Entrer quelque part (cd)",
      lesson="'cd' (change directory) permet d'entrer dans un dossier. 'cd maison' puis 'pwd' pour verifier. "
             "C'est comme pousser une porte.",
      mission="Entre dans le dossier maison avec :  cd maison",
      setup=SETUP_HOME,
      checks=[C_cwd("{ws}/maison")],
      hints=["cd, espace, nom du dossier.", "Tape : cd maison"],
      solution="cd maison",
      story="Une petite maison t'attend dans l'arene. Pousse la porte et entre."),

    L(22, "Descendre plus bas",
      lesson="On peut enchainer : 'cd maison' puis 'cd cuisine'. Ou directement 'cd maison/cuisine'. "
             "Le slash '/' separe les dossiers du chemin.",
      mission="Va dans la cuisine : depuis l'arene, tape  cd maison/cuisine  (puis verifie avec pwd).",
      setup=SETUP_HOME,
      checks=[C_cwd("{ws}/maison/cuisine")],
      hints=["Les dossiers s'enchainent avec des slashs.", "Tape : cd maison/cuisine"],
      solution="cd maison/cuisine"),

    L(23, "Remonter (..)",
      lesson="'..' (point-point) signifie 'le dossier parent'. 'cd ..' remonte d'un cran. "
             "C'est l'escalier de secours du terminal.",
      mission="Va dans maison/cuisine, puis remonte d'un cran avec :  cd ..",
      setup=SETUP_HOME,
      checks=[C_cmd(r"\bcd\s+\.\.")],
      hints=["Fais d'abord : cd maison/cuisine", "Puis : cd .."],
      solution="cd maison/cuisine puis cd .."),

    L(24, "Naviguer malin (../)",
      lesson="On peut combiner : depuis 'cuisine', 'cd ../salon' remonte puis entre dans le salon. "
             "Un seul saut au lieu de deux !",
      mission="Depuis la cuisine, va directement au salon avec :  cd ../salon",
      setup=SETUP_HOME,
      checks=[C_cwd("{ws}/maison/salon")],
      hints=["Va d'abord dans maison/cuisine.", "Puis : cd ../salon"],
      solution="cd maison/cuisine puis cd ../salon"),

    L(25, "Le boomerang (cd -)",
      lesson="'cd -' (tiret) retourne dans le dossier precedent. Ideal pour jongler entre deux dossiers "
             "sans retaper les chemins.",
      mission="Va dans maison, puis reviens en arriere avec :  cd -",
      setup=SETUP_HOME,
      checks=[C_cmd(r"\bcd\s+-")],
      hints=["Va d'abord dans maison : cd maison", "Puis : cd -"],
      solution="cd maison puis cd -",
      story="Tu fais des allers-retours entre deux pieces. Les admins paresseux (les meilleurs) utilisent cd -."),

    L(26, "Rentrer chez soi (~)",
      lesson="'~' (tilde) represente ton dossier personnel (/home/ton-nom). 'cd ~' ou juste 'cd' tout seul : retour a la maison, "
             "ou que tu sois.",
      mission="Perds-toi dans maison/cuisine, puis rentre chez toi avec :  cd ~",
      setup=SETUP_HOME,
      checks=[C_cwd("~")],
      hints=["Va d'abord dans maison/cuisine.", "Puis : cd ~"],
      solution="cd maison/cuisine puis cd ~"),

    L(27, "Retour a l'arene",
      lesson="Le jeu affiche toujours le chemin de l'arene. Pour y retourner : 'cd' + le chemin affiche. "
             "Astuce : la touche TAB complete les chemins toute seule !",
      mission="Retourne dans l'arene du niveau avec cd et son chemin complet (affiche par le jeu).",
      setup=SETUP_HOME,
      checks=[C_cwd("{ws}")],
      hints=["Regarde le chemin 'cd ...' affiche dans la carte du niveau.",
             "Copie-colle le dans l'onglet JOUEUR."],
      solution="cd <chemin de l'arene>"),

    L(28, "Chemin absolu",
      lesson="Un chemin ABSOLU part de la racine '/' (ex: /home/marie). Un chemin RELATIF part d'ou tu es (ex: maison). "
             "'cd /tmp' marche depuis n'importe ou.",
      mission="Va dans /tmp avec un chemin absolu :  cd /tmp  (puis reviens dans l'arene).",
      setup=SETUP_HOME,
      checks=[C_cmd(r"\bcd\s+/tmp\b"), C_cwd("{ws}")],
      hints=["Tape : cd /tmp", "Puis retourne dans l'arene (chemin affiche par le jeu)."],
      solution="cd /tmp puis cd <arene>"),

    L(29, "Prouver ou on est",
      lesson="Combiner : se deplacer PUIS agir. 'pwd > fichier' enregistre ta position dans un fichier. "
             "Les scripts d'admin font ca en permanence.",
      mission="Depuis l'arene, enregistre ta position avec :  pwd > ou-suis-je.txt",
      setup=SETUP_HOME,
      checks=[C_fe("ou-suis-je.txt"), C_fc("ou-suis-je.txt", regex=r"niveau-0029")],
      hints=["Assure-toi d'etre dans l'arene (cd + chemin du jeu).", "Puis : pwd > ou-suis-je.txt"],
      solution="pwd > ou-suis-je.txt"),

    L(30, "BOSS du jour : raid express",
      lesson="Revision : cd, .., chemins, redirection. Un admin ne clique pas : il vole de dossier en dossier.",
      mission="En UNE ligne : va dans maison/cuisine ET enregistre ta position dans position.txt A LA RACINE de l'arene. "
              "Indice : 'cd X && pwd > ...' et '../..' remonte de deux crans.",
      setup=SETUP_HOME,
      checks=[C_fe("position.txt"), C_fc("position.txt", text="cuisine")],
      hints=["Depuis l'arene : cd maison/cuisine && pwd > ../../position.txt",
             "Le && enchaine deux commandes ; ../../ remonte deux fois."],
      solution="cd maison/cuisine && pwd > ../../position.txt",
      story="Mission commando : infiltrer la cuisine, transmettre ta position, ressortir. En une seule ligne.",
      xp=25, boss=True),
]
