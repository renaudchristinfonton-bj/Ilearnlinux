"""Jours 11-100 (niveaux 101-1000) : 900 niveaux jouables generes a partir de modeles.

Chaque bloc de 10 jours = 100 niveaux construits sur ~10 modeles varies
(noms, nombres, cibles differents). Tous sont auto-verifies, sans droits root
et sans toucher au systeme : tout se passe dans l'arene, et les commandes
systeme utilisees sont en lecture seule.

Blocs :
  101-200 : permissions, droits, liens (jours 11-20)
  201-300 : utilisateurs, groupes, identites (jours 21-30)
  301-400 : archives et compression (jours 31-40)
  401-500 : systeme et materiel en lecture seule (jours 41-50)
  501-600 : processus et taches de fond (jours 51-60)
  601-700 : reseau local (jours 61-70)
  701-800 : cles SSH et copies (jours 71-80)
  801-900 : scripting shell (jours 81-90)
  901-1000 : admin pro + MEGA-BOSS final (jours 91-100)
"""

from .common import (
    L, F, D, C_cmd, C_fe, C_de, C_ne, C_fc, C_eq, C_nempty,
    C_perm, C_exe, C_sym,
)

MODES_NUM = ["644", "600", "640", "755", "700", "750", "664", "444", "775", "711"]
OPS_SYMBOLIC = [
    ("644", "u+x", "755"), ("777", "o-w", "775"), ("777", "g-w", "757"),
    ("755", "o-x", "754"), ("600", "g+r", "640"), ("640", "o+r", "644"),
    ("777", "a-x", "666"), ("666", "u+x", "766"), ("755", "g-x", "745"),
    ("700", "o+rx", "705"),
]
FRUITS = ["pomme", "banane", "cerise", "mangue", "orange", "kiwi",
          "ananas", "fraise", "citron", "pasteque"]


def _bossify(level):
    lid = level["id"]
    if lid == 1000:
        return level
    if lid % 10 == 0:
        level["xp"] = 25
        level["boss"] = True
        level["title"] = "BOSS : " + level["title"]
    return level


# ---------------------------------------------------------------- Bloc B : permissions
def _block_b():
    levels = []
    for n in range(100):
        lid = 101 + n
        t, k = n % 10, n // 10
        if t == 0:
            s = "lance-{}.sh".format(k)
            levels.append(L(lid, "Rendre executable : {}".format(s),
                lesson="Un fichier texte ne s'execute pas seul : il faut le droit 'x' (execute). "
                       "'chmod +x script.sh' donne ce droit, puis './script.sh' le lance.",
                mission="Rends {} executable avec chmod +x.".format(s),
                setup=[F(s, "#!/bin/bash\necho mission-ok\n")],
                checks=[C_exe(s)],
                hints=["chmod +x {}".format(s), "'x' = droit d'execution."],
                solution="chmod +x {}".format(s),
                story="Ce script contient un sort puissant, mais Linux refuse de le lancer : droit 'x' manquant."))
        elif t == 1:
            f = "doc-{}.txt".format(k)
            mode = MODES_NUM[k]
            levels.append(L(lid, "chmod {} sur {}".format(mode, f),
                lesson="Permissions numeriques : 3 chiffres = droits du proprietaire, du groupe, des autres. "
                       "4=lecture, 2=ecriture, 1=execution. 7=tout, 6=lecture+ecriture, 5=lecture+execution.",
                mission="Donne les permissions {} a {} avec chmod.".format(mode, f),
                setup=[F(f, "contenu\n")],
                checks=[C_perm(f, mode)],
                hints=["chmod {} {}".format(mode, f), "Verifie avec ls -l."],
                solution="chmod {} {}".format(mode, f),
                story="Chaque fichier a ses gardes du corps : les permissions. Regle-les au chiffre exact."))
        elif t == 2:
            f = "outil-{}.sh".format(k)
            levels.append(L(lid, "chmod u+x : {}".format(f),
                lesson="En symbolique : u=proprietaire, g=groupe, o=autres, a=tous. '+' ajoute, '-' retire. "
                       "'u+x' = le proprietaire gagne l'execution (644 devient 755).",
                mission="Ajoute l'execution au proprietaire de {} : chmod u+x {} (644 -> 755).".format(f, f),
                setup=[F(f, "x\n", mode="644")],
                checks=[C_perm(f, "755")],
                hints=["chmod u+x {}".format(f), "u=user (proprietaire), +x=ajouter l'execution."],
                solution="chmod u+x {}".format(f)))
        elif t == 3:
            start, op, end = OPS_SYMBOLIC[k]
            f = "fichier-{}.txt".format(k)
            levels.append(L(lid, "chmod {} : {} -> {}".format(op, start, end),
                mission="Applique '{}' a {} (droits actuels : {}). Resultat attendu : {}.".format(op, f, start, end),
                lesson="u/g/o/a + '+-=' + r/w/x : la grammaire complete des droits. Lis l'operation comme une phrase : "
                       "'{}' sur '{}'.".format(op, start),
                setup=[F(f, "x\n", mode=start)],
                checks=[C_perm(f, end)],
                hints=["chmod {} {}".format(op, f), "Verifie avec ls -l : tu dois obtenir {}.".format(end)],
                solution="chmod {} {}".format(op, f)))
        elif t == 4:
            d = "projet-{}".format(k)
            levels.append(L(lid, "chmod -R 755 : {}/".format(d),
                lesson="'chmod -R' applique les droits RECURSIVEMENT : le dossier et tout son contenu. "
                       "Indispensable apres une copie qui a casse les droits.",
                mission="Applique 755 a {}/ et tout son contenu : chmod -R 755 {}".format(d, d),
                setup=[D(d), D(d + "/src"), F(d + "/lisez.txt", "x\n"), F(d + "/src/code.txt", "x\n")],
                checks=[C_perm(d, "755"), C_perm(d + "/src/code.txt", "755")],
                hints=["chmod -R 755 {}".format(d), "-R = recursif : tout l'arbre y passe."],
                solution="chmod -R 755 {}".format(d),
                story="Une copie a tout casse : les droits sont en vrac dans {}. Repare tout d'un coup.".format(d)))
        elif t == 5:
            s = "run-{}.sh".format(k)
            r = "sortie-{}.txt".format(k)
            levels.append(L(lid, "Lancer {}".format(s),
                lesson="Lancer un script : 1) chmod +x, 2) ./script.sh. Le './' dit 'ici, dans ce dossier' : "
                       "par securite, Linux n'execute jamais un programme du dossier courant sans chemin explicite.",
                mission="Rends {} executable puis lance-le en sauvant sa sortie dans {} : ./{} > {}".format(s, r, s, r),
                setup=[F(s, "#!/bin/bash\necho reussi\n")],
                checks=[C_exe(s), C_fc(r, text="reussi")],
                hints=["1) chmod +x {}".format(s), "2) ./{} > {}".format(s, r)],
                solution="chmod +x {} && ./{} > {}".format(s, s, r)))
        elif t == 6:
            f = "cible-{}.txt".format(k)
            r = "droits-{}.txt".format(k)
            levels.append(L(lid, "Lire les droits de {}".format(f),
                lesson="'ls -l' affiche les droits style '-rwxr-xr-x' : 1er caractere = type (- fichier, d dossier), "
                       "puis 3x3 lettres rwx pour u/g/o.",
                mission="Enregistre les details de {} dans {} : ls -l {} > {}".format(f, r, f, r),
                setup=[F(f, "x\n")],
                checks=[C_fe(r), C_fc(r, text=f)],
                hints=["ls -l {} > {}".format(f, r), "La ligne detaillee contient le nom du fichier."],
                solution="ls -l {} > {}".format(f, r)))
        elif t == 7:
            d = "prive-{}".format(k)
            levels.append(L(lid, "Coffre-fort {}/ (700)".format(d),
                lesson="'700' = seul le proprietaire peut tout faire (rwx------). Le mode des dossiers secrets : "
                       "~/.ssh est en 700, par exemple.",
                mission="Cree le dossier {} et mets-le en 700.".format(d),
                checks=[C_de(d), C_perm(d, "700")],
                hints=["1) mkdir {}".format(d), "2) chmod 700 {}".format(d)],
                solution="mkdir {} && chmod 700 {}".format(d, d),
                story="Tu dois cacher des documents ultra-secrets. Construis un coffre-fort numerique."))
        elif t == 8:
            f = "secret-{}.txt".format(k)
            levels.append(L(lid, "Secret {} (600)".format(f),
                lesson="'600' = seul le proprietaire lit et ecrit (rw-------). Le mode des fichiers sensibles : "
                       "cles privees, mots de passe, tokens.",
                mission="Cree {} avec un mot secret dedans, en 600.".format(f),
                checks=[C_fe(f), C_perm(f, "600"), C_nempty(f)],
                hints=["echo ... > ... puis chmod 600 ...",
                       "Modele : echo s3cret-{} > {} && chmod 600 {}".format(k, f, f)],
                solution="echo s3cret-{} > {} && chmod 600 {}".format(k, f, f)))
        else:
            c = "cible-{}.txt".format(k)
            l = "lien-{}".format(k)
            levels.append(L(lid, "Raccourci : {} -> {}".format(l, c),
                lesson="'ln -s cible lien' cree un LIEN SYMBOLIQUE : un raccourci vers un autre fichier. "
                       "Tres utilise pour configs et versions (/usr/bin/python -> python3).",
                mission="Cree un lien {} vers {} : ln -s {} {}".format(l, c, c, l),
                setup=[F(c, "contenu\n")],
                checks=[C_sym(l, c)],
                hints=["ln -s {} {}".format(c, l), "ln -s = LiNk Symbolique."],
                solution="ln -s {} {}".format(c, l)))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc C : utilisateurs / groupes
