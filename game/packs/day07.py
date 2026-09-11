"""Jour 7 (niveaux 61-70) : Redirections et tubes (pipes)."""

from .common import L, F, D, C_cmd, C_fe, C_fc, C_nempty

LEVELS = [
    L(61, "Ecrire avec >",
      lesson="'.' ENVOIE la sortie d'une commande dans un fichier (en ECrasant l'ancien contenu). "
             "'echo hello > salut.txt' : le fichier contient 'hello'.",
      mission="Cree salut.txt contenant 'hello' :  echo hello > salut.txt",
      checks=[C_fe("salut.txt"), C_fc("salut.txt", text="hello")],
      hints=["echo hello > salut.txt", "Le > dirige le texte vers le fichier."],
      solution="echo hello > salut.txt",
      story="Tu as un message a graver dans le marbre (enfin, dans un fichier). Une ligne suffit."),

    L(62, "Ajouter avec >>",
      lesson="'>>' AJOUTE a la fin du fichier sans effacer. '>' = remplacer, '>>' = completer. "
             "Confondre les deux a deja fait pleurer des admins : grave cette difference dans ta tete.",
      mission="Ajoute la ligne 'ligne2' a la fin de journal.txt (qui contient deja 'ligne1') avec >>.",
      setup=[F("journal.txt", "ligne1\n")],
      checks=[C_fc("journal.txt", text="ligne1"), C_fc("journal.txt", text="ligne2")],
      hints=["echo ligne2 >> journal.txt", ">> ajoute, > ecrase : ici il faut AJOUTER."],
      solution="echo ligne2 >> journal.txt"),

    L(63, "Fusionner avec cat et >",
      lesson="'cat a.txt b.txt > total.txt' : cat colle, '>' sauvegarde. C'est l'usine d'assemblage du terminal.",
      mission="Assemble haut.txt et bas.txt dans total.txt en une commande.",
      setup=[F("haut.txt", "tete\n"), F("bas.txt", "pieds\n")],
      checks=[C_fe("total.txt"), C_fc("total.txt", text="tete"), C_fc("total.txt", text="pieds")],
      hints=["cat haut.txt bas.txt > total.txt", "cat affiche les deux, > capture le tout."],
      solution="cat haut.txt bas.txt > total.txt"),

    L(64, "Capturer les erreurs (2>)",
      lesson="Les programmes parlent sur 2 canaux : 1 = sorties normales, 2 = erreurs. "
             "'2>' capture les erreurs seules. 'ls inexistant 2> erreurs.txt' : le message d'erreur part dans le fichier.",
      mission="Liste le fichier inexistant 'fantome' et capture l'erreur dans erreurs.txt :  ls fantome 2> erreurs.txt",
      checks=[C_fe("erreurs.txt"), C_nempty("erreurs.txt")],
      hints=["ls fantome 2> erreurs.txt", "2> = 'redirige le canal des erreurs'."],
      solution="ls fantome 2> erreurs.txt",
      story="Un fichier fantome hante l'arene. Capture son message d'outre-tombe dans un fichier."),

    L(65, "Tout capturer (2>&1)",
      lesson="'2>&1' dit : 'erreurs, rejoignez les sorties normales'. 'cmd > tout.txt 2>&1' met TOUT dans le fichier. "
             "C'est LE reflexe pour les logs complets.",
      mission="Liste ok.txt ET fantome en capturant sorties + erreurs dans tout.txt :  ls ok.txt fantome > tout.txt 2>&1",
      setup=[F("ok.txt", "ok\n")],
      checks=[C_fe("tout.txt"), C_fc("tout.txt", text="ok.txt")],
      hints=["ls ok.txt fantome > tout.txt 2>&1", "Ordre important : d'abord >, puis 2>&1."],
      solution="ls ok.txt fantome > tout.txt 2>&1"),

    L(66, "Le tube (|)",
      lesson="Le pipe '|' branche la sortie d'une commande sur l'entree de la suivante. "
             "'cat liste.txt | wc -l' : cat lit, wc compte les lignes. C'est ca, la magie UNIX : des petits outils qui s'emboitent.",
      mission="Compte les lignes de liste.txt avec un pipe :  cat liste.txt | wc -l",
      setup=[F("liste.txt", "un\ndeux\ntrois\nquatre\n")],
      checks=[C_cmd(r"\bcat\b[^\n]*\|[^\n]*\bwc\b")],
      hints=["cat liste.txt | wc -l", "Le | se tape avec AltGr+6 (ou Maj+\\)."],
      solution="cat liste.txt | wc -l",
      story="Deux commandes, un tube : bienvenue dans la plomberie UNIX. Ca coule tout seul."),

    L(67, "Pipe + sauvegarde",
      lesson="On peut chainer pipe ET redirection : 'ls -1 | head -n 2 > debut.txt' garde le debut de la liste dans un fichier.",
      mission="Garde les 2 premieres lignes de la liste des fichiers dans debut.txt :  ls -1 | head -n 2 > debut.txt",
      setup=[F("a.txt", "a\n"), F("b.txt", "b\n"), F("c.txt", "c\n")],
      checks=[C_fe("debut.txt"), C_nempty("debut.txt")],
      hints=["ls -1 | head -n 2 > debut.txt", "ls produit, head coupe, > sauvegarde."],
      solution="ls -1 | head -n 2 > debut.txt"),

    L(68, "Compter les fichiers",
      lesson="'ls -1 | wc -l' compte les fichiers d'un dossier. Un admin s'en sert 50 fois par jour : "
             "'combien de logs ? combien de sauvegardes ?'",
      mission="Compte les fichiers de l'arene et sauvegarde le resultat dans compte.txt :  ls -1 | wc -l > compte.txt",
      setup=[F("a.txt", "a\n"), F("b.txt", "b\n")],
      checks=[C_fe("compte.txt"), C_fc("compte.txt", regex=r"\d+")],
      hints=["ls -1 | wc -l > compte.txt", "wc -l compte, > sauvegarde."],
      solution="ls -1 | wc -l > compte.txt"),

    L(69, "Voir ET sauver (tee)",
      lesson="'tee' affiche ET ecrit dans un fichier en meme temps (comme un T de plomberie : ca continue tout droit + ca derive). "
             "'echo coucou | tee copie.txt' : tu vois 'coucou' ET il est sauve.",
      mission="Affiche 'coucou' tout en le sauvant dans copie.txt :  echo coucou | tee copie.txt",
      checks=[C_fe("copie.txt"), C_fc("copie.txt", text="coucou")],
      hints=["echo coucou | tee copie.txt", "tee = le T qui affiche + sauve."],
      solution="echo coucou | tee copie.txt"),

    L(70, "BOSS du jour : chaine de production",
      lesson="Revision : cat lit, | branche, wc compte, > sauve. Quatre outils, une chaine, zero effort.",
      mission="Compte les lignes de notes.txt et sauve le resultat dans stats.txt, en UNE ligne avec pipe + redirection.",
      setup=[F("notes.txt", "un\ndeux\ntrois\n")],
      checks=[C_fe("stats.txt"), C_fc("stats.txt", regex=r"3")],
      hints=["cat notes.txt | wc -l > stats.txt", "cat -> pipe -> wc -> redirection."],
      solution="cat notes.txt | wc -l > stats.txt",
      story="L'usine tourne a plein regime : la matiere (notes.txt) entre, la stat sort. Monte la chaine.",
      xp=25, boss=True),
]
