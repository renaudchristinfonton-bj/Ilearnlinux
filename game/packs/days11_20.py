"""Jours 11-20 (niveaux 101-200) : permissions & droits, ecrits a la main.

Histoire suivie : ton stage au datacenter "Pingouin & Cie".
Chaque jour melange les 10 defis du bloc avec de nouveaux scenarios :
chmod +x, modes numeriques, symboliques, recursif, scripts, lecture ls -l,
dossiers 700, secrets 600, liens symboliques (+ BOSS chaque jour).
"""

from .common import L, F, D, C_cmd, C_fe, C_de, C_fc, C_nempty, C_perm, C_exe, C_sym

LEVELS = [
    # ================= JOUR 11 : arrivee au datacenter =================
    L(101, "Le portail du datacenter",
      story="Premier jour de stage chez Pingouin & Cie. Devant toi : un portail immense... "
            "qui ne s'ouvre qu'en lancant le script portail.sh. Sauf qu'il refuse de se lancer !",
      lesson="Un script ne se lance que s'il porte le droit 'x' (execute). Sans lui, Linux repond "
             "'Permission non accordee'. 'chmod +x' : c'est le badge qui ouvre les portes.",
      mission="Rends portail.sh executable avec chmod +x.",
      setup=[F("portail.sh", "#!/bin/bash\necho bienvenue-au-datacenter\n")],
      checks=[C_exe("portail.sh")],
      hints=["chmod +x portail.sh", "Puis tu pourras le lancer avec ./portail.sh (des demain !)."],
      solution="chmod +x portail.sh"),

    L(102, "Ton badge d'acces",
      story="La cheffe te tend ton badge... avec des droits en vrac. Ici, les badges sont regles en 644 : "
            "toi tu peux tout faire, les autres peuvent juste lire.",
      lesson="644 = rw-r--r-- : le proprietaire lit+ecrit, le groupe et les autres lisent seulement. "
             "C'est LE reglage standard des fichiers normaux.",
      mission="Regle badge.txt en 644 avec chmod.",
      setup=[F("badge.txt", "stagiaire autorise\n", mode="600")],
      checks=[C_perm("badge.txt", "644")],
      hints=["chmod 644 badge.txt", "Verifie avec ls -l : tu dois voir -rw-r--r--."],
      solution="chmod 644 badge.txt"),

    L(103, "La lampe du garde",
      story="Le garde te prete sa lampe-torche electronique (lampe.sh). Probleme : elle ne s'allume pas. "
            "'Ajoute-toi le droit d'execution, stagiaire, et ne touche pas aux autres droits !'",
      lesson="En symbolique, 'u' = user (proprietaire), '+' = ajouter, 'x' = execution. "
             "'chmod u+x' ajoute juste ce qu'il faut, sans toucher au reste.",
      mission="Ajoute l'execution au proprietaire de lampe.sh : chmod u+x lampe.sh (644 -> 755).",
      setup=[F("lampe.sh", "#!/bin/bash\necho faisceau\n", mode="644")],
      checks=[C_perm("lampe.sh", "755")],
      hints=["chmod u+x lampe.sh", "u+x = le proprietaire gagne le droit de lancer."],
      solution="chmod u+x lampe.sh"),

    L(104, "La serrure electronique",
      story="La serrure du hall est trop permissive : n'importe qui peut la modifier ! La cheffe exige : "
            "retire l'ecriture aux autres (777 -> 775).",
      lesson="'o' = others (les autres), '-' = retirer, 'w' = write (ecriture). "
             "'chmod o-w' : les autres gardent lecture+execution, mais ne modifient plus.",
      mission="Applique o-w a serrure.txt (droits actuels : 777). Resultat attendu : 775.",
      setup=[F("serrure.txt", "clac\n", mode="777")],
      checks=[C_perm("serrure.txt", "775")],
      hints=["chmod o-w serrure.txt", "Verifie avec ls -l : -rwxrwxr-x."],
      solution="chmod o-w serrure.txt"),

    L(105, "Le grand hall",
      story="Coupure de courant cette nuit : TOUS les droits du hall/ sont en vrac. La cheffe : "
            "'Remets tout en 755, le dossier et son contenu. En UNE commande, on n'a pas la journee.'",
      lesson="'chmod -R' = recursif : le dossier ET tout ce qu'il contient, quel que soit la profondeur. "
             "755 = rwxr-xr-x : le reglage standard des dossiers partages.",
      mission="Applique 755 a hall/ et tout son contenu : chmod -R 755 hall",
      setup=[D("hall"), D("hall/mezzanine"), F("hall/accueil.txt", "x\n"), F("hall/mezzanine/plan.txt", "x\n")],
      checks=[C_perm("hall", "755"), C_perm("hall/mezzanine/plan.txt", "755")],
      hints=["chmod -R 755 hall", "-R descend dans tous les sous-dossiers."],
      solution="chmod -R 755 hall"),

    L(106, "Le reveil du stagiaire",
      story="Tu as failli rater ton premier jour... Heureusement, le script reveil.sh affiche 'debout' "
            "quand on le lance. Rends-le executable, lance-le, et prouve que tu es debout !",
      lesson="Le rituel complet : 1) chmod +x, 2) ./script.sh. Le './' dit 'ici, dans ce dossier' : "
             "par securite, Linux n'execute rien du dossier courant sans chemin explicite.",
      mission="Rends reveil.sh executable puis lance-le vers matin.txt : ./reveil.sh > matin.txt",
      setup=[F("reveil.sh", "#!/bin/bash\necho debout\n")],
      checks=[C_exe("reveil.sh"), C_fc("matin.txt", text="debout")],
      hints=["1) chmod +x reveil.sh", "2) ./reveil.sh > matin.txt"],
      solution="chmod +x reveil.sh && ./reveil.sh > matin.txt"),

    L(107, "Le registre d'accueil",
      story="Le registre demande : 'quels sont les droits EXACTS de la pancarte ?' Les stagiaires precedents "
            "repondaient au pif. Toi, tu vas prouver avec un vrai 'ls -l'.",
      lesson="'ls -l fichier' affiche LA ligne des droits : type + rwx + liens + proprietaire + taille + date + nom. "
             "La rediriger dans un fichier = une preuve horodatable.",
      mission="Enregistre les details de pancarte.txt dans droits.txt : ls -l pancarte.txt > droits.txt",
      setup=[F("pancarte.txt", "bienvenue\n")],
      checks=[C_fe("droits.txt"), C_fc("droits.txt", text="pancarte.txt")],
      hints=["ls -l pancarte.txt > droits.txt", "La ligne detaillee contient le nom du fichier."],
      solution="ls -l pancarte.txt > droits.txt"),

    L(108, "Ton bureau perso",
      story="La cheffe te montre un coin : 'C'est ton bureau. Mets-le en 700 : TOI SEUL y entres. "
            "Meme moi je n'irai pas... enfin, officiellement.'",
      lesson="'700' = rwx------ : le proprietaire fait tout, les autres ne voient meme pas le contenu. "
             "Le mode des dossiers prives (~/.ssh est en 700 !).",
      mission="Cree le dossier bureau et mets-le en 700.",
      checks=[C_de("bureau"), C_perm("bureau", "700")],
      hints=["1) mkdir bureau", "2) chmod 700 bureau"],
      solution="mkdir bureau && chmod 700 bureau"),

    L(109, "Le code d'alarme",
      story="Chut... La cheffe te glisse le code d'alarme sur un papier. 'Recopie-le dans code.txt, "
            "et mets-le en 600. Si Kevin le lit, c'est la catastrophe.'",
      lesson="'600' = rw------- : lecture+ecriture pour toi seul, rien pour les autres. "
             "Le mode des secrets : cles, mots de passe, codes d'alarme.",
      mission="Cree code.txt contenant le code 'p1ng0u1n' et mets-le en 600.",
      checks=[C_fe("code.txt"), C_perm("code.txt", "600"), C_fc("code.txt", text="p1ng0u1n")],
      hints=["1) echo p1ng0u1n > code.txt", "2) chmod 600 code.txt"],
      solution="echo p1ng0u1n > code.txt && chmod 600 code.txt"),

    L(110, "BOSS : le plan d'evacuation",
      story="Exercice incendie surprise ! Le plan est au fond du disque... Il faut un RACCOURCI 'entree' "
            "vers plan.txt, VISIBLE des l'entree. La vie des pingouins est en jeu (enfin, presque).",
      lesson="'ln -s cible lien' cree un lien symbolique : un raccourci. 'ls -l' le montre avec une fleche : "
             "entree -> plan.txt. Les raccourcis sauvent des vies (et du temps).",
      mission="Cree un lien 'entree' vers plan.txt : ln -s plan.txt entree",
      setup=[F("plan.txt", "sortie au fond a gauche\n")],
      checks=[C_sym("entree", "plan.txt")],
      hints=["ln -s plan.txt entree", "Ordre : ln -s CIBLE LIEN."],
      solution="ln -s plan.txt entree",
      xp=25, boss=True),

    # ================= JOUR 12 : la salle des machines =================
    L(111, "Les ventilateurs",
      story="La salle des machines ronronne. Le script ventilateur.sh regle la clim... mais il a perdu son droit x "
            "pendant la nuit. Les serveurs commencent a avoir chaud !",
      lesson="Un droit x qui disparait = un outil qui ne demarre plus. 'chmod +x' est aussi un geste de DEPANNAGE, "
             "pas seulement d'installation.",
      mission="Rends ventilateur.sh executable avec chmod +x.",
      setup=[F("ventilateur.sh", "#!/bin/bash\necho fffffff\n")],
      checks=[C_exe("ventilateur.sh")],
      hints=["chmod +x ventilateur.sh", "Vite, les serveurs transpirent !"],
      solution="chmod +x ventilateur.sh"),

    L(112, "Le voyant rouge",
      story="Le voyant est passe au rouge : le fichier voyant.txt est lisible par tout le monde, "
            "y compris les visiteurs. La consigne : 600, toi seul.",
      lesson="600 = rw------- : ton jardin secret. Quand un fichier contient des infos sensibles, "
             "600 d'abord, questions ensuite.",
      mission="Regle voyant.txt en 600 avec chmod.",
      setup=[F("voyant.txt", "surchauffe rangee 3\n", mode="644")],
      checks=[C_perm("voyant.txt", "600")],
      hints=["chmod 600 voyant.txt", "Verifie avec ls -l : -rw-------."],
      solution="chmod 600 voyant.txt"),

    L(113, "Le moteur auxiliaire",
      story="Le moteur auxiliaire (moteur.sh) doit pouvoir etre lance par toi, sans changer les droits des autres. "
            "Chirurgie de precision demandee.",
      lesson="'u+x' ajoute l'execution AU SEUL proprietaire. Le reste (groupe, autres) ne bouge pas d'un bit. "
             "De 644, on passe a 755.",
      mission="Ajoute l'execution au proprietaire de moteur.sh : chmod u+x moteur.sh (644 -> 755).",
      setup=[F("moteur.sh", "#!/bin/bash\necho vrom\n", mode="644")],
      checks=[C_perm("moteur.sh", "755")],
      hints=["chmod u+x moteur.sh", "Seul le 'u' change : rw- devient rwx."],
      solution="chmod u+x moteur.sh"),

    L(114, "La vanne de secours",
      story="Alerte : le groupe 'visiteurs' peut encore ECRIRE sur la vanne de secours ! "
            "Retire l'ecriture au groupe : 777 -> 757.",
      lesson="'g' = group (le groupe), '-w' = retirer l'ecriture. Apres 'chmod g-w', le groupe peut lire et lancer, "
             "mais plus modifier. Ouf.",
      mission="Applique g-w a vanne.txt (droits actuels : 777). Resultat attendu : 757.",
      setup=[F("vanne.txt", "ne-pas-toucher\n", mode="777")],
      checks=[C_perm("vanne.txt", "757")],
      hints=["chmod g-w vanne.txt", "g-w = le groupe perd le crayon, garde les yeux."],
      solution="chmod g-w vanne.txt"),

    L(115, "Toute la salle",
      story="Le technicien d'hier a tout regle n'importe comment dans salle-machines/. La cheffe soupire : "
            "'Remets tout en 755, proprement, d'un coup.'",
      lesson="'-R' = recursif : un seul ordre, et tout l'arbre obeit. C'est l'arme absolue apres un bazar generalise... "
             "a manier avec respect (jamais sur / !).",
      mission="Applique 755 a salle-machines/ et tout son contenu : chmod -R 755 salle-machines",
      setup=[D("salle-machines"), D("salle-machines/rangee3"), F("salle-machines/plan.txt", "x\n"),
             F("salle-machines/rangee3/serveur.txt", "x\n")],
      checks=[C_perm("salle-machines", "755"), C_perm("salle-machines/rangee3/serveur.txt", "755")],
      hints=["chmod -R 755 salle-machines", "Un ordre, tout l'arbre obeit."],
      solution="chmod -R 755 salle-machines"),

    L(116, "Demarrage des machines",
      story="6h du matin : il faut demarrer la rangee 3. Le script demarrage.sh affiche 'vroum' quand tout va bien. "
            "Lance-le et garde la preuve dans rapport.txt !",
      lesson="'./script.sh > preuve.txt' : lancer ET garder la trace. Un demarrage sans preuve ecrite, "
             "c'est comme s'il n'avait jamais eu lieu (dixit l'auditeur).",
      mission="Rends demarrage.sh executable puis lance-le vers rapport.txt : ./demarrage.sh > rapport.txt",
      setup=[F("demarrage.sh", "#!/bin/bash\necho vroum\n")],
      checks=[C_exe("demarrage.sh"), C_fc("rapport.txt", text="vroum")],
      hints=["1) chmod +x demarrage.sh", "2) ./demarrage.sh > rapport.txt"],
      solution="chmod +x demarrage.sh && ./demarrage.sh > rapport.txt"),

    L(117, "L'etiquette du serveur",
      story="Chaque serveur porte une etiquette avec ses droits exacts. Recopie la fiche de etiquette.txt "
            "dans fiche.txt avec un vrai 'ls -l'.",
      lesson="Dans 'ls -l', chaque colonne a un sens : droits, liens, proprietaire, groupe, taille, date, nom. "
             "Savoir la lire = savoir qui peut quoi.",
      mission="Enregistre les details de etiquette.txt dans fiche.txt : ls -l etiquette.txt > fiche.txt",
      setup=[F("etiquette.txt", "serveur-3\n")],
      checks=[C_fe("fiche.txt"), C_fc("fiche.txt", text="etiquette.txt")],
      hints=["ls -l etiquette.txt > fiche.txt", "Lis la ligne obtenue : -rw-r--r--, proprietaire, taille..."],
      solution="ls -l etiquette.txt > fiche.txt"),

    L(118, "Le local technique",
      story="Le local technique abrite les outils dangereux. Seuls toi (et la cheffe, chut) pouvez y entrer : 700.",
      lesson="Sur un DOSSIER, 'x' = le droit d'Y ENTRER, 'r' = le droit d'en lister le contenu. "
             "En 700, les autres ne peuvent ni entrer ni regarder. Parfait pour les outils dangereux.",
      mission="Cree le dossier local-technique et mets-le en 700.",
      checks=[C_de("local-technique"), C_perm("local-technique", "700")],
      hints=["1) mkdir local-technique", "2) chmod 700 local-technique"],
      solution="mkdir local-technique && chmod 700 local-technique"),

    L(119, "La consigne secrete",
      story="La consigne de nuit contient les codes des alarmes. Recopie 'ronde-a-minuit' dans consigne.txt, "
            "et verrouille en 600 avant que Kevin passe par la.",
      lesson="Ecrire un secret = 2 gestes : 1) echo ... > fichier, 2) chmod 600. Toujours dans cet ordre : "
             "on n'ecrit pas un secret pour le laisser ouvert, meme 10 secondes.",
      mission="Cree consigne.txt contenant 'ronde-a-minuit' et mets-le en 600.",
      checks=[C_fe("consigne.txt"), C_perm("consigne.txt", "600"), C_fc("consigne.txt", text="ronde-a-minuit")],
      hints=["1) echo ronde-a-minuit > consigne.txt", "2) chmod 600 consigne.txt"],
      solution="echo ronde-a-minuit > consigne.txt && chmod 600 consigne.txt"),

    L(120, "BOSS : l'acces rapide au schema",
      story="Le schema electrique (schema.txt) est range au fin fond de l'atelier. Le depanneur de garde veut "
            "un acces direct 'acces-rapide' depuis l'entree. En pleine nuit, chaque seconde compte !",
      lesson="Un lien symbolique, c'est une porte magique : 'acces-rapide' OUVRE schema.txt sans le deplacer. "
             "Si la cible bouge, le lien est casse : c'est le seul piege.",
      mission="Cree un lien 'acces-rapide' vers schema.txt : ln -s schema.txt acces-rapide",
      setup=[F("schema.txt", "fil rouge sur le bouton rouge\n")],
      checks=[C_sym("acces-rapide", "schema.txt")],
      hints=["ln -s schema.txt acces-rapide", "Verifie avec ls -l : tu dois voir la fleche ->."],
      solution="ln -s schema.txt acces-rapide",
      xp=25, boss=True),

    # ================= JOUR 13 : panne de nuit =================
    L(121, "Le generateur de secours",
      story="23h47 : PANNE DE COURANT ! Le generateur se pilote avec generateur.sh... qui n'a plus son droit x. "
            "Le datacenter est dans le noir. COURS !",
      lesson="En pleine urgence, 'Permission non accordee' n'est pas une reponse acceptable. "
             "'chmod +x' : le premier geste du depanneur nocturne.",
      mission="Rends generateur.sh executable avec chmod +x.",
      setup=[F("generateur.sh", "#!/bin/bash\necho courant-retabli\n")],
      checks=[C_exe("generateur.sh")],
      hints=["chmod +x generateur.sh", "Vite ! Les onduleurs tiennent 10 minutes..."],
      solution="chmod +x generateur.sh"),

    L(122, "Le cahier de nuit",
      story="Tu consignes la panne dans nuit.txt. Les visiteurs de jour ne doivent pas le modifier, "
            "mais peuvent le lire : 644.",
      lesson="644, le reglage 'affiche publique' : toi tu ecris, tout le monde lit. Ideal pour les rapports, "
            "les cahiers, les pancartes.",
      mission="Regle nuit.txt en 644 avec chmod.",
      setup=[F("nuit.txt", "panne 23h47, tout repare\n", mode="600")],
      checks=[C_perm("nuit.txt", "644")],
      hints=["chmod 644 nuit.txt", "rw-r--r-- : ecriture pour toi, lecture pour tous."],
      solution="chmod 644 nuit.txt"),

    L(123, "La torche de secours",
      story="Dans le noir, ta torche electronique (torche.sh) refuse de s'allumer : elle est en 644. "
            "Donne-toi le droit de la lancer, SANS toucher aux autres droits.",
      lesson="'chmod u+x' : la retouche chirurgicale. Seul bit qui change : le x du proprietaire. "
             "644 devient 755, le reste est intact.",
      mission="Ajoute l'execution au proprietaire de torche.sh : chmod u+x torche.sh (644 -> 755).",
      setup=[F("torche.sh", "#!/bin/bash\necho flash\n", mode="644")],
      checks=[C_perm("torche.sh", "755")],
      hints=["chmod u+x torche.sh", "Dans le noir, on vise juste : u+x, rien d'autre."],
      solution="chmod u+x torche.sh"),

    L(124, "Le fusible",
      story="Le fusible general (fusible.txt) est en 755 : n'importe qui peut le LANCER. En pleine nuit, "
            "retire l'execution aux autres : 755 -> 754.",
      lesson="'o-x' : les autres perdent le droit d'execution. Ils peuvent encore lire le mode d'emploi, "
             "mais plus declencher le fusible. Prudence nocturne.",
      mission="Applique o-x a fusible.txt (droits actuels : 755). Resultat attendu : 754.",
      setup=[F("fusible.txt", "200 amperes\n", mode="755")],
      checks=[C_perm("fusible.txt", "754")],
      hints=["chmod o-x fusible.txt", "Les autres gardent 'r', perdent 'x'."],
      solution="chmod o-x fusible.txt"),

    L(125, "Tout le sous-sol",
      story="La panne a mis les droits du sous-sol/ sens dessus dessous. Remets tout en 755 d'une seule commande, "
            "a la lampe torche.",
      lesson="Quand tout un arbre est en vrac, on ne repare pas branche par branche : 'chmod -R' traite "
             "le dossier et TOUTE sa descendance.",
      mission="Applique 755 a sous-sol/ et tout son contenu : chmod -R 755 sous-sol",
      setup=[D("sous-sol"), D("sous-sol/caveau"), F("sous-sol/compteur.txt", "x\n"),
             F("sous-sol/caveau/soupape.txt", "x\n")],
      checks=[C_perm("sous-sol", "755"), C_perm("sous-sol/caveau/soupape.txt", "755")],
      hints=["chmod -R 755 sous-sol", "Meme dans le noir, -R voit tous les fichiers."],
      solution="chmod -R 755 sous-sol"),

    L(126, "L'alerte est donnee",
      story="Le courant revient ! Lance alerte.sh (il crie 'courage') et garde son message dans message.txt : "
            "la preuve que le generateur a pris le relais.",
      lesson="Lancer + capturer : './alerte.sh > message.txt'. Le fichier garde le cri de victoire, "
            "meme quand le terminal est ferme depuis longtemps.",
      mission="Rends alerte.sh executable puis lance-le vers message.txt : ./alerte.sh > message.txt",
      setup=[F("alerte.sh", "#!/bin/bash\necho courage\n")],
      checks=[C_exe("alerte.sh"), C_fc("message.txt", text="courage")],
      hints=["1) chmod +x alerte.sh", "2) ./alerte.sh > message.txt"],
      solution="chmod +x alerte.sh && ./alerte.sh > message.txt"),

    L(127, "Le releve de l'affiche",
      story="L'affiche de securite (affiche.txt) : l'inspecteur voudra la preuve de ses droits exacts. "
            "Fais un releve 'ls -l' dans releve.txt.",
      lesson="Un releve 'ls -l' dans un fichier, c'est une photo des droits a l'instant T. "
             "En cas d'incident, on compare les photos avant/apres.",
      mission="Enregistre les details de affiche.txt dans releve.txt : ls -l affiche.txt > releve.txt",
      setup=[F("affiche.txt", "en cas de panne, garder son calme\n")],
      checks=[C_fe("releve.txt"), C_fc("releve.txt", text="affiche.txt")],
      hints=["ls -l affiche.txt > releve.txt", "Une photo des droits, datee et signee."],
      solution="ls -l affiche.txt > releve.txt"),

    L(128, "L'abri de nuit",
      story="En attendant la fin de l'alerte, tu te replies dans l'abri. Verrouille-le en 700 : "
            "personne n'entre pendant la ronde.",
      lesson="700 sur un dossier = forteresse personnelle. Meme lister le contenu est impossible pour les autres. "
             "Ton abri, tes regles.",
      mission="Cree le dossier abri et mets-le en 700.",
      checks=[C_de("abri"), C_perm("abri", "700")],
      hints=["1) mkdir abri", "2) chmod 700 abri"],
      solution="mkdir abri && chmod 700 abri"),

    L(129, "Le mot de passe de nuit",
      story="Le mot de passe de nuit ('hibou-007') doit dormir dans mot-de-passe.txt, en 600. "
            "Si quelqu'un d'autre le lit, l'alarme... enfin, imagine.",
      lesson="600 = le coffre-fort des fichiers. Lecture+ecriture pour toi, NEANT pour les autres. "
             "Les mots de passe n'ont rien a faire en 644.",
      mission="Cree mot-de-passe.txt contenant 'hibou-007' et mets-le en 600.",
      checks=[C_fe("mot-de-passe.txt"), C_perm("mot-de-passe.txt", "600"), C_fc("mot-de-passe.txt", text="hibou-007")],
      hints=["1) echo hibou-007 > mot-de-passe.txt", "2) chmod 600 mot-de-passe.txt"],
      solution="echo hibou-007 > mot-de-passe.txt && chmod 600 mot-de-passe.txt"),

    L(130, "BOSS : l'issue de secours",
      story="Exercice d'evacuation nocturne ! Le chemin (sortie.txt) est complique... Pose un raccourci 'issue' "
            "lumineux vers sortie.txt. Les pingouins comptent sur toi.",
      lesson="BOSS de la nuit : creer un lien symbolique sous pression. 'ln -s CIBLE LIEN' : cite-le dans ton sommeil, "
             "c'est le reflexe qui sauve.",
      mission="Cree un lien 'issue' vers sortie.txt : ln -s sortie.txt issue",
      setup=[F("sortie.txt", "porte de derriere, escalier B\n")],
      checks=[C_sym("issue", "sortie.txt")],
      hints=["ln -s sortie.txt issue", "Cible d'abord, nom du lien ensuite."],
      solution="ln -s sortie.txt issue",
      xp=25, boss=True),

    # ================= JOUR 14 : le serveur grincheux =================
    L(131, "Grognon ne demarre pas",
      story="Le vieux serveur 'Grognon' se pilote avec grognon.sh. Ce matin, il grogne : 'Permission non accordee'. "
            "Traduction : il manque le x. Comme d'habitude avec lui.",
      lesson="Les vieux serveurs perdent leurs droits comme on perd ses cles. 'chmod +x' : le premier reflexe "
             "devant un 'Permission denied' sur un script a toi.",
      mission="Rends grognon.sh executable avec chmod +x.",
      setup=[F("grognon.sh", "#!/bin/bash\necho grognon-pret\n")],
      checks=[C_exe("grognon.sh")],
      hints=["chmod +x grognon.sh", "Grognon grogne, mais il obeit au +x."],
      solution="chmod +x grognon.sh"),

    L(132, "L'humeur de Grognon",
      story="Tu notes l'humeur du serveur dans humeur.txt. Le groupe des techniciens doit pouvoir la LIRE "
            "sans l'effacer : 640.",
      lesson="640 = rw-r----- : toi tout, le groupe lecture, les autres rien. Le reglage 'equipe de confiance' : "
             "on partage en lecture, pas en ecriture.",
      mission="Regle humeur.txt en 640 avec chmod.",
      setup=[F("humeur.txt", "grognon mais fonctionnel\n", mode="600")],
      checks=[C_perm("humeur.txt", "640")],
      hints=["chmod 640 humeur.txt", "Le groupe gagne le 'r', rien de plus."],
      solution="chmod 640 humeur.txt"),

    L(133, "Le gros bouton rouge",
      story="Grognon a un bouton (bouton.sh) : seul TOI peux l'activer. Ajoute-toi le x sans toucher au reste "
            "(644 -> 755). Doucement... c'est un vieux monsieur.",
      lesson="'u+x' : +x POUR TOI SEUL. Le groupe et les autres gardent leurs droits actuels. "
             "La precision du chirurgien, pas la masse du bucheron.",
      mission="Ajoute l'execution au proprietaire de bouton.sh : chmod u+x bouton.sh (644 -> 755).",
      setup=[F("bouton.sh", "#!/bin/bash\necho bip\n", mode="644")],
      checks=[C_perm("bouton.sh", "755")],
      hints=["chmod u+x bouton.sh", "u = toi, +x = lancer. Rien d'autre ne bouge."],
      solution="chmod u+x bouton.sh"),

    L(134, "Le carnet de Grognon",
      story="Le carnet du vieux serveur (vieux-serveur.txt) est en 600 : meme le groupe ne peut pas le lire. "
            "La cheffe ordonne : le groupe doit pouvoir le LIRE : 600 -> 640.",
      lesson="'g+r' : le groupe gagne la lecture. De 600 (moi seul) a 640 (moi + groupe en lecture). "
             "Partager sans donner les cles.",
      mission="Applique g+r a vieux-serveur.txt (droits actuels : 600). Resultat attendu : 640.",
      setup=[F("vieux-serveur.txt", "ne pas debrancher, merci\n", mode="600")],
      checks=[C_perm("vieux-serveur.txt", "640")],
      hints=["chmod g+r vieux-serveur.txt", "g+r = le groupe peut lire."],
      solution="chmod g+r vieux-serveur.txt"),

    L(135, "Le hangar a Grognon",
      story="Grognon vit dans un hangar/ plein de vieux dossiers, aux droits fantaisistes. Uniformise TOUT en 755, "
            "d'une seule commande. Il rale, mais il aime l'ordre.",
      lesson="Uniformiser un arbre entier : 'chmod -R 755 dossier'. Une commande, des dizaines de fichiers repares. "
             "Grognon rale toujours, mais ses droits sont carres.",
      mission="Applique 755 a hangar/ et tout son contenu : chmod -R 755 hangar",
      setup=[D("hangar"), D("hangar/etagere"), F("hangar/mode-emploi.txt", "x\n"),
             F("hangar/etagere/poussiere.txt", "x\n")],
      checks=[C_perm("hangar", "755"), C_perm("hangar/etagere/poussiere.txt", "755")],
      hints=["chmod -R 755 hangar", "R comme 'Remets-moi-tout-ca-droit'."],
      solution="chmod -R 755 hangar"),

    L(136, "Le cafe de Grognon",
      story="Astuce d'ancien : Grognon travaille mieux apres un cafe. Le script cafe.sh affiche 'grognon-ok'. "
            "Lance-le, garde la preuve dans pause.txt, et admire : il ronronne !",
      lesson="Certains scripts affichent un statut ('ok', 'pret'...). Le capturer avec '>' dans un fichier, "
             "c'est garder la preuve que tout roule.",
      mission="Rends cafe.sh executable puis lance-le vers pause.txt : ./cafe.sh > pause.txt",
      setup=[F("cafe.sh", "#!/bin/bash\necho grognon-ok\n")],
      checks=[C_exe("cafe.sh"), C_fc("pause.txt", text="grognon-ok")],
      hints=["1) chmod +x cafe.sh", "2) ./cafe.sh > pause.txt"],
      solution="chmod +x cafe.sh && ./cafe.sh > pause.txt"),

    L(137, "Le post-it de Grognon",
      story="Grognon communique par post-it. Recopie les droits EXACTS de postit.txt dans memo.txt : "
            "demain, on comparera pour voir s'il a tripote ses propres droits (il en est capable).",
      lesson="Comparer les droits avant/apres : la base de la surveillance. On photographie avec 'ls -l > fichier', "
             "et on compare plus tard avec un nouveau cliche.",
      mission="Enregistre les details de postit.txt dans memo.txt : ls -l postit.txt > memo.txt",
      setup=[F("postit.txt", "j'ai faim. - Grognon\n")],
      checks=[C_fe("memo.txt"), C_fc("memo.txt", text="postit.txt")],
      hints=["ls -l postit.txt > memo.txt", "Un cliche des droits, pour comparer demain."],
      solution="ls -l postit.txt > memo.txt"),

    L(138, "Le coin tranquille",
      story="Grognon fait la sieste... dans coin-tranquille. Ce dossier doit etre en 700 : personne ne derange "
            "un vieux serveur qui dort. PERSONNE.",
      lesson="700 = 'prive, circulez'. Ni lecture, ni entree pour les autres. Meme 'ls' leur repondra "
             "'Permission non accordee'. Silence, ca dort.",
      mission="Cree le dossier coin-tranquille et mets-le en 700.",
      checks=[C_de("coin-tranquille"), C_perm("coin-tranquille", "700")],
      hints=["1) mkdir coin-tranquille", "2) chmod 700 coin-tranquille"],
      solution="mkdir coin-tranquille && chmod 700 coin-tranquille"),

    L(139, "La recette du cafe",
      story="La recette du cafe qui amadoue Grognon ('arabica-double') dort dans recette-cafe.txt. "
            "En 600, evidemment : c'est un secret industriel.",
      lesson="Un secret industriel en 644, c'est une porte ouverte. En 600, c'est un coffre. "
             "La difference tient en un chmod.",
      mission="Cree recette-cafe.txt contenant 'arabica-double' et mets-le en 600.",
      checks=[C_fe("recette-cafe.txt"), C_perm("recette-cafe.txt", "600"), C_fc("recette-cafe.txt", text="arabica-double")],
      hints=["1) echo arabica-double > recette-cafe.txt", "2) chmod 600 recette-cafe.txt"],
      solution="echo arabica-double > recette-cafe.txt && chmod 600 recette-cafe.txt"),

    L(140, "BOSS : le manuel de Grognon",
      story="Grognon a ENFIN accepte qu'on l'aide... a condition d'avoir son manuel (manuel.txt) accessible "
            "via un raccourci 'aide'. Un vieux serveur ne change pas ses habitudes : c'est a toi de t'adapter.",
      lesson="BOSS du jour : 'ln -s CIBLE LIEN'. Les vieux systemes sont pleins de raccourcis historiques : "
             "savoir les creer (et les lire avec ls -l), c'est parler leur langue.",
      mission="Cree un lien 'aide' vers manuel.txt : ln -s manuel.txt aide",
      setup=[F("manuel.txt", "chapitre 1 : ne pas me debrancher\n")],
      checks=[C_sym("aide", "manuel.txt")],
      hints=["ln -s manuel.txt aide", "Grognon observe... ne te trompe pas d'ordre !"],
      solution="ln -s manuel.txt aide",
      xp=25, boss=True),

    # ================= JOUR 15 : audit de securite =================
    L(141, "Le script de l'auditeur",
      story="L'auditeur debarque avec son script audit.sh... qui ne se lance pas (droit x manquant, evidemment). "
            "Il te regarde : 'Alors, stagiaire, on sait depanner ?'",
      lesson="Devant un auditeur, on ne panique pas : on diagnostique. 'Permission non accordee' sur un script = "
             "probablement le x. 'chmod +x', et l'audit peut commencer.",
      mission="Rends audit.sh executable avec chmod +x.",
      setup=[F("audit.sh", "#!/bin/bash\necho audit-demarre\n")],
      checks=[C_exe("audit.sh")],
      hints=["chmod +x audit.sh", "L'auditeur prend des notes... impressionne-le."],
      solution="chmod +x audit.sh"),

    L(142, "La grille d'audit",
      story="La grille d'audit (grille.txt) doit etre lisible par tous mais modifiable par toi seul : 644. "
            "Transparence + controle : la devise de l'auditeur.",
      lesson="644 = la vitrine : tout le monde regarde, toi seul touches. Pour les grilles, rapports publics, "
             "documentations : 644 est ton ami.",
      mission="Regle grille.txt en 644 avec chmod.",
      setup=[F("grille.txt", "point 1 : droits\npoint 2 : droits aussi\n", mode="600")],
      checks=[C_perm("grille.txt", "644")],
      hints=["chmod 644 grille.txt", "L'auditeur verifiera avec ls -l. Sois carre."],
      solution="chmod 644 grille.txt"),

    L(143, "Le tampon officiel",
      story="Pour tamponner les rapports, l'auditeur utilise tampon.sh (en 644). Il veut pouvoir le LANCER "
            "sans changer les autres droits. Chirurgie, acte II.",
      lesson="'u+x' encore et toujours : le geste de precision. 644 -> 755. Les audits adorent les gestes propres "
             "et documentes... et toi, tu progresses.",
      mission="Ajoute l'execution au proprietaire de tampon.sh : chmod u+x tampon.sh (644 -> 755).",
      setup=[F("tampon.sh", "#!/bin/bash\necho TAMPONNE\n", mode="644")],
      checks=[C_perm("tampon.sh", "755")],
      hints=["chmod u+x tampon.sh", "L'auditeur hoche la tete. Bien."],
      solution="chmod u+x tampon.sh"),

    L(144, "Le dossier d'audit partage",
      story="Le dossier d'audit (dossier-audit.txt) est en 640 : le groupe lit, les autres non. L'auditeur exige "
            "la transparence TOTALE : les autres doivent pouvoir le LIRE aussi (640 -> 644).",
      lesson="'o+r' : les autres (others) gagnent la lecture. De 640 a 644. La transparence a un prix : "
             "une lettre et un symbole.",
      mission="Applique o+r a dossier-audit.txt (droits actuels : 640). Resultat attendu : 644.",
      setup=[F("dossier-audit.txt", "tout est en regle (ou presque)\n", mode="640")],
      checks=[C_perm("dossier-audit.txt", "644")],
      hints=["chmod o+r dossier-audit.txt", "o+r = transparence pour les autres."],
      solution="chmod o+r dossier-audit.txt"),

    L(145, "Toutes les archives",
      story="'TOUTES les archives doivent etre en 755 !' tonne l'auditeur. Le dossier archives/ et son contenu, "
            "d'une seule commande. Il chronometre.",
      lesson="Sous pression, 'chmod -R' est ton meilleur ami : un ordre, tout l'arbre obeit. "
             "L'auditeur arrete son chrono : 3 secondes. Record du datacenter.",
      mission="Applique 755 a archives/ et tout son contenu : chmod -R 755 archives",
      setup=[D("archives"), D("archives/2025"), F("archives/sommaire.txt", "x\n"),
             F("archives/2025/janvier.txt", "x\n")],
      checks=[C_perm("archives", "755"), C_perm("archives/2025/janvier.txt", "755")],
      hints=["chmod -R 755 archives", "Vite ! Il chronometre..."],
      solution="chmod -R 755 archives"),

    L(146, "Le verdict de l'auditeur",
      story="L'audit touche a sa fin. Le script controle.sh affiche 'conforme' si tout va bien. Lance-le, "
            "et grave le verdict dans verdict.txt !",
      lesson="Le moment de verite : executer et archiver le resultat. './controle.sh > verdict.txt' : "
             "le verdict est grave dans le marbre (numerique).",
      mission="Rends controle.sh executable puis lance-le vers verdict.txt : ./controle.sh > verdict.txt",
      setup=[F("controle.sh", "#!/bin/bash\necho conforme\n")],
      checks=[C_exe("controle.sh"), C_fc("verdict.txt", text="conforme")],
      hints=["1) chmod +x controle.sh", "2) ./controle.sh > verdict.txt"],
      solution="chmod +x controle.sh && ./controle.sh > verdict.txt"),

    L(147, "La preuve ecrite",
      story="'Montrez-moi les droits EXACTS de l'affiche !' L'auditeur ne croit que les preuves ecrites : "
            "un 'ls -l' de affiche-audit.txt dans preuve.txt.",
      lesson="En audit, une affirmation sans preuve vaut zero. 'ls -l fichier > preuve.txt' : la preuve ecrite, "
             "datable, archivable. Les auditeurs adorent.",
      mission="Enregistre les details de affiche-audit.txt dans preuve.txt : ls -l affiche-audit.txt > preuve.txt",
      setup=[F("affiche-audit.txt", "l'audit, c'est la sante\n")],
      checks=[C_fe("preuve.txt"), C_fc("preuve.txt", text="affiche-audit.txt")],
      hints=["ls -l affiche-audit.txt > preuve.txt", "Ecrit, signe, range. Comme un pro."],
      solution="ls -l affiche-audit.txt > preuve.txt"),

    L(148, "La salle d'audit",
      story="Les deliberations ont lieu dans salle-audit, en 700 : secret des deliberations oblige. "
            "Meme Kevin n'y entre pas (surtout Kevin).",
      lesson="700 = confidentialite absolue du dossier. Pour les deliberations, les dossiers perso, "
             "les secrets d'equipe : 700, point final.",
      mission="Cree le dossier salle-audit et mets-le en 700.",
      checks=[C_de("salle-audit"), C_perm("salle-audit", "700")],
      hints=["1) mkdir salle-audit", "2) chmod 700 salle-audit"],
      solution="mkdir salle-audit && chmod 700 salle-audit"),

    L(149, "Les conclusions secretes",
      story="Les conclusions (' RAS, stagiaire genial') vont dans conclusions.txt, en 600 : "
            "meme l'auditeur ne les lira qu'avec TA permission.",
      lesson="600 = lecture et ecriture pour toi seul. Les conclusions sensibles ne trainent jamais en 644. "
             "Jamais.",
      mission="Cree conclusions.txt contenant 'RAS-stagiaire-genial' et mets-le en 600.",
      checks=[C_fe("conclusions.txt"), C_perm("conclusions.txt", "600"), C_fc("conclusions.txt", text="RAS-stagiaire-genial")],
      hints=["1) echo RAS-stagiaire-genial > conclusions.txt", "2) chmod 600 conclusions.txt"],
      solution="echo RAS-stagiaire-genial > conclusions.txt && chmod 600 conclusions.txt"),

    L(150, "BOSS : la norme de reference",
      story="Pour clore l'audit, l'auditeur veut un raccourci 'reference' vers norme.txt, accessible immediatement. "
            "'Un bon admin met les normes a portee de main, stagiaire.'",
      lesson="BOSS de l'audit : 'ln -s CIBLE LIEN', sans faute, devant temoin. Les normes a portee de main, "
             "l'auditeur conquis, le stage valide (presque).",
      mission="Cree un lien 'reference' vers norme.txt : ln -s norme.txt reference",
      setup=[F("norme.txt", "norme ISO-PINGOUIN-9001\n")],
      checks=[C_sym("reference", "norme.txt")],
      hints=["ln -s norme.txt reference", "L'auditeur observe... et sourit deja."],
      solution="ln -s norme.txt reference",
      xp=25, boss=True),

    # ================= JOUR 16 : le coffre-fort =================
    L(151, "Le coffre ne s'ouvre pas",
      story="Aujourd'hui : la chambre forte ! Son ouverture se pilote avec coffre.sh... qui refuse de se lancer. "
            "Un coffre qui ne s'ouvre pas, c'est embetant. Un script sans x, c'est classique.",
      lesson="Meme les coffres-forts obeissent aux permissions UNIX. Pas de x, pas d'ouverture. "
             "'chmod +x' : la premiere cle du trousseau.",
      mission="Rends coffre.sh executable avec chmod +x.",
      setup=[F("coffre.sh", "#!/bin/bash\necho clac-clac\n")],
      checks=[C_exe("coffre.sh")],
      hints=["chmod +x coffre.sh", "La premiere cle du trousseau..."],
      solution="chmod +x coffre.sh"),

    L(152, "Le blindage",
      story="La fiche du blindage (blindage.txt) : toi tout, le groupe et les autres en lecture+execution... "
            "non attends : la consigne dit 755 exactement.",
      lesson="755 = rwxr-xr-x : toi tout, les autres lecture+execution. LE reglage des scripts partages et "
             "des dossiers publics.",
      mission="Regle blindage.txt en 755 avec chmod.",
      setup=[F("blindage.txt", "triple epaisseur\n", mode="600")],
      checks=[C_perm("blindage.txt", "755")],
      hints=["chmod 755 blindage.txt", "rwxr-xr-x : le classique des classiques."],
      solution="chmod 755 blindage.txt"),

    L(153, "La cle electronique",
      story="Ta cle electronique (cle.sh) est en 644 : elle ne PILOTE rien. Ajoute-toi le droit de l'utiliser "
            "(u+x), sans toucher aux autres droits.",
      lesson="Une cle qui ne tourne pas = un x qui manque. 'chmod u+x' : ta cle tourne, "
             "les serrures des autres ne changent pas.",
      mission="Ajoute l'execution au proprietaire de cle.sh : chmod u+x cle.sh (644 -> 755).",
      setup=[F("cle.sh", "#!/bin/bash\necho clic\n", mode="644")],
      checks=[C_perm("cle.sh", "755")],
      hints=["chmod u+x cle.sh", "Clic ! La cle tourne."],
      solution="chmod u+x cle.sh"),

    L(154, "Desarmer les executions",
      story="Urgence : serrure-forte.txt est en 777, n'importe qui peut tout faire ! La cheffe : "
            "'Retire l'execution a TOUT LE MONDE : 777 -> 666. TOUT DE SUITE.'",
      lesson="'a' = all (tous) : u+g+o d'un coup. 'chmod a-x' retire l'execution a tout le monde. "
             "De 777 a 666 : lecture+ecriture pour tous, execution pour personne.",
      mission="Applique a-x a serrure-forte.txt (droits actuels : 777). Resultat attendu : 666.",
      setup=[F("serrure-forte.txt", "ultra-sensible\n", mode="777")],
      checks=[C_perm("serrure-forte.txt", "666")],
      hints=["chmod a-x serrure-forte.txt", "a-x = desarmer tout le monde d'un coup."],
      solution="chmod a-x serrure-forte.txt"),

    L(155, "Toute la chambre forte",
      story="La chambre-forte/ contient des casiers aux droits heteroclites. Uniformise TOUT en 755, "
            "d'une commande. Le coffre aime l'ordre.",
      lesson="'chmod -R 755' : l'uniforme du coffre. Tous les casiers, tous les tiroirs, un seul ordre. "
             "Les coffres bien ranges se cambriolent moins (proverbe admin).",
      mission="Applique 755 a chambre-forte/ et tout son contenu : chmod -R 755 chambre-forte",
      setup=[D("chambre-forte"), D("chambre-forte/casiers"), F("chambre-forte/registre.txt", "x\n"),
             F("chambre-forte/casiers/casier1.txt", "x\n")],
      checks=[C_perm("chambre-forte", "755"), C_perm("chambre-forte/casiers/casier1.txt", "755")],
      hints=["chmod -R 755 chambre-forte", "Un ordre, tous les casiers obeissent."],
      solution="chmod -R 755 chambre-forte"),

    L(156, "Ouverture du coffre",
      story="Le grand moment : lance ouverture.sh (il affiche 'verrouille'... euh, 'deverrouille' ? "
            "non : 'verrouille' — c'est le statut AVANT. Bref, lance et capture dans acces.txt !)",
      lesson="Les scripts de statut affichent un mot-cle ('verrouille', 'ok'...). Le capturer dans un fichier "
             "avec '>', c'est figer l'etat a l'instant T.",
      mission="Rends ouverture.sh executable puis lance-le vers acces.txt : ./ouverture.sh > acces.txt",
      setup=[F("ouverture.sh", "#!/bin/bash\necho verrouille\n")],
      checks=[C_exe("ouverture.sh"), C_fc("acces.txt", text="verrouille")],
      hints=["1) chmod +x ouverture.sh", "2) ./ouverture.sh > acces.txt"],
      solution="chmod +x ouverture.sh && ./ouverture.sh > acces.txt"),

    L(157, "La plaque du coffre",
      story="Chaque coffre porte une plaque avec ses droits graves. Grave (faccon de parler) les droits de plaque.txt "
            "dans inventaire.txt avec 'ls -l'.",
      lesson="'ls -l' lit la plaque d'identite d'un fichier : droits, proprietaire, taille, date. "
             "La recopier dans un inventaire = tracer le patrimoine.",
      mission="Enregistre les details de plaque.txt dans inventaire.txt : ls -l plaque.txt > inventaire.txt",
      setup=[F("plaque.txt", "coffre n°7\n")],
      checks=[C_fe("inventaire.txt"), C_fc("inventaire.txt", text="plaque.txt")],
      hints=["ls -l plaque.txt > inventaire.txt", "La plaque, gravee dans l'inventaire."],
      solution="ls -l plaque.txt > inventaire.txt"),

    L(158, "Le sas",
      story="Avant le coffre : le sas. Un dossier en 700 ou tu es SEUL pendant l'ouverture. "
            "Protocole : personne d'autre ne regarde.",
      lesson="700 = isolement total. Pour les sas, les zones de quarantaine, les dossiers ultra-prives : "
             "on entre seul, on ressort seul.",
      mission="Cree le dossier sas et mets-le en 700.",
      checks=[C_de("sas"), C_perm("sas", "700")],
      hints=["1) mkdir sas", "2) chmod 700 sas"],
      solution="mkdir sas && chmod 700 sas"),

    L(159, "La combinaison",
      story="La combinaison du coffre ('gauche-12-droite-7') dort dans combinaison.txt. En 600 : "
            "si Kevin la lit, on change TOUTES les serrures.",
      lesson="Une combinaison en 644 = ecrite sur un post-it sur l'ecran. En 600 = dans ta tete (et ton fichier). "
             "Le choix est vite fait.",
      mission="Cree combinaison.txt contenant 'gauche-12-droite-7' et mets-le en 600.",
      checks=[C_fe("combinaison.txt"), C_perm("combinaison.txt", "600"), C_fc("combinaison.txt", text="gauche-12-droite-7")],
      hints=["1) echo gauche-12-droite-7 > combinaison.txt", "2) chmod 600 combinaison.txt"],
      solution="echo gauche-12-droite-7 > combinaison.txt && chmod 600 combinaison.txt"),

    L(160, "BOSS : le raccourci vers le tresor",
      story="Au fond du coffre : le tresor (tresor.txt, des bons d'achat cantine). La cheffe veut un raccourci "
            "'raccourci'... euh, un lien 'vitrine' vers le tresor. VITE, avant la fermeture !",
      lesson="BOSS du coffre : 'ln -s CIBLE LIEN'. Meme les tresors meritent un raccourci bien place. "
             "La vitrine brille, les bons d'achat sont a portee de main.",
      mission="Cree un lien 'vitrine' vers tresor.txt : ln -s tresor.txt vitrine",
      setup=[F("tresor.txt", "bons d'achat cantine : 3 kebabs\n")],
      checks=[C_sym("vitrine", "tresor.txt")],
      hints=["ln -s tresor.txt vitrine", "Le tresor, a portee de main. Miam."],
      solution="ln -s tresor.txt vitrine",
      xp=25, boss=True),

    # ================= JOUR 17 : la nuit des sauvegardes =================
    L(161, "Le script de backup",
      story="Cette nuit : SAUVEGARDES GENERALES. Le script backup.sh doit tourner a minuit... mais il n'a pas le x. "
            "A minuit moins une, c'est ballot.",
      lesson="Un backup qui ne se lance pas = pas de backup. Verifier le x des scripts critiques AVANT l'heure H : "
             "le rituel de tout admin serieux.",
      mission="Rends backup.sh executable avec chmod +x.",
      setup=[F("backup.sh", "#!/bin/bash\necho backup-lance\n")],
      checks=[C_exe("backup.sh")],
      hints=["chmod +x backup.sh", "Minuit approche..."],
      solution="chmod +x backup.sh"),

    L(162, "Le planning secret",
      story="Le planning des backups (planning.txt) : toi tout, le groupe RIEN, les autres RIEN... "
            "non : la consigne dit 700. Radical.",
      lesson="700 sur un FICHIER = lecture+ecriture+execution pour toi seul. On l'utilise pour les scripts prives "
             "qu'on est seul a lancer.",
      mission="Regle planning.txt en 700 avec chmod.",
      setup=[F("planning.txt", "minuit : tout sauvegarder\n", mode="600")],
      checks=[C_perm("planning.txt", "700")],
      hints=["chmod 700 planning.txt", "rwx------ : toi seul, tout seul."],
      solution="chmod 700 planning.txt"),

    L(163, "Le disque de secours",
      story="Le disque de secours se monte avec disque.sh (en 644). Ajoute-toi le droit de le lancer, "
            "sans toucher aux autres. Les backups n'attendent pas.",
      lesson="'u+x', le geste qui devient un reflexe : 644 -> 755. Tu le tapes maintenant sans reflechir ? "
             "C'est bon signe : tes doigts apprennent.",
      mission="Ajoute l'execution au proprietaire de disque.sh : chmod u+x disque.sh (644 -> 755).",
      setup=[F("disque.sh", "#!/bin/bash\necho disque-monte\n", mode="644")],
      checks=[C_perm("disque.sh", "755")],
      hints=["chmod u+x disque.sh", "Tes doigts connaissent deja la chanson."],
      solution="chmod u+x disque.sh"),

    L(164, "La bande magnetique",
      story="La vieille bande (bande.txt) est en 666 : tout le monde lit et ecrit, personne ne lance. "
            "Toi, tu dois pouvoir LANCER sa procedure : 666 -> 766.",
      lesson="'u+x' sur 666 : le proprietaire passe de rw- a rwx, les autres restent en rw-. "
             "Resultat : 766. Toi tu pilotes, les autres consultent.",
      mission="Applique u+x a bande.txt (droits actuels : 666). Resultat attendu : 766.",
      setup=[F("bande.txt", "sauvegarde 1998, ne pas rire\n", mode="666")],
      checks=[C_perm("bande.txt", "766")],
      hints=["chmod u+x bande.txt", "666 + u+x = 766. Toi tu pilotes."],
      solution="chmod u+x bande.txt"),

    L(165, "Toute la salle des backups",
      story="La salle-backups/ contient des dossiers de toutes les annees, aux droits anarchiques. "
            "Uniformise TOUT en 755 : les backups aiment l'ordre.",
      lesson="'chmod -R 755' : le grand menage annuel. Un ordre, des centaines de fichiers alignes. "
             "Les backups bien ranges se restaurent mieux.",
      mission="Applique 755 a salle-backups/ et tout son contenu : chmod -R 755 salle-backups",
      setup=[D("salle-backups"), D("salle-backups/2026"), F("salle-backups/lisez-moi.txt", "x\n"),
             F("salle-backups/2026/janvier.txt", "x\n")],
      checks=[C_perm("salle-backups", "755"), C_perm("salle-backups/2026/janvier.txt", "755")],
      hints=["chmod -R 755 salle-backups", "Le grand menage annuel, en une ligne."],
      solution="chmod -R 755 salle-backups"),

    L(166, "Le bilan de nuit",
      story="5h du matin : les backups sont finis. Le script copie.sh affiche 'sauve'. Lance-le et garde "
            "le bilan dans bilan.txt : demain, la cheffe veut la preuve.",
      lesson="Un backup sans bilan ecrit = un backup qui n'a peut-etre pas eu lieu. './copie.sh > bilan.txt' : "
             "la preuve du travail de nuit.",
      mission="Rends copie.sh executable puis lance-le vers bilan.txt : ./copie.sh > bilan.txt",
      setup=[F("copie.sh", "#!/bin/bash\necho sauve\n")],
      checks=[C_exe("copie.sh"), C_fc("bilan.txt", text="sauve")],
      hints=["1) chmod +x copie.sh", "2) ./copie.sh > bilan.txt"],
      solution="chmod +x copie.sh && ./copie.sh > bilan.txt"),

    L(167, "L'etiquette du backup",
      story="Chaque backup porte une etiquette avec ses droits. Recopie ceux de etiquette-bak.txt dans liste.txt : "
            "le registre des sauvegardes doit etre complet.",
      lesson="'ls -l etiquette > registre' : chaque backup est trace avec ses droits. En cas de restauration, "
             "on sait EXACTEMENT ce qu'on restaure.",
      mission="Enregistre les details de etiquette-bak.txt dans liste.txt : ls -l etiquette-bak.txt > liste.txt",
      setup=[F("etiquette-bak.txt", "backup du 15, verifie\n")],
      checks=[C_fe("liste.txt"), C_fc("liste.txt", text="etiquette-bak.txt")],
      hints=["ls -l etiquette-bak.txt > liste.txt", "Trace, date, range. Le backup est carre."],
      solution="ls -l etiquette-bak.txt > liste.txt"),

    L(168, "La reserve",
      story="Les bandes les plus precieuses dorment dans la reserve, en 700. Toi seul y entres : "
            "ce sont les backups des backups.",
      lesson="700 = le saint des saints. Les copies critiques, les cles de chiffrement, les plans de secours : "
             "derriere du 700, toujours.",
      mission="Cree le dossier reserve et mets-le en 700.",
      checks=[C_de("reserve"), C_perm("reserve", "700")],
      hints=["1) mkdir reserve", "2) chmod 700 reserve"],
      solution="mkdir reserve && chmod 700 reserve"),

    L(169, "La cle de chiffrement",
      story="Les backups sont CHIFFRES. La cle ('sel-poivre-42') dort dans cle-chiffrement.txt, en 600. "
            "Sans elle, les backups sont des grimoires illisibles.",
      lesson="Une cle de chiffrement, c'est le pouvoir absolu sur les donnees. En 644, c'est une catastrophe. "
             "En 600, c'est un secret. Il n'y a pas de troisieme option.",
      mission="Cree cle-chiffrement.txt contenant 'sel-poivre-42' et mets-le en 600.",
      checks=[C_fe("cle-chiffrement.txt"), C_perm("cle-chiffrement.txt", "600"), C_fc("cle-chiffrement.txt", text="sel-poivre-42")],
      hints=["1) echo sel-poivre-42 > cle-chiffrement.txt", "2) chmod 600 cle-chiffrement.txt"],
      solution="echo sel-poivre-42 > cle-chiffrement.txt && chmod 600 cle-chiffrement.txt"),

    L(170, "BOSS : la procedure de restauration",
      story="Catastrophe simulee : TOUT est efface (c'est un exercice, respire). La procedure de restauration "
            "(restauration.txt) doit etre accessible via le lien 'procedure'. Les minutes comptent !",
      lesson="BOSS des backups : 'ln -s CIBLE LIEN' en situation de crise (simulee). En vrai incident, "
             "c'est ce reflexe qui fait gagner 10 minutes.",
      mission="Cree un lien 'procedure' vers restauration.txt : ln -s restauration.txt procedure",
      setup=[F("restauration.txt", "etape 1 : ne pas paniquer\netape 2 : restaurer\n")],
      checks=[C_sym("procedure", "restauration.txt")],
      hints=["ln -s restauration.txt procedure", "Etape 1 : ne pas paniquer. Etape 2 : ln -s."],
      solution="ln -s restauration.txt procedure",
      xp=25, boss=True),

    # ================= JOUR 18 : Kevin a tout casse =================
    L(171, "L'aspirateur de Kevin",
      story="Kevin, le nouveau stagiaire, a 'nettoye' les droits de aspirateur.sh : le x a disparu ! "
            "Remets-le. (Et plus tard, on expliquera a Kevin.)",
      lesson="Reparer les degats des autres : 50% du metier d'admin. 'chmod +x' : le pansement universel "
             "des scripts blesses par Kevin.",
      mission="Rends aspirateur.sh executable avec chmod +x.",
      setup=[F("aspirateur.sh", "#!/bin/bash\necho vroum\n")],
      checks=[C_exe("aspirateur.sh")],
      hints=["chmod +x aspirateur.sh", "Kevin s'excuse. Il apprendra. Comme toi avant."],
      solution="chmod +x aspirateur.sh"),

    L(172, "Le constat des degats",
      story="Tu consignes les degats dans degats.txt. Le groupe doit pouvoir le lire ET l'enrichir, "
            "les autres juste le lire : 664.",
      lesson="664 = rw-rw-r-- : toi et le groupe lisez+ecrivez, les autres lisent. Le reglage 'travail d'equipe' : "
             "on collabore, les visiteurs regardent.",
      mission="Regle degats.txt en 664 avec chmod.",
      setup=[F("degats.txt", "Kevin a touche aux droits\n", mode="600")],
      checks=[C_perm("degats.txt", "664")],
      hints=["chmod 664 degats.txt", "Le groupe ecrit aussi : rw-rw-r--."],
      solution="chmod 664 degats.txt"),

    L(173, "Le balai de service",
      story="Pour nettoyer le bazar de Kevin, il faut lancer balai.sh (en 644). Ajoute-toi le x, "
            "precisement, proprement. Contrairement a Kevin.",
      lesson="'u+x' : 644 -> 755. Tu fais ca les yeux fermes maintenant. Kevin, lui, en est a confondre "
             "chmod et shampooing. Patience.",
      mission="Ajoute l'execution au proprietaire de balai.sh : chmod u+x balai.sh (644 -> 755).",
      setup=[F("balai.sh", "#!/bin/bash\necho swiff\n", mode="644")],
      checks=[C_perm("balai.sh", "755")],
      hints=["chmod u+x balai.sh", "Precision de pro. Kevin prend des notes."],
      solution="chmod u+x balai.sh"),

    L(174, "Les miettes de Kevin",
      story="Kevin a mis miettes.txt en 755 : le groupe peut LANCER n'importe quoi ! Retire l'execution "
            "au groupe : 755 -> 745.",
      lesson="'g-x' : le groupe perd le x. De 755 (rwxr-xr-x) a 745 (rwxr--r-x). Le groupe lit toujours, "
            "mais ne lance plus. Merci pour eux.",
      mission="Applique g-x a miettes.txt (droits actuels : 755). Resultat attendu : 745.",
      setup=[F("miettes.txt", "miettes de Numeros\n", mode="755")],
      checks=[C_perm("miettes.txt", "745")],
      hints=["chmod g-x miettes.txt", "g-x = le groupe range le lanceur, garde les lunettes."],
      solution="chmod g-x miettes.txt"),

    L(175, "Le bureau de Kevin",
      story="Le bureau-kevin/ est... indescriptible. Des droits dans tous les sens. Uniformise TOUT en 755 "
            "d'une commande. Kevin regarde, ebloui.",
      lesson="'chmod -R 755' : le level-set du bazar. Un ordre, et le chaos de Kevin devient un jardin a la francaise. "
             "Kevin applaudit. La cheffe aussi.",
      mission="Applique 755 a bureau-kevin/ et tout son contenu : chmod -R 755 bureau-kevin",
      setup=[D("bureau-kevin"), D("bureau-kevin/tas"), F("bureau-kevin/truc.txt", "x\n"),
             F("bureau-kevin/tas/machin.txt", "x\n")],
      checks=[C_perm("bureau-kevin", "755"), C_perm("bureau-kevin/tas/machin.txt", "755")],
      hints=["chmod -R 755 bureau-kevin", "Du chaos au jardin a la francaise, en une ligne."],
      solution="chmod -R 755 bureau-kevin"),

    L(176, "Le constat de reparation",
      story="Tout est repare ! Le script reparation.sh affiche 'repare'. Lance-le et grave le constat "
            "dans constat.txt : Kevin signera en bas.",
      lesson="Apres une reparation, on prouve : './reparation.sh > constat.txt'. Le constat signe, "
             "c'est la fin officielle de l'incident 'Kevin'.",
      mission="Rends reparation.sh executable puis lance-le vers constat.txt : ./reparation.sh > constat.txt",
      setup=[F("reparation.sh", "#!/bin/bash\necho repare\n")],
      checks=[C_exe("reparation.sh"), C_fc("constat.txt", text="repare")],
      hints=["1) chmod +x reparation.sh", "2) ./reparation.sh > constat.txt"],
      solution="chmod +x reparation.sh && ./reparation.sh > constat.txt"),

    L(177, "Les excuses de Kevin",
      story="Kevin a ecrit ses excuses dans excuse.txt. Pour le dossier, archive ses droits EXACTS "
            "dans pardon.txt avec 'ls -l'. L'administration adore les dossiers complets.",
      lesson="Meme les excuses se tracent : 'ls -l excuse.txt > pardon.txt'. Un dossier complet = "
             "le contenu + les droits + la date. L'administration est heureuse.",
      mission="Enregistre les details de excuse.txt dans pardon.txt : ls -l excuse.txt > pardon.txt",
      setup=[F("excuse.txt", "desole, je ne toucherai plus aux droits - Kevin\n")],
      checks=[C_fe("pardon.txt"), C_fc("pardon.txt", text="excuse.txt")],
      hints=["ls -l excuse.txt > pardon.txt", "Pardon accorde, dossier classe."],
      solution="ls -l excuse.txt > pardon.txt"),

    L(178, "Le placard de Kevin",
      story="En punition (gentille), Kevin range ses affaires dans placard/, en 700 : "
            "personne ne touchera a ses affaires pendant qu'il revise ses chmod.",
      lesson="700 = chacun chez soi. Meme pour un placard a balais : la privacy, c'est aussi pour Kevin. "
             "Surtout pour Kevin.",
      mission="Cree le dossier placard et mets-le en 700.",
      checks=[C_de("placard"), C_perm("placard", "700")],
      hints=["1) mkdir placard", "2) chmod 700 placard"],
      solution="mkdir placard && chmod 700 placard"),

    L(179, "Les secrets de Kevin",
      story="Kevin te confie ses secrets ('kevin-aime-les-chmod') dans secrets-kevin.txt. En 600, promis-jure : "
            "un secret de stagiaire est sacre.",
      lesson="600 = secret sacre. Meme (surtout) les secrets un peu betes : si on ne protege pas les petits secrets, "
             "on ne saura pas proteger les gros.",
      mission="Cree secrets-kevin.txt contenant 'kevin-aime-les-chmod' et mets-le en 600.",
      checks=[C_fe("secrets-kevin.txt"), C_perm("secrets-kevin.txt", "600"), C_fc("secrets-kevin.txt", text="kevin-aime-les-chmod")],
      hints=["1) echo kevin-aime-les-chmod > secrets-kevin.txt", "2) chmod 600 secrets-kevin.txt"],
      solution="echo kevin-aime-les-chmod > secrets-kevin.txt && chmod 600 secrets-kevin.txt"),

    L(180, "BOSS : le mode d'emploi pour Kevin",
      story="Pour que Kevin ne casse plus rien, la cheffe veut un raccourci 'mode-emploi' vers notice.txt, "
            "BIEN VISIBLE. L'avenir des droits du datacenter en depend.",
      lesson="BOSS pedagogique : 'ln -s CIBLE LIEN'. Un bon raccourci au bon endroit evite des catastrophes. "
             "Kevin te remercie. Les droits aussi.",
      mission="Cree un lien 'mode-emploi' vers notice.txt : ln -s notice.txt mode-emploi",
      setup=[F("notice.txt", "ne jamais chmod -R 777 /, merci - la direction\n")],
      checks=[C_sym("mode-emploi", "notice.txt")],
      hints=["ln -s notice.txt mode-emploi", "Kevin lit la notice. Tout va mieux."],
      solution="ln -s notice.txt mode-emploi",
      xp=25, boss=True),

    # ================= JOUR 19 : revision avant inspection =================
    L(181, "La derniere ligne droite",
      story="J-1 avant LA GRANDE INSPECTION. On revise tout ! D'abord : revision.sh ne se lance pas. "
            "Le x, vite, on n'a plus une minute a perdre.",
      lesson="Revision express : pas de x, pas de lancement. 'chmod +x' en 2 secondes, sans reflechir. "
             "C'est ca, le niveau 'jambes qui tremblent mais doigts qui savent'.",
      mission="Rends revision.sh executable avec chmod +x.",
      setup=[F("revision.sh", "#!/bin/bash\necho on-revise\n")],
      checks=[C_exe("revision.sh")],
      hints=["chmod +x revision.sh", "J-1... respire, tape, valide."],
      solution="chmod +x revision.sh"),

    L(182, "La checklist",
      story="La checklist (checklist.txt) doit etre en lecture seule pour TOUS, toi compris : 444. "
            "Plus personne ne la modifie avant l'inspection. Fige !",
      lesson="444 = r--r--r-- : lecture pour tous, ecriture pour PERSONNE (meme toi). Le mode 'musee' : "
             "on regarde, on ne touche pas. (Tu pourras rechanger apres.)",
      mission="Regle checklist.txt en 444 avec chmod.",
      setup=[F("checklist.txt", "1. droits 2. droits 3. droits\n", mode="600")],
      checks=[C_perm("checklist.txt", "444")],
      hints=["chmod 444 checklist.txt", "444 = musee : on regarde, on ne touche pas."],
      solution="chmod 444 checklist.txt"),

    L(183, "Le surligneur",
      story="Pour reviser, tu utilises surligneur.sh (en 644). Ajoute-toi le droit de le lancer. "
            "Revision active : on fait, on ne relit pas !",
      lesson="'u+x' : 644 -> 755. Tu l'as fait 8 fois : cette fois, c'est de la revision active. "
             "Tes doigts tapent avant que ton cerveau ait fini de lire. Parfait.",
      mission="Ajoute l'execution au proprietaire de surligneur.sh : chmod u+x surligneur.sh (644 -> 755).",
      setup=[F("surligneur.sh", "#!/bin/bash\necho fluo\n", mode="644")],
      checks=[C_perm("surligneur.sh", "755")],
      hints=["chmod u+x surligneur.sh", "Revision active : les doigts avant le cerveau."],
      solution="chmod u+x surligneur.sh"),

    L(184, "Le brouillon partage",
      story="Ton brouillon (brouillon.txt) est en 700 : personne ne peut le relire. Pour la relecture croisee, "
            "les autres doivent pouvoir le lire ET le lancer : 700 -> 705.",
      lesson="'o+rx' : les autres gagnent lecture+execution d'un coup. De 700 a 705. "
             "Partager en lecture, sans donner le crayon.",
      mission="Applique o+rx a brouillon.txt (droits actuels : 700). Resultat attendu : 705.",
      setup=[F("brouillon.txt", "brouillon de genie\n", mode="700")],
      checks=[C_perm("brouillon.txt", "705")],
      hints=["chmod o+rx brouillon.txt", "o+rx = les autres lisent et lancent."],
      solution="chmod o+rx brouillon.txt"),

    L(185, "Toute la salle de revision",
      story="La salle-revision/ ressemble au bureau de Kevin (pardon Kevin). Uniformise TOUT en 755 "
            "d'une commande : on revise dans l'ordre ou on ne revise pas.",
      lesson="'chmod -R 755' : l'ordre en une ligne. Une salle bien rangee, des idees bien rangees. "
             "Demain, l'inspection. Aujourd'hui, l'ordre.",
      mission="Applique 755 a salle-revision/ et tout son contenu : chmod -R 755 salle-revision",
      setup=[D("salle-revision"), D("salle-revision/fiches"), F("salle-revision/programme.txt", "x\n"),
             F("salle-revision/fiches/chmod.txt", "x\n")],
      checks=[C_perm("salle-revision", "755"), C_perm("salle-revision/fiches/chmod.txt", "755")],
      hints=["chmod -R 755 salle-revision", "L'ordre dehors, l'ordre dedans."],
      solution="chmod -R 755 salle-revision"),

    L(186, "L'essai general",
      story="Essai general avant l'inspection ! Le script essai.sh affiche 'pret'. Lance-le, capture dans "
            "resultat.txt : si ca affiche 'pret', tu dors tranquille.",
      lesson="L'essai general : executer + archiver. './essai.sh > resultat.txt'. Si le fichier dit 'pret', "
             "c'est que TOUTE la chaine marche : droits, script, redirection.",
      mission="Rends essai.sh executable puis lance-le vers resultat.txt : ./essai.sh > resultat.txt",
      setup=[F("essai.sh", "#!/bin/bash\necho pret\n")],
      checks=[C_exe("essai.sh"), C_fc("resultat.txt", text="pret")],
      hints=["1) chmod +x essai.sh", "2) ./essai.sh > resultat.txt"],
      solution="chmod +x essai.sh && ./essai.sh > resultat.txt"),

    L(187, "Le pense-bete",
      story="Pour demain, archive les droits de pense-bete.txt dans note.txt. Pendant l'inspection, "
            "tu sortiras cette preuve au bon moment. Effet garanti.",
      lesson="'ls -l pense-bete.txt > note.txt' : la preuve dans la poche. Les inspecteurs aiment les stagiaires "
             "qui prouvent au lieu d'affirmer.",
      mission="Enregistre les details de pense-bete.txt dans note.txt : ls -l pense-bete.txt > note.txt",
      setup=[F("pense-bete.txt", "u+x, 755, -R, ln -s\n")],
      checks=[C_fe("note.txt"), C_fc("note.txt", text="pense-bete.txt")],
      hints=["ls -l pense-bete.txt > note.txt", "La preuve dans la poche. Demain, tu brilles."],
      solution="ls -l pense-bete.txt > note.txt"),

    L(188, "La bulle de concentration",
      story="Derniere revision au calme dans ta bulle, en 700. Personne ne te derange : "
            "ni Kevin, ni Grognon, ni l'angoisse.",
      lesson="700 = bulle de concentration. Ni lecture ni entree pour les autres. "
             "Parfois, le meilleur droit, c'est le silence.",
      mission="Cree le dossier bulle et mets-le en 700.",
      checks=[C_de("bulle"), C_perm("bulle", "700")],
      hints=["1) mkdir bulle", "2) chmod 700 bulle"],
      solution="mkdir bulle && chmod 700 bulle"),

    L(189, "L'antiseche (autorisee)",
      story="L'antiseche est AUTORISEE demain (si, si). Recopie 'u-g-o-a-plus-moins-rwx' dans antiseche.txt, "
            "en 600 : c'est TA fiche, pas celle de Kevin.",
      lesson="600 = ta fiche perso. Meme une antiseche autorisee merite d'etre protegee : "
             "on ne partage pas ses fiches la veille de l'examen. (Si, avec Kevin. Apres.)",
      mission="Cree antiseche.txt contenant 'u-g-o-a-plus-moins-rwx' et mets-le en 600.",
      checks=[C_fe("antiseche.txt"), C_perm("antiseche.txt", "600"), C_fc("antiseche.txt", text="u-g-o-a-plus-moins-rwx")],
      hints=["1) echo u-g-o-a-plus-moins-rwx > antiseche.txt", "2) chmod 600 antiseche.txt"],
      solution="echo u-g-o-a-plus-moins-rwx > antiseche.txt && chmod 600 antiseche.txt"),

    L(190, "BOSS : l'index du programme",
      story="Dernier exercice avant le jour J : un raccourci 'index' vers programme.txt, pour retrouver "
            "le programme en une seconde pendant l'inspection. Rapidite = points bonus.",
      lesson="BOSS de la veille : 'ln -s CIBLE LIEN', vite et sans faute. Demain, quand l'inspectrice dira "
            "'montrez-moi le programme', tu auras deja le lien sous la main.",
      mission="Cree un lien 'index' vers programme.txt : ln -s programme.txt index",
      setup=[F("programme.txt", "inspection : 9h, salle des machines\n")],
      checks=[C_sym("index", "programme.txt")],
      hints=["ln -s programme.txt index", "Vite et sans faute. Demain, tu brilles."],
      solution="ln -s programme.txt index",
      xp=25, boss=True),

    # ================= JOUR 20 : l'inspection finale =================
    L(191, "La fanfare d'accueil",
      story="Jour J ! L'inspectrice arrive. La fanfare d'accueil (fanfare.sh) doit se lancer... "
            "mais elle n'a pas le x. La honte serait totale. VITE !",
      lesson="Le jour J, pas de 'Permission non accordee'. 'chmod +x' en 2 secondes, le sourire aux levres. "
            "L'inspectrice n'a rien vu. Ouf.",
      mission="Rends fanfare.sh executable avec chmod +x.",
      setup=[F("fanfare.sh", "#!/bin/bash\necho ta-ta-taaa\n")],
      checks=[C_exe("fanfare.sh")],
      hints=["chmod +x fanfare.sh", "Ta-ta-taaa ! L'inspectrice sourit."],
      solution="chmod +x fanfare.sh"),

    L(192, "Le diplome",
      story="Ton diplome de stage (diplome.txt) : toi tout (lecture+ecriture+execution), le groupe lecture+execution, "
            "les autres execution seule : 711. Oui, c'est bizarre. Oui, c'est la consigne.",
      lesson="711 = rwx--x--x : toi tout, les autres... execution SEULE. Etrange ? C'est le mode des dossiers "
            "qu'on peut traverser sans pouvoir les lister. L'inspectrice adore pieger avec ca.",
      mission="Regle diplome.txt en 711 avec chmod.",
      setup=[F("diplome.txt", "stagiaire meritoire\n", mode="600")],
      checks=[C_perm("diplome.txt", "711")],
      hints=["chmod 711 diplome.txt", "711 = rwx--x--x. Execute, mais ne regarde pas !"],
      solution="chmod 711 diplome.txt"),

    L(193, "La medaille",
      story="L'inspectrice te remet la medaille (medaille.sh, en 644)... qu'il faut pouvoir LANCER pour la faire "
            "briller. u+x, une derniere fois, avec elegance.",
      lesson="Dernier 'u+x' du bloc : 644 -> 755. Tu l'as fait 10 fois. Cette fois, c'est devant l'inspectrice. "
             "Elegance, precision, medaille.",
      mission="Ajoute l'execution au proprietaire de medaille.sh : chmod u+x medaille.sh (644 -> 755).",
      setup=[F("medaille.sh", "#!/bin/bash\necho medaille-dor\n", mode="644")],
      checks=[C_perm("medaille.sh", "755")],
      hints=["chmod u+x medaille.sh", "Elegance, precision... medaille !"],
      solution="chmod u+x medaille.sh"),

    L(194, "Le sceau officiel",
      story="Le sceau officiel (sceau.txt) est en 644. L'inspectrice : 'Ajoutez-vous l'execution. "
            "Montrez-moi la forme symbolique, pas la numerique !'",
      lesson="Dernier acte symbolique : 'u+x' sur 644 donne 755. L'inspectrice voulait la forme symbolique : "
             "elle prouve que tu COMPRENDS, pas que tu recites.",
      mission="Applique u+x a sceau.txt (droits actuels : 644). Resultat attendu : 755.",
      setup=[F("sceau.txt", "certifie conforme\n", mode="644")],
      checks=[C_perm("sceau.txt", "755")],
      hints=["chmod u+x sceau.txt", "La forme symbolique : la preuve que tu comprends."],
      solution="chmod u+x sceau.txt"),

    L(195, "Toute la grande salle",
      story="'Montrez-moi que TOUTE la grande-salle/ est en 755 !' Uniformise le dossier et son contenu "
            "d'une commande, devant l'inspectrice. Sans trembler.",
      lesson="'chmod -R 755', devant temoin, sans trembler. Une commande, tout l'arbre. "
             "L'inspectrice coche la case. Une de plus.",
      mission="Applique 755 a grande-salle/ et tout son contenu : chmod -R 755 grande-salle",
      setup=[D("grande-salle"), D("grande-salle/estrade"), F("grande-salle/pupitre.txt", "x\n"),
             F("grande-salle/estrade/micro.txt", "x\n")],
      checks=[C_perm("grande-salle", "755"), C_perm("grande-salle/estrade/micro.txt", "755")],
      hints=["chmod -R 755 grande-salle", "Sans trembler. Elle coche la case."],
      solution="chmod -R 755 grande-salle"),

    L(196, "La proclamation",
      story="Le moment supreme : le script couronnement.sh affiche 'victoire'. Lance-le, capture dans "
            "proclamation.txt. Toute la salle retient son souffle...",
      lesson="Le bouquet final : './couronnement.sh > proclamation.txt'. Executer, capturer, triompher. "
             "Apres 196 niveaux, ce geste est grave dans tes doigts.",
      mission="Rends couronnement.sh executable puis lance-le vers proclamation.txt : ./couronnement.sh > proclamation.txt",
      setup=[F("couronnement.sh", "#!/bin/bash\necho victoire\n")],
      checks=[C_exe("couronnement.sh"), C_fc("proclamation.txt", text="victoire")],
      hints=["1) chmod +x couronnement.sh", "2) ./couronnement.sh > proclamation.txt"],
      solution="chmod +x couronnement.sh && ./couronnement.sh > proclamation.txt"),

    L(197, "Le palmares officiel",
      story="'Archivez-moi les droits de l'affiche finale !' L'inspectrice veut affiche-finale.txt photographie "
            "dans palmares.txt. La derniere preuve du bloc.",
      lesson="Derniere photo du bloc : 'ls -l affiche-finale.txt > palmares.txt'. Apres 20 jours, "
             "tu sais que les droits se prouvent, pas s'affirment.",
      mission="Enregistre les details de affiche-finale.txt dans palmares.txt : ls -l affiche-finale.txt > palmares.txt",
      setup=[F("affiche-finale.txt", "inspection reussie\n")],
      checks=[C_fe("palmares.txt"), C_fc("palmares.txt", text="affiche-finale.txt")],
      hints=["ls -l affiche-finale.txt > palmares.txt", "La derniere preuve du bloc. Souris !"],
      solution="ls -l affiche-finale.txt > palmares.txt"),

    L(198, "Le bureau d'admin",
      story="L'inspectrice te montre une porte : 'C'est votre futur bureau d'admin. Mettez-le en 700 : "
            "un admin protege son espace.' Ton coeur fait boum.",
      lesson="700 = le bureau de l'admin. Espace protege, acces reserve. Dans 80 jours, ce sera officiel. "
             "En attendant, c'est ton objectif grave dans un chmod.",
      mission="Cree le dossier bureau-admin et mets-le en 700.",
      checks=[C_de("bureau-admin"), C_perm("bureau-admin", "700")],
      hints=["1) mkdir bureau-admin", "2) chmod 700 bureau-admin"],
      solution="mkdir bureau-admin && chmod 700 bureau-admin"),

    L(199, "Le mot supreme",
      story="L'inspectrice te confie le mot supreme ('je-suis-admin') dans mot-supreme.txt. En 600, "
            "c'est sacre. Tu n'es plus un stagiaire comme les autres.",
      lesson="600 = les secrets des grands. Le mot supreme dort en 600, a l'abri des regards. "
             "Tu sais maintenant proteger ce qui compte.",
      mission="Cree mot-supreme.txt contenant 'je-suis-admin' et mets-le en 600.",
      checks=[C_fe("mot-supreme.txt"), C_perm("mot-supreme.txt", "600"), C_fc("mot-supreme.txt", text="je-suis-admin")],
      hints=["1) echo je-suis-admin > mot-supreme.txt", "2) chmod 600 mot-supreme.txt"],
      solution="echo je-suis-admin > mot-supreme.txt && chmod 600 mot-supreme.txt"),

    L(200, "BOSS FINAL : le serment de l'admin",
      story="L'inspectrice se leve : 'Pour clore ce bloc, posez le serment (charte.txt) a portee de main, "
            "via le lien serment. Puis lisez-le a voix haute.' Le bloc Permissions touche a sa fin...",
      lesson="BOSS final du bloc : 'ln -s charte.txt serment'. 100 niveaux de permissions derriere toi : "
             "chmod n'a plus aucun secret. Le serment t'attend : lis-le, et deviens Gardien des Droits.",
      mission="Cree un lien 'serment' vers charte.txt : ln -s charte.txt serment",
      setup=[F("charte.txt", "je protegerai les droits des fichiers, avec sagesse et chmod\n")],
      checks=[C_sym("serment", "charte.txt")],
      hints=["ln -s charte.txt serment", "Puis lis le serment avec cat. A voix haute !"],
      solution="ln -s charte.txt serment",
      xp=25, boss=True),
]