def _block_c():
    levels = []
    for n in range(100):
        lid = 201 + n
        t, k = n % 10, n // 10
        if t == 0:
            r = "moi-{}.txt".format(k)
            levels.append(L(lid, "Carte d'identite : {}".format(r),
                lesson="'whoami' affiche ton identifiant. L'enregistrer garde une trace : les scripts d'audit "
                       "notent QUI a fait QUOI.",
                mission="Enregistre ton nom d'utilisateur dans {} : whoami > {}".format(r, r),
                checks=[C_fe(r), C_nempty(r)],
                hints=["whoami > {}".format(r), "whoami affiche, > sauve."],
                solution="whoami > {}".format(r)))
        elif t == 1:
            r = "identite-{}.txt".format(k)
            levels.append(L(lid, "Identite complete : {}".format(r),
                lesson="'id' affiche uid, gid et tous tes groupes. uid 0 = root, le super-utilisateur tout-puissant.",
                mission="Enregistre ton identite complete dans {} : id > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="uid=")],
                hints=["id > {}".format(r), "La sortie de id contient toujours 'uid='."],
                solution="id > {}".format(r)))
        elif t == 2:
            r = "groupes-{}.txt".format(k)
            levels.append(L(lid, "Tes groupes : {}".format(r),
                lesson="'groups' liste tes groupes. Les groupes donnent des droits : 'sudo' permet d'administrer, "
                       "'docker' de piloter Docker...",
                mission="Liste tes groupes dans {} : groups > {}".format(r, r),
                checks=[C_fe(r), C_nempty(r)],
                hints=["groups > {}".format(r), "Chaque groupe = des droits en plus."],
                solution="groups > {}".format(r)))
        elif t == 3:
            r = "connectes-{}.txt".format(k)
            levels.append(L(lid, "Qui est connecte ? ({})".format(r),
                lesson="'who' montre les utilisateurs connectes a la machine. Sur un serveur, c'est la premiere chose "
                       "a regarder quand 'quelque chose cloche'.",
                mission="Liste les utilisateurs connectes dans {} : who > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"(^|[;&|]\s*)\bwho\b")],
                hints=["who > {}".format(r), "who = qui est la ?"],
                solution="who > {}".format(r),
                story="Il se passe des choses bizarres sur le serveur... Qui est connecte en ce moment ?"))
        elif t == 4:
            r = "uid-{}.txt".format(k)
            levels.append(L(lid, "Ton numero : {}".format(r),
                lesson="'id -u' donne juste ton numero (uid). Les scripts testent souvent : 'si uid == 0, je suis root'.",
                mission="Enregistre ton uid dans {} : id -u > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, regex=r"\d+")],
                hints=["id -u > {}".format(r), "Un uid est un nombre."],
                solution="id -u > {}".format(r)))
        elif t == 5:
            r = "maligne-{}.txt".format(k)
            levels.append(L(lid, "Ta fiche annuaire : {}".format(r),
                lesson="'/etc/passwd' contient la fiche de chaque utilisateur. Lisible par tous, c'est l'annuaire du systeme. "
                       "'$(whoami)' est remplace par ton nom avant execution.",
                mission="Extrait ta ligne de l'annuaire : grep \"^$(whoami):\" /etc/passwd > {}".format(r),
                checks=[C_fe(r), C_fc(r, text=":")],
                hints=["grep \"^$(whoami):\" /etc/passwd > {}".format(r),
                       "$(whoami) devient ton nom d'utilisateur."],
                solution="grep \"^$(whoami):\" /etc/passwd > {}".format(r)))
        elif t == 6:
            r = "nb-comptes-{}.txt".format(k)
            levels.append(L(lid, "Recensement : {}".format(r),
                lesson="Une ligne de /etc/passwd = un compte (y compris les comptes systeme jamais connectes). "
                       "'wc -l' les compte tous.",
                mission="Compte les comptes du systeme : wc -l < /etc/passwd > {}".format(r),
                checks=[C_fe(r), C_fc(r, regex=r"\d+")],
                hints=["wc -l < /etc/passwd > {}".format(r), "< envoie le fichier a wc, > sauve le chiffre."],
                solution="wc -l < /etc/passwd > {}".format(r),
                story="L'auditeur veut le nombre EXACT de comptes. Recense, et prouve avec le fichier."))
        elif t == 7:
            levels.append(L(lid, "Qui possede l'annuaire ? (enquete {})".format(k + 1),
                lesson="'ls -l /etc/passwd' montre proprietaire et droits de l'annuaire. Les fichiers systeme "
                       "appartiennent a root : c'est lui le patron.",
                mission="Affiche les details de /etc/passwd : ls -l /etc/passwd",
                checks=[C_cmd(r"\bls\b[^\n]*-l[^\n]*passwd")],
                hints=["ls -l /etc/passwd", "Regarde le proprietaire : c'est root."],
                solution="ls -l /etc/passwd"))
        elif t == 8:
            levels.append(L(lid, "Le passe-partout sudo (exercice {})".format(k + 1),
                lesson="'sudo' execute UNE commande en root. 'command -v sudo' dit OU il est. "
                       "Dans ce jeu, jamais besoin de sudo : tout se passe dans l'arene.",
                mission="Localise la commande sudo : command -v sudo",
                checks=[C_cmd(r"\bcommand\b[^\n]*-v[^\n]*\bsudo\b")],
                hints=["command -v sudo", "command -v = 'ou es-tu ?' pour une commande."],
                solution="command -v sudo"))
        else:
            r = "root-{}.txt".format(k)
            levels.append(L(lid, "Fiche de root : {}".format(r),
                lesson="'id root' affiche l'identite du super-utilisateur : uid=0, gid=0. Le zero, c'est le grade : "
                       "root peut tout faire, meme casser le systeme.",
                mission="Enregistre l'identite de root dans {} : id root > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="uid=0")],
                hints=["id root > {}".format(r), "root a toujours uid=0."],
                solution="id root > {}".format(r),
                story="Tu veux savoir a quoi ressemble le patron ? Voici sa fiche d'identite. Impressionnant, non ?"))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc D : archives / compression
