"""Jour 10 (niveaux 91-100) : Trier, decouper, transformer + grande revision."""

from .common import L, F, D, C_cmd, C_fe, C_de, C_fc, C_nempty, C_eq

LEVELS = [
    L(91, "Trier (sort)",
      lesson="'sort' trie les lignes par ordre alphabetique. 'sort prenoms.txt > tries.txt' : la liste devient impeccable. "
             "Les donnees rangees, c'est les donnees comprises.",
      mission="Trie prenoms.txt dans tries.txt :  sort prenoms.txt > tries.txt",
      setup=[F("prenoms.txt", "zoe\nmarie\npaul\n")],
      checks=[C_eq("tries.txt", "marie\npaul\nzoe\n")],
      hints=["sort prenoms.txt > tries.txt", "sort lit, trie, > sauve."],
      solution="sort prenoms.txt > tries.txt",
      story="La liste des invites est dans le desordre. Avant d'imprimer, on trie."),

    L(92, "Trier a l'envers (-r)",
      lesson="'sort -r' trie en ordre INVERSE (r = reverse). Z vers A, 9 vers 0. "
             "Pour les podiums, les tops 10, les 'plus gros d'abord'.",
      mission="Trie prenoms.txt a l'envers dans inverse.txt :  sort -r prenoms.txt > inverse.txt",
      setup=[F("prenoms.txt", "marie\npaul\nzoe\n")],
      checks=[C_eq("inverse.txt", "zoe\npaul\nmarie\n")],
      hints=["Ajoute -r au sort.", "Tape : sort -r prenoms.txt > inverse.txt"],
      solution="sort -r prenoms.txt > inverse.txt"),

    L(93, "Trier des nombres (-n)",
      lesson="'sort -n' trie NUMERIQUEMENT. Sans -n, '10' passe avant '2' (car '1' < '2' en alphabetique) : le piege classique ! "
             "Pour des chiffres, toujours -n.",
      mission="Trie scores.txt numeriquement dans classement.txt :  sort -n scores.txt > classement.txt",
      setup=[F("scores.txt", "10\n2\n30\n")],
      checks=[C_eq("classement.txt", "2\n10\n30\n")],
      hints=["sort -n scores.txt > classement.txt", "-n = numeric (numerique)."],
      solution="sort -n scores.txt > classement.txt"),

    L(94, "Doublons dehors (uniq)",
      lesson="'uniq' supprime les lignes DOUBLES CONSECUTIVES. Piege : il faut TRIER avant ! "
             "'sort d.txt | uniq > uniques.txt' : le combo officiel anti-doublons.",
      mission="Supprime les doublons de fruits.txt :  sort fruits.txt | uniq > uniques.txt",
      setup=[F("fruits.txt", "pomme\nbanane\npomme\ncerise\nbanane\n")],
      checks=[C_eq("uniques.txt", "banane\ncerise\npomme\n")],
      hints=["sort fruits.txt | uniq > uniques.txt", "Toujours sort AVANT uniq."],
      solution="sort fruits.txt | uniq > uniques.txt",
      story="La liste de courses contient 3 fois 'pomme'. Ton frigo n'est pas extensible : dedup !"),

    L(95, "Compter les doublons (uniq -c)",
      lesson="'uniq -c' compte les repetitions : '2 pomme' = pomme x2. 'sort | uniq -c | sort -nr' donne meme un TOP des plus frequents : "
             "la requete preferee des admins pour analyser des logs.",
      mission="Compte les fruits :  sort fruits.txt | uniq -c > compteur.txt (verifie : pomme doit apparaitre 2 fois).",
      setup=[F("fruits.txt", "pomme\nbanane\npomme\n")],
      checks=[C_fe("compteur.txt"), C_fc("compteur.txt", text="pomme"), C_fc("compteur.txt", regex=r"2")],
      hints=["sort fruits.txt | uniq -c > compteur.txt", "-c = count : uniq affiche le nombre devant."],
      solution="sort fruits.txt | uniq -c > compteur.txt"),

    L(96, "Decouper des colonnes (cut)",
      lesson="'cut -d: -f1' decoupe chaque ligne sur ':' et garde le champ 1. Pour extraire les noms d'utilisateurs "
             "de /etc/passwd ou une colonne d'un CSV.",
      mission="Extrait les prenoms de classe.txt :  cut -d: -f1 classe.txt > noms.txt",
      setup=[F("classe.txt", "marie:12:lyon\npaul:11:paris\n")],
      checks=[C_eq("noms.txt", "marie\npaul\n")],
      hints=["cut -d: -f1 classe.txt > noms.txt", "-d: = separateur ':', -f1 = champ 1."],
      solution="cut -d: -f1 classe.txt > noms.txt"),

    L(97, "Majuscules (tr)",
      lesson="'tr a-z A-Z' convertit minuscules en MAJUSCULES. 'tr a-z A-Z < petit.txt > GRAND.txt' : le < envoie le fichier en entree. "
             "Pour gueuler poliment... dans un fichier.",
      mission="Convertis petit.txt en majuscules dans GRAND.txt :  tr a-z A-Z < petit.txt > GRAND.txt",
      setup=[F("petit.txt", "bonjour\n")],
      checks=[C_eq("GRAND.txt", "BONJOUR\n")],
      hints=["tr a-z A-Z < petit.txt > GRAND.txt", "< envoie le fichier a tr, > sauve le resultat."],
      solution="tr a-z A-Z < petit.txt > GRAND.txt"),

    L(98, "Revision : creer et remplir",
      lesson="Jour 10 : on revise les bases. echo + '>' = creer et remplir en une ligne. "
             "Si tu fais ca sans reflechir, tes doigts ont deja le niveau.",
      mission="Cree revision.txt contenant exactement 'je-revise' (echo + redirection).",
      checks=[C_fe("revision.txt"), C_fc("revision.txt", text="je-revise")],
      hints=["echo je-revise > revision.txt", "Simple, rapide, efficace."],
      solution="echo je-revise > revision.txt",
      story="Interro surprise ! Montre que les bases sont gravees dans tes doigts."),

    L(99, "Revision : la grande chaine",
      lesson="Le tube ultime : 'cat f1 f2 | sort | uniq > final.txt' fusionne, trie, dedup, sauve. "
             "Quatre outils, une ligne, zero souris. C'est ca, etre un admin.",
      mission="Fusionne f1.txt et f2.txt, trie, supprime les doublons, sauve dans final.txt — en UNE ligne.",
      setup=[F("f1.txt", "b\na\n"), F("f2.txt", "a\nc\n")],
      checks=[C_eq("final.txt", "a\nb\nc\n")],
      hints=["cat f1.txt f2.txt | sort | uniq > final.txt", "cat colle, sort trie, uniq dedup, > sauve."],
      solution="cat f1.txt f2.txt | sort | uniq > final.txt"),

    L(100, "MEGA-BOSS : 10 jours en un niveau",
      lesson="Examen final des jours 1-10 : mkdir, mv + joker, ls + redirection, grep. "
             "Reussis ca et tu passes officiellement 'Explorateur'.",
      mission="Dans l'arene : 1) cree range/ 2) deplaces-y les .txt de fouillis/ 3) liste range/ dans inventaire.txt "
              "4) verifie avec grep que inventaire contient 'a.txt'.",
      setup=[D("fouillis"), F("fouillis/a.txt", "a\n"), F("fouillis/b.txt", "b\n"), F("fouillis/photo.jpg", "p\n")],
      checks=[C_de("range"), C_fe("range/a.txt"), C_fe("range/b.txt"), C_fe("inventaire.txt"),
              C_fc("inventaire.txt", text="a.txt"), C_cmd(r"\bgrep\b[^\n]*a\.txt")],
      hints=["1) mkdir range", "2) mv fouillis/*.txt range/", "3) ls -1 range/ > inventaire.txt", "4) grep a.txt inventaire.txt"],
      solution="mkdir range && mv fouillis/*.txt range/ && ls -1 range/ > inventaire.txt && grep a.txt inventaire.txt",
      story="Le conseil des Admins observe ton examen final..mkdir, mv, ls, grep : montre-leur de quoi tu es capable.",
      xp=50, boss=True),
]
