"""Jours 21-30 (niveaux 201-300) : utilisateurs & groupes, ecrits a la main.

Histoire suivie : le grand recensement de Pingouin & Cie.
Nouveaux collegues, annuaire mysterieux, clubs secrets, espions de nuit...
et la rencontre avec le grand patron : root.
Chaque jour melange les 10 defis du bloc : whoami, id, groups, who, id -u,
/etc/passwd, recensement, ls -l systeme, sudo, id root (+ BOSS chaque jour).
"""

from .common import L, F, C_cmd, C_fe, C_fc, C_nempty

LEVELS = [
    # ================= JOUR 21 : les nouveaux collegues =================
    L(201, "Bienvenue aux nouveaux",
      story="Trois nouveaux collegues arrivent aujourd'hui. Pour preparer leurs badges, la cheffe commence par TOI : "
            "'C'est quoi deja ton nom d'utilisateur ? Prouve-le moi dans nom-badge.txt.'",
      lesson="Ton nom d'utilisateur, c'est ton prenom officiel pour Linux. 'whoami' le dit, '>' le grave. "
            "Les badges, les rapports, les audits : tout commence par un nom.",
      mission="Enregistre ton nom d'utilisateur dans nom-badge.txt : whoami > nom-badge.txt",
      checks=[C_fe("nom-badge.txt"), C_nempty("nom-badge.txt")],
      hints=["whoami > nom-badge.txt", "whoami = who am i = qui suis-je ?"],
      solution="whoami > nom-badge.txt"),

    L(202, "La fiche du personnel",
      story="Les RH veulent ta fiche COMPLETE : uid, gid, groupes. 'Un simple nom ne suffit pas, stagiaire !' "
            "Heureusement, la commande 'id' raconte toute ta vie.",
      lesson="'id' affiche ton uid (ton numero), ton gid (ton groupe principal) et TOUS tes groupes. "
            "C'est la carte d'identite complete, en une ligne.",
      mission="Enregistre ton identite complete dans fiche-perso.txt : id > fiche-perso.txt",
      checks=[C_fe("fiche-perso.txt"), C_fc("fiche-perso.txt", text="uid=")],
      hints=["id > fiche-perso.txt", "La sortie contient toujours 'uid=' suivi de ton numero."],
      solution="id > fiche-perso.txt"),

    L(203, "Les equipes",
      story="Chez Pingouin & Cie, on travaille en equipes : reseau, serveurs, securite... "
            "De quelles equipes fais-tu partie ? Liste tes groupes dans equipes.txt !",
      lesson="'groups' liste tes groupes, un par un. Chaque groupe = une equipe = des droits. "
            "Etre dans 'sudo' ne donne pas les memes pouvoirs qu'etre dans 'visiteurs' !",
      mission="Liste tes groupes dans equipes.txt : groups > equipes.txt",
      checks=[C_fe("equipes.txt"), C_nempty("equipes.txt")],
      hints=["groups > equipes.txt", "Chaque mot liste est une de tes equipes."],
      solution="groups > equipes.txt"),

    L(204, "L'appel du matin",
      story="9h : l'appel ! Qui est connecte ce matin a la machine ? Fais l'appel avec 'who' "
            "et consigne les presents dans presence.txt.",
      lesson="'who' montre les utilisateurs CONNECTES : qui, depuis ou, depuis quand. "
            "Sur un serveur partage, c'est le premier regard du matin.",
      mission="Liste les utilisateurs connectes dans presence.txt : who > presence.txt",
      checks=[C_fe("presence.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > presence.txt", "who = qui est la, en ce moment ?"],
      solution="who > presence.txt"),

    L(205, "Ton matricule",
      story="Ton badge affiche un NUMERO, pas un nom : ton uid ! Les machines adorent les numeros. "
            "Decouvre ton matricule et grave-le dans matricule.txt.",
      lesson="'id -u' donne juste ton numero (uid). Les scripts adorent : comparer des nombres, "
            "c'est plus simple que comparer des noms. (uid 0 = root, le patron.)",
      mission="Enregistre ton uid dans matricule.txt : id -u > matricule.txt",
      checks=[C_fe("matricule.txt"), C_fc("matricule.txt", regex=r"\d+")],
      hints=["id -u > matricule.txt", "Un numero, rien qu'un numero."],
      solution="id -u > matricule.txt"),

    L(206, "Ta fiche dans l'annuaire",
      story="Le grand annuaire /etc/passwd contient une ligne par personne... dont la tienne ! "
            "Extrais TA ligne dans ma-fiche.txt. Tu verras : nom, numero, dossier, shell.",
      lesson="'/etc/passwd' : une ligne = une personne (nom:motdepasse:uid:gid:info:dossier:shell). "
              "'grep \"^$(whoami):\"' peche exactement TA ligne. Lisible par tous : c'est l'annuaire public.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > ma-fiche.txt",
      checks=[C_fe("ma-fiche.txt"), C_fc("ma-fiche.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > ma-fiche.txt", "$(whoami) devient ton nom avant l'execution."],
      solution="grep \"^$(whoami):\" /etc/passwd > ma-fiche.txt"),

    L(207, "Combien sommes-nous ?",
      story="La cheffe : 'Combien de comptes existent sur cette machine ? Y compris les comptes systeme !' "
            "Compte les lignes de l'annuaire dans nb-comptes.txt.",
      lesson="Une ligne de /etc/passwd = un compte. 'wc -l < fichier' compte les lignes. "
             "Tu seras surpris : il y a bien plus de comptes systeme que d'humains !",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > nb-comptes.txt",
      checks=[C_fe("nb-comptes.txt"), C_fc("nb-comptes.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > nb-comptes.txt", "< nourrit wc avec le fichier, > sauve le chiffre."],
      solution="wc -l < /etc/passwd > nb-comptes.txt"),

    L(208, "Qui garde l'annuaire ?",
      story="L'annuaire est precieux : qui le possede ? Quels sont ses droits ? "
            "Affiche les details de /etc/passwd. Si ce n'est pas root, on a un probleme...",
      lesson="'ls -l /etc/passwd' : proprietaire, groupe, droits. Les fichiers systeme appartiennent a root "
             "et sont en lecture seule pour les autres. Verifier ca = verifier la sante du systeme.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Le proprietaire doit etre root."],
      solution="ls -l /etc/passwd"),

    L(209, "Le passe-partout",
      story="On te parle d'un passe-partout magique : 'sudo'. Il permet d'agir EN ROOT pour une commande. "
            "Avant de l'utiliser (bien plus tard !), verifie simplement OU il habite.",
      lesson="'command -v sudo' dit ou vit la commande sudo (ex: /usr/bin/sudo). 'command -v' = le GPS des commandes. "
             "Dans ce jeu, on n'utilise JAMAIS sudo : tout se passe dans l'arene.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "command -v = 'ou habites-tu ?' pour une commande."],
      solution="command -v sudo"),

    L(210, "BOSS : le grand patron",
      story="Dernier jour de la semaine d'accueil : tu rencontres (de loin !) le grand patron : root. "
            "uid 0, gid 0, tous les pouvoirs. Enregistre sa fiche dans le-patron.txt. Impressionnant, non ?",
      lesson="BOSS du jour : 'id root'. uid=0 = le grade supreme. root lit, ecrit, supprime PARTOUT. "
             "C'est pour ca qu'on ne se connecte JAMAIS en root au quotidien : trop dangereux.",
      mission="Enregistre l'identite de root dans le-patron.txt : id root > le-patron.txt",
      checks=[C_fe("le-patron.txt"), C_fc("le-patron.txt", text="uid=0")],
      hints=["id root > le-patron.txt", "uid=0 : le zero des tout-puissants."],
      solution="id root > le-patron.txt",
      xp=25, boss=True),

    # ================= JOUR 22 : l'annuaire mysterieux =================
    L(211, "Le miroir magique",
      story="Au fond du couloir, un vieux terminal affiche TOUJOURS ton nom, quel que soit l'utilisateur. "
            "Son secret ? Il lance 'whoami'. Reproduis la magie dans reflet.txt.",
      lesson="'whoami' ne ment jamais : il demande au systeme 'qui execute cette commande ?'. "
             "C'est le miroir magique : il reflete TOUJOURS le vrai visage.",
      mission="Enregistre ton nom d'utilisateur dans reflet.txt : whoami > reflet.txt",
      checks=[C_fe("reflet.txt"), C_nempty("reflet.txt")],
      hints=["whoami > reflet.txt", "Le miroir ne ment jamais."],
      solution="whoami > reflet.txt"),

    L(212, "La carte complete",
      story="L'annuaire mysterieux ne s'ouvre qu'avec une identite COMPLETE : uid, gid, groupes. "
            "Fournis ta carte dans identite.txt (commande 'id').",
      lesson="'id' sans argument = TOUTE ton identite. uid (toi), gid (ton groupe), groups (tes equipes). "
             "Trois infos, une commande. La carte complete.",
      mission="Enregistre ton identite complete dans identite.txt : id > identite.txt",
      checks=[C_fe("identite.txt"), C_fc("identite.txt", text="uid=")],
      hints=["id > identite.txt", "uid=..., gid=..., groups=... : la totale."],
      solution="id > identite.txt"),

    L(213, "Les cercles secrets",
      story="Il parait qu'il existe des cercles secrets : docker, sudo, adm... Fais-tu partie d'un cercle ? "
            "Liste tes groupes dans cercles.txt et cherche les noms intrigants.",
      lesson="Chaque groupe donne des pouvoirs : 'sudo' = administrer, 'docker' = conteneurs, 'adm' = lire les logs... "
             "'groups' revele tes cercles. Les tiens, pas ceux des autres.",
      mission="Liste tes groupes dans cercles.txt : groups > cercles.txt",
      checks=[C_fe("cercles.txt"), C_nempty("cercles.txt")],
      hints=["groups > cercles.txt", "Lis la liste : un nom t'intrigue ?"],
      solution="groups > cercles.txt"),

    L(214, "Apparitions et disparitions",
      story="Etrange : hier soir, quelqu'un etait connecte... Qui est la MAINTENANT ? "
            "Fais le point avec 'who' dans apparitions.txt.",
      lesson="'who' = photo des connectes a l'instant T. Un inconnu dans la liste un dimanche a 3h du matin ? "
             "C'est comme ca que commencent les enquetes de securite.",
      mission="Liste les utilisateurs connectes dans apparitions.txt : who > apparitions.txt",
      checks=[C_fe("apparitions.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > apparitions.txt", "Une photo des presents, ici et maintenant."],
      solution="who > apparitions.txt"),

    L(215, "Le numero de serie",
      story="Chaque employe a un numero de serie : son uid ! Le tien est grave quelque part dans le systeme. "
            "Retrouve-le avec 'id -u' dans numero-serie.txt.",
      lesson="Les humains ont des noms, les machines des numeros. 'id -u' = ton numero de serie. "
             "Les permissions, les processus, les fichiers : tout utilise ce numero en interne.",
      mission="Enregistre ton uid dans numero-serie.txt : id -u > numero-serie.txt",
      checks=[C_fe("numero-serie.txt"), C_fc("numero-serie.txt", regex=r"\d+")],
      hints=["id -u > numero-serie.txt", "Ton numero de serie, en chiffres."],
      solution="id -u > numero-serie.txt"),

    L(216, "La page te concernant",
      story="L'annuaire mysterieux fait 40 pages... mais UNE SEULE parle de toi. Trouve-la avec grep "
            "et recopie-la dans entree.txt.",
      lesson="'grep \"^NOM:\" /etc/passwd' : le '^' dit 'en debut de ligne', le ':' final evite les homonymes "
             "(marie ne matche pas marie-line). De la peche de precision.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > entree.txt",
      checks=[C_fe("entree.txt"), C_fc("entree.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > entree.txt", "^ = debut de ligne, : = fin du nom. Precision !"],
      solution="grep \"^$(whoami):\" /etc/passwd > entree.txt"),

    L(217, "La population du systeme",
      story="L'annuaire contient des humains... et BEAUCOUP de comptes systeme (daemon, nobody, systemd-...). "
            "Recense toute la population dans population.txt.",
      lesson="'wc -l < /etc/passwd' compte TOUT : humains + systeme. La plupart des comptes ne se connecteront "
             "JAMAIS : ce sont des identites de service. Le systeme est une ville peuplee de fantomes utiles.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > population.txt",
      checks=[C_fe("population.txt"), C_fc("population.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > population.txt", "Humains + fantomes utiles : tout le monde compte."],
      solution="wc -l < /etc/passwd > population.txt"),

    L(218, "Le gardien de l'annuaire",
      story="Un annuaire aussi precieux doit avoir un gardien irreprochable. Verifie que /etc/passwd appartient "
            "bien a root, avec les bons droits.",
      lesson="Si /etc/passwd appartenait a un simple utilisateur, n'importe qui pourrait se creer un compte root ! "
             "'ls -l' + oeil vigilant = securite de base.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Proprietaire root, droits carres : tout va bien."],
      solution="ls -l /etc/passwd"),

    L(219, "Ou dort le passe ?",
      story="Le passe-partout 'sudo' dort quelque part dans les couloirs du systeme (/usr/bin ? /bin ?). "
            "Localise-le sans le reveiller (sans l'utiliser !).",
      lesson="'command -v' cherche une commande dans le PATH sans l'executer. Zero risque, 100% info. "
             "Le reflexe avant d'utiliser un outil puissant : savoir OU il est.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Localiser, pas utiliser. Chut, il dort."],
      solution="command -v sudo"),

    L(220, "BOSS : la fiche du patron",
      story="L'annuaire mysterieux se referme... sur la fiche la plus impressionnante : celle de root. "
            "uid 0. Enregistre-la dans fiche-du-patron.txt et medite : un jour, tu administreras comme lui.",
      lesson="BOSS : 'id root > fiche'. uid=0, gid=0. Retiens ce zero : dans les scripts, 'if [ $(id -u) -eq 0 ]' "
             "veut dire 'si je suis root'. Tu utiliseras ca toute ta vie d'admin.",
      mission="Enregistre l'identite de root dans fiche-du-patron.txt : id root > fiche-du-patron.txt",
      checks=[C_fe("fiche-du-patron.txt"), C_fc("fiche-du-patron.txt", text="uid=0")],
      hints=["id root > fiche-du-patron.txt", "uid=0 : memorise ce zero, il reviendra souvent."],
      solution="id root > fiche-du-patron.txt",
      xp=25, boss=True),

    # ================= JOUR 23 : le club des groupes =================
    L(221, "Ton pseudo officiel",
      story="Pour rejoindre les clubs, il faut d'abord prouver ton pseudo officiel. Ni surnom, ni blague : "
            "ton VRAI nom d'utilisateur, dans pseudo.txt.",
      lesson="'whoami' = le pseudo officiel, celui que le systeme connait. Les clubs serieux n'acceptent que ca. "
             "Prouve ton identite, et les portes s'ouvrent.",
      mission="Enregistre ton nom d'utilisateur dans pseudo.txt : whoami > pseudo.txt",
      checks=[C_fe("pseudo.txt"), C_nempty("pseudo.txt")],
      hints=["whoami > pseudo.txt", "Ton pseudo officiel, sans triche."],
      solution="whoami > pseudo.txt"),

    L(222, "Les papiers d'inscription",
      story="L'inscription au club demande tes papiers COMPLETS : uid, gid, groupes. "
            "Remplis le formulaire papiers.txt avec la commande 'id'.",
      lesson="'id' = le formulaire d'inscription universel. Un uid, un gid, des groupes : avec ca, "
             "n'importe quel club (service, application) sait qui tu es et ce que tu peux faire.",
      mission="Enregistre ton identite complete dans papiers.txt : id > papiers.txt",
      checks=[C_fe("papiers.txt"), C_fc("papiers.txt", text="uid=")],
      hints=["id > papiers.txt", "uid, gid, groupes : le dossier complet."],
      solution="id > papiers.txt"),

    L(223, "De quels clubs es-tu ?",
      story="Le club des admins veut savoir : de quels clubs fais-tu DEJA partie ? "
            "Montre ta carte de membre (tes groupes) dans clubs.txt !",
      lesson="Tes groupes = tes cartes de membre. On ne rejoint pas le club 'sudo' par hasard : "
             "c'est root qui distribue les cartes. 'groups' montre ta collection.",
      mission="Liste tes groupes dans clubs.txt : groups > clubs.txt",
      checks=[C_fe("clubs.txt"), C_nempty("clubs.txt")],
      hints=["groups > clubs.txt", "Ta collection de cartes de membre."],
      solution="groups > clubs.txt"),

    L(224, "Qui est au club ?",
      story="Le club est-il vide ou plein ? Fais l'appel des connectes avec 'who' "
            "dans membres-presents.txt.",
      lesson="'who' liste les presents. Simple, instantane, fiable. Avant une reunion (ou une maintenance), "
             "on fait l'appel : qui est la, qui sera derange ?",
      mission="Liste les utilisateurs connectes dans membres-presents.txt : who > membres-presents.txt",
      checks=[C_fe("membres-presents.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > membres-presents.txt", "L'appel du club, ici et maintenant."],
      solution="who > membres-presents.txt"),

    L(225, "Ton dossard",
      story="Pour le tournoi inter-clubs, chaque joueur porte son dossard : son uid ! "
            "Recupere ton dossard dans dossard.txt.",
      lesson="'id -u' = ton dossard. Que tu sois 'marie' ou 'stagiaire-2026', pour l'arbitre (le noyau), "
             "tu es un numero. Et c'est tres bien comme ca.",
      mission="Enregistre ton uid dans dossard.txt : id -u > dossard.txt",
      checks=[C_fe("dossard.txt"), C_fc("dossard.txt", regex=r"\d+")],
      hints=["id -u > dossard.txt", "Ton dossard : un numero, fierte du joueur."],
      solution="id -u > dossard.txt"),

    L(226, "Le registre des inscriptions",
      story="Le grand registre /etc/passwd garde la trace de TOUTES les inscriptions. "
            "Retrouve la tienne dans inscription.txt.",
      lesson="Chaque compte nait d'une ligne dans /etc/passwd. 'grep \"^$(whoami):\"' retrouve ton acte de naissance "
             "numerique : nom, uid, dossier, shell.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > inscription.txt",
      checks=[C_fe("inscription.txt"), C_fc("inscription.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > inscription.txt", "Ton acte de naissance numerique."],
      solution="grep \"^$(whoami):\" /etc/passwd > inscription.txt"),

    L(227, "Tous les membres",
      story="L'assemblee generale veut le nombre EXACT de membres (comptes). Humains ET systeme : "
            "tout le monde compte ! Total dans membres-total.txt.",
      lesson="'wc -l < /etc/passwd' : le decompte officiel. Les comptes systeme sont des membres a part entiere : "
             "sans eux, pas de services, pas d'imprimante, pas de reseau.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > membres-total.txt",
      checks=[C_fe("membres-total.txt"), C_fc("membres-total.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > membres-total.txt", "Le decompte officiel de l'AG."],
      solution="wc -l < /etc/passwd > membres-total.txt"),

    L(228, "Le coffre du club",
      story="Le registre du club (/etc/passwd) dort dans un coffre : verifie qu'il appartient bien a root. "
            "Un registre modifiable par tous = des faux membres !",
      lesson="Securite du registre : proprietaire root, ecriture reservee a root. Si 'ls -l' montre autre chose, "
             "c'est une alerte rouge. Verifie, c'est ton devoir de membre vigilant.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Le coffre doit appartenir a root."],
      solution="ls -l /etc/passwd"),

    L(229, "La cle du club VIP",
      story="Le club VIP s'ouvre avec 'sudo'. Tu n'y entreras pas aujourd'hui (patience, stagiaire !), "
            "mais localise au moins la serrure.",
      lesson="'command -v sudo' : reperer la serrure sans la forcer. Un bon admin connait ses outils AVANT d'en avoir "
             "besoin. Le jour ou tu utiliseras sudo, tu sauras ou il vit.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Reperer, pas forcer. Patience..."],
      solution="command -v sudo"),

    L(230, "BOSS : le president du club",
      story="Le president du club des clubs, c'est root. uid 0, tous les clubs, tous les pouvoirs. "
            "Archive sa carte de membre dans president.txt. Un jour, peut-etre, tu siegeras a sa table...",
      lesson="BOSS : 'id root'. Le president a uid 0. Note aussi ses groupes : root fait partie du groupe root. "
             "Simple, logique, tout-puissant.",
      mission="Enregistre l'identite de root dans president.txt : id root > president.txt",
      checks=[C_fe("president.txt"), C_fc("president.txt", text="uid=0")],
      hints=["id root > president.txt", "Le president : uid 0, sans discussion."],
      solution="id root > president.txt",
      xp=25, boss=True),

    # ================= JOUR 24 : le grand patron =================
    L(231, "Devant le patron",
      story="Aujourd'hui, tu es convoque devant... la fiche du grand patron. D'abord, presente-toi proprement : "
            "ton nom d'utilisateur dans prenom.txt. Tiens-toi droit !",
      lesson="Se presenter : 'whoami > prenom.txt'. Devant le patron (ou dans un script), on ne suppose jamais : "
             "on affiche, on enregistre, on prouve.",
      mission="Enregistre ton nom d'utilisateur dans prenom.txt : whoami > prenom.txt",
      checks=[C_fe("prenom.txt"), C_nempty("prenom.txt")],
      hints=["whoami > prenom.txt", "Tiens-toi droit, presente-toi."],
      solution="whoami > prenom.txt"),

    L(232, "Ton dossier est vide ?",
      story="Le patron veut TON DOSSIER complet sur son bureau : uid, gid, groupes. "
            "Depose acte.txt. Gare aux taches de cafe !",
      lesson="'id > acte.txt' : le dossier complet, propre, sans tache. Les patrons aiment les dossiers complets. "
             "Les scripts aussi.",
      mission="Enregistre ton identite complete dans acte.txt : id > acte.txt",
      checks=[C_fe("acte.txt"), C_fc("acte.txt", text="uid=")],
      hints=["id > acte.txt", "Le dossier complet, sans tache de cafe."],
      solution="id > acte.txt"),

    L(233, "Tes alliances",
      story="'Avec qui tu traines ?' demande le patron. Traduction polie : liste tes groupes dans alliances.txt. "
            "Montre tes belles frequentations.",
      lesson="Tes groupes = tes alliances. 'sudo', 'docker', 'adm' : de belles frequentations. "
             "'groups' les affiche. Le patron juge. (Bienveillamment. Enfin, esperons.)",
      mission="Liste tes groupes dans alliances.txt : groups > alliances.txt",
      checks=[C_fe("alliances.txt"), C_nempty("alliances.txt")],
      hints=["groups > alliances.txt", "Montre tes belles frequentations."],
      solution="groups > alliances.txt"),

    L(234, "La salle d'audience",
      story="Qui attend dans la salle d'audience (connecte en ce moment) ? Fais l'appel avec 'who' "
            "dans audience.txt.",
      lesson="'who' : qui attend en ce moment ? Sur un serveur, la 'salle d'audience' est toujours ouverte. "
             "L'admin qui ne fait jamais l'appel aura des surprises.",
      mission="Liste les utilisateurs connectes dans audience.txt : who > audience.txt",
      checks=[C_fe("audience.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > audience.txt", "Qui attend dans la salle ?"],
      solution="who > audience.txt"),

    L(235, "Ton rang",
      story="Dans la hierarchie, chacun a un rang : son uid. Les petits numeros sont les anciens (les services), "
            "les grands les nouveaux. Grave ton rang dans rang.txt.",
      lesson="uid < 1000 = comptes systeme (les anciens), uid >= 1000 = humains (les nouveaux). "
             "'id -u' revele ton rang dans l'ordre ancien du systeme.",
      mission="Enregistre ton uid dans rang.txt : id -u > rang.txt",
      checks=[C_fe("rang.txt"), C_fc("rang.txt", regex=r"\d+")],
      hints=["id -u > rang.txt", "Petit numero = ancien. Grand = nouveau. Et toi ?"],
      solution="id -u > rang.txt"),

    L(236, "Ton dossier RH",
      story="Ton dossier RH dort dans /etc/passwd. Le patron veut le voir : extrais TA ligne dans dossier.txt.",
      lesson="Ton dossier RH : nom, uid, gid, dossier perso, shell. Une ligne, 7 champs separes par ':'. "
             "Lis-la : c'est ton CV officiel pour le systeme.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > dossier.txt",
      checks=[C_fe("dossier.txt"), C_fc("dossier.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > dossier.txt", "7 champs, ton CV officiel."],
      solution="grep \"^$(whoami):\" /etc/passwd > dossier.txt"),

    L(237, "Tous les sujets",
      story="Le patron regne sur combien de sujets (comptes) ? Humains et systeme : tout le royaume compte. "
            "Recense dans sujets.txt.",
      lesson="Le royaume = tous les comptes. 'wc -l < /etc/passwd' : le recensement royal. "
             "Un bon roi connait le nombre de ses sujets.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > sujets.txt",
      checks=[C_fe("sujets.txt"), C_fc("sujets.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > sujets.txt", "Le recensement royal. Longue vie au roi !"],
      solution="wc -l < /etc/passwd > sujets.txt"),

    L(238, "Le sceau royal",
      story="Le registre royal (/etc/passwd) porte le sceau de root. Verifie-le : proprietaire, droits. "
            "Un sceau brise = trahison !",
      lesson="'ls -l /etc/passwd' : verifier le sceau royal. Proprietaire root, droits stricts. "
             "Les rois prudents verifient leurs sceaux. Les admins aussi.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Le sceau doit etre intact : root, droits stricts."],
      solution="ls -l /etc/passwd"),

    L(239, "Le sceptre",
      story="Le sceptre du pouvoir s'appelle 'sudo'. Tu ne le toucheras pas (ordre royal !), "
            "mais tu dois savoir ou il est range.",
      lesson="'command -v sudo' : savoir ou est range le sceptre. Le jour de ton couronnement (admin), "
             "tu l'utiliseras. En attendant, respect et distance.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Respect et distance. Pour l'instant."],
      solution="command -v sudo"),

    L(240, "BOSS : audience royale",
      story="Le moment est venu : audience avec root EN PERSONNE (enfin, sa fiche). uid 0, gid 0. "
            "Archive l'entrevue dans root-en-personne.txt. Historique !",
      lesson="BOSS royal : 'id root'. Contemple : uid=0, gid=0, groupes=root. La fiche la plus courte et la plus "
             "puissante du systeme. Un jour, tu auras ces pouvoirs. Avec sagesse.",
      mission="Enregistre l'identite de root dans root-en-personne.txt : id root > root-en-personne.txt",
      checks=[C_fe("root-en-personne.txt"), C_fc("root-en-personne.txt", text="uid=0")],
      hints=["id root > root-en-personne.txt", "La fiche la plus puissante du systeme."],
      solution="id root > root-en-personne.txt",
      xp=25, boss=True),

    # ================= JOUR 25 : la nuit des espions =================
    L(241, "Nom de code",
      story="Mission secrete : cette nuit, tu es un espion. Mais meme un espion a un vrai nom pour le systeme. "
            "Rends ton nom de code... euh, ton vrai nom, dans agent.txt. Chut.",
      lesson="Meme les espions ont un 'whoami'. Le systeme se moque des trench-coats : il veut un uid. "
             "Ton nom de code officiel, dans agent.txt. Chut.",
      mission="Enregistre ton nom d'utilisateur dans agent.txt : whoami > agent.txt",
      checks=[C_fe("agent.txt"), C_nempty("agent.txt")],
      hints=["whoami > agent.txt", "Chut... c'est une mission secrete."],
      solution="whoami > agent.txt"),

    L(242, "La couverture",
      story="Ta couverture : une identite complete et credible (uid, gid, groupes). Fabrique-la avec 'id' "
            "dans couverture.txt. Sans faute : l'ennemi verifie tout.",
      lesson="'id' = identite credible complete. Les espions qui oublient leur gid se font reperer. "
             "Toi, tu fournis uid + gid + groupes. Couverture parfaite.",
      mission="Enregistre ton identite complete dans couverture.txt : id > couverture.txt",
      checks=[C_fe("couverture.txt"), C_fc("couverture.txt", text="uid=")],
      hints=["id > couverture.txt", "Couverture parfaite : uid, gid, groupes."],
      solution="id > couverture.txt"),

    L(243, "Tes reseaux",
      story="Un bon espion a des reseaux (des groupes !). Liste tes reseaux d'influence dans reseaux.txt. "
            "Dis-moi qui tu frequentes, je te dirai ce que tu peux faire.",
      lesson="'groups' = tes reseaux d'influence. Chaque groupe ouvre des portes. Les espions collectionnent "
             "les groupes comme les timbres. Toi aussi, avec le temps.",
      mission="Liste tes groupes dans reseaux.txt : groups > reseaux.txt",
      checks=[C_fe("reseaux.txt"), C_nempty("reseaux.txt")],
      hints=["groups > reseaux.txt", "Tes reseaux d'influence, agent."],
      solution="groups > reseaux.txt"),

    L(244, "Qui est dans la planque ?",
      story="La planque (le serveur) est-elle vide ? Des espions ennemis pourraient etre connectes EN CE MOMENT. "
            "Verifie avec 'who' dans planque.txt !",
      lesson="'who' en pleine nuit = mission de contre-espionnage. Une connexion inconnue a 3h du matin ? "
             "Alerte rouge. Les admins font ca pour de vrai.",
      mission="Liste les utilisateurs connectes dans planque.txt : who > planque.txt",
      checks=[C_fe("planque.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > planque.txt", "Contre-espionnage : qui est la, a cette heure ?!"],
      solution="who > planque.txt"),

    L(245, "Le code agent",
      story="Ton code agent : un numero, pas un nom. Les numeros ne mentent pas et ne se devinent pas. "
            "Ton uid dans code-agent.txt. Memorise-le.",
      lesson="'id -u' = ton code agent. 4 ou 5 chiffres, facile a retenir, impossible a deviner. "
             "Les numeros, c'est le langage des initiés... et des machines.",
      mission="Enregistre ton uid dans code-agent.txt : id -u > code-agent.txt",
      checks=[C_fe("code-agent.txt"), C_fc("code-agent.txt", regex=r"\d+")],
      hints=["id -u > code-agent.txt", "Ton code agent. Memorise-le, puis oublie ce message."],
      solution="id -u > code-agent.txt"),

    L(246, "Le dossier de l'agence",
      story="L'agence garde un dossier sur TOI dans /etc/passwd. Les espions verifient toujours leur propre dossier "
            "(on ne sait jamais). Extrais-le dans fiche-agent.txt.",
      lesson="Verifier son propre dossier : le reflexe de l'espion prudent. 'grep \"^$(whoami):\" /etc/passwd' : "
             "ta ligne, ton dossier perso, ton shell. Tout est en ordre, agent ?",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > fiche-agent.txt",
      checks=[C_fe("fiche-agent.txt"), C_fc("fiche-agent.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > fiche-agent.txt", "Verifie ton dossier. Tout est en ordre ?"],
      solution="grep \"^$(whoami):\" /etc/passwd > fiche-agent.txt"),

    L(247, "Les effectifs de l'agence",
      story="Combien d'agents (comptes) dans l'agence ? Humains, taupes systeme, tout le monde ! "
            "Compte dans effectifs.txt. Secret defense.",
      lesson="'wc -l < /etc/passwd' : les effectifs secrets. La plupart sont des 'taupes systeme' (daemon, sys, nobody) "
             "qui ne dorment jamais et ne parlent a personne. Parfait pour une agence.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > effectifs.txt",
      checks=[C_fe("effectifs.txt"), C_fc("effectifs.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > effectifs.txt", "Secret defense, evidemment."],
      solution="wc -l < /etc/passwd > effectifs.txt"),

    L(248, "Le coffre de l'agence",
      story="Le fichier des agents (/etc/passwd) est dans un coffre : verifie qu'il appartient a root. "
            "Si un agent double le modifiait, catastrophe !",
      lesson="Securite du fichier des agents : 'ls -l /etc/passwd'. Proprietaire root ou alerte maximale. "
             "Les espions verifient les serrures. Les admins aussi.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Le coffre appartient a root. Sinon : alerte maximale."],
      solution="ls -l /etc/passwd"),

    L(249, "L'arme secrete",
      story="L'agence possede une arme secrete : 'sudo'. Tu n'as pas l'autorisation de t'en servir (niveau trop bas, "
            "agent), mais tu dois connaitre sa cachette.",
      lesson="'command -v sudo' : reperer la cachette de l'arme secrete. Un jour, avec l'autorisation (le mot de passe "
             "et le groupe sudo), tu t'en serviras. Pas cette nuit.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Niveau d'autorisation insuffisant... pour l'instant."],
      solution="command -v sudo"),

    L(250, "BOSS : le big boss",
      story="Au sommet de l'agence : le big boss, nom de code 'root'. uid 0. Personne ne l'a jamais vu "
            "(il ne se connecte jamais). Archive sa fiche secrete dans big-boss.txt.",
      lesson="BOSS de la nuit : 'id root'. Le big boss ne se connecte JAMAIS directement : trop risque. "
             "Il agit via sudo, comme les grands. Retiens la lecon, agent.",
      mission="Enregistre l'identite de root dans big-boss.txt : id root > big-boss.txt",
      checks=[C_fe("big-boss.txt"), C_fc("big-boss.txt", text="uid=0")],
      hints=["id root > big-boss.txt", "Le big boss : uid 0, invisible, tout-puissant."],
      solution="id root > big-boss.txt",
      xp=25, boss=True),

    # ================= JOUR 26 : le registre du royaume =================
    L(251, "Citoyen, presente-toi",
      story="Halte-la, voyageur ! Pour entrer dans le royaume, decline ton identite : "
            "ton nom d'utilisateur dans citoyen.txt. Le garde du pont ne plaisante pas.",
      lesson="'whoami' = decliner son identite au garde du pont. Sans nom officiel, pas d'entree dans le royaume. "
             "Les gardes (comme les systemes) n'aiment pas les inconnus.",
      mission="Enregistre ton nom d'utilisateur dans citoyen.txt : whoami > citoyen.txt",
      checks=[C_fe("citoyen.txt"), C_nempty("citoyen.txt")],
      hints=["whoami > citoyen.txt", "Halte-la ! Ton nom, voyageur !"],
      solution="whoami > citoyen.txt"),

    L(252, "Le parchemin d'identite",
      story="Le scribe te demande un parchemin d'identite COMPLET : uid, gid, groupes. "
            "Rouleau de parchemin... enfin, fichier parchemin.txt, commande 'id'.",
      lesson="'id' = le parchemin d'identite. Déroule-le : uid, gid, groupes. Les scribes (et les programmes) "
             "lisent ce parchemin avant de te laisser passer.",
      mission="Enregistre ton identite complete dans parchemin.txt : id > parchemin.txt",
      checks=[C_fe("parchemin.txt"), C_fc("parchemin.txt", text="uid=")],
      hints=["id > parchemin.txt", "Le scribe deroule... et approuve."],
      solution="id > parchemin.txt"),

    L(253, "Les guildes",
      story="Dans le royaume, on appartient a des guildes : forgerons, scribes, gardes... "
            "Tes guildes (groupes) dans guildes.txt, citoyen !",
      lesson="Les guildes = les groupes. 'groups' dit a quelles guildes tu appartiens. "
             "La guilde 'sudo' mene au chateau. Les autres menent... ailleurs.",
      mission="Liste tes groupes dans guildes.txt : groups > guildes.txt",
      checks=[C_fe("guildes.txt"), C_nempty("guildes.txt")],
      hints=["groups > guildes.txt", "Tes guildes, citoyen. Montre ton blason."],
      solution="groups > guildes.txt"),

    L(254, "La place publique",
      story="Qui se promene sur la place publique (connecte en ce moment) ? Le heraut fait l'appel avec 'who' : "
            "resultats dans place-publique.txt.",
      lesson="'who' = le heraut qui fait l'appel sur la place. Qui est la ? Depuis quelle porte (terminal) ? "
             "Depuis quand ? Le heraut sait tout, dit tout.",
      mission="Liste les utilisateurs connectes dans place-publique.txt : who > place-publique.txt",
      checks=[C_fe("place-publique.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > place-publique.txt", "Le heraut fait l'appel : qui est la ?"],
      solution="who > place-publique.txt"),

    L(255, "Le numero de sceau",
      story="Chaque citoyen porte un numero de sceau : son uid. Le tien est frappe dans le bronze du systeme. "
            "Releve-le dans sceau-numero.txt.",
      lesson="Le numero de sceau (uid) est frappe une fois pour toutes. 'id -u' le revele. "
             "On peut changer de nom, pas de numero : le bronze, ca ne s'efface pas.",
      mission="Enregistre ton uid dans sceau-numero.txt : id -u > sceau-numero.txt",
      checks=[C_fe("sceau-numero.txt"), C_fc("sceau-numero.txt", regex=r"\d+")],
      hints=["id -u > sceau-numero.txt", "Frappe dans le bronze. Ineffacable."],
      solution="id -u > sceau-numero.txt"),

    L(256, "Ta ligne au registre",
      story="Le grand registre /etc/passwd garde UNE ligne par citoyen. Trouve la tienne, recopie-la "
            "dans ligne-registre.txt. Verifie que le scribe ne s'est pas trompe !",
      lesson="Le registre ne ment pas (sauf erreur de scribe). 'grep \"^$(whoami):\"' retrouve ta ligne : "
             "nom, uid, dossier, shell. Verifie : un bon citoyen connait sa ligne.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > ligne-registre.txt",
      checks=[C_fe("ligne-registre.txt"), C_fc("ligne-registre.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > ligne-registre.txt", "Verifie que le scribe ne s'est pas trompe !"],
      solution="grep \"^$(whoami):\" /etc/passwd > ligne-registre.txt"),

    L(257, "Toutes les ames",
      story="Le roi veut compter TOUTES les ames du royaume : humains, serviteurs systeme, fantomes... "
            "Compte dans ames.txt. N'oublie personne !",
      lesson="'wc -l < /etc/passwd' : le decompte des ames. Serviteurs (daemon), fantomes (nobody), "
             "gardes (systemd-...) : le royaume grouille de vie invisible.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > ames.txt",
      checks=[C_fe("ames.txt"), C_fc("ames.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > ames.txt", "Toutes les ames, meme les invisibles."],
      solution="wc -l < /etc/passwd > ames.txt"),

    L(258, "Le tresor royal",
      story="Le registre (/etc/passwd) est un tresor royal : verifie qu'il appartient au roi (root). "
            "Un tresor sans gardien attire les brigands !",
      lesson="'ls -l /etc/passwd' : inspecter le tresor. Gardien root, droits stricts = royaume en paix. "
             "Les brigands testent toujours les serrures du tresor en premier.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Gardien root ? Droits stricts ? Le royaume est en paix."],
      solution="ls -l /etc/passwd"),

    L(259, "L'epee du roi",
      story="L'epee du pouvoir s'appelle 'sudo'. Tu n'es pas encore adoube chevalier, mais tu dois savoir "
            "ou elle est exposee. Localise-la (sans la toucher !).",
      lesson="'command -v sudo' : localiser l'epee sans la toucher. Les futurs chevaliers admirent, "
             "les chevaliers utilisent. Patience, ecuyer.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Admire, ne touche pas. Patience, ecuyer."],
      solution="command -v sudo"),

    L(260, "BOSS : le roi",
      story="Le roi lui-meme ! Nom : root. Numero : 0. Pouvoir : absolu. Tu es admis a contempler sa fiche "
            "dans le-roi.txt. Salue bien bas, citoyen.",
      lesson="BOSS royal : 'id root'. uid=0 : le numero du roi. Personne d'autre ne porte le zero. "
             "Si un jour tu vois un autre uid 0... c'est un usurpateur. Alerte !",
      mission="Enregistre l'identite de root dans le-roi.txt : id root > le-roi.txt",
      checks=[C_fe("le-roi.txt"), C_fc("le-roi.txt", text="uid=0")],
      hints=["id root > le-roi.txt", "Le zero est unique : c'est le sceau du roi."],
      solution="id root > le-roi.txt",
      xp=25, boss=True),

    # ================= JOUR 27 : recensement general =================
    L(261, "Porte a porte",
      story="Recensement general ! L'agent recenseur frappe a TA porte en premier : "
            "ton nom d'utilisateur dans habitant.txt. Souris, c'est pour les statistiques.",
      lesson="Le recensement commence par soi-meme : 'whoami > habitant.txt'. Les statistiques officielles "
             "ne se font pas au doigt mouille : un nom exact, grave dans un fichier.",
      mission="Enregistre ton nom d'utilisateur dans habitant.txt : whoami > habitant.txt",
      checks=[C_fe("habitant.txt"), C_nempty("habitant.txt")],
      hints=["whoami > habitant.txt", "Souris, c'est pour les statistiques."],
      solution="whoami > habitant.txt"),

    L(262, "L'etat civil",
      story="L'etat civil veut ton dossier COMPLET : uid, gid, groupes. Remplis le formulaire etat-civil.txt. "
            "Ecris lisiblement (la commande 'id' ecrit tres lisiblement).",
      lesson="'id' = l'etat civil : ne-le (uid), famille (gid), associations (groupes). Un formulaire rempli "
             "en une commande. Les fonctionnaires revent de ca.",
      mission="Enregistre ton identite complete dans etat-civil.txt : id > etat-civil.txt",
      checks=[C_fe("etat-civil.txt"), C_fc("etat-civil.txt", text="uid=")],
      hints=["id > etat-civil.txt", "Le formulaire officiel, rempli en une commande."],
      solution="id > etat-civil.txt"),

    L(263, "Les corporations",
      story="Question du recenseur : 'A quelles corporations appartenez-vous ?' Liste tes groupes "
            "dans corporations.txt. Tout declarer, c'est la loi !",
      lesson="'groups' : declaration officielle de tes corporations. Tout declarer : le recenseur verifie "
             "et le systeme, lui, ne pardonne pas les oublis.",
      mission="Liste tes groupes dans corporations.txt : groups > corporations.txt",
      checks=[C_fe("corporations.txt"), C_nempty("corporations.txt")],
      hints=["groups > corporations.txt", "Tout declarer, c'est la loi !"],
      solution="groups > corporations.txt"),

    L(264, "Qui est a la maison ?",
      story="Le recenseur frappe aux portes : qui est PRESENT (connecte) en ce moment ? "
            "Fais la tournee avec 'who' dans portes.txt.",
      lesson="'who' = la tournee du recenseur. Qui est a la maison, depuis quelle porte (terminal) ? "
             "Les absents seront recenses une autre fois. Peut-etre.",
      mission="Liste les utilisateurs connectes dans portes.txt : who > portes.txt",
      checks=[C_fe("portes.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > portes.txt", "Toc toc... qui est present ?"],
      solution="who > portes.txt"),

    L(265, "Le numero de foyer",
      story="Chaque foyer a un numero : le tien, c'est ton uid ! Declare ton numero de foyer dans foyer.txt. "
            "Les numeros pairs gagnent... rien du tout. Mais declare quand meme.",
      lesson="'id -u' = ton numero de foyer. Unique, officiel, obligatoire. Les statistiques adorent les numeros : "
             "ca se trie, ca se compte, ca ne discute pas.",
      mission="Enregistre ton uid dans foyer.txt : id -u > foyer.txt",
      checks=[C_fe("foyer.txt"), C_fc("foyer.txt", regex=r"\d+")],
      hints=["id -u > foyer.txt", "Ton numero de foyer. Obligatoire, unique."],
      solution="id -u > foyer.txt"),

    L(266, "L'extrait de naissance",
      story="Le recenseur exige ton extrait de naissance : ta ligne de /etc/passwd ! "
            "Delivre-le dans extrait.txt, avec le tampon grep.",
      lesson="L'extrait de naissance numerique : ta ligne de /etc/passwd. 'grep \"^$(whoami):\"' + tampon officiel. "
             "Delivre en une commande, valable a vie (ou jusqu'a suppression du compte).",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > extrait.txt",
      checks=[C_fe("extrait.txt"), C_fc("extrait.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > extrait.txt", "Tamponne, signe, delivre."],
      solution="grep \"^$(whoami):\" /etc/passwd > extrait.txt"),

    L(267, "Le chiffre officiel",
      story="LE moment du recensement : le chiffre OFFICIEL de la population (tous les comptes). "
            "Proclame-le dans total.txt. Les historiens s'en souviendront.",
      lesson="'wc -l < /etc/passwd' = le chiffre officiel. Proclame, grave, archive. Dans 100 ans, "
             "les historiens sauront combien de comptes vivaient sur cette machine.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > total.txt",
      checks=[C_fe("total.txt"), C_fc("total.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > total.txt", "Le chiffre officiel. Solennel. Definitif."],
      solution="wc -l < /etc/passwd > total.txt"),

    L(268, "Le bureau du recensement",
      story="Les archives du recensement (/etc/passwd) sont gardees par root. Verifie le gardien "
            "et les droits : des archives trafiquees fausseraient tout !",
      lesson="Des archives trafiquees = un recensement faux. 'ls -l /etc/passwd' : on verifie le gardien (root) "
             "et les droits avant de croire les chiffres.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "On verifie les archives avant de croire les chiffres."],
      solution="ls -l /etc/passwd"),

    L(269, "Le tampon supreme",
      story="Le recensement se clot avec le tampon supreme : 'sudo'. Tu ne tamponneras pas toi-meme "
            "(pas le grade !), mais localise le tampon.",
      lesson="'command -v sudo' : localiser le tampon supreme. Seuls les grades superieurs tamponnent. "
             "Toi, tu observes, tu apprends, tu attends ton grade.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Observe, apprends, attends ton grade."],
      solution="command -v sudo"),

    L(270, "BOSS : le souverain",
      story="Cloture du recensement : le souverain (root, uid 0) signe le registre. Archive sa signature "
            "(sa fiche id) dans souverain.txt. Le recensement est officiel !",
      lesson="BOSS du recensement : 'id root'. La signature du souverain : uid=0. Avec elle, le recensement "
             "devient officiel. Sans elle, ce n'est qu'un brouillon.",
      mission="Enregistre l'identite de root dans souverain.txt : id root > souverain.txt",
      checks=[C_fe("souverain.txt"), C_fc("souverain.txt", text="uid=0")],
      hints=["id root > souverain.txt", "La signature du souverain : uid=0."],
      solution="id root > souverain.txt",
      xp=25, boss=True),

    # ================= JOUR 28 : le passe-partout =================
    L(271, "Le detenteur",
      story="On raconte que quelqu'un, ici, detient de grands pouvoirs... Pour commencer l'enquete : "
            "qui ES-TU, toi ? Ton nom dans detenteur.txt. (Suspect n°1 : toi-meme.)",
      lesson="Toute enquete commence par soi : 'whoami > detenteur.txt'. Qui suis-je ? Quels sont mes pouvoirs ? "
             "Le detectice qui s'ignore lui-meme resout peu d'affaires.",
      mission="Enregistre ton nom d'utilisateur dans detenteur.txt : whoami > detenteur.txt",
      checks=[C_fe("detenteur.txt"), C_nempty("detenteur.txt")],
      hints=["whoami > detenteur.txt", "Suspect n°1 : toi-meme. Verifie."],
      solution="whoami > detenteur.txt"),

    L(272, "Le laissez-passer",
      story="Pour circuler pendant l'enquete, il faut un laissez-passer COMPLET : uid, gid, groupes. "
            "Etablis-le dans laissez-passer.txt.",
      lesson="'id' = le laissez-passer. Avec uid + gid + groupes en regle, on circule partout (en lecture). "
             "Sans papiers, on reste a la porte.",
      mission="Enregistre ton identite complete dans laissez-passer.txt : id > laissez-passer.txt",
      checks=[C_fe("laissez-passer.txt"), C_fc("laissez-passer.txt", text="uid=")],
      hints=["id > laissez-passer.txt", "Papiers en regle : circulez, agent."],
      solution="id > laissez-passer.txt"),

    L(273, "Les cercles de confiance",
      story="L'enquete porte sur les cercles de confiance (les groupes). Lesquels frequente-t-ON dans cette maison ? "
            "Commence par lister les TIENS dans cercles-confiance.txt.",
      lesson="Les cercles de confiance = les groupes. 'groups' montre les tiens. L'enqueteur note : "
             "qui frequente 'sudo' detient (peut-etre) le passe-partout...",
      mission="Liste tes groupes dans cercles-confiance.txt : groups > cercles-confiance.txt",
      checks=[C_fe("cercles-confiance.txt"), C_nempty("cercles-confiance.txt")],
      hints=["groups > cercles-confiance.txt", "Qui frequente qui ? L'enquete note tout."],
      solution="groups > cercles-confiance.txt"),

    L(274, "Les entrees et sorties",
      story="Le concierge note les entrees et sorties : qui est connecte MAINTENANT ? "
            "Consulte son registre avec 'who' dans entrees.txt.",
      lesson="'who' = le registre du concierge. Entrees, sorties, presents. Les concierges (comme les logs) "
             "voient tout et oublient rien.",
      mission="Liste les utilisateurs connectes dans entrees.txt : who > entrees.txt",
      checks=[C_fe("entrees.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > entrees.txt", "Le concierge voit tout. Consulte son registre."],
      solution="who > entrees.txt"),

    L(275, "Le numero de cle",
      story="Chaque passe a un numero : le tien, c'est ton uid. Releve ton numero de cle dans cle-numero.txt. "
            "Sauf le zero... le zero, c'est une autre histoire.",
      lesson="'id -u' = ton numero de cle. Tous les numeros ouvrent des portes, sauf... le zero. "
             "Le zero ouvre TOUTES les portes. Mais ca, c'est une autre histoire.",
      mission="Enregistre ton uid dans cle-numero.txt : id -u > cle-numero.txt",
      checks=[C_fe("cle-numero.txt"), C_fc("cle-numero.txt", regex=r"\d+")],
      hints=["id -u > cle-numero.txt", "Tous les numeros ouvrent des portes. Surtout un..."],
      solution="id -u > cle-numero.txt"),

    L(276, "L'autorisation",
      story="Ton autorisation officielle dort dans /etc/passwd. Sors ta ligne dans autorisation.txt : "
            "l'enqueteur veut verifier tes papiers.",
      lesson="Papiers, s'il vous plait : 'grep \"^$(whoami):\" /etc/passwd'. L'enqueteur verifie nom, uid, dossier. "
             "En regle ? Circulez.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > autorisation.txt",
      checks=[C_fe("autorisation.txt"), C_fc("autorisation.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > autorisation.txt", "Papiers en regle ? Circulez."],
      solution="grep \"^$(whoami):\" /etc/passwd > autorisation.txt"),

    L(277, "Tous les detenteurs",
      story="Combien de detenteurs de comptes dans cette maison ? L'inventaire complet dans detenteurs.txt : "
            "l'enquete exige l'exhaustivite.",
      lesson="'wc -l < /etc/passwd' : l'inventaire exhaustif. Enqueteur serieux = comptes exacts. "
             "On ne resout pas une affaire avec des 'a peu pres'.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > detenteurs.txt",
      checks=[C_fe("detenteurs.txt"), C_fc("detenteurs.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > detenteurs.txt", "L'exhaustivite, toujours."],
      solution="wc -l < /etc/passwd > detenteurs.txt"),

    L(278, "Le coffre aux dossiers",
      story="Les dossiers de l'enquete (/etc/passwd) sont sous scelles : verifies par root. "
            "Controle les scelles avec 'ls -l'.",
      lesson="Dossiers sous scelles : 'ls -l /etc/passwd'. Gardien root, scelles intacts ? L'enquete continue. "
             "Scelles brises ? On recommence tout.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Scelles intacts ? L'enquete continue."],
      solution="ls -l /etc/passwd"),

    L(279, "La piece a conviction",
      story="PIECE A CONVICTION N°1 : le passe-partout 'sudo' lui-meme ! Localise-le (sans le toucher, "
            "les empreintes !). 'command -v', gants en latex.",
      lesson="'command -v sudo' : reperer la piece a conviction sans l'alterer. Pas d'execution, pas d'empreintes : "
             "juste la position exacte. Travail de pro.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Gants en latex : on repere, on ne touche pas."],
      solution="command -v sudo"),

    L(280, "BOSS : le grand maitre",
      story="L'enquete touche au but : le detenteur du passe-partout supreme, c'est root, uid 0. "
            "Archive sa fiche dans grand-maitre.txt et boucle l'enquete. Elementaire !",
      lesson="BOSS de l'enquete : 'id root'. Le grand maitre : uid=0. Mystere resolu : tous les passe-partout "
             "menent a root. Elementaire, mon cher admin.",
      mission="Enregistre l'identite de root dans grand-maitre.txt : id root > grand-maitre.txt",
      checks=[C_fe("grand-maitre.txt"), C_fc("grand-maitre.txt", text="uid=0")],
      hints=["id root > grand-maitre.txt", "Elementaire : tous les passe menent a root."],
      solution="id root > grand-maitre.txt",
      xp=25, boss=True),

    # ================= JOUR 29 : la fete du personnel =================
    L(281, "Le carton d'invitation",
      story="C'est la fete du personnel ! A l'entree, le videur demande ton nom OFFICIEL. "
            "Pas de pseudo rigolo : ton vrai nom d'utilisateur dans invite.txt. Et bonne fete !",
      lesson="Meme a la fete, on s'identifie : 'whoami > invite.txt'. Le videur (le systeme) ne laisse entrer "
             "que les vrais comptes. Les fantomes restent dehors.",
      mission="Enregistre ton nom d'utilisateur dans invite.txt : whoami > invite.txt",
      checks=[C_fe("invite.txt"), C_nempty("invite.txt")],
      hints=["whoami > invite.txt", "Ton vrai nom, et entre : la fete t'attend !"],
      solution="whoami > invite.txt"),

    L(282, "Le carton VIP",
      story="Carton VIP pour les employes verifies : uid, gid, groupes, tout doit y figurer ! "
            "Imprime ton carton.txt avec la commande 'id'.",
      lesson="'id' = le carton VIP. Avec uid + gid + groupes imprimes en regle, tu accedes au buffet (lecture) "
             "et a la piste (execution). Sans carton : dehors.",
      mission="Enregistre ton identite complete dans carton.txt : id > carton.txt",
      checks=[C_fe("carton.txt"), C_fc("carton.txt", text="uid=")],
      hints=["id > carton.txt", "Carton VIP : acces buffet + piste."],
      solution="id > carton.txt"),

    L(283, "Les tables",
      story="Le plan de table est organise par GROUPES : chaque groupe a sa table ! De quelles tables fais-tu partie ? "
            "Liste dans tables.txt, et rejoins tes amis.",
      lesson="'groups' = ton plan de table. Chaque groupe = une table pleine d'amis (et de droits). "
             "La table 'sudo' est au fond, pres des serveurs. Un jour, tu y mangeras.",
      mission="Liste tes groupes dans tables.txt : groups > tables.txt",
      checks=[C_fe("tables.txt"), C_nempty("tables.txt")],
      hints=["groups > tables.txt", "Trouve tes tables, rejoins tes amis."],
      solution="groups > tables.txt"),

    L(284, "Qui est sur la piste ?",
      story="Qui danse sur la piste (connecte en ce moment) ? Le DJ fait l'appel au micro avec 'who' : "
            "reponses dans piste.txt. Ambiance !",
      lesson="'who' = le DJ qui fait l'appel. Qui danse (connecte) ? Depuis quel coin (terminal) ? "
             "Le DJ voit toute la piste d'un coup d'oeil.",
      mission="Liste les utilisateurs connectes dans piste.txt : who > piste.txt",
      checks=[C_fe("piste.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > piste.txt", "Le DJ fait l'appel : qui danse ?!"],
      solution="who > piste.txt"),

    L(285, "Le bracelet",
      story="A l'entree, on te remet un bracelet numerote : ton uid ! Grave ton numero de bracelet "
            "dans bracelet.txt. Ne le perds pas dans la soiree.",
      lesson="'id -u' = ton bracelet numerote. Unique, incessible, obligatoire. Meme apres trois jus d'orange, "
             "ton uid ne change pas. Fiable, le bracelet.",
      mission="Enregistre ton uid dans bracelet.txt : id -u > bracelet.txt",
      checks=[C_fe("bracelet.txt"), C_fc("bracelet.txt", regex=r"\d+")],
      hints=["id -u > bracelet.txt", "Ne le perds pas dans la soiree !"],
      solution="id -u > bracelet.txt"),

    L(286, "La liste des invites",
      story="Le videur verifie chaque invite dans le grand registre /etc/passwd. Prouve que tu es sur la liste : "
            "extrais ta ligne dans liste-invites.txt.",
      lesson="Etre sur la liste = avoir sa ligne dans /etc/passwd. 'grep \"^$(whoami):\"' : le videur retrouve ta ligne "
             "en une seconde. Entre, tu es des notres !",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > liste-invites.txt",
      checks=[C_fe("liste-invites.txt"), C_fc("liste-invites.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > liste-invites.txt", "Sur la liste ? Entre, tu es des notres !"],
      solution="grep \"^$(whoami):\" /etc/passwd > liste-invites.txt"),

    L(287, "Combien de convives ?",
      story="Le traiteur demande le nombre EXACT de convives (tous les comptes, meme les discrets du fond). "
            "Compte dans convives.txt. Pas assez de petits fours serait dramatique.",
      lesson="'wc -l < /etc/passwd' : le nombre de convives. Meme les discrets (comptes systeme) comptent : "
             "eux aussi veulent leurs petits fours (leurs ressources).",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > convives.txt",
      checks=[C_fe("convives.txt"), C_fc("convives.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > convives.txt", "Assez de petits fours pour tout le monde !"],
      solution="wc -l < /etc/passwd > convives.txt"),

    L(288, "Le livre d'or",
      story="Le livre d'or de la fete (/etc/passwd, pas touche !) est precieux : verifie qu'il appartient a root. "
            "On ne tague pas le livre d'or.",
      lesson="Meme a la fete, on protege le livre d'or : 'ls -l /etc/passwd'. Gardien root, droits stricts. "
             "La fete est belle quand le registre est sur.",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "On ne tague pas le livre d'or."],
      solution="ls -l /etc/passwd"),

    L(289, "Le micro du patron",
      story="Le micro supreme ('sudo') permet de parler PLUS FORT que tout le monde. Tu ne t'en serviras pas "
            "(karaoke interdit aux stagiaires), mais localise-le.",
      lesson="'command -v sudo' : localiser le micro supreme. Un jour, pour le discours de fin d'annee (une vraie "
             "tache d'admin), tu le prendras. Ce soir : karaoke interdit.",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Karaoke interdit aux stagiaires. Pour l'instant."],
      solution="command -v sudo"),

    L(290, "BOSS : l'invite d'honneur",
      story="Tonnerre d'applaudissements : l'invite d'honneur arrive ! C'est... root ! uid 0 ! "
            "Archive sa fiche dans invite-dhonneur.txt. La fete peut commencer. VRAIMENT.",
      lesson="BOSS de la fete : 'id root'. Quand root entre, tout le monde se leve. uid=0 : "
             "le seul, l'unique, l'invite d'honneur de tous les systemes.",
      mission="Enregistre l'identite de root dans invite-dhonneur.txt : id root > invite-dhonneur.txt",
      checks=[C_fe("invite-dhonneur.txt"), C_fc("invite-dhonneur.txt", text="uid=0")],
      hints=["id root > invite-dhonneur.txt", "Tout le monde se leve : c'est root !"],
      solution="id root > invite-dhonneur.txt",
      xp=25, boss=True),

    # ================= JOUR 30 : le conseil des sages =================
    L(291, "Le jeune sage",
      story="Dernier jour du bloc : tu es admis devant le conseil des sages. Premiere epreuve, la plus simple "
            "et la plus profonde : 'Qui es-tu ?' Reponds dans sage.txt.",
      lesson="Dernier jour, premiere question : 'whoami'. Apres 90 niveaux, tu reponds sans hesiter. "
             "Les sages hochent la tete : le jeune apprend.",
      mission="Enregistre ton nom d'utilisateur dans sage.txt : whoami > sage.txt",
      checks=[C_fe("sage.txt"), C_nempty("sage.txt")],
      hints=["whoami > sage.txt", "'Qui es-tu ?' La question eternelle."],
      solution="whoami > sage.txt"),

    L(292, "La sagesse complete",
      story="Deuxieme epreuve : 'Montre-nous TOUTE ton identite.' uid, gid, groupes : rien ne se cache devant "
            "les sages. Depose sagesse.txt.",
      lesson="'id' devant les sages : transparence totale. uid, gid, groupes : tout est revele. "
             "Les sages approuvent : un admin ne cache rien a son systeme.",
      mission="Enregistre ton identite complete dans sagesse.txt : id > sagesse.txt",
      checks=[C_fe("sagesse.txt"), C_fc("sagesse.txt", text="uid=")],
      hints=["id > sagesse.txt", "Transparence totale devant les sages."],
      solution="id > sagesse.txt"),

    L(293, "Les conseils",
      story="Troisieme epreuve : 'Quels conseils (groupes) frequente-tu ?' Les sages veulent connaitre "
            "tes influences. Liste dans conseils.txt.",
      lesson="'groups' : tes influences. On est la somme de ses groupes, disent les sages. "
             "Frequente 'sudo', 'docker', 'adm' : tu grandiras. Frequente 'visiteurs' : tu resteras petit.",
      mission="Liste tes groupes dans conseils.txt : groups > conseils.txt",
      checks=[C_fe("conseils.txt"), C_nempty("conseils.txt")],
      hints=["groups > conseils.txt", "Dis-moi qui tu frequentes..."],
      solution="groups > conseils.txt"),

    L(294, "L'assemblee",
      story="Quatrieme epreuve : 'Qui siege en ce moment ?' Fais l'appel de l'assemblee des connectes "
            "avec 'who' dans assemblee.txt.",
      lesson="'who' : l'appel de l'assemblee. Les sages savent toujours qui siege. "
             "Un admin qui ignore qui est connecte est un aveugle au milieu de la place.",
      mission="Liste les utilisateurs connectes dans assemblee.txt : who > assemblee.txt",
      checks=[C_fe("assemblee.txt"), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
      hints=["who > assemblee.txt", "Qui siege ? Fais l'appel."],
      solution="who > assemblee.txt"),

    L(295, "Le siege numero...",
      story="Cinquieme epreuve : 'Quel est ton siege ?' Chaque sage a un numero grave dans la pierre : "
            "ton uid, dans siege.txt.",
      lesson="'id -u' : ton siege grave dans la pierre. Les numeros ne mentent pas, ne changent pas, "
             "ne se volent pas. Ton siege t'attendait depuis la creation du compte.",
      mission="Enregistre ton uid dans siege.txt : id -u > siege.txt",
      checks=[C_fe("siege.txt"), C_fc("siege.txt", regex=r"\d+")],
      hints=["id -u > siege.txt", "Ton siege, grave dans la pierre."],
      solution="id -u > siege.txt"),

    L(296, "Le decret personnel",
      story="Sixieme epreuve : 'Montre-nous ton decret.' Ton decret dort dans /etc/passwd : "
            "extrais ta ligne dans decret.txt et lis-la aux sages.",
      lesson="Ton decret : ta ligne de /etc/passwd. 'grep \"^$(whoami):\"' l'extrait des archives. "
             "Lis-le a voix haute : nom, uid, dossier, shell. Les sages ecoutent.",
      mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > decret.txt",
      checks=[C_fe("decret.txt"), C_fc("decret.txt", text=":")],
      hints=["grep \"^$(whoami):\" /etc/passwd > decret.txt", "Lis ton decret a voix haute."],
      solution="grep \"^$(whoami):\" /etc/passwd > decret.txt"),

    L(297, "Le denombrement",
      story="Septieme epreuve : 'Combien d'ames ?' Denombre TOUS les comptes du systeme dans sages-total.txt. "
            "Les sages comptent sur toi. Sans jeu de mots. Bon, un peu.",
      lesson="'wc -l < /etc/passwd' : le denombrement sacre. Toutes les ames, humaines et systeme. "
             "Les sages aiment les chiffres exacts. Toi aussi, maintenant.",
      mission="Compte les comptes du systeme : wc -l < /etc/passwd > sages-total.txt",
      checks=[C_fe("sages-total.txt"), C_fc("sages-total.txt", regex=r"\d+")],
      hints=["wc -l < /etc/passwd > sages-total.txt", "Les sages comptent sur toi."],
      solution="wc -l < /etc/passwd > sages-total.txt"),

    L(298, "Les tablettes sacrees",
      story="Huitieme epreuve : 'Montre-nous les tablettes.' Les tablettes sacrees (/etc/passwd) : "
            "proprietaire, droits. Les sages verifient TOUT.",
      lesson="'ls -l /etc/passwd' : presenter les tablettes sacrees. Gardien root, droits stricts : "
             "les sages hochent la tete. Une tablette mal gardee, et c'est l'exil (ou pire : Kevin).",
      mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
      checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
      hints=["ls -l /etc/passwd", "Les sages verifient TOUT."],
      solution="ls -l /etc/passwd"),

    L(299, "Le baton de pouvoir",
      story="Neuvieme epreuve : 'Ou est le baton de pouvoir ?' Le baton 'sudo' : localise-le sans le toucher. "
            "Les sages n'accordent le baton qu'aux meritants. Bientot, toi...",
      lesson="'command -v sudo' : designer le baton sans le toucher. Les meritants l'utiliseront un jour. "
             "Toi, dans quelques blocs, quand tu seras pret. Les sages te regardent...",
      mission="Localise la commande sudo : command -v sudo",
      checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
      hints=["command -v sudo", "Designe le baton. Ne le touche pas. Encore."],
      solution="command -v sudo"),

    L(300, "BOSS FINAL : l'archimage",
      story="Derniere epreuve : contempler la fiche de l'archimage supreme : root, uid 0. "
            "Archive sa fiche dans archimage.txt. Les sages se levent : 'Tu connais desormais les habitants du systeme. "
            "Le bloc Utilisateurs est clos.'",
      lesson="BOSS final : 'id root'. 100 niveaux sur les utilisateurs derriere toi : whoami, id, groups, who, "
             "passwd, sudo, root. Tu sais QUI vit dans un systeme Linux. Et c'est le debut de la sagesse.",
      mission="Enregistre l'identite de root dans archimage.txt : id root > archimage.txt",
      checks=[C_fe("archimage.txt"), C_fc("archimage.txt", text="uid=0")],
      hints=["id root > archimage.txt", "Contemple l'archimage. Puis repose-toi : demain, les archives !"],
      solution="id root > archimage.txt",
      xp=25, boss=True),
]