def _block_d():
    levels = []
    for n in range(100):
        lid = 301 + n
        t, k = n % 10, n // 10
        f1 = "page1-{}.txt".format(k)
        f2 = "page2-{}.txt".format(k)
        if t == 0:
            a = "docs-{}.tar".format(k)
            levels.append(L(lid, "Paquet {}".format(a),
                lesson="'tar -cf archive.tar fichiers' emballe plusieurs fichiers en UN seul (c=create, f=file). "
                       "Le demenagement version Linux.",
                mission="Emballe {} et {} dans {} : tar -cf {} {} {}".format(f1, f2, a, a, f1, f2),
                setup=[F(f1, "page un\n"), F(f2, "page deux\n")],
                checks=[C_fe(a), C_nempty(a)],
                hints=["tar -cf {} {} {}".format(a, f1, f2), "c=creer, f=l'archive juste apres."],
                solution="tar -cf {} {} {}".format(a, f1, f2)))
        elif t == 1:
            a = "colis-{}.tar".format(k)
            r = "contenu-{}.txt".format(k)
            levels.append(L(lid, "Regarder sans ouvrir : {}".format(a),
                lesson="'tar -tf archive' LISTE le contenu sans extraire (t=list). On regarde dans le colis "
                       "sans le decacheter.",
                mission="Cree {} avec {} et {}, puis liste son contenu dans {}.".format(a, f1, f2, r),
                setup=[F(f1, "un\n"), F(f2, "deux\n")],
                checks=[C_fe(a), C_fe(r), C_fc(r, text=f1)],
                hints=["1) tar -cf {} {} {}".format(a, f1, f2), "2) tar -tf {} > {}".format(a, r)],
                solution="tar -cf {} {} {} && tar -tf {} > {}".format(a, f1, f2, a, r)))
        elif t == 2:
            a = "presse-{}.tar.gz".format(k)
            levels.append(L(lid, "Compresser : {}".format(a),
                lesson="'tar -czf' emballe ET compresse avec gzip (z=gzip). Le .tar.gz : format d'echange n°1 du monde Linux.",
                mission="Emballe et compresse {} et {} dans {} : tar -czf ...".format(f1, f2, a),
                setup=[F(f1, "un\n"), F(f2, "deux\n")],
                checks=[C_fe(a), C_nempty(a)],
                hints=["tar -czf {} {} {}".format(a, f1, f2), "z = compresser avec gzip."],
                solution="tar -czf {} {} {}".format(a, f1, f2)))
        elif t == 3:
            f = "note-{}.txt".format(k)
            a = "note-{}.tar.gz".format(k)
            levels.append(L(lid, "Sauvetage : {}".format(a),
                lesson="'tar -xzf archive' EXTRAIT le contenu (x=extract). Boucle complete de la sauvegarde : "
                       "archiver, supprimer l'original, re-extraire.",
                mission="Archive {} dans {}, supprime {}, puis re-extrais-le. {} doit exister a nouveau.".format(f, a, f, f),
                setup=[F(f, "precious\n")],
                checks=[C_fe(a), C_fe(f), C_fc(f, text="precious")],
                hints=["1) tar -czf {} {}".format(a, f), "2) rm {}".format(f), "3) tar -xzf {}".format(a)],
                solution="tar -czf {} {} && rm {} && tar -xzf {}".format(a, f, f, a),
                story="Exercice de catastrophe : si {} brulait, pourrais-tu le ressusciter depuis l'archive ?".format(f)))
        elif t == 4:
            f = "fichier-{}.txt".format(k)
            levels.append(L(lid, "Presser : {}".format(f),
                lesson="'gzip fichier' compresse ET supprime l'original (remplace par .gz). Pour garder l'original : "
                       "'gzip -k' (keep).",
                mission="Compresse {} avec gzip (l'original disparait, le .gz apparait).".format(f),
                setup=[F(f, "bla bla\n" * 50)],
                checks=[C_fe(f + ".gz"), C_ne(f)],
                hints=["gzip {}".format(f), "gzip remplace le fichier par sa version .gz."],
                solution="gzip {}".format(f)))
        elif t == 5:
            f = "lettre-{}.txt".format(k)
            levels.append(L(lid, "Decompresser : {}.gz".format(f),
                lesson="'gunzip fichier.gz' (ou 'gzip -d') restaure l'original et supprime le .gz. L'aller-retour parfait.",
                mission="Compresse {} puis decompresse-le : {} doit exister avec son contenu.".format(f, f),
                setup=[F(f, "cher journal\n")],
                checks=[C_fe(f), C_fc(f, text="cher journal"), C_ne(f + ".gz")],
                hints=["1) gzip {}".format(f), "2) gunzip {}.gz".format(f)],
                solution="gzip {} && gunzip {}.gz".format(f, f)))
        elif t == 6:
            r = "taille-{}.txt".format(k)
            levels.append(L(lid, "Peser l'arene : {}".format(r),
                lesson="'du -sb .' donne la taille TOTALE du dossier en octets (s=summary, b=bytes). "
                       "Quand le disque est plein, du trouve les gloutons.",
                mission="Pese l'arene en octets dans {} : du -sb . > {}".format(r, r),
                setup=[F("x.txt", "x\n")],
                checks=[C_fe(r), C_fc(r, regex=r"\d+")],
                hints=["du -sb . > {}".format(r), "du=disk usage, s=total, b=octets."],
                solution="du -sb . > {}".format(r)))
        elif t == 7:
            a = "colisd-{}.tar".format(k)
            r = "details-{}.txt".format(k)
            levels.append(L(lid, "Fiche colis : {}".format(a),
                lesson="'tar -tvf' liste AVEC details (droits, tailles, dates). Le bordereau du colis.",
                mission="Cree {} avec {} et {}, puis liste ses details dans {}.".format(a, f1, f2, r),
                setup=[F(f1, "un\n"), F(f2, "deux\n")],
                checks=[C_fe(r), C_fc(r, text=f1)],
                hints=["1) tar -cf {} {} {}".format(a, f1, f2), "2) tar -tvf {} > {}".format(a, r)],
                solution="tar -cf {} {} {} && tar -tvf {} > {}".format(a, f1, f2, a, r)))
        elif t == 8:
            f = "garde-{}.txt".format(k)
            levels.append(L(lid, "Compresser sans perdre : {}".format(f),
                lesson="'gzip -k' (keep) compresse en GARDANT l'original. On obtient le fichier ET son .gz. "
                       "La prudence, toujours.",
                mission="Compresse {} en gardant l'original : gzip -k {}".format(f, f),
                setup=[F(f, "important\n")],
                checks=[C_fe(f), C_fe(f + ".gz")],
                hints=["gzip -k {}".format(f), "-k = keep (garder)."],
                solution="gzip -k {}".format(f)))
        else:
            f = "gros-{}.txt".format(k)
            r = "tailles-{}.txt".format(k)
            levels.append(L(lid, "Avant/apres compression : {}".format(f),
                lesson="Un texte repetitif se compresse enormement (10x, 100x !). C'est pour ca qu'on compresse les logs.",
                mission="Compresse {} (en gardant l'original) puis liste les deux tailles dans {} : gzip -k ... && ls -lh {}* > {}".format(f, r, f, r),
                setup=[F(f, "aaaaaaaaaaaaaaaa\n" * 200)],
                checks=[C_fe(f + ".gz"), C_fe(r), C_fc(r, text=f)],
                hints=["1) gzip -k {}".format(f), "2) ls -lh {}* > {}".format(f, r)],
                solution="gzip -k {} && ls -lh {}* > {}".format(f, f, r),
                story="Ce fichier est enorme mais plein de repetitions. Presse-le et admire la difference."))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc E : systeme / materiel
def _block_e():
    levels = []
    for n in range(100):
        lid = 401 + n
        t, k = n % 10, n // 10
        if t == 0:
            r = "noyau-{}.txt".format(k)
            levels.append(L(lid, "Version du noyau : {}".format(r),
                lesson="'uname -r' donne la version du NOYAU Linux (le coeur du systeme). Pour savoir si on peut "
                       "installer tel pilote ou telle fonctionnalite.",
                mission="Enregistre la version du noyau dans {} : uname -r > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text=".")],
                hints=["uname -r > {}".format(r), "Une version contient toujours des points."],
                solution="uname -r > {}".format(r)))
        elif t == 1:
            r = "machine-{}.txt".format(k)
            levels.append(L(lid, "Nom de la machine : {}".format(r),
                lesson="'hostname' affiche le nom de la machine. Sur un parc de 50 serveurs, c'est comme ca qu'on sait "
                       "OU on est connecte.",
                mission="Enregistre le nom de la machine dans {} : hostname > {}".format(r, r),
                checks=[C_fe(r), C_nempty(r)],
                hints=["hostname > {}".format(r), "hostname = le badge de la machine."],
                solution="hostname > {}".format(r)))
        elif t == 2:
            r = "arch-{}.txt".format(k)
            levels.append(L(lid, "Architecture : {}".format(r),
                lesson="'uname -m' donne l'architecture (x86_64, aarch64...). Pour telecharger le bon programme : "
                       "un binaire ARM ne tourne pas sur Intel.",
                mission="Enregistre l'architecture dans {} : uname -m > {}".format(r, r),
                checks=[C_fe(r), C_nempty(r)],
                hints=["uname -m > {}".format(r), "m = machine (architecture)."],
                solution="uname -m > {}".format(r)))
        elif t == 3:
            r = "disques-{}.txt".format(k)
            levels.append(L(lid, "Espace disque : {}".format(r),
                lesson="'df -h' montre l'espace libre de chaque disque (h=humain : G, M). Le 'plus jamais a court de place' "
                       "commence par un df regulier.",
                mission="Enregistre l'etat des disques dans {} : df -h > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="%")],
                hints=["df -h > {}".format(r), "df affiche toujours une colonne de pourcentages."],
                solution="df -h > {}".format(r),
                story="Le disque systeme se remplit... Fais un etat des lieux avant la panne."))
        elif t == 4:
            r = "systeme-{}.txt".format(k)
            levels.append(L(lid, "Carte du systeme : {}".format(r),
                lesson="'/etc/os-release' est la carte d'identite de la distribution (Ubuntu, Debian...). "
                       "Tous les scripts serieux la lisent pour s'adapter.",
                mission="Copie la carte d'identite dans {} : cat /etc/os-release > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="NAME")],
                hints=["cat /etc/os-release > {}".format(r), "Le fichier contient toujours une ligne NAME=...."],
                solution="cat /etc/os-release > {}".format(r)))
        elif t == 5:
            r = "charge-{}.txt".format(k)
            levels.append(L(lid, "Depuis quand ca tourne ? ({})".format(r),
                lesson="'uptime' dit depuis quand la machine tourne et sa charge. Un serveur qui tourne depuis 900 jours "
                       "sans reboot : fierte de l'admin.",
                mission="Enregistre l'uptime dans {} : uptime > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"(^|[;&|]\s*)\buptime\b")],
                hints=["uptime > {}".format(r), "uptime = temps de fonctionnement."],
                solution="uptime > {}".format(r)))
        elif t == 6:
            r = "memoire-{}.txt".format(k)
            levels.append(L(lid, "Memoire vive : {}".format(r),
                lesson="'free -h' montre la RAM totale, utilisee, libre. Quand une machine rame, free est le premier "
                       "temoin a interroger.",
                mission="Enregistre l'etat de la memoire dans {} : free -h > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bfree\b")],
                hints=["free -h > {}".format(r), "free = memoire libre."],
                solution="free -h > {}".format(r),
                story="La machine rame... Premier reflexe : verifier la memoire. Fais ton rapport."))
        elif t == 7:
            r = "cpu-{}.txt".format(k)
            levels.append(L(lid, "Fiche processeur : {}".format(r),
                lesson="'lscpu' detaille le processeur : modele, coeurs, threads. Pour savoir si la machine peut "
                       "encaisser la charge.",
                mission="Enregistre la fiche CPU dans {} : lscpu > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="CPU")],
                hints=["lscpu > {}".format(r), "ls + cpu : lister le processeur."],
                solution="lscpu > {}".format(r)))
        elif t == 8:
            r = "blocs-{}.txt".format(k)
            levels.append(L(lid, "Disques et partitions : {}".format(r),
                lesson="'lsblk' dessine l'arbre des disques et partitions (sda, sda1...). La carte du stockage, "
                       "indispensable avant de toucher aux partitions.",
                mission="Enregistre la carte des disques dans {} : lsblk > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="NAME")],
                hints=["lsblk > {}".format(r), "blk = block devices (disques)."],
                solution="lsblk > {}".format(r)))
        else:
            r = "version-{}.txt".format(k)
            levels.append(L(lid, "Acte de naissance : {}".format(r),
                lesson="'/proc/version' contient la version exacte du noyau. /proc est un dossier magique : "
                       "il n'existe pas sur disque, le noyau l'invente en direct.",
                mission="Copie l'acte de naissance dans {} : cat /proc/version > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="Linux")],
                hints=["cat /proc/version > {}".format(r), "/proc = fenetre sur le noyau vivant."],
                solution="cat /proc/version > {}".format(r)))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc F : processus
def _block_f():
    levels = []
    for n in range(100):
        lid = 501 + n
        t, k = n % 10, n // 10
        if t == 0:
            r = "processus-{}.txt".format(k)
            levels.append(L(lid, "Qui tourne ? ({})".format(r),
                lesson="'ps aux' photographie TOUS les processus : programmes en cours, leur PID (numero), leur consommation. "
                       "La radio du systeme.",
                mission="Photographie les processus dans {} : ps aux > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="PID")],
                hints=["ps aux > {}".format(r), "La premiere ligne contient toujours 'PID'."],
                solution="ps aux > {}".format(r)))
        elif t == 1:
            r = "proc-{}.txt".format(k)
            levels.append(L(lid, "Autre angle : {}".format(r),
                lesson="'ps -ef' est la variante classique (style UNIX) : UID, PID, PPID (parent)... Deux syntaxes, "
                       "meme metier : voir ce qui tourne.",
                mission="Liste les processus style UNIX dans {} : ps -ef > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="UID")],
                hints=["ps -ef > {}".format(r), "Le header contient 'UID'."],
                solution="ps -ef > {}".format(r)))
        elif t == 2:
            r = "jobs-{}.txt".format(k)
            levels.append(L(lid, "Taches de fond : {}".format(r),
                lesson="'commande &' lance en ARRIERE-PLAN (tu recuperes la main). 'jobs' liste tes taches de fond. "
                       "Le multitache du terminal.",
                mission="Lance 'sleep 30' en fond puis liste tes jobs dans {} : sleep 30 & puis jobs > {}".format(r, r),
                checks=[C_cmd(r"\bsleep\b[^\n]*&"), C_fe(r), C_fc(r, text="sleep")],
                hints=["1) sleep 30 &", "2) jobs > {}".format(r)],
                solution="sleep 30 & jobs > {}".format(r),
                story="Tu dois attendre 30 secondes... mais pas question de rester bloque : envoie ca en fond."))
        elif t == 3:
            p = "pid-{}.txt".format(k)
            levels.append(L(lid, "Numero de tache : {}".format(p),
                lesson="'$!' contient le PID de la derniere tache lancee en fond. 'echo $!' juste apres le '&' : "
                       "tu connais son numero, tu peux la piloter.",
                mission="Lance 'sleep 25' en fond puis sauve son PID dans {} : sleep 25 & puis echo $! > {}".format(p, p),
                checks=[C_cmd(r"\bsleep\b[^\n]*&"), C_fe(p), C_fc(p, regex=r"\d+")],
                hints=["1) sleep 25 &", "2) echo $! > {}".format(p)],
                solution="sleep 25 & echo $! > {}".format(p)))
        elif t == 4:
            p = "pid-{}.txt".format(k)
            levels.append(L(lid, "Mission elimination (PID dans {})".format(p),
                lesson="'kill PID' demande poliment a un processus de s'arreter. Pour TES propres sleep, pas besoin de sudo. "
                       "(kill -9, c'est la maniere forte : on verra plus tard.)",
                mission="Lance 'sleep 25' en fond, sauve son PID dans {}, puis tue-le avec kill $(cat {}).".format(p, p),
                checks=[C_fe(p), C_cmd(r"\bkill\b")],
                hints=["1) sleep 25 & echo $! > {}".format(p), "2) kill $(cat {})".format(p)],
                solution="sleep 25 & echo $! > {} && kill $(cat {})".format(p, p),
                story="Un processus s'est emballe (c'est toi qui l'as lance, chut). Elimine-le proprement."))
        elif t == 5:
            r = "trouve-{}.txt".format(k)
            levels.append(L(lid, "Chasseur de processus : {}".format(r),
                lesson="'pgrep -f motif' donne les PID des processus qui matchent. Plus propre que 'ps aux | grep' "
                       "(qui se trouve lui-meme, le maladroit).",
                mission="Lance 'sleep 25' en fond puis retrouve son PID : sleep 25 & puis pgrep -f \"sleep 25\" > {}".format(r),
                checks=[C_fe(r), C_fc(r, regex=r"\d+")],
                hints=["1) sleep 25 &", "2) pgrep -f \"sleep 25\" > {}".format(r)],
                solution="sleep 25 & pgrep -f \"sleep 25\" > {}".format(r)))
        elif t == 6:
            r = "jobs-l-{}.txt".format(k)
            levels.append(L(lid, "Jobs detailles : {}".format(r),
                lesson="'jobs -l' (long) affiche les jobs AVEC leurs PID. Le meilleur des deux mondes : noms + numeros.",
                mission="Lance 'sleep 25' en fond puis jobs -l dans {} : sleep 25 & puis jobs -l > {}".format(r, r),
                checks=[C_cmd(r"\bsleep\b[^\n]*&"), C_fe(r), C_fc(r, text="sleep")],
                hints=["1) sleep 25 &", "2) jobs -l > {}".format(r)],
                solution="sleep 25 & jobs -l > {}".format(r)))
        elif t == 7:
            p = "pid-{}.txt".format(k)
            r = "etat-{}.txt".format(k)
            levels.append(L(lid, "Dossier du suspect : {}".format(r),
                lesson="'ps -p PID' affiche UN processus precis. Ideal pour surveiller : 'il tourne toujours ? "
                       "combien il consomme ?'",
                mission="Lance 'sleep 25' en fond, sauve son PID dans {}, puis affiche sa fiche dans {} : ps -p $(cat {}) > {}".format(p, r, p, r),
                checks=[C_fe(r), C_fc(r, text="sleep")],
                hints=["1) sleep 25 & echo $! > {}".format(p), "2) ps -p $(cat {}) > {}".format(p, r)],
                solution="sleep 25 & echo $! > {} && ps -p $(cat {}) > {}".format(p, p, r)))
        elif t == 8:
            r = "top-{}.txt".format(k)
            levels.append(L(lid, "Top 20 des gloutons : {}".format(r),
                lesson="'top -b -n 1' prend UNE photo des plus gros consommateurs (b=batch : pas d'affichage interactif). "
                       "En analyse de 'ca rame', c'est la piece n°1.",
                mission="Photographie les gloutons dans {} : top -b -n 1 | head -n 20 > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="PID")],
                hints=["top -b -n 1 | head -n 20 > {}".format(r), "-b = non-interactif, -n 1 = une seule photo."],
                solution="top -b -n 1 | head -n 20 > {}".format(r),
                story="Alerte : 'le serveur rame !'. Avant de paniquer, photographie les suspects."))
        else:
            r = "sortie-nohup-{}.txt".format(k)
            levels.append(L(lid, "Survivre a la fermeture : {}".format(r),
                lesson="'nohup commande &' lance un processus qui SURVIT a la fermeture du terminal. Pour les longs calculs, "
                       "les serveurs... Les sorties vont dans le fichier indique.",
                mission="Lance un sleep qui survivra : nohup sleep 3 > {} 2>&1 & (puis verifie que {} existe).".format(r, r),
                checks=[C_cmd(r"\bnohup\b"), C_fe(r)],
                hints=["nohup sleep 3 > {} 2>&1 &".format(r), "nohup = no hangup : 'ne raccroche pas'."],
                solution="nohup sleep 3 > {} 2>&1 &".format(r)))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc G : reseau local
def _block_g():
    levels = []
    for n in range(100):
        lid = 601 + n
        t, k = n % 10, n // 10
        if t == 0:
            r = "ping-{}.txt".format(k)
            levels.append(L(lid, "Sonar local : {}".format(r),
                lesson="'ping' envoie un echo et mesure le retour. 127.0.0.1 = 'localhost', ta propre machine. "
                       "Si ca ne repond pas, la pile reseau est cassee.",
                mission="Pinge ta machine 2 fois et sauve dans {} : ping -c 2 127.0.0.1 > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="127.0.0.1")],
                hints=["ping -c 2 127.0.0.1 > {}".format(r), "-c 2 = 2 paquets puis stop."],
                solution="ping -c 2 127.0.0.1 > {}".format(r)))
        elif t == 1:
            r = "ping-nom-{}.txt".format(k)
            levels.append(L(lid, "Pinger par son nom : {}".format(r),
                lesson="'localhost' est le NOM de 127.0.0.1 (defini dans /etc/hosts). Les noms, c'est pour les humains ; "
                       "les IP, pour les machines.",
                mission="Pinge 'localhost' 1 fois dans {} : ping -c 1 localhost > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="localhost")],
                hints=["ping -c 1 localhost > {}".format(r), "localhost = le petit nom de ta machine."],
                solution="ping -c 1 localhost > {}".format(r)))
        elif t == 2:
            r = "reseau-{}.txt".format(k)
            levels.append(L(lid, "Carte reseau : {}".format(r),
                lesson="'ip addr' (ou 'ip a') liste les interfaces et leurs IP : lo (boucle locale), eth0/wlan0... "
                       "La carte d'identite reseau.",
                mission="Enregistre tes interfaces dans {} : ip addr > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="127.0.0.1")],
                hints=["ip addr > {}".format(r), "L'interface 'lo' porte toujours 127.0.0.1."],
                solution="ip addr > {}".format(r)))
        elif t == 3:
            r = "bref-{}.txt".format(k)
            levels.append(L(lid, "Version courte : {}".format(r),
                lesson="'ip -br addr' : la meme chose en COMPACT (une ligne par interface). Pour les grands ecrans... "
                       "et les petits.",
                mission="Liste compacte dans {} : ip -br addr > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="lo")],
                hints=["ip -br addr > {}".format(r), "-br = brief (bref)."],
                solution="ip -br addr > {}".format(r)))
        elif t == 4:
            r = "hote-{}.txt".format(k)
            levels.append(L(lid, "Annuaire : {}".format(r),
                lesson="'getent hosts nom' interroge la resolution de noms (fichiers + DNS). 'localhost' doit repondre "
                       "127.0.0.1 (et/ou ::1).",
                mission="Resous 'localhost' dans {} : getent hosts localhost > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="localhost")],
                hints=["getent hosts localhost > {}".format(r), "getent = interroger les bases du systeme."],
                solution="getent hosts localhost > {}".format(r)))
        elif t == 5:
            r = "hosts-{}.txt".format(k)
            levels.append(L(lid, "Copie de l'annuaire : {}".format(r),
                lesson="'/etc/hosts' associe noms et IP en local. C'est lui qui dit que localhost = 127.0.0.1. "
                       "Les admins y ajoutent leurs serveurs.",
                mission="Copie /etc/hosts dans {} : cat /etc/hosts > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="localhost")],
                hints=["cat /etc/hosts > {}".format(r), "localhost est toujours dans ce fichier."],
                solution="cat /etc/hosts > {}".format(r)))
        elif t == 6:
            r = "ports-{}.txt".format(k)
            levels.append(L(lid, "Ports a l'ecoute : {}".format(r),
                lesson="'ss -tln' liste les ports TCP a l'ECOUTE (t=tcp, l=listening, n=numerique). "
                       "'Qui ecoute sur cette machine ?' : question n°1 de securite.",
                mission="Liste les ports a l'ecoute dans {} : ss -tln > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bss\b")],
                hints=["ss -tln > {}".format(r), "ss = socket statistics (le remplacant de netstat)."],
                solution="ss -tln > {}".format(r),
                story="Audit securite : avant de blinders, il faut savoir QUELS ports ecoutent. Inspecte."))
        elif t == 7:
            r = "dns-{}.txt".format(k)
            levels.append(L(lid, "Serveurs DNS : {}".format(r),
                lesson="'/etc/resolv.conf' dit quels serveurs DNS interroger ('nameserver ...'). "
                       "Pas de DNS = pas d'Internet (par noms).",
                mission="Copie la config DNS dans {} : cat /etc/resolv.conf > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bcat\b[^\n]*resolv\.conf")],
                hints=["cat /etc/resolv.conf > {}".format(r), "resolv = resolver (resolution de noms)."],
                solution="cat /etc/resolv.conf > {}".format(r)))
        elif t == 8:
            r = "nom-{}.txt".format(k)
            levels.append(L(lid, "Badge de la machine : {}".format(r),
                lesson="Sur le reseau, chaque machine a un nom ('hostname'). C'est ce nom que verront les autres "
                       "dans les logs, le DHCP, le monitoring.",
                mission="Enregistre le nom reseau dans {} : hostname > {}".format(r, r),
                checks=[C_fe(r), C_nempty(r)],
                hints=["hostname > {}".format(r), "Le nom reseau = l'etiquette de la machine."],
                solution="hostname > {}".format(r)))
        else:
            r = "web-{}.txt".format(k)
            levels.append(L(lid, "Premier telechargement : {}".format(r),
                lesson="'curl' telecharge n'importe quelle URL (http, ftp... et file:// pour les fichiers locaux). "
                       "Le couteau suisse du web en terminal.",
                mission="Telecharge /etc/hosts via curl dans {} : curl -s file:///etc/hosts > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="localhost")],
                hints=["curl -s file:///etc/hosts > {}".format(r), "-s = silencieux (pas de barre de progression)."],
                solution="curl -s file:///etc/hosts > {}".format(r)))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc H : cles SSH / copies
def _block_h():
    levels = []
    for n in range(100):
        lid = 701 + n
        t, k = n % 10, n // 10
        if t == 0:
            key = "macle-{}".format(k)
            levels.append(L(lid, "Ta premiere cle : {}".format(key),
                lesson="'ssh-keygen' cree une paire : privee (secrete, JAMAIS partagee) + publique (.pub, a distribuer). "
                       "Fini les mots de passe : bonjour les cles !",
                mission="Cree une cle ed25519 sans mot de passe : ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                checks=[C_fe(key), C_fe(key + ".pub")],
                hints=["ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key), "-t = type, -f = fichier, -N = mot de passe vide."],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                story="Pour te connecter aux serveurs sans mot de passe, il te faut une paire de cles. Forge-la."))
        elif t == 1:
            key = "cle-{}".format(k)
            r = "recup-{}.pub".format(k)
            levels.append(L(lid, "Retrouver la publique : {}".format(r),
                lesson="Publique perdue ? Pas grave : 'ssh-keygen -y -f PRIVE' la REGENERE depuis la privee. "
                       "(L'inverse est impossible : c'est tout l'interet.)",
                mission="Cree {} puis regenere sa publique dans {} : ssh-keygen ... && ssh-keygen -y -f ./{} > {}".format(key, r, key, r),
                checks=[C_fe(r), C_fc(r, text="ssh-ed25519")],
                hints=["1) ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                       "2) ssh-keygen -y -f ./{} > {}".format(key, r)],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\" && ssh-keygen -y -f ./{} > {}".format(key, key, r)))
        elif t == 2:
            key = "cle-{}".format(k)
            r = "empreinte-{}.txt".format(k)
            levels.append(L(lid, "Empreinte : {}".format(r),
                lesson="'ssh-keygen -lf cle.pub' affiche l'EMPREINTE (fingerprint) : un resume unique pour verifier une cle "
                       "('c'est bien celle de mon serveur ?').",
                mission="Cree {} puis affiche son empreinte dans {} : ... && ssh-keygen -lf ./{}.pub > {}".format(key, r, key, r),
                checks=[C_fe(r), C_fc(r, text="SHA256:")],
                hints=["1) ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                       "2) ssh-keygen -lf ./{}.pub > {}".format(key, r)],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\" && ssh-keygen -lf ./{}.pub > {}".format(key, key, r)))
        elif t == 3:
            key = "cle-{}".format(k)
            levels.append(L(lid, "Proteger {} (600/644)".format(key),
                lesson="Regle d'or SSH : privee en 600 (moi seul), publique en 644 (lisible). Sinon SSH refuse "
                       "('bad permissions')... et il a raison.",
                mission="Cree {} puis mets la privee en 600 et la publique en 644.".format(key),
                checks=[C_perm(key, "600"), C_perm(key + ".pub", "644")],
                hints=["1) ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                       "2) chmod 600 ./{} && chmod 644 ./{}.pub".format(key, key)],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\" && chmod 600 ./{} && chmod 644 ./{}.pub".format(key, key, key)))
        elif t == 4:
            key = "cle-{}".format(k)
            a = "cles-autorisees-{}".format(k)
            levels.append(L(lid, "Autoriser {}".format(key),
                lesson="Sur un serveur, les publiques autorisees vivent dans ~/.ssh/authorized_keys (une par ligne). "
                       "Y ajouter ta publique = ouvrir ta serrure a ta cle.",
                mission="Cree {} puis ajoute sa publique a {} : ... && cat ./{}.pub >> {}".format(key, a, key, a),
                checks=[C_fe(a), C_fc(a, text="ssh-ed25519")],
                hints=["1) ssh-keygen -t ed25519 -f ./{} -N \"\"".format(key),
                       "2) cat ./{}.pub >> {}".format(key, a)],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\" && cat ./{}.pub >> {}".format(key, key, a),
                story="Le serveur ne te connait pas encore. Depose ta cle publique sur le paillasson autorise."))
        elif t == 5:
            r = "version-ssh-{}.txt".format(k)
            levels.append(L(lid, "Version SSH : {}".format(r),
                lesson="'ssh -V' affiche la version du client SSH... sur le canal des ERREURS. D'ou le '2>' pour la capturer. "
                       "Les vieux outils ont leurs manies.",
                mission="Capture la version SSH dans {} : ssh -V 2> {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="OpenSSH")],
                hints=["ssh -V 2> {}".format(r), "ssh parle sur le canal 2 : il faut 2> pour le capturer."],
                solution="ssh -V 2> {}".format(r)))
        elif t == 6:
            s = "doc-{}.txt".format(k)
            d = "copie-{}.txt".format(k)
            levels.append(L(lid, "Copie securisee : {}".format(s),
                lesson="'scp' copie via SSH (chiffre). En local, 'scp a b' marche comme cp : parfait pour s'entrainer "
                       "avant de copier VRAIMENT vers un serveur.",
                mission="Copie {} vers {} avec scp : scp {} {}".format(s, d, s, d),
                setup=[F(s, "document secret {}\n".format(k))],
                checks=[C_fe(d), C_fc(d, text="secret {}".format(k))],
                hints=["scp {} {}".format(s, d), "scp source destination, comme cp."],
                solution="scp {} {}".format(s, d)))
        elif t == 7:
            key = "cle-{}.txt".format(k) if False else "cle-{}".format(k)
            levels.append(L(lid, "Cle signee : {}".format(key),
                lesson="'-C commentaire' signe ta cle (souvent user@machine). Quand le serveur a 50 cles, le commentaire "
                       "dit a qui appartient chacune.",
                mission="Cree {} signee 'ilearn-{}' : ssh-keygen -t ed25519 -f ./{} -N \"\" -C \"ilearn-{}\"".format(key, k, key, k),
                checks=[C_fe(key + ".pub"), C_fc(key + ".pub", text="ilearn-{}".format(k))],
                hints=["ssh-keygen -t ed25519 -f ./{} -N \"\" -C \"ilearn-{}\"".format(key, k),
                       "-C = commentaire joint a la cle."],
                solution="ssh-keygen -t ed25519 -f ./{} -N \"\" -C \"ilearn-{}\"".format(key, k)))
        elif t == 8:
            r = "config-{}".format(k)
            levels.append(L(lid, "Carnet d'adresses SSH : {}".format(r),
                lesson="~/.ssh/config memorise tes serveurs : 'Host monserveur / HostName ... / User ...'. Ensuite, "
                       "'ssh monserveur' suffit. Ici, on s'entraine avec un faux carnet.",
                mission="Cree {} contenant un bloc Host : printf 'Host test\\n HostName localhost\\n' > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="HostName localhost")],
                hints=["printf 'Host test\\n HostName localhost\\n' > {}".format(r),
                       "printf interprete \\n comme un retour a la ligne."],
                solution="printf 'Host test\\n HostName localhost\\n' > {}".format(r)))
        else:
            d = "dossier-{}".format(k)
            b = "sauvegarde-{}".format(k)
            levels.append(L(lid, "Sauvegarde (locale) : {}/".format(b),
                lesson="'scp -r' copie tout un DOSSIER via SSH. C'est comme ca qu'on deploie un site ou qu'on recupere "
                       "des logs : un dossier entier, chiffre, en une ligne.",
                mission="Copie {}/ vers {}/ avec scp -r : scp -r {} {}".format(d, b, d, b),
                setup=[F(d + "/fichier.txt", "donnees\n")],
                checks=[C_fe(b + "/fichier.txt")],
                hints=["scp -r {} {}".format(d, b), "-r = recursif : le dossier et son contenu."],
                solution="scp -r {} {}".format(d, b),
                story="Deploiement ! Envoie le dossier complet vers la 'machine distante' (ici, juste a cote)."))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc I : scripting shell
def _block_i():
    levels = []
    for n in range(100):
        lid = 801 + n
        t, k = n % 10, n // 10
        if t == 0:
            fruit = FRUITS[k]
            r = "var-{}.txt".format(k)
            levels.append(L(lid, "Variable FRUIT={}".format(fruit),
                lesson="En shell, 'NOM=valeur' cree une variable (SANS espaces autour du = !). '$NOM' la reutilise. "
                       "La base de tous les scripts.",
                mission="Stocke '{}' dans FRUIT puis sauve-le dans {} : FRUIT={} puis echo $FRUIT > {}".format(fruit, r, fruit, r),
                checks=[C_fe(r), C_fc(r, text=fruit)],
                hints=["1) FRUIT={} (pas d'espaces !)".format(fruit), "2) echo $FRUIT > {}".format(r)],
                solution="FRUIT={} && echo $FRUIT > {}".format(fruit, r)))
        elif t == 1:
            r = "home-{}.txt".format(k)
            levels.append(L(lid, "Variable HOME : {}".format(r),
                lesson="'$HOME' contient ton dossier personnel. Les bons scripts ecrivent '$HOME/sauvegardes', jamais "
                       "'/home/marie/...' : ca marche pour tout le monde.",
                mission="Sauve ton dossier perso dans {} : echo $HOME > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="/")],
                hints=["echo $HOME > {}".format(r), "$HOME = ta maison, ou que tu sois."],
                solution="echo $HOME > {}".format(r)))
        elif t == 2:
            s = "bonjour-{}.sh".format(k)
            r = "out-{}.txt".format(k)
            levels.append(L(lid, "Script {}".format(s),
                lesson="Un script = des commandes dans un fichier + droit x. '#!/bin/bash' (shebang) dit QUEL interprete "
                       "l'executer. chmod +x, ./go : tu es scripteur.",
                mission="Cree {} affichant 'salut-{}', rends-le executable, lance-le vers {}.".format(s, k, r),
                checks=[C_exe(s), C_fe(r), C_fc(r, text="salut-{}".format(k))],
                hints=["1) printf '#!/bin/bash\\necho salut-{}\\n' > {}".format(k, s),
                       "2) chmod +x {}".format(s),
                       "3) ./{} > {}".format(s, r)],
                solution="printf '#!/bin/bash\\necho salut-{}\\n' > {} && chmod +x {} && ./{} > {}".format(k, s, s, s, r)))
        elif t == 3:
            r = "nombres-{}.txt".format(k)
            levels.append(L(lid, "Boucle 1-2-3 : {}".format(r),
                lesson="'for i in 1 2 3; do ...; done' repete 3 fois avec $i = 1, puis 2, puis 3. "
                       "La boucle for : l'employe qui ne se fatigue jamais.",
                mission="Genere 1,2,3 dans {} : for i in 1 2 3; do echo $i >> {}; done (si rate : rm {} et recommence).".format(r, r, r),
                checks=[C_eq(r, "1\n2\n3\n")],
                hints=["for i in 1 2 3; do echo $i >> {}; done".format(r),
                       ">> ajoute chaque tour (avec > on ecraserait)."],
                solution="for i in 1 2 3; do echo $i >> {}; done".format(r)))
        elif t == 4:
            levels.append(L(lid, "3 fichiers d'un coup (boucle {})".format(k + 1),
                lesson="La boucle for + echo cree des SERIES de fichiers : rapports, sauvegardes... "
                       "'ligne-$i.txt' : $i change a chaque tour.",
                mission="Cree ligne-1.txt, ligne-2.txt, ligne-3.txt avec 'ligne N' dedans : for i in 1 2 3; do echo \"ligne $i\" > ligne-$i.txt; done",
                checks=[C_fe("ligne-1.txt"), C_fe("ligne-2.txt"), C_fe("ligne-3.txt"),
                        C_fc("ligne-2.txt", text="ligne 2")],
                hints=["for i in 1 2 3; do echo \"ligne $i\" > ligne-$i.txt; done",
                       "$i vaut 1, puis 2, puis 3."],
                solution="for i in 1 2 3; do echo \"ligne $i\" > ligne-$i.txt; done",
                story="Le chef veut 3 rapports, un par region. Une boucle, et c'est regle avant le cafe."))
        elif t == 5:
            flag = "drapeau-{}.txt".format(k)
            r = "test-{}.txt".format(k)
            levels.append(L(lid, "Decision : {}".format(r),
                lesson="'if [ -f fichier ]; then ...; fi' = 'SI le fichier existe, ALORS...'. Les crochets [ ] sont un TEST "
                       "(espaces obligatoires dedans !).",
                mission="Si {} existe, ecris 'oui' dans {} : if [ -f {} ]; then echo oui > {}; fi".format(flag, r, flag, r),
                setup=[F(flag, "flotte\n")],
                checks=[C_fe(r), C_fc(r, text="oui")],
                hints=["if [ -f {} ]; then echo oui > {}; fi".format(flag, r),
                       "Espaces obligatoires : [ -f ... ] — sinon erreur."],
                solution="if [ -f {} ]; then echo oui > {}; fi".format(flag, r)))
        elif t == 6:
            r = "compte-{}.txt".format(k)
            levels.append(L(lid, "Commande dans commande : {}".format(r),
                lesson="'$(commande)' insere le RESULTAT d'une commande dans une autre. 'echo \"il y a $(ls | wc -l) fichiers\"' : "
                       "ls compte AVANT qu'echo parle.",
                mission="Ecris 'il y a N entrees' dans {} : echo \"il y a $(ls -1 | wc -l) entrees\" > {}".format(r, r),
                setup=[F("a.txt", "a\n")],
                checks=[C_fe(r), C_fc(r, text="entrees"), C_fc(r, regex=r"\d+")],
                hints=["echo \"il y a $(ls -1 | wc -l) entrees\" > {}".format(r),
                       "$(...) est calcule avant echo."],
                solution="echo \"il y a $(ls -1 | wc -l) entrees\" > {}".format(r)))
        elif t == 7:
            r = "f-{}.txt".format(k)
            levels.append(L(lid, "Ta fonction : {}".format(r),
                lesson="'mafonction() { ...; }' DEFINIT une fonction, 'mafonction' l'APPELLE. "
                       "Une fonction = une commande sur mesure, reutilisable.",
                mission="Definis puis appelle une fonction ecrivant 'coucou-{}' dans {} : coucou() {{ echo coucou-{}; }}; coucou > {}".format(k, r, k, r),
                checks=[C_fe(r), C_fc(r, text="coucou-{}".format(k))],
                hints=["coucou() {{ echo coucou-{}; }}; coucou > {}".format(k, r),
                       "D'abord definir (avec les accolades), puis appeler."],
                solution="coucou() {{ echo coucou-{}; }}; coucou > {}".format(k, r)))
        elif t == 8:
            src = "liste-{}.txt".format(k)
            r = "out-{}.txt".format(k)
            levels.append(L(lid, "Lire ligne par ligne : {}".format(r),
                lesson="'cat f | while read l; do ...; done' traite CHAQUE ligne (dans $l). Le tapis roulant du shell : "
                       "chaque ligne passe, le traitement s'applique.",
                mission="Prefixe chaque ligne de {} par '>>' dans {} : cat {} | while read l; do echo \">>$l\" >> {}; done (si rate : rm {} et recommence).".format(src, r, src, r, r),
                setup=[F(src, "a\nb\n")],
                checks=[C_eq(r, ">>a\n>>b\n")],
                hints=["cat {} | while read l; do echo \">>$l\" >> {}; done".format(src, r),
                       "$l contient la ligne courante."],
                solution="cat {} | while read l; do echo \">>$l\" >> {}; done".format(src, r)))
        else:
            r = "env-{}.txt".format(k)
            levels.append(L(lid, "Variable d'environnement : {}".format(r),
                lesson="'printenv NOM' affiche une variable D'ENVIRONNEMENT (connue de tous les programmes). "
                       "HOME, PATH, USER... : le contexte invisible de chaque commande.",
                mission="Affiche HOME via printenv dans {} : printenv HOME > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="/")],
                hints=["printenv HOME > {}".format(r), "printenv = afficher l'environnement."],
                solution="printenv HOME > {}".format(r)))
    return [_bossify(lv) for lv in levels]


# ------------------------------------------------- Bloc J : admin pro + boss final
def _block_j():
    levels = []
    for n in range(100):
        lid = 901 + n
        t, k = n % 10, n // 10
        if lid == 1000:
            levels.append(_mega_boss())
            continue
        if t == 0:
            r = "journal-sys-{}.txt".format(k)
            levels.append(L(lid, "Logs systeme : {}".format(r),
                lesson="'journalctl' lit le journal de systemd (TOUS les services). '-n 3' = 3 dernieres lignes, "
                       "'--no-pager' = pas de page par page. Sur un vrai serveur, c'est la bible.",
                mission="Lis les 3 dernieres lignes du journal dans {} : journalctl --no-pager -n 3 > {} 2>&1".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bjournalctl\b")],
                hints=["journalctl --no-pager -n 3 > {} 2>&1".format(r),
                       "2>&1 : meme les erreurs sont capturees."],
                solution="journalctl --no-pager -n 3 > {} 2>&1".format(r),
                story="Le serveur a toussote cette nuit. Ouvre le grand journal et prends les dernieres lignes."))
        elif t == 1:
            r = "systemd-{}.txt".format(k)
            levels.append(L(lid, "Version systemd : {}".format(r),
                lesson="'systemctl --version' donne la version du superviseur de services (meme sans services a gerer). "
                       "systemd pilote le demarrage de la plupart des Linux.",
                mission="Enregistre la version de systemd dans {} : systemctl --version > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text="systemd")],
                hints=["systemctl --version > {}".format(r), "systemctl = piloter systemd."],
                solution="systemctl --version > {}".format(r)))
        elif t == 2:
            r = "logs-sys-{}.txt".format(k)
            levels.append(L(lid, "Le grenier a logs : {}".format(r),
                lesson="'/var/log' est LE grenier : syslog, auth.log, kern.log... Quand tout brule, on vient ici "
                       "avec grep et tail.",
                mission="Liste le grenier dans {} : ls /var/log > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bls\b[^\n]*/var/log")],
                hints=["ls /var/log > {}".format(r), "/var/log = tous les journaux cote a cote."],
                solution="ls /var/log > {}".format(r)))
        elif t == 3:
            r = "demarrage-{}.txt".format(k)
            levels.append(L(lid, "Messages du noyau : {}".format(r),
                lesson="'dmesg' affiche les messages du NOYAU (materiel, pilotes...). '| head -n 5' : juste le debut. "
                       "'2>/dev/null' : poubelle pour les erreurs.",
                mission="Garde le debut des messages noyau dans {} : dmesg 2>/dev/null | head -n 5 > {}".format(r, r),
                checks=[C_fe(r), C_cmd(r"\bdmesg\b")],
                hints=["dmesg 2>/dev/null | head -n 5 > {}".format(r), "dmesg = diagnostic messages."],
                solution="dmesg 2>/dev/null | head -n 5 > {}".format(r)))
        elif t == 4:
            big = "GROS-{}.dat".format(k)
            r = "plus-gros-{}.txt".format(k)
            levels.append(L(lid, "Chasse au glouton : {}".format(r),
                lesson="'du -sb * | sort -nr | head -n 1' : pese tout, trie (plus gros d'abord), garde le 1er. "
                       "LA commande 'disque plein' que tout admin connait par coeur.",
                mission="Trouve le plus gros dans {} : du -sb * | sort -nr | head -n 1 > {}".format(r, r),
                setup=[F("petit1.txt", "a\n"), F(big, "y" * 50000), F("petit2.txt", "b\n")],
                checks=[C_fe(r), C_fc(r, text=big)],
                hints=["du -sb * | sort -nr | head -n 1 > {}".format(r),
                       "du pese, sort -nr trie (gros d'abord), head garde le 1er."],
                solution="du -sb * | sort -nr | head -n 1 > {}".format(r),
                story="ALERTE DISQUE PLEIN. Trouve le fichier glouton avant que tout s'arrete. Vite."))
        elif t == 5:
            s = "sauvegarde-{}.sh".format(k)
            r = "resultat-{}.txt".format(k)
            levels.append(L(lid, "Reparer {}".format(s),
                lesson="Ticket support : 'le script ne se lance pas'. Diagnostic classique n°1 : le droit x manque. "
                       "chmod +x, relancer, verifier la sortie.",
                mission="Repare et lance {} vers {} (le script doit afficher 'sauvegarde-ok-{}').".format(s, r, k),
                setup=[F(s, "#!/bin/bash\necho sauvegarde-ok-{}\n".format(k), mode="644")],
                checks=[C_exe(s), C_fe(r), C_fc(r, text="sauvegarde-ok-{}".format(k))],
                hints=["1) chmod +x {}".format(s), "2) ./{} > {}".format(s, r)],
                solution="chmod +x {} && ./{} > {}".format(s, s, r),
                story="La sauvegarde de nuit a echoue : le script 'ne se lance pas'. Sauve la mise."))
        elif t == 6:
            d = "logs-{}".format(k)
            levels.append(L(lid, "Compresser les vieux logs : {}/".format(d),
                lesson="Les logs grossissent sans fin : on les COMPRESSE ('gzip *.log' : chaque .log devient .log.gz). "
                       "C'est le metier de logrotate, en automatique.",
                mission="Compresse les 3 .log de {}/ avec gzip (garde lisez-moi.txt intact).".format(d),
                setup=[D(d), F(d + "/a.log", "a\n" * 20), F(d + "/b.log", "b\n" * 20),
                       F(d + "/c.log", "c\n" * 20), F(d + "/lisez-moi.txt", "lire\n")],
                checks=[C_fe(d + "/a.log.gz"), C_fe(d + "/b.log.gz"), C_fe(d + "/c.log.gz"),
                        C_fe(d + "/lisez-moi.txt")],
                hints=["gzip {}/*.log".format(d), "gzip traite chaque fichier : .log -> .log.gz."],
                solution="gzip {}/*.log".format(d)))
        elif t == 7:
            log = "app-{}.log".format(k)
            r = "nb-erreurs-{}.txt".format(k)
            levels.append(L(lid, "Combien d'erreurs ? ({})".format(r),
                lesson="Ticket : 'l'appli a plante cette nuit'. Premier geste : compter les ERROR dans le log. "
                       "'grep -c' : le thermometre de l'admin.",
                mission="Compte les ERROR de {} dans {} : grep -c ERROR {} > {}".format(log, r, log, r),
                setup=[F(log, "INFO demarrage\nERROR disque\nINFO suite\nERROR reseau\nERROR memoire\nINFO fin\n")],
                checks=[C_fe(r), C_fc(r, regex=r"3")],
                hints=["grep -c ERROR {} > {}".format(log, r), "-c = count (compter)."],
                solution="grep -c ERROR {} > {}".format(log, r),
                story="L'appli a plante a 3h du matin. Le rapport d'incident commence par UN chiffre : combien d'erreurs ?"))
        elif t == 8:
            log = "acces-{}.log".format(k)
            r = "top-{}.txt".format(k)
            levels.append(L(lid, "Qui frappe a la porte ? ({})".format(r),
                lesson="'sort | uniq -c | sort -nr | head -n 1' : LE top-1 des occurrences. Quelle IP frappe le plus ? "
                       "Attaque ou client fidele ? L'enquete commence.",
                mission="Trouve l'IP la plus frequente de {} dans {} : sort {} | uniq -c | sort -nr | head -n 1 > {}".format(log, r, log, r),
                setup=[F(log, "10.0.0.1\n10.0.0.2\n10.0.0.1\n10.0.0.1\n10.0.0.3\n")],
                checks=[C_fe(r), C_fc(r, text="10.0.0.1")],
                hints=["sort {} | uniq -c | sort -nr | head -n 1 > {}".format(log, r),
                       "Trie, compte, re-trie (gros d'abord), garde le top 1."],
                solution="sort {} | uniq -c | sort -nr | head -n 1 > {}".format(log, r),
                story="Le pare-feu signale un trafic bizarre. Quelle IP frappe le plus a la porte ?"))
        else:
            r = "charge-sys-{}.txt".format(k)
            levels.append(L(lid, "Charge systeme : {}".format(r),
                lesson="'/proc/loadavg' : la charge moyenne (1, 5, 15 min). Au-dessus du nombre de coeurs = ca rame. "
                       "Le pouls de la machine, en direct.",
                mission="Copie le pouls dans {} : cat /proc/loadavg > {}".format(r, r),
                checks=[C_fe(r), C_fc(r, text=".")],
                hints=["cat /proc/loadavg > {}".format(r), "La charge contient des nombres a virgule."],
                solution="cat /proc/loadavg > {}".format(r)))
    return [_bossify(lv) for lv in levels]


def _mega_boss():
    return L(1000, "MEGA-BOSS FINAL : deploiement",
        story="Dernier jour. Le grand serveur t'attend. Deploie le projet comme un pro : structure, script, "
              "execution, archive, preuve. Tout ce que tu as appris, en un seul niveau.",
        lesson="L'examen final combine TOUT : mkdir, script, chmod, redirection, tar. "
               "Un deploiement miniature, comme les grands.",
        mission=("1) mkdir projet-final  2) cree projet-final/app.sh affichant 'en-ligne'  3) chmod +x  "
                 "4) lance-le vers projet-final/statut.txt  5) ajoute la ligne 'version:1.0' a statut.txt  "
                 "6) cree projet-final.tar.gz  7) liste l'archive dans preuve.txt"),
        checks=[
            C_de("projet-final"),
            C_exe("projet-final/app.sh"),
            C_fc("projet-final/statut.txt", text="en-ligne"),
            C_fc("projet-final/statut.txt", text="version:1.0"),
            C_fe("projet-final.tar.gz"),
            C_nempty("projet-final.tar.gz"),
            C_fe("preuve.txt"),
            C_fc("preuve.txt", text="app.sh"),
        ],
        hints=["1) mkdir projet-final",
               "2) printf '#!/bin/bash\\necho en-ligne\\n' > projet-final/app.sh",
               "3) chmod +x projet-final/app.sh  4) ./projet-final/app.sh > projet-final/statut.txt",
               "5) echo version:1.0 >> projet-final/statut.txt  6) tar -czf projet-final.tar.gz projet-final",
               "7) tar -tzf projet-final.tar.gz > preuve.txt"],
        solution=("mkdir projet-final && printf '#!/bin/bash\\necho en-ligne\\n' > projet-final/app.sh && "
                  "chmod +x projet-final/app.sh && ./projet-final/app.sh > projet-final/statut.txt && "
                  "echo version:1.0 >> projet-final/statut.txt && "
                  "tar -czf projet-final.tar.gz projet-final && tar -tzf projet-final.tar.gz > preuve.txt"),
        xp=100, boss=True)


def build():
    """Construit les 900 niveaux des jours 11-100."""
    levels = []
    levels.extend(_block_b())
    levels.extend(_block_c())
    levels.extend(_block_d())
    levels.extend(_block_e())
    levels.extend(_block_f())
    levels.extend(_block_g())
    levels.extend(_block_h())
    levels.extend(_block_i())
    levels.extend(_block_j())
    return sorted(levels, key=lambda lv: lv["id"])
