"""Saison 2 - Agent Cyber (niveaux 1001-1100, jours 101-110), ecrite a la main.

Missions facon TryHackMe : recrutement de l'agence, scans nmap, intrusions SSH,
chasse aux flags, craquage de mots de passe (john), forensics de logs,
enumeration web, pivot, escalation de privilees, examen final (mini-CTF).

Les cibles (nmap/ssh) sont simulees par game/fakebin ; tout le reste utilise
de VRAIES commandes Linux. Le scenario de chaque mission est dans "scenario".
"""

from .common import L, F, D, C_cmd, C_fe, C_fc, C_eq, C_nempty


def _port(port, service, version="", state="open"):
    return {"port": port, "service": service, "version": version, "state": state}


def _target(ip, ports=(), os_name="Linux 5.15", users=(), fs=None, banner=None):
    entry = {"os": os_name, "ports": list(ports)}
    if users:
        entry["users"] = list(users)
        entry["fs"] = fs if fs is not None else {}
        entry["banner"] = banner or "Welcome to Ubuntu 22.04 LTS (GNU/Linux)"
    return {ip: entry}


def _scen(*targets):
    hosts = {}
    for t in targets:
        hosts.update(t)
    return {"hosts": hosts}


AUTH_LOG = (
    "Sep 10 03:11:02 srv sshd[1201]: Failed password for root from 45.61.22.9 port 51231 ssh2\n"
    "Sep 10 03:11:19 srv sshd[1202]: Failed password for root from 45.61.22.9 port 51288 ssh2\n"
    "Sep 10 03:12:05 srv sshd[1203]: Failed password for invalid user admin from 45.61.22.9 port 51302 ssh2\n"
    "Sep 10 03:12:44 srv sshd[1204]: Failed password for root from 45.61.22.9 port 51401 ssh2\n"
    "Sep 10 03:13:12 srv sshd[1205]: Failed password for root from 91.44.10.2 port 41120 ssh2\n"
    "Sep 10 03:13:58 srv sshd[1206]: Failed password for root from 45.61.22.9 port 51555 ssh2\n"
    "Sep 10 03:14:20 srv sshd[1207]: Accepted password for marie from 192.168.1.20 port 60210 ssh2\n"
    "Sep 10 03:15:03 srv sshd[1208]: Failed password for root from 45.61.22.9 port 51672 ssh2\n"
    "Sep 10 03:15:47 srv sshd[1209]: Failed password for invalid user test from 91.44.10.2 port 41233 ssh2\n"
    "Sep 10 03:16:22 srv sshd[1210]: Failed password for root from 45.61.22.9 port 51790 ssh2\n"
    "Sep 10 03:17:09 srv sshd[1211]: Failed password for root from 203.0.113.7 port 33210 ssh2\n"
    "Sep 10 03:18:31 srv sshd[1212]: Failed password for root from 203.0.113.7 port 33312 ssh2\n"
    "Sep 10 03:19:02 srv sshd[1213]: Failed password for invalid user guest from 91.44.10.2 port 41440 ssh2\n"
    "Sep 10 03:20:15 srv sshd[1214]: Accepted password for marie from 192.168.1.20 port 60312 ssh2\n"
)

SITE_FILES = (
    D("site/admin"), D("site/.git"), D("site/js"), D("site/images"),
    F("site/index.html", "<html>\n<!-- DEBUG password=s3cr3t-avant-prod A RETIRER -->\n<h1>Bienvenue</h1>\n</html>\n"),
    F("site/robots.txt", "User-agent: *\nDisallow: /admin/\nDisallow: /backup/\n"),
    F("site/admin/index.html", "<h1>admin</h1>\n"),
    F("site/admin/config.bak", "db_pass=FLAG{web-1}\n"),
    F("site/.git/config", "[remote \"origin\"]\n\turl = git@git.pingouin.cie:site.git\n"),
    F("site/js/app.js", "// cle api : FLAG{web-2}\nconsole.log('ok');\n"),
    F("site/images/logo.png", "PNGFAKE\x00FLAG{web-3}\x00\n"),
    F("site/index.html~", "ancienne version 0.9, voir TODO\n"),
)


LEVELS = [
    # ============ JOUR 101 : bienvenue a l'agence (1001-1010) ============
    L(1001, "Ton premier flag",
      story="Bienvenue a l'agence, recrue ! Ici, les preuves s'appellent des FLAGS : des codes comme FLAG{...}. "
            "Ton premier est dans flag1.txt. Lis-le : tout agent commence par lire.",
      lesson="Un flag (drapeau) prouve que tu as reussi une tache : trouver un fichier, decoder un message... "
             "Format standard : FLAG{quelque-chose}. 'cat' l'affiche. Simple, non ?",
      mission="Lis le fichier flag1.txt avec cat.",
      setup=[F("flag1.txt", "FLAG{bienvenue-agent}\n")],
      checks=[C_cmd(r"\bcat\b[^\n;|&]*flag1")],
      hints=["cat flag1.txt", "cat affiche le contenu : ton premier flag !"],
      solution="cat flag1.txt"),

    L(1002, "C'est quoi ce fichier ?",
      story="On t'a remis un fichier 'mystere', sans extension, sans explication. Avant de l'ouvrir, "
            "un agent IDENTIFIE : c'est la commande 'file' qui parle.",
      lesson="'file' devine le type d'un fichier en lisant son contenu (pas son nom !). Texte, image, executable... "
             "Les extensions mentent, 'file' non.",
      mission="Identifie le fichier mystere : file mystere",
      setup=[F("mystere", "juste un texte secret\n")],
      checks=[C_cmd(r"(^|[;&|]\s*)\bfile\b")],
      hints=["file mystere", "file lit le contenu, pas le nom."],
      solution="file mystere"),

    L(1003, "L'empreinte MD5",
      story="Pour prouver qu'un document n'a pas ete modifie, l'agence calcule son EMPREINTE (hash MD5) : "
            "32 caracteres qui changent a la moindre virgule.",
      lesson="'md5sum fichier' calcule l'empreinte MD5 : une signature du contenu. "
             "Meme fichier = meme empreinte, toujours. Fichier modifie = empreinte differente.",
      mission="Calcule l'empreinte de doc.txt dans empreinte.txt : md5sum doc.txt > empreinte.txt",
      setup=[F("doc.txt", "document officiel\n")],
      checks=[C_cmd(r"\bmd5sum\b"), C_fc("empreinte.txt", regex=r"[0-9a-f]{32}")],
      hints=["md5sum doc.txt > empreinte.txt", "Une empreinte MD5 = 32 caracteres hexa."],
      solution="md5sum doc.txt > empreinte.txt"),

    L(1004, "L'empreinte SHA-256",
      story="MD5 commence a dater : pour les documents vraiment sensibles, l'agence utilise SHA-256 "
            "(64 caracteres, beaucoup plus solide).",
      lesson="'sha256sum' = la version musclée de md5sum : 64 caracteres, quasi-impossible a falsifier. "
             "C'est elle qui protege les telechargements, les blockchains, les mots de passe (avec du sel !).",
      mission="Calcule l'empreinte SHA-256 de doc.txt dans empreinte256.txt : sha256sum doc.txt > empreinte256.txt",
      setup=[F("doc.txt", "document officiel\n")],
      checks=[C_cmd(r"\bsha256sum\b"), C_fc("empreinte256.txt", regex=r"[0-9a-f]{64}")],
      hints=["sha256sum doc.txt > empreinte256.txt", "SHA-256 = 64 caracteres hexa."],
      solution="sha256sum doc.txt > empreinte256.txt"),

    L(1005, "Message code (base64)",
      story="Intercepte ennemie ! Le message est code en base64 (un alphabet bizarre plein de lettres et de '='). "
            "Decode-le : c'est souvent un flag qui se cache derriere.",
      lesson="Base64 transforme n'importe quoi en texte lisible (et inversement). Ce n'est PAS du chiffrement, "
             "juste un emballage : 'base64 -d' deballe. Les espions l'utilisent pour cacher des flags en pleine vue.",
      mission="Decode message.b64 dans clair.txt : base64 -d message.b64 > clair.txt",
      setup=[F("message.b64", "RkxBR3tiNjQtaW5pdGllfQ==\n")],
      checks=[C_fe("clair.txt"), C_fc("clair.txt", text="FLAG{b64-initie}")],
      hints=["base64 -d message.b64 > clair.txt", "-d = decode (deballe le message)."],
      solution="base64 -d message.b64 > clair.txt"),

    L(1006, "Coder un message",
      story="A ton tour d'envoyer un message code a l'agence ! Encode 'coucou' en base64 dans code.txt. "
            "Les espions codent aussi bien qu'ils decodent.",
      lesson="'echo texte | base64' emballe en base64. Sans '-d', base64 ENCODE. "
             "Dans les deux sens, c'est instantane : l'emballage prefere des flags.",
      mission="Encode 'coucou' en base64 dans code.txt : echo coucou | base64 > code.txt",
      checks=[C_cmd(r"\bbase64\b"), C_nempty("code.txt")],
      hints=["echo coucou | base64 > code.txt", "Sans -d, base64 encode."],
      solution="echo coucou | base64 > code.txt"),

    L(1007, "Lire dans le binaire",
      story="Un fichier binaire suspect (binaire.dat) : illisible avec cat ! Mais les textes caches dedans "
            "se voient avec 'strings'. Les mots de passe oublies adorent s'y cacher.",
      lesson="'strings' extrait les bouts de texte lisibles d'un fichier binaire. Executables, images, firmwares : "
             "tout contient des textes (messages, chemins, parfois des secrets...).",
      mission="Extrait les textes de binaire.dat dans textes.txt : strings binaire.dat > textes.txt",
      setup=[F("binaire.dat", "MZ\x00\x01FAKEBIN\x00FLAG{strings-1}\x00\x01\x02fin\n")],
      checks=[C_fe("textes.txt"), C_fc("textes.txt", text="FLAG{strings-1}")],
      hints=["strings binaire.dat > textes.txt", "strings peche les textes dans le binaire."],
      solution="strings binaire.dat > textes.txt"),

    L(1008, "Ratissage au grep",
      story="Le flag est cache QUELQUE PART dans le dossier indices/... mais ou ? Ratisse TOUT avec grep -r : "
            "aucun flag ne resiste au ratissage.",
      lesson="'grep -r MOTIF .' cherche dans TOUS les fichiers, tous les sous-dossiers. 'FLAG{' est le motif "
             "des chasseurs de flags : tous les flags commencent pareil !",
      mission="Trouve le flag cache : grep -r \"FLAG{\" . > trouvailles.txt",
      setup=[D("indices"), F("indices/a.txt", "rien ici\n"), F("indices/b.txt", "le flag est FLAG{piste-1}, chut\n")],
      checks=[C_fe("trouvailles.txt"), C_fc("trouvailles.txt", text="FLAG{piste-1}")],
      hints=["grep -r \"FLAG{\" . > trouvailles.txt", "-r = recursif : tout le dossier y passe."],
      solution="grep -r \"FLAG{\" . > trouvailles.txt"),

    L(1009, "Le fichier invisible",
      story="Un fichier INVISIBLE (commençant par un point) se cache ici. 'ls' seul ne le voit pas : "
            "il faut 'ls -a'. Puis lis-le et prouve ta trouvaille dans vu.txt.",
      lesson="Les fichiers commencant par '.' sont caches : configs, cles, ... et flags planques ! "
             "'ls -a' les revele. Un agent ne fait JAMAIS confiance a un simple 'ls'.",
      mission="Liste tout (y compris caches) puis lis .flag-cache dans vu.txt : ls -a, puis cat .flag-cache > vu.txt",
      setup=[F(".flag-cache", "FLAG{cache-1}\n"), F("normal.txt", "rien\n")],
      checks=[C_cmd(r"\bls\b[^\n;|&]*-a"), C_fc("vu.txt", text="FLAG{cache-1}")],
      hints=["1) ls -a (repere le fichier cache)", "2) cat .flag-cache > vu.txt"],
      solution="ls -a && cat .flag-cache > vu.txt"),

    L(1010, "BOSS : le dossier melange",
      story="Premier dossier d'enquete : doc.txt. L'agence veut : 1) son TYPE (file), 2) son empreinte MD5, "
            "3) le nombre de lignes contenant 'o'. Le tout dans hash.txt. Methodique, agent !",
      lesson="BOSS : enchainer file + md5sum + grep -c. Un vrai rapport d'analyse : type, empreinte, contenu. "
             "C'est exactement ce que fait un analyste en arrivant sur un fichier inconnu.",
      mission="1) file doc.txt  2) md5sum doc.txt > hash.txt  3) grep -c \"o\" doc.txt >> hash.txt",
      setup=[F("doc.txt", "rapport confidentiel\n")],
      checks=[C_cmd(r"(^|[;&|]\s*)\bfile\b"), C_fc("hash.txt", regex=r"[0-9a-f]{32}"),
              C_fc("hash.txt", regex=r"(?m)^1$")],
      hints=["1) file doc.txt", "2) md5sum doc.txt > hash.txt", "3) grep -c \"o\" doc.txt >> hash.txt"],
      solution="file doc.txt && md5sum doc.txt > hash.txt && grep -c \"o\" doc.txt >> hash.txt",
      xp=25, boss=True),

    # ============ JOUR 102 : reconnaissance (1011-1020) ============
    L(1011, "Premier scan",
      story="Objectif repere : 10.10.0.5. Avant toute intrusion, on OBSERVE : 'nmap' scanne la cible et liste "
            "ses ports ouverts. C'est legal ici : c'est NOTRE reseau d'entrainement.",
      lesson="'nmap CIBLE' = scanner les 1000 ports les plus courants. 'open' = une porte ouverte (un service). "
             "La reconnaissance ne casse rien : on regarde, on note. Les pros scannent TOUJOURS avant d'agir.",
      mission="Scanne 10.10.0.5 et sauve le rapport : nmap 10.10.0.5 > rapport.txt (le port 22 doit y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")])),
      checks=[C_cmd(r"\bnmap\b[^\n]*10\.10\.0\.5"), C_fc("rapport.txt", text="22")],
      hints=["nmap 10.10.0.5 > rapport.txt", "Cherche la ligne 'open' : c'est une porte ouverte."],
      solution="nmap 10.10.0.5 > rapport.txt"),

    L(1012, "La porte du web",
      story="Nouvelle cible, nouveau scan : 10.10.0.5 heberge-t-il un site web ? Le port 80 (HTTP) "
            "le dira. Scanne et note dans web.txt.",
      lesson="Port 80 = HTTP (web), 443 = HTTPS (web securise), 22 = SSH, 21 = FTP... Les ports sont des numeros "
             "de porte : chacun mene a un service. Les connaitre par coeur = parler reseau couramment.",
      mission="Scanne 10.10.0.5 dans web.txt : nmap 10.10.0.5 > web.txt (le port 80 doit y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(80, "http", "Apache 2.4.41")])),
      checks=[C_fe("web.txt"), C_fc("web.txt", text="80")],
      hints=["nmap 10.10.0.5 > web.txt", "Port 80 = la porte du web."],
      solution="nmap 10.10.0.5 > web.txt"),

    L(1013, "Trois portes ouvertes",
      story="Cette cible a TROIS portes ouvertes. Trouve-les toutes (22, 80, 443) et archive le scan "
            "dans complet.txt. Un agent ne laisse passer aucune porte.",
      lesson="Plus il y a de portes ouvertes, plus il y a d'entrees possibles... pour toi ET pour les attaquants. "
             "Compter les ports ouverts = mesurer la surface d'attaque.",
      mission="Scanne 10.10.0.5 dans complet.txt : les ports 22, 80 et 443 doivent y figurer.",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9"),
                                           _port(80, "http", "Apache 2.4.41"),
                                           _port(443, "https", "Apache 2.4.41")])),
      checks=[C_fc("complet.txt", text="22"), C_fc("complet.txt", text="80"), C_fc("complet.txt", text="443")],
      hints=["nmap 10.10.0.5 > complet.txt", "22 (ssh), 80 (web), 443 (web securise) : les trois classiques."],
      solution="nmap 10.10.0.5 > complet.txt"),

    L(1014, "Les versions parlent (-sV)",
      story="Savoir qu'une porte est ouverte, c'est bien. Savoir QUEL logiciel la garde (et sa version), "
            "c'est mieux : 'nmap -sV' interroge les services. Les vieilles versions = des failles connues !",
      lesson="'-sV' = detection de versions (ex: OpenSSH 8.9, Apache 2.4.41). Ensuite, on cherche 'OpenSSH 8.9 faille' "
             "dans les bases de vulnerabilites. C'est comme ca que naissent les plans d'attaque... et de defense.",
      mission="Scanne avec versions : nmap -sV 10.10.0.5 > versions.txt (OpenSSH doit y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9p1"),
                                           _port(80, "http", "Apache httpd 2.4.41")])),
      checks=[C_cmd(r"\bnmap\b[^\n]*-sV"), C_fc("versions.txt", text="OpenSSH")],
      hints=["nmap -sV 10.10.0.5 > versions.txt", "-sV = s'il vous plait, les Versions !"],
      solution="nmap -sV 10.10.0.5 > versions.txt"),

    L(1015, "Deviner le systeme (-O)",
      story="Linux ? Windows ? Routeur ? 'nmap -O' devine le SYSTEME d'exploitation en analysant les reponses. "
            "Connaitre l'OS = choisir les bons outils pour la suite.",
      lesson="'-O' = detection d'OS (fingerprinting). Chaque systeme repond legerement differemment aux paquets : "
             "nmap compare et devine. Precision bluffante, rien qu'en observant.",
      mission="Detecte l'OS : nmap -O 10.10.0.5 > os.txt (Linux doit y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], os_name="Linux 5.15")),
      checks=[C_cmd(r"\bnmap\b[^\n]*-O"), C_fc("os.txt", text="Linux")],
      hints=["nmap -O 10.10.0.5 > os.txt", "-O comme OS (Operating System)."],
      solution="nmap -O 10.10.0.5 > os.txt"),

    L(1016, "Cible eteinte",
      story="Tu scannes 10.10.0.99... et RIEN. 'Host seems down' : la machine ne repond pas (eteinte ? inexistante ?). "
            "Un bon agent note aussi les echecs : archive dans etat.txt.",
      lesson="'Host seems down' = la cible ne repond pas aux pings. Soit elle est eteinte, soit elle filtre. "
             "Dans la vraie vie, on reessaie avec -Pn (sans ping)... ici, on note et on passe a la suivante.",
      mission="Scanne 10.10.0.99 dans etat.txt : nmap 10.10.0.99 > etat.txt (le mot 'down' doit y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")])),
      checks=[C_fe("etat.txt"), C_fc("etat.txt", text="down")],
      hints=["nmap 10.10.0.99 > etat.txt", "'Host seems down' : elle ne repond pas. Note-le !"],
      solution="nmap 10.10.0.99 > etat.txt"),

    L(1017, "Porte filttee",
      story="Etrange : le port 23 (telnet) est 'filtered' — ni ouvert ni ferme, un pare-feu le bloque. "
            "Archive le scan : les pare-feu aussi font partie du rapport.",
      lesson="'filtered' = un pare-feu jette les paquets sans repondre. Ca revele une defense (bien !) mais aussi "
             "un service a proteger (interessant...). open/closed/filtered : les trois visages d'un port.",
      mission="Scanne 10.10.0.5 dans filtrage.txt ('filtered' et '22' doivent y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9"),
                                           _port(23, "telnet", state="filtered")])),
      checks=[C_fc("filtrage.txt", text="filtered"), C_fc("filtrage.txt", text="22")],
      hints=["nmap 10.10.0.5 > filtrage.txt", "filtered = pare-feu silencieux. Note-le dans le rapport."],
      solution="nmap 10.10.0.5 > filtrage.txt"),

    L(1018, "Le grand scan",
      story="Mission complete : ports + versions + OS, d'un coup ! 'nmap -sV -O' : l'artillerie lourde "
            "de la reconnaissance. Rapport dans grand-scan.txt.",
      lesson="'-sV -O' combines : versions des services + systeme d'exploitation. C'est LE scan standard "
             "d'un audit : complet, mais encore discret. (Les scans agressifs, c'est pour plus tard.)",
      mission="Grand scan : nmap -sV -O 10.10.0.5 > grand-scan.txt (Apache et Linux doivent y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9p1"),
                                           _port(80, "http", "Apache httpd 2.4.41")], os_name="Linux 5.15")),
      checks=[C_fc("grand-scan.txt", text="Apache"), C_fc("grand-scan.txt", text="Linux")],
      hints=["nmap -sV -O 10.10.0.5 > grand-scan.txt", "-sV = versions, -O = OS. Les deux !"],
      solution="nmap -sV -O 10.10.0.5 > grand-scan.txt"),

    L(1019, "Deux cibles",
      story="Deux machines a reconnaitre : 10.10.0.5 et 10.10.0.6. Scanne-les separement (scan-a.txt, scan-b.txt) : "
            "un rapport par cible, toujours. La rigueur fait l'agent.",
      lesson="Un rapport PAR cible : la regle d'or. Melanger deux scans dans un fichier, c'est la confusion assuree. "
             "Deux cibles = deux scans = deux fichiers.",
      mission="Scanne 10.10.0.5 dans scan-a.txt (port 22) et 10.10.0.6 dans scan-b.txt (port 80).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")]),
                     _target("10.10.0.6", [_port(80, "http", "nginx 1.18.0")])),
      checks=[C_fc("scan-a.txt", text="22"), C_fc("scan-b.txt", text="80")],
      hints=["1) nmap 10.10.0.5 > scan-a.txt", "2) nmap 10.10.0.6 > scan-b.txt"],
      solution="nmap 10.10.0.5 > scan-a.txt && nmap 10.10.0.6 > scan-b.txt"),

    L(1020, "BOSS : audit express",
      story="BOSS : audit express de 10.10.0.5 ! Ports + versions : trouve le SSH (22/OpenSSH) et la base "
            "de donnees MySQL (3306). Rapport dans audit.txt. L'agence attend ton rapport, agent.",
      lesson="BOSS de reconnaissance : '-sV' + lecture methodique. Port 3306 = MySQL : une base de donnees ouverte, "
             "c'est une mine d'or... ou une catastrophe. Tout est dans le rapport.",
      mission="Audit : nmap -sV 10.10.0.5 > audit.txt (22, OpenSSH et mysql doivent y figurer).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9p1"),
                                           _port(3306, "mysql", "MariaDB 10.6.7")])),
      checks=[C_fc("audit.txt", text="22"), C_fc("audit.txt", text="OpenSSH"), C_fc("audit.txt", text="mysql")],
      hints=["nmap -sV 10.10.0.5 > audit.txt", "22 = SSH, 3306 = MySQL. Trouve les deux + la version SSH."],
      solution="nmap -sV 10.10.0.5 > audit.txt",
      xp=25, boss=True),

    # ============ JOUR 103 : connexion SSH (1021-1030) ============
    L(1021, "Ta cle d'agent",
      story="Pour te connecter aux machines sans mot de passe, il te faut ta CLE d'agent : une paire "
            "privee/publique. Forge-la avec ssh-keygen. C'est ton badge numerique.",
      lesson="'ssh-keygen -t ed25519 -f ./macle -N \"\"' : cree macle (privee, SECRETE) + macle.pub (publique, "
             "a distribuer). La privee ne voyage JAMAIS. La connexion par cle : pas de mot de passe a voler !",
      mission="Cree une cle ed25519 : ssh-keygen -t ed25519 -f ./macle -N \"\"",
      checks=[C_fe("macle"), C_fe("macle.pub")],
      hints=["ssh-keygen -t ed25519 -f ./macle -N \"\"", "-t = type, -f = fichier, -N = mot de passe vide."],
      solution="ssh-keygen -t ed25519 -f ./macle -N \"\""),

    L(1022, "Premiere connexion",
      story="Le grand moment : connecte-toi a 10.10.0.5 en tant qu'agent ! 'ssh agent@10.10.0.5'. "
            "Ta cle est deja autorisee la-bas (c'est l'agence qui l'a deposee). Explore, puis tape 'exit'.",
      lesson="'ssh UTILISATEUR@CIBLE' : la connexion chiffree. Dedans, c'est un vrai shell distant : "
             "ls, cd, cat, pwd... et 'exit' pour revenir. Bienvenue dans la machine !",
      mission="Connecte-toi : ssh agent@10.10.0.5 (explore avec ls/cat, puis exit).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"bienvenue.txt": "bienvenue agent\n"}}})),
      checks=[C_cmd(r"\bssh\b[^\n]*agent@10\.10\.0\.5")],
      hints=["ssh agent@10.10.0.5", "Dedans : ls, cat bienvenue.txt... puis exit pour revenir."],
      solution="ssh agent@10.10.0.5"),

    L(1023, "Le flag distant",
      story="Un flag dort sur la cible : /home/agent/flag.txt. Connecte-toi, lis-le, puis RECOPIE-LE "
            "dans reponse.txt ICI (en local). Les flags se ramenent a la base !",
      lesson="Exfiltration de flag : 1) ssh vers la cible, 2) cat le flag, 3) exit, 4) echo le flag dans un fichier "
             "local. Lire a distance, prouver en local : le rituel du CTF.",
      mission="Lis /home/agent/flag.txt sur la cible et recopie le flag dans reponse.txt (local).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"flag.txt": "FLAG{ssh-1}\n"}}})),
      checks=[C_fc("reponse.txt", text="FLAG{ssh-1}")],
      hints=["1) ssh agent@10.10.0.5, 2) cat flag.txt, 3) exit",
             "4) echo FLAG{...} > reponse.txt (avec le flag lu)"],
      solution="ssh agent@10.10.0.5 puis cat flag.txt puis exit puis echo du flag > reponse.txt"),

    L(1024, "Le serveur web de la cible",
      story="La cible heberge un site dans /var/www/ ! Connecte-toi, va dans /var/www, lis le flag, "
            "et ramene-le dans web-loot.txt. Les serveurs web oublient souvent des flags...",
      lesson="Apres 'ssh', on explore comme en local : 'cd /var/www', 'ls', 'cat flag.txt'. "
             "Les dossiers interessants : /var/www (web), /home (utilisateurs), /tmp (oublis), /opt (applis).",
      mission="Sur la cible : cd /var/www, lis flag.txt, recopie-le dans web-loot.txt (local).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {}}, "var": {"www": {"flag.txt": "FLAG{ssh-web}\n"}}})),
      checks=[C_cmd(r"\bssh\b"), C_fc("web-loot.txt", text="FLAG{ssh-web}")],
      hints=["ssh agent@10.10.0.5, puis cd /var/www, cat flag.txt, exit",
             "Puis en local : echo FLAG{...} > web-loot.txt"],
      solution="ssh agent@10.10.0.5, cd /var/www, cat flag.txt, exit, echo du flag > web-loot.txt"),

    L(1025, "Qui suis-je, la-bas ?",
      story="Sur la cible, es-tu bien 'agent' ? Verifie avec 'whoami' et 'pwd' DANS la session SSH, "
            "puis note le nom dans carnet.txt (local). On ne fait confiance a personne : on verifie.",
      lesson="'whoami' et 'pwd' marchent aussi a distance : apres un ssh, TOUJOURS verifier qui on est et ou on est. "
             "Les pros le font par reflexe : une erreur d'utilisateur = une catastrophe.",
      mission="En SSH : whoami + pwd. Puis en local, note le nom distant dans carnet.txt.",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"note.txt": "rien\n"}}})),
      checks=[C_cmd(r"\bssh\b"), C_fc("carnet.txt", text="agent")],
      hints=["ssh agent@10.10.0.5, tape whoami et pwd, exit", "Puis : echo agent > carnet.txt"],
      solution="ssh agent@10.10.0.5, whoami, pwd, exit, echo agent > carnet.txt"),

    L(1026, "Le flag planque",
      story="Cette fois, le flag est CACHE (fichier commencant par un point) dans le dossier de l'agent distant. "
            "'ls -a' a distance, 'cat' le fichier, ramene dans cache-loot.txt.",
      lesson="Les flags caches existent aussi a distance ! 'ls -a' DANS la session SSH revele les fichiers "
             "invisibles. Meme reflexes qu'en local, juste... ailleurs.",
      mission="En SSH : trouve le fichier cache (.cache/note.txt), lis-le, recopie dans cache-loot.txt (local).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {".cache": {"note.txt": "FLAG{ssh-cache}\n"}}}})),
      checks=[C_fc("cache-loot.txt", text="FLAG{ssh-cache}")],
      hints=["ssh agent@10.10.0.5, puis ls -a, cat .cache/note.txt, exit",
             "Puis en local : echo FLAG{...} > cache-loot.txt"],
      solution="ssh + ls -a + cat .cache/note.txt + exit + echo du flag > cache-loot.txt"),

    L(1027, "Le code du coffre",
      story="Sur la cible, un fichier code.txt contient un code a 4 chiffres. Lis-le a distance, "
            "recopie le code dans code.txt (local). Les codes ouvrent des portes... plus tard.",
      lesson="Tout ne s'exfiltre pas en un flag : parfois c'est un code, un mot de passe, une note. "
             "La methode reste la meme : lire a distance (cat), recopier en local (echo >).",
      mission="Lis code.txt sur la cible (code: 7399) et recopie le code dans code.txt (local).",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"code.txt": "code: 7399\n"}}})),
      checks=[C_fc("code.txt", text="7399")],
      hints=["ssh agent@10.10.0.5, cat code.txt, exit", "Puis : echo 7399 > code.txt"],
      solution="ssh + cat code.txt + exit + echo 7399 > code.txt"),

    L(1028, "Mauvais utilisateur !",
      story="Tu essaies 'ssh root@10.10.0.5'... REFUSE ('Permission denied') : seul 'agent' est autorise ! "
            "C'est normal : root par SSH, c'est interdit (bonne pratique). Recommence en agent et ramene flag2.",
      lesson="'Permission denied (publickey)' = mauvais utilisateur ou cle non autorisee. Et c'est BIEN que root "
             "soit refuse : autoriser root en SSH, c'est offrir le royaume. Les pros se connectent en user, jamais root.",
      mission="1) Essaie ssh root@10.10.0.5 (echec normal)  2) Connecte-toi en agent, ramene flag2.txt > butin2.txt.",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"flag2.txt": "FLAG{ssh-2}\n"}}})),
      checks=[C_cmd(r"\bssh\b[^\n]*root@10\.10\.0\.5"), C_fc("butin2.txt", text="FLAG{ssh-2}")],
      hints=["1) ssh root@10.10.0.5 (observe le refus, c'est la lecon !)",
             "2) ssh agent@10.10.0.5, cat flag2.txt, exit, echo > butin2.txt"],
      solution="ssh root@10.10.0.5 puis ssh agent@10.10.0.5, cat flag2.txt, exit, echo > butin2.txt"),

    L(1029, "Connexion avec cle precise",
      story="Tu as plusieurs cles ? Precise laquelle avec '-i' : 'ssh -i macle agent@10.10.0.5'. "
            "Cree d'abord ta cle (comme au niveau 1021), connecte-toi avec, ramene flag3.",
      lesson="'-i macle' = 'utilise CETTE cle-ci'. Avec plusieurs cles (perso, travail, agence...), "
             "on precise toujours. Sinon SSH essaie dans l'ordre... et peut se faire bloquer. Precision !",
      mission="Cree ta cle (macle), connecte-toi avec -i, ramene flag3.txt dans butin3.txt.",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"flag3.txt": "FLAG{ssh-3}\n"}}})),
      checks=[C_cmd(r"\bssh\b[^\n]*-i[^\n]*agent@"), C_fc("butin3.txt", text="FLAG{ssh-3}")],
      hints=["1) ssh-keygen -t ed25519 -f ./macle -N \"\"",
             "2) ssh -i macle agent@10.10.0.5, cat flag3.txt, exit, echo > butin3.txt"],
      solution="ssh-keygen... puis ssh -i macle agent@10.10.0.5, cat flag3.txt, exit, echo > butin3.txt"),

    L(1030, "BOSS : intrusion complete",
      story="BOSS : intrusion COMPLETE, en solo ! 1) Forge ta cle 2) Connecte-toi 3) Lis final.txt "
            "4) Ramene le flag dans rapport.txt. Sans aide, comme un grand. L'agence observe...",
      lesson="BOSS SSH : keygen + ssh + cat + exfiltration. La boucle complete d'un acces legitime : "
             "cle, connexion, lecture, preuve locale. Maitrise ca, et tu sais 'entrer' proprement.",
      mission="Cle + connexion + lecture de final.txt + flag dans rapport.txt.",
      scenario=_scen(_target("10.10.0.5", [_port(22, "ssh", "OpenSSH 8.9")], users=["agent"],
                             fs={"home": {"agent": {"final.txt": "FLAG{ssh-final}\n"}}})),
      checks=[C_fe("macle"), C_fe("macle.pub"), C_fc("rapport.txt", text="FLAG{ssh-final}")],
      hints=["1) ssh-keygen -t ed25519 -f ./macle -N \"\"",
             "2) ssh -i macle agent@10.10.0.5, cat final.txt, exit",
             "3) echo FLAG{...} > rapport.txt"],
      solution="keygen + ssh -i macle agent@10.10.0.5 + cat final.txt + exit + echo > rapport.txt",
      xp=25, boss=True),

    # ============ JOUR 104 : chasse aux flags (1031-1040) ============
    L(1031, "La planque invisible",
      story="Un flag dort dans un fichier invisible (.planque). Liste TOUT dans liste.txt (avec -a !), "
            "puis lis-le. Les planques invisibles sont la base du metier.",
      lesson="'ls -a > liste.txt' : la photo complete, caches inclus. Puis 'cat .planque'. "
             "Ordre de mission d'un agent : TOUJOURS regarder les caches. Toujours.",
      mission="1) ls -a > liste.txt  2) cat .planque (lis le flag).",
      setup=[F(".planque", "FLAG{planque-1}\n"), F("decoy.txt", "rien\n")],
      checks=[C_fc("liste.txt", text=".planque"), C_cmd(r"\bcat\b[^\n]*planque")],
      hints=["1) ls -a > liste.txt", "2) cat .planque"],
      solution="ls -a > liste.txt && cat .planque"),

    L(1032, "Enterre profond",
      story="Le drapeau (drapeau.txt) est enterre SOUS des sous-dossiers. Tu ne sais pas ou : 'find' le denichera. "
            "Prouve sa position dans piste.txt.",
      lesson="'find . -name \"*drapeau*\"' : le chien truffier. Il renifle les noms dans TOUT l'arbre. "
             "Les flags enterres profond ne resistent pas a find.",
      mission="Localise drapeau.txt : find . -name \"*drapeau*\" > piste.txt",
      setup=[D("a/b"), F("a/b/drapeau.txt", "FLAG{profond-1}\n"), F("a/lisez.txt", "rien\n")],
      checks=[C_fe("piste.txt"), C_fc("piste.txt", text="drapeau")],
      hints=["find . -name \"*drapeau*\" > piste.txt", "Les guillemets protegent le * : c'est find qui cherche."],
      solution="find . -name \"*drapeau*\" > piste.txt"),

    L(1033, "Dans le fouillis",
      story="Le dossier fouillis/ contient des dizaines de fichiers... et UN flag. Ratisse avec grep -r "
            "et mets le butin dans butin.txt.",
      lesson="'grep -r FLAG fouillis/ > butin.txt' : ratissage + preuve ecrite. Le motif 'FLAG' suffit : "
             "tous les flags le contiennent. Ratisse large, prouve par ecrit.",
      mission="Ratisse : grep -r FLAG fouillis/ > butin.txt",
      setup=[D("fouillis"), F("fouillis/n1.txt", "rien\n"), F("fouillis/n2.txt", "toujours rien\n"),
             F("fouillis/n3.txt", "ah ! FLAG{fouille-1} ici !\n")],
      checks=[C_fe("butin.txt"), C_fc("butin.txt", text="FLAG{fouille-1}")],
      hints=["grep -r FLAG fouillis/ > butin.txt", "grep -r fouille le dossier ET ses sous-dossiers."],
      solution="grep -r FLAG fouillis/ > butin.txt"),

    L(1034, "Trouve ET lis (-exec)",
      story="Niveau avance : trouve tresor.txt ET lis-le, en UNE commande ! 'find ... -exec cat {} \\;' : "
            "find cherche, cat lit. Les agents presses adorent.",
      lesson="'-exec cat {} \\;' : pour chaque fichier trouve, execute 'cat' dessus. '{}' = le fichier trouve, "
             "'\\;' = fin de l'ordre. Chercher ET agir en une ligne : la signature des pros.",
      mission="Trouve et lis : find . -name tresor.txt -exec cat {} \\; > tresor-lu.txt",
      setup=[D("x/y"), F("x/y/tresor.txt", "FLAG{tresor-1}\n")],
      checks=[C_fe("tresor-lu.txt"), C_fc("tresor-lu.txt", text="FLAG{tresor-1}")],
      hints=["find . -name tresor.txt -exec cat {} \\; > tresor-lu.txt",
             "{} = le fichier trouve, \\; = fin. Ne pas oublier l'espace avant \\;."],
      solution="find . -name tresor.txt -exec cat {} \\; > tresor-lu.txt"),

    L(1035, "Alerte dans les logs",
      story="Le fichier gros.log fait 20 lignes... dont UNE avec une ALERTE et un flag. Filtre avec grep "
            "dans alerte.txt. Les logs mentent rarement.",
      lesson="'grep ALERTE gros.log > alerte.txt' : filtrer le signal dans le bruit. Les analystes passent leur vie "
             "a filtrer des logs : 99% de bruit, 1% d'alerte. Et c'est ce 1% qui compte.",
      mission="Filtre l'alerte : grep ALERTE gros.log > alerte.txt",
      setup=[F("gros.log", "log ok 1\nlog ok 2\nlog ok 3\nlog ok 4\nlog ok 5\nlog ok 6\nlog ok 7\n"
                           "log ok 8\nlog ok 9\nlog ok 10\nlog ok 11\nlog ok 12\nlog ok 13\nlog ok 14\n"
                           "log ok 15\nlog ok 16\nlog ok 17\nALERTE FLAG{alerte-1} intrusion !\nlog ok 19\nlog ok 20\n")],
      checks=[C_fe("alerte.txt"), C_fc("alerte.txt", text="FLAG{alerte-1}")],
      hints=["grep ALERTE gros.log > alerte.txt", "Une ligne sur vingt : grep la trouve en un clin d'oeil."],
      solution="grep ALERTE gros.log > alerte.txt"),

    L(1036, "Dans le binaire",
      story="Le programme prog.bin cache un flag dans ses entrailles. 'strings' l'extrait, 'grep FLAG' le peche. "
            "Les deux, en pipe, dans trouve.txt.",
      lesson="'strings prog.bin | grep FLAG > trouve.txt' : extraire PUIS filtrer. Le pipe branche les outils : "
             "strings sort des pages de texte, grep ne garde que le flag. Du grand art.",
      mission="Extrais et peche : strings prog.bin | grep FLAG > trouve.txt",
      setup=[F("prog.bin", "\x7fELF\x00\x02\x01\x00start\x00FLAG{binaire-1}\x00end\x00\n")],
      checks=[C_fe("trouve.txt"), C_fc("trouve.txt", text="FLAG{binaire-1}")],
      hints=["strings prog.bin | grep FLAG > trouve.txt", "strings extrait, grep peche, > sauve."],
      solution="strings prog.bin | grep FLAG > trouve.txt"),

    L(1037, "Poupee russe",
      story="Diabolique : le flag est code en base64... DEUX FOIS ! Decode etape1.b64 vers etape2.b64, "
            "puis vers final.txt. Les poupees russes n'effraient pas un agent.",
      lesson="Double encodage = double decodage. 'base64 -d etape1.b64 > etape2.b64 && base64 -d etape2.b64 > final.txt'. "
             "Si le resultat ressemble encore a du charabia, decode ENCORE.",
      mission="Decode deux fois : base64 -d etape1.b64 > etape2.b64 puis base64 -d etape2.b64 > final.txt",
      setup=[F("etape1.b64", "Umt4QlIzdHdiM1Z3WldVdGNuVnpjMlY5\n")],
      checks=[C_fe("final.txt"), C_fc("final.txt", text="FLAG{poupee-russe}")],
      hints=["1) base64 -d etape1.b64 > etape2.b64", "2) base64 -d etape2.b64 > final.txt"],
      solution="base64 -d etape1.b64 > etape2.b64 && base64 -d etape2.b64 > final.txt"),

    L(1038, "Le fichier a espaces",
      story="Piege classique : le fichier s'appelle 'mon flag.txt' (AVEC un espace). 'cat mon flag.txt' echoue ! "
            "Il faut des guillemets. Lis-le dans lu.txt.",
      lesson="Les espaces cassent les commandes : le shell voit DEUX arguments. 'cat \"mon flag.txt\"' : "
             "les guillemets collent le nom en UN argument. Les attaquants ADORENT les noms pieges.",
      mission="Lis le fichier a espaces : cat \"mon flag.txt\" > lu.txt",
      setup=[F("mon flag.txt", "FLAG{espaces-1}\n")],
      checks=[C_fe("lu.txt"), C_fc("lu.txt", text="FLAG{espaces-1}")],
      hints=["cat \"mon flag.txt\" > lu.txt", "Sans guillemets, le shell voit deux fichiers. Avec : un seul."],
      solution="cat \"mon flag.txt\" > lu.txt"),

    L(1039, "Combien de flags ?",
      story="Le fichier melange.txt contient PLUSIEURS flags colles au texte. Compte-les EXACTEMENT : "
            "'grep -o' sort chaque flag sur sa ligne, 'wc -l' compte. Resultat dans nombre.txt.",
      lesson="'grep -o \"FLAG{[^}]*}\"' : -o = SEULEMENT le morceau qui matche (un par ligne). Puis '| wc -l' compte. "
             "Extraire PUIS compter : la methode officielle de l'inventaire.",
      mission="Compte : grep -o \"FLAG{[^}]*}\" melange.txt | wc -l > nombre.txt (attendu : 3).",
      setup=[F("melange.txt", "xxFLAG{m1}yy FLAG{m2} zzFLAG{m3}ww\n")],
      checks=[C_eq("nombre.txt", "3\n")],
      hints=["grep -o \"FLAG{[^}]*}\" melange.txt | wc -l > nombre.txt",
             "-o = un match par ligne, wc -l compte les lignes."],
      solution="grep -o \"FLAG{[^}]*}\" melange.txt | wc -l > nombre.txt"),

    L(1040, "BOSS : le grand inventaire",
      story="BOSS : inventaire TOTAL du dossier affaire/ ! Extrais TOUS les flags (y compris caches), "
            "tries, dans tous.txt. 'grep -r -h -o ... | sort' : la formule magique de l'inventaire.",
      lesson="BOSS : 'grep -r -h -o \"FLAG{[^}]*}\" affaire/ | sort > tous.txt'. -r = partout, -h = sans noms de "
             "fichiers, -o = que les flags, sort = ranges. L'inventaire parfait, en une ligne.",
      mission="Inventaire : grep -r -h -o \"FLAG{[^}]*}\" affaire/ | sort > tous.txt",
      setup=[D("affaire/profond"), F("affaire/.cache1", "FLAG{boss-a}\n"),
             F("affaire/profond/x.txt", "bla FLAG{boss-b} bla\n"), F("affaire/rien.txt", "rien\n")],
      checks=[C_eq("tous.txt", "FLAG{boss-a}\nFLAG{boss-b}\n")],
      hints=["grep -r -h -o \"FLAG{[^}]*}\" affaire/ | sort > tous.txt",
             "-r partout, -h sans noms, -o que les flags, sort pour ranger."],
      solution="grep -r -h -o \"FLAG{[^}]*}\" affaire/ | sort > tous.txt",
      xp=25, boss=True),

    # ============ JOUR 105 : mots de passe (1041-1050) ============
    L(1041, "Premier craquage",
      story="On a vole (legalement, c'est l'entrainement) un hash MD5 : celui du mot de passe de 'admin'. "
            "Avec une petite wordlist et 'john', craque-le en quelques secondes !",
      lesson="'john --wordlist=mots.txt hash.txt' : John the Ripper essaie chaque mot de la wordlist, "
             "calcule son hash, compare. Si ca matche : GAGNE. Les mots de passe faibles tombent en secondes.",
      mission="Craque : john --wordlist=mots1.txt hash1.txt puis note le mot de passe dans password.txt.",
      setup=[F("hash1.txt", "admin:23206deb7eba65b3fbc80a2ffbc53c28\n"),
             F("mots1.txt", "azerty\nsoleil\n123456\ndragon\nbonjour\nmdp\nsoleil\ncafé\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("password.txt", text="soleil")],
      hints=["1) john --wordlist=mots1.txt hash1.txt (lis le mot trouve !)",
             "2) echo soleil > password.txt"],
      solution="john --wordlist=mots1.txt hash1.txt puis echo soleil > password.txt"),

    L(1042, "Craquage SHA-1",
      story="Nouveau hash, format SHA-1 (40 caracteres) ! Meme methode : john + wordlist. "
            "Le format change, la faiblesse reste : un mot courant.",
      lesson="SHA-1 = 40 caracteres hexa. Plus long que MD5, mais un mot faible reste faible : "
             "john s'en moque, il compare betement. La robustesse vient du MOT, pas (seulement) de l'algo.",
      mission="Craque : john --wordlist=mots2.txt hash2.txt puis note dans password2.txt.",
      setup=[F("hash2.txt", "user:0acc7fadbc8e372aa5774ce7d593474e2e61f159\n"),
             F("mots2.txt", "lune\neclipse\nstars\nnuit\nsoleil\njour\nmatin\nsoir\npluie\nvent\nneige\norage\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("password2.txt", text="eclipse")],
      hints=["1) john --wordlist=mots2.txt hash2.txt", "2) echo eclipse > password2.txt"],
      solution="john --wordlist=mots2.txt hash2.txt puis echo eclipse > password2.txt"),

    L(1043, "Craquage SHA-256",
      story="SHA-256 (64 caracteres), l'algo des grands... avec un mot de passe RIDICULE. "
            "Prouve que meme SHA-256 ne sauve pas 'nebuleuse'.",
      lesson="SHA-256 protege contre la falsification, PAS contre les mots faibles ! Un hash, c'est a sens unique "
             "(on ne 'decode' pas), mais john DEVINE en comparant. Mot faible = craque, quel que soit l'algo.",
      mission="Craque : john --wordlist=mots3.txt hash3.txt puis note dans password3.txt.",
      setup=[F("hash3.txt", "chef:30484fb82db58d3309bcede01203578edca7d8ec09a2b202e92830238c6ee503\n"),
             F("mots3.txt", "galaxie\nnebuleuse\nquasar\ncomete\norbite\nsaturne\njupiter\nmars\nvenus\nterre\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("password3.txt", text="nebuleuse")],
      hints=["1) john --wordlist=mots3.txt hash3.txt", "2) echo nebuleuse > password3.txt"],
      solution="john --wordlist=mots3.txt hash3.txt puis echo nebuleuse > password3.txt"),

    L(1044, "Reconnaitre un MD5",
      story="Avant de craquer, un agent IDENTIFIE le hash : 32 caracteres hexa = MD5, 40 = SHA-1, 64 = SHA-256. "
            "Regarde hash4.txt et note son type dans type.txt.",
      lesson="La longueur trahit l'algo : 32 = MD5, 40 = SHA-1, 64 = SHA-256. 'cat' le hash, compte (a l'oeil, "
             "32 c'est court, 64 c'est long), note le type. Identification avant action, toujours.",
      mission="1) cat hash4.txt  2) echo md5 > type.txt (c'est un MD5, 32 caracteres).",
      setup=[F("hash4.txt", "de05930dd46a984ca32aad9feac718e8\n")],
      checks=[C_cmd(r"\bcat\b"), C_fc("type.txt", text="md5")],
      hints=["1) cat hash4.txt (compte : 32 caracteres = MD5)", "2) echo md5 > type.txt"],
      solution="cat hash4.txt puis echo md5 > type.txt"),

    L(1045, "Le sel, c'est la vie",
      story="Pourquoi saler les hashes ? Demonstration : 'soleil' avec sel1 vs sel2 donnent des empreintes "
            "DIFFERENTES ! Meme mot, hashes differents : les pirates pleurent.",
      lesson="Le SEL (salt) : un bout aleatoire ajoute avant de hasher. Meme mot de passe = hashes differents partout. "
             "Sans sel, john craque 1000 comptes d'un coup. Avec sel, il recommence pour chacun. Salez, toujours.",
      mission="Compare : sha256sum a.txt b.txt > compara.txt (a et b contiennent 'soleil' avec des sels differents).",
      setup=[F("a.txt", "sel1:soleil\n"), F("b.txt", "sel2:soleil\n")],
      checks=[C_cmd(r"\bsha256sum\b"), C_fc("compara.txt", text="a.txt"), C_fc("compara.txt", text="b.txt")],
      hints=["sha256sum a.txt b.txt > compara.txt", "Meme mot, sels differents : hashes differents !"],
      solution="sha256sum a.txt b.txt > compara.txt"),

    L(1046, "Generer un vrai secret",
      story="Assez des mots faibles ! Genere un VRAI secret aleatoire avec /dev/urandom (le generateur d'alea "
            "du noyau) + base64. 12 octets d'alea pur dans secret.txt.",
      lesson="'head -c 12 /dev/urandom | base64' : 12 octets aleatoires, encodes en texte. Imprevisible, "
             "incraquable par dictionnaire. C'est comme ca qu'on cree des cles, des tokens, des vrais secrets.",
      mission="Genere : head -c 12 /dev/urandom | base64 > secret.txt",
      checks=[C_cmd(r"urandom"), C_nempty("secret.txt")],
      hints=["head -c 12 /dev/urandom | base64 > secret.txt", "/dev/urandom = de l'alea pur, offert par le noyau."],
      solution="head -c 12 /dev/urandom | base64 > secret.txt"),

    L(1047, "Grosse wordlist",
      story="Cette fois, la wordlist fait 30 mots ! john les essaie TOUS, un par un. Patience... "
            "(quelques millisecondes). Trouve le mot de 'root'.",
      lesson="Plus la wordlist est grosse, plus john cherche longtemps... mais les vraies wordlists (rockyou.txt) "
             "font des MILLIONS de mots ! Les attaquants les passent en heures. D'ou l'importance des mots LONGS.",
      mission="Craque : john --wordlist=gros.txt hash5.txt puis note dans password5.txt.",
      setup=[F("hash5.txt", "root:de05930dd46a984ca32aad9feac718e8\n"),
             F("gros.txt", "alpha\nbravo\ncharlie\ndelta\necho\nfoxtrot\ngolf\nhotel\nindia\njuliett\nkilo\n"
                           "lima\nmike\nnovember\noscar\npapa\nquebec\nromeo\nsierra\ntango\nuniform\nvictor\n"
                           "whiskey\nxray\nyankee\nzulu\nsupernova\ncosmos\natome\nquark\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("password5.txt", text="supernova")],
      hints=["1) john --wordlist=gros.txt hash5.txt", "2) echo supernova > password5.txt"],
      solution="john --wordlist=gros.txt hash5.txt puis echo supernova > password5.txt"),

    L(1048, "Echec honorable",
      story="Parfois, john NE TROUVE PAS : le mot n'est pas dans la wordlist ('0 cracked'). C'est NORMAL : "
            "aucune wordlist ne contient tout. Constate l'echec et note 'introuvable' dans verdict.txt.",
      lesson="'0 password hashes cracked' = le mot n'est pas dans la liste. Les attaquants essaient alors d'autres "
             "listes, des regles, du brute-force... ou abandonnent. Un mot absent des listes = un mot qui resiste.",
      mission="1) john --wordlist=petit.txt hash6.txt (observe le 0)  2) echo introuvable > verdict.txt",
      setup=[F("hash6.txt", "admin:de05930dd46a984ca32aad9feac718e8\n"),
             F("petit.txt", "lundi\nmardi\nmercredi\njeudi\nvendredi\nsamedi\ndimanche\nfete\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("verdict.txt", text="introuvable")],
      hints=["1) john --wordlist=petit.txt hash6.txt (0 cracked : normal !)",
             "2) echo introuvable > verdict.txt"],
      solution="john --wordlist=petit.txt hash6.txt puis echo introuvable > verdict.txt"),

    L(1049, "La taille compte",
      story="Avant de lancer john, un agent verifie la TAILLE de sa wordlist : 'wc -l'. "
            "20 mots ici : compte-les dans compte.txt. (rockyou.txt en a 14 millions !)",
      lesson="'wc -l liste.txt' = nombre de mots a essayer. 20 mots = instantane. 14 millions = des heures. "
             "Estimer avant de lancer : le reflexe qui evite d'attendre 3 jours pour rien.",
      mission="Compte : wc -l < liste20.txt > compte.txt (attendu : 20).",
      setup=[F("liste20.txt", "m01\nm02\nm03\nm04\nm05\nm06\nm07\nm08\nm09\nm10\n"
                               "m11\nm12\nm13\nm14\nm15\nm16\nm17\nm18\nm19\nm20\n")],
      checks=[C_eq("compte.txt", "20\n")],
      hints=["wc -l < liste20.txt > compte.txt", "< envoie le fichier, wc -l compte les lignes."],
      solution="wc -l < liste20.txt > compte.txt"),

    L(1050, "BOSS : craquage pro",
      story="BOSS : dossier complet ! 1) Identifie le hash (md5, 32 car.) 2) Craque-le avec john 3) Rapport "
            "dans rapport.txt : le type + le mot de passe. Methode complete, comme un pro.",
      lesson="BOSS : identifier (longueur) + craquer (john) + rapporter. C'est LE workflow du pentester face a "
             "un hash : type, wordlist, resultat, rapport. Clean, carre, professionnel.",
      mission="1) echo md5 > rapport.txt  2) john --wordlist=mots.txt hash.txt  3) echo pirate >> rapport.txt",
      setup=[F("hash.txt", "agent:ad015ef45d838cbf619d2f9f7bbdad86\n"),
             F("mots.txt", "chat\nchien\npirate\noiseau\npoisson\nlapin\ntigre\nlion\nours\nloup\n")],
      checks=[C_cmd(r"\bjohn\b"), C_fc("rapport.txt", text="md5"), C_fc("rapport.txt", text="pirate")],
      hints=["1) echo md5 > rapport.txt", "2) john --wordlist=mots.txt hash.txt (lis le mot !)",
             "3) echo pirate >> rapport.txt"],
      solution="echo md5 > rapport.txt && john --wordlist=mots.txt hash.txt puis echo pirate >> rapport.txt",
      xp=25, boss=True),

    # ============ JOUR 106 : forensics (1051-1060) ============
    L(1051, "Nuit d'attaque",
      story="Cette nuit, quelqu'un a attaque le serveur SSH ! Le journal auth.log contient tout : "
            "des 'Failed password' suspects... et des connexions legitimes. Filtre les echecs dans echecs.txt.",
      lesson="'grep Failed auth.log > echecs.txt' : isoler les echecs. En forensics (analyse post-incident), "
             "on commence TOUJOURS par filtrer : echecs d'un cote, succes de l'autre. Le journal ne ment jamais.",
      mission="Filtre les echecs : grep Failed auth.log > echecs.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_cmd(r"\bgrep\b"), C_nempty("echecs.txt")],
      hints=["grep Failed auth.log > echecs.txt", "Failed = echec. Isole-les pour les compter."],
      solution="grep Failed auth.log > echecs.txt"),

    L(1052, "Compter l'attaque",
      story="Combien de tentatives ratees cette nuit ? Le rapport d'incident exige UN chiffre exact. "
            "Compte avec grep -c dans nombre.txt.",
      lesson="'grep -c Failed auth.log' : compter au lieu d'afficher. 12 echecs en 9 minutes = une attaque "
             "automatisee (brute-force), pas un humain qui se trompe. Les chiffres racontent l'histoire.",
      mission="Compte : grep -c Failed auth.log > nombre.txt (attendu : 12).",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_eq("nombre.txt", "12\n")],
      hints=["grep -c Failed auth.log > nombre.txt", "-c = count : le chiffre, rien que le chiffre."],
      solution="grep -c Failed auth.log > nombre.txt"),

    L(1053, "L'attaquant principal",
      story="Plusieurs IP ont frappe... mais UNE revient sans cesse ! Trouve la plus frequente : extrais les IP "
            "(cut), trie, compte, garde le top 1. LA formule de l'analyste.",
      lesson="'grep Failed auth.log | cut -d\" \" -f11 | sort | uniq -c | sort -nr | head -n 1' : LA pipeline "
             "forensics. Filtrer, extraire le champ IP, trier, compter, classer, garder le top 1. Apprends-la par coeur.",
      mission="Top attaquant dans top.txt : grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fc("top.txt", text="45.61.22.9")],
      hints=["grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt",
             "Filtre, extrait (champ 11 = IP), trie, compte, classe, top 1."],
      solution="grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt"),

    L(1054, "Les connexions legitimes",
      story="Parmi l'attaque, de VRAIES connexions ('Accepted') : marie s'est connectee deux fois. "
            "Isole-les dans succes.txt : en forensics, on verifie aussi que les legitimes vont bien.",
      lesson="'grep Accepted' : les succes. Un bon analyste regarde les DEUX cotes : qui a echoue (attaquants ?) "
             "et qui a reussi (leger ? pirate avec le bon mot de passe ?). Les deux listes comptent.",
      mission="Isole les succes : grep Accepted auth.log > succes.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fe("succes.txt"), C_fc("succes.txt", text="marie")],
      hints=["grep Accepted auth.log > succes.txt", "Accepted = reussi. Qui ? marie, deux fois."],
      solution="grep Accepted auth.log > succes.txt"),

    L(1055, "Extraire les IP",
      story="Pour bloquer les attaquants au pare-feu, il faut la LISTE des IP (champ 11 des lignes Failed sur root). "
            "Extrais avec cut dans ips.txt.",
      lesson="'cut -d\" \" -f11' : decoupe sur les espaces, garde le champ 11 (l'IP). Les logs SSH ont un format fixe : "
             "quand on connait le numero du champ, on extrait en une commande.",
      mission="Extrais les IP : grep \"Failed password for root\" auth.log | cut -d' ' -f11 > ips.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fe("ips.txt"), C_fc("ips.txt", text="45.61.22.9")],
      hints=["grep \"Failed password for root\" auth.log | cut -d' ' -f11 > ips.txt",
             "Champ 11 = l'IP. Le pare-feu attend ta liste !"],
      solution="grep \"Failed password for root\" auth.log | cut -d' ' -f11 > ips.txt"),

    L(1056, "Le classement complet",
      story="Le rapport exige le CLASSEMENT complet des attaquants : IP + nombre de tentatives, tries. "
            "Meme pipeline qu'avant, SANS le head : tout le podium dans classement.txt.",
      lesson="Sans 'head', on garde TOUT le classement : '... | sort | uniq -c | sort -nr'. Le top 1 frappe 7 fois, "
             "les autres moins. Un rapport complet montre tout le podium, pas seulement le vainqueur.",
      mission="Classement : grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr > classement.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fc("classement.txt", text="45.61.22.9"), C_fc("classement.txt", regex=r"7")],
      hints=["grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr > classement.txt",
             "Le top 1 : 7 tentatives. Le chiffre doit figurer !"],
      solution="grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr > classement.txt"),

    L(1057, "La fin de l'histoire",
      story="Comment l'attaque s'est-elle TERMINEE ? Les 5 dernieres lignes du journal (tail) dans fin.txt : "
            "la fin d'un log raconte souvent la resolution.",
      lesson="'tail -n 5' : les dernieres lignes = les evenements les plus recents. Ici : l'attaque s'arrete, "
             "marie se connecte normalement. Fin heureuse... cette fois.",
      mission="Lis la fin : tail -n 5 auth.log > fin.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fe("fin.txt"), C_fc("fin.txt", text="Accepted")],
      hints=["tail -n 5 auth.log > fin.txt", "La fin du log = la fin de l'histoire."],
      solution="tail -n 5 auth.log > fin.txt"),

    L(1058, "Qui etait vise ?",
      story="Les attaquants visaient QUEL compte ? Compte les attaques contre 'root' dans vs-root.txt. "
            "Spoiler : root est la cible n°1 mondiale (il existe partout !).",
      lesson="'grep -c \"Failed password for root\"' : 9 attaques sur 12 visent root ! C'est pour ca qu'on interdit "
             "root en SSH : il est attaque en permanence, partout, tout le temps.",
      mission="Compte : grep -c \"Failed password for root\" auth.log > vs-root.txt (attendu : 9).",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_eq("vs-root.txt", "9\n")],
      hints=["grep -c \"Failed password for root\" auth.log > vs-root.txt",
             "9 sur 12 visent root : la cible preferee des robots."],
      solution="grep -c \"Failed password for root\" auth.log > vs-root.txt"),

    L(1059, "Le casier de l'attaquant",
      story="Casier judiciaire de 45.61.22.9 : combien de tentatives EXACTEMENT ? 'grep -c' avec le motif complet "
            "dans contre-attaque.txt. Precision d'expert.",
      lesson="'grep -c \"Failed.*45.61.22.9\"' : le motif combine ('Failed' PUIS l'IP). 7 tentatives : "
             "le casier est charge. Au-dela de 5, on bloque l'IP (fail2ban le fait tout seul !).",
      mission="Compte : grep -c \"Failed.*45.61.22.9\" auth.log > contre-attaque.txt (attendu : 7).",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_eq("contre-attaque.txt", "7\n")],
      hints=["grep -c \"Failed.*45.61.22.9\" auth.log > contre-attaque.txt",
             ".* = 'n'importe quoi entre' : Failed ... IP."],
      solution="grep -c \"Failed.*45.61.22.9\" auth.log > contre-attaque.txt"),

    L(1060, "BOSS : rapport d'incident",
      story="BOSS : le RAPPORT D'INCIDENT officiel ! Top attaquant (IP + nombre) + compte vise, dans rapport.txt. "
            "Trois infos, un fichier, zero blabla. Le chef de la securite lit ton rapport...",
      lesson="BOSS forensics : pipeline top-1 + annotation. Un rapport d'incident = QUI (IP), COMBIEN (tentatives), "
             "QUOI (cible). Avec ca, le chef decide : blocage, alerte, contre-mesures.",
      mission="1) ... | sort | uniq -c | sort -nr | head -n 1 > rapport.txt  2) echo \"cible: root\" >> rapport.txt",
      setup=[F("auth.log", AUTH_LOG)],
      checks=[C_fc("rapport.txt", text="45.61.22.9"), C_fc("rapport.txt", regex=r"7"),
              C_fc("rapport.txt", text="root")],
      hints=["1) grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > rapport.txt",
             "2) echo \"cible: root\" >> rapport.txt"],
      solution="grep Failed auth.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > rapport.txt && echo \"cible: root\" >> rapport.txt",
      xp=25, boss=True),

    # ============ JOUR 107 : enumeration web (1061-1070) ============
    L(1061, "Visite du site",
      story="Mission : auditer le site web (dossier site/). Avant tout, CARTOGRAPHIE : 'ls -R' affiche TOUT "
            "l'arborescence. Un auditeur commence toujours par la carte.",
      lesson="'ls -R' = la carte du site : dossiers, fichiers, profondeur. Avant de chercher des failles, "
             "on sait OU chercher. Les auditeurs pressés qui sautent cette etape ratent des trucs.",
      mission="Cartographie : ls -R site",
      setup=SITE_FILES,
      checks=[C_cmd(r"\bls\b[^\n;|&]*-R")],
      hints=["ls -R site", "-R = recursif : toute la carte d'un coup."],
      solution="ls -R site"),

    L(1062, "Le robots.txt bavard",
      story="Le fichier robots.txt dit aux moteurs de recherche quoi NE PAS visiter... et revele donc les coins "
            "caches (/admin/ !). Les attaquants le lisent EN PREMIER. Toi aussi.",
      lesson="'grep Disallow site/robots.txt' : la liste des chemins 'secrets'... publiee en clair ! "
             "robots.txt n'est PAS une protection : c'est un panneau 'ne pas entrer' sans serrure.",
      mission="Liste les chemins caches : grep Disallow site/robots.txt > piste.txt (/admin/ doit y figurer).",
      setup=SITE_FILES,
      checks=[C_cmd(r"\bgrep\b"), C_fc("piste.txt", text="/admin/")],
      hints=["grep Disallow site/robots.txt > piste.txt", "Disallow = 'ne pas entrer'... donc : ENTRE ! (audit legal)."],
      solution="grep Disallow site/robots.txt > piste.txt"),

    L(1063, "Le dossier cache",
      story="Un dossier cache (commençant par un point) se planque dans site/ ! 'ls -la' le deniche. "
            "Prouve ta trouvaille dans cache.txt. Les .git oublies sont des mines d'or...",
      lesson="'ls -la site/ > cache.txt' : avec -a, le '.git' apparait ! Un dossier .git expose sur un site = "
            "tout l'historique du code en telechargement. Faille classique, oubliee partout.",
      mission="Deniche le cache : ls -la site > cache.txt (.git doit y figurer).",
      setup=SITE_FILES,
      checks=[C_fe("cache.txt"), C_fc("cache.txt", text=".git")],
      hints=["ls -la site > cache.txt", "-a revele les caches : .git apparait !"],
      solution="ls -la site > cache.txt"),

    L(1064, "Le backup oublie",
      story="Les developpeurs oublient des BACKUPS (.bak) sur les serveurs... avec les mots de passe dedans ! "
            "Trouve le .bak avec find, puis lis-le.",
      lesson="'find site -name \"*.bak\"' : traquer les backups oublies. .bak, .old, ~, .swp : les extensions "
             "de la honte. Un backup = le code + les secrets, sans protection.",
      mission="1) find site -name \"*.bak\" > bak.txt  2) cat site/admin/config.bak",
      setup=SITE_FILES,
      checks=[C_fc("bak.txt", text="config.bak"), C_cmd(r"\bcat\b[^\n]*config\.bak")],
      hints=["1) find site -name \"*.bak\" > bak.txt", "2) cat site/admin/config.bak (admire le mot de passe...)"],
      solution="find site -name \"*.bak\" > bak.txt && cat site/admin/config.bak"),

    L(1065, "Ratissage de flags",
      story="Deux flags dorment dans le code du site (backup + JavaScript). Ratisse TOUT avec grep -r "
            "dans flags-web.txt. Les secrets dans le code : la plaie du web.",
      lesson="'grep -r \"FLAG{\" site/' : ratisser le code. Mots de passe, cles API, flags : les developpeurs "
             "laissent des secrets DANS le code constamment. Le ratissage, c'est la peche aux secrets.",
      mission="Ratisse : grep -r \"FLAG{\" site/ > flags-web.txt (web-1 et web-2 doivent y figurer).",
      setup=SITE_FILES,
      checks=[C_fc("flags-web.txt", text="FLAG{web-1}"), C_fc("flags-web.txt", text="FLAG{web-2}")],
      hints=["grep -r \"FLAG{\" site/ > flags-web.txt", "Backup + JS : deux secrets, deux flags."],
      solution="grep -r \"FLAG{\" site/ > flags-web.txt"),

    L(1066, "Le mot de passe en commentaire",
      story="Pire que le backup : un mot de passe EN COMMENTAIRE dans le HTML, visible par TOUS les visiteurs ! "
            "Trouve-le avec grep -ri (insensible a la casse) dans secrets.txt.",
      lesson="'grep -ri password site/' : -r partout, -i sans se soucier de la casse. Les commentaires HTML "
             "voyagent jusqu'au navigateur de tout le monde : un secret en commentaire = un secret public.",
      mission="Trouve : grep -ri \"password\" site/ > secrets.txt (s3cr3t-avant-prod doit y figurer).",
      setup=SITE_FILES,
      checks=[C_fe("secrets.txt"), C_fc("secrets.txt", text="s3cr3t-avant-prod")],
      hints=["grep -ri \"password\" site/ > secrets.txt", "-i attrape password, PASSWORD, Password..."],
      solution="grep -ri \"password\" site/ > secrets.txt"),

    L(1067, "Le .git expose",
      story="Le dossier .git du site est accessible ! Son fichier config revele l'adresse du depot prive. "
            "Lis-le dans depot.txt. (En vrai, on telechargerait tout l'historique...)",
      lesson="'.git/config contient l'URL du depot (souvent prive !). Un .git expose = code source + historique + "
             "anciens secrets, en libre-service. Verifie TOUJOURS les .git oublies.",
      mission="Lis : cat site/.git/config > depot.txt (url doit y figurer).",
      setup=SITE_FILES,
      checks=[C_cmd(r"\bcat\b"), C_fc("depot.txt", text="url")],
      hints=["cat site/.git/config > depot.txt", ".git expose = tout l'historique en libre-service."],
      solution="cat site/.git/config > depot.txt"),

    L(1068, "Le fichier tilda",
      story="Les editeurs laissent des fichiers '~' (tilda) : des copies de secours... accessibles ! "
            "Trouve index.html~ avec find dans vieux.txt.",
      lesson="'find site -name \"*~\"' : traquer les tildas. Ces copies contiennent souvent d'ANCIENNES versions "
             "avec d'anciens secrets. Les editeurs sont bavards, les attaquants ecoutent.",
      mission="Traque : find site -name \"*~\" > vieux.txt (index.html~ doit y figurer).",
      setup=SITE_FILES,
      checks=[C_fe("vieux.txt"), C_fc("vieux.txt", text="index.html~")],
      hints=["find site -name \"*~\" > vieux.txt", "*~ = les copies de secours des editeurs."],
      solution="find site -name \"*~\" > vieux.txt"),

    L(1069, "Dans l'image !",
      story="Le logo (logo.png) contient du texte cache ! 'grep' seul refuse ('Binary file matches') : "
            "il faut '-a' (forcer le mode texte). Peche le flag dans logo-flag.txt.",
      lesson="'grep -ra FLAG site/images/' : -a = traiter le binaire comme du texte. Images, PDF, executables : "
             "tout peut cacher du texte (steganographie du pauvre). -a force la lecture.",
      mission="Peche : grep -ra FLAG site/images/ > logo-flag.txt (FLAG{web-3} doit y figurer).",
      setup=SITE_FILES,
      checks=[C_fe("logo-flag.txt"), C_fc("logo-flag.txt", text="FLAG{web-3}")],
      hints=["grep -ra FLAG site/images/ > logo-flag.txt", "-a = forcer le mode texte sur les binaires."],
      solution="grep -ra FLAG site/images/ > logo-flag.txt"),

    L(1070, "BOSS : audit web",
      story="BOSS : rapport d'audit du site ! Les 2 flags du code (web-1, web-2) + le chemin cache /admin/, "
            "dans audit-web.txt. Trois preuves, un rapport. Le client attend...",
      lesson="BOSS web : combiner les trouvailles en UN rapport. 'grep -rh -o' pour les flags, 'grep Disallow' "
             "pour les chemins. Un audit = des preuves rangees, pas des 'il me semble que'.",
      mission="1) grep -rh -o \"FLAG{[^}]*}\" site/admin site/js > audit-web.txt  2) grep Disallow site/robots.txt >> audit-web.txt",
      setup=SITE_FILES,
      checks=[C_fc("audit-web.txt", text="FLAG{web-1}"), C_fc("audit-web.txt", text="FLAG{web-2}"),
              C_fc("audit-web.txt", text="/admin/")],
      hints=["1) grep -rh -o \"FLAG{[^}]*}\" site/admin site/js > audit-web.txt",
             "2) grep Disallow site/robots.txt >> audit-web.txt"],
      solution="grep -rh -o \"FLAG{[^}]*}\" site/admin site/js > audit-web.txt && grep Disallow site/robots.txt >> audit-web.txt",
      xp=25, boss=True),

    # ============ JOUR 108 : pivot (1071-1080) ============
    L(1071, "Reconaissance du pivot",
      story="Nouveau reseau : 10.10.0.6. Avant d'entrer, on OBSERVE : detecte son OS avec nmap -O "
            "dans os.txt. Le pivot (sauter de machine en machine) commence par la reco.",
      lesson="Le PIVOT : compromettre une machine, puis rebondir vers les suivantes. Chaque saut commence pareil : "
             "reco (nmap), acces (ssh), exploration. Ici : d'abord l'OS de .6.",
      mission="Detecte l'OS : nmap -O 10.10.0.6 > os.txt (Linux doit y figurer).",
      scenario=_scen(_target("10.10.0.6", [_port(22, "ssh", "OpenSSH 8.9p1")], os_name="Linux 5.15",
                             users=["agent"], fs={"home": {"agent": {
                                 "note.txt": "serveur backup : 10.10.0.7, utilisateur 'sauve'\n"}}})),
      checks=[C_cmd(r"\bnmap\b[^\n]*-O"), C_fc("os.txt", text="Linux")],
      hints=["nmap -O 10.10.0.6 > os.txt", "Reco d'abord, intrusion ensuite. Toujours."],
      solution="nmap -O 10.10.0.6 > os.txt"),

    L(1072, "La deuxieme cible",
      story="Le reseau contient une DEUXIEME machine : 10.10.0.7. Scanne ses versions (-sV) dans srv.txt. "
            "Deux cibles, deux fiches : la rigueur du pivot.",
      lesson="Chaque machine pivot a sa fiche : IP, ports, versions. 'nmap -sV' remplit la fiche de .7. "
             "On ne saute jamais vers l'inconnu : on fiche d'abord.",
      mission="Fiche la .7 : nmap -sV 10.10.0.7 > srv.txt (OpenSSH doit y figurer).",
      scenario=_scen(_target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["sauve"],
                             fs={"home": {"sauve": {"flag2.txt": "FLAG{pivot-2}\n"}}})),
      checks=[C_cmd(r"\bnmap\b[^\n]*-sV"), C_fc("srv.txt", text="OpenSSH")],
      hints=["nmap -sV 10.10.0.7 > srv.txt", "Fiche complete avant de sauter."],
      solution="nmap -sV 10.10.0.7 > srv.txt"),

    L(1073, "L'indice sur .6",
      story="Connecte-toi a .6 (agent) : un fichier note.txt donne la SUITE (l'utilisateur de .7) ! "
            "Les pivots vivent de ces indices : lis la note, recopie-la dans note.txt (local).",
      lesson="Pivot etape 1 : exploiter .6 pour apprendre .7. Les notes, les historiques, les configs : "
             "chaque machine raconte la suivante. Lis TOUT, note TOUT.",
      mission="En SSH sur .6 : cat note.txt. Recopie (le mot 'sauve') dans note.txt (local).",
      scenario=_scen(_target("10.10.0.6", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {
                                 "note.txt": "serveur backup : 10.10.0.7, utilisateur 'sauve'\n"}}})),
      checks=[C_cmd(r"\bssh\b"), C_fc("note.txt", text="sauve")],
      hints=["ssh agent@10.10.0.6, cat note.txt, exit", "Puis : echo sauve > note.txt (l'indice !)"],
      solution="ssh agent@10.10.0.6, cat note.txt, exit, echo sauve > note.txt"),

    L(1074, "Le saut vers .7",
      story="Tu as l'indice : utilisateur 'sauve' sur .7 ! Saute : ssh sauve@10.10.0.7, lis flag2.txt, "
            "ramene dans flag2.txt (local). LE PIVOT, ton premier vrai rebond !",
      lesson="Pivot etape 2 : utiliser l'indice pour sauter. 'ssh sauve@10.10.0.7' : nouvelle machine, "
             "nouvel utilisateur, nouveau flag. C'est comme ca qu'on traverse un reseau entier.",
      mission="Saute : ssh sauve@10.10.0.7, cat flag2.txt, recopie dans flag2.txt (local).",
      scenario=_scen(_target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["sauve"],
                             fs={"home": {"sauve": {"flag2.txt": "FLAG{pivot-2}\n"}}})),
      checks=[C_cmd(r"\bssh\b[^\n]*sauve@10\.10\.0\.7"), C_fc("flag2.txt", text="FLAG{pivot-2}")],
      hints=["ssh sauve@10.10.0.7, cat flag2.txt, exit", "Puis : echo FLAG{...} > flag2.txt"],
      solution="ssh sauve@10.10.0.7, cat flag2.txt, exit, echo du flag > flag2.txt"),

    L(1075, "Lire la banniere",
      story="En te connectant a .6, lis BIEN la banniere d'accueil : elle dit 'Ubuntu 22.04' ! "
            "Les bannieres trahissent les versions. Note 'Ubuntu' dans banner.txt.",
      lesson="Les bannieres SSH ('Welcome to Ubuntu 22.04...') cadeau : elles donnent l'OS et parfois la version ! "
             "Les pros les notent : une vieille banniere = une vieille machine = des failles.",
      mission="Connecte-toi a .6, lis la banniere, note Ubuntu dans banner.txt (local).",
      scenario=_scen(_target("10.10.0.6", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {}}})),
      checks=[C_cmd(r"\bssh\b[^\n]*10\.10\.0\.6"), C_fc("banner.txt", text="Ubuntu")],
      hints=["ssh agent@10.10.0.6 (lis la banniere !), exit", "Puis : echo Ubuntu > banner.txt"],
      solution="ssh agent@10.10.0.6, exit, echo Ubuntu > banner.txt"),

    L(1076, "Le flag oublie sur .7",
      story="Sur .7, les admins ont oublie un flag dans un dossier CACHE (.cache/vieux.txt). "
            "'ls -a' a distance, 'cat', ramene dans oublie.txt. Les oublis sont partout, meme ailleurs.",
      lesson="Pivot + cache : 'ls -a' DANS le ssh vers .7. Chaque machine pivot merite sa fouille complete : "
             "ls -a, find, cat. Les oublis voyagent avec les admins.",
      mission="Sur .7 (sauve) : ls -a, cat .cache/vieux.txt, recopie dans oublie.txt (local).",
      scenario=_scen(_target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["sauve"],
                             fs={"home": {"sauve": {".cache": {"vieux.txt": "FLAG{pivot-cache}\n"}}}})),
      checks=[C_fc("oublie.txt", text="FLAG{pivot-cache}")],
      hints=["ssh sauve@10.10.0.7, ls -a, cat .cache/vieux.txt, exit",
             "Puis : echo FLAG{...} > oublie.txt"],
      solution="ssh sauve@10.10.0.7, ls -a, cat .cache/vieux.txt, exit, echo > oublie.txt"),

    L(1077, "Double scan",
      story="Cartographie COMPLETE : scanne .6 ET .7, un rapport chacun (scan1.txt, scan2.txt). "
            "Les deux doivent dire 'Host is up'. Un reseau se cartographie entierement.",
      lesson="Deux cibles = deux scans = deux rapports. 'Host is up' dans chacun = les deux vivent. "
             "La cartographie complete avant le pivot complet.",
      mission="1) nmap 10.10.0.6 > scan1.txt  2) nmap 10.10.0.7 > scan2.txt",
      scenario=_scen(_target("10.10.0.6", [_port(22, "ssh", "OpenSSH 8.9p1")]),
                     _target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")])),
      checks=[C_fc("scan1.txt", text="Host is up"), C_fc("scan2.txt", text="Host is up")],
      hints=["1) nmap 10.10.0.6 > scan1.txt", "2) nmap 10.10.0.7 > scan2.txt"],
      solution="nmap 10.10.0.6 > scan1.txt && nmap 10.10.0.7 > scan2.txt"),

    L(1078, "Versions des deux",
      story="Fiches versions des DEUX machines : nmap -sV sur .6 (v1.txt) et .7 (v2.txt). "
            "OpenSSH des deux cotes : compare les versions, agent.",
      lesson="Comparer les versions : si .6 a OpenSSH 8.9 et .7 une vieillerie, on attaque .7 d'abord ! "
             "Les versions guident la strategie : toujours frapper le plus faible.",
      mission="1) nmap -sV 10.10.0.6 > v1.txt  2) nmap -sV 10.10.0.7 > v2.txt (OpenSSH dans les deux).",
      scenario=_scen(_target("10.10.0.6", [_port(22, "ssh", "OpenSSH 8.9p1")]),
                     _target("10.10.0.7", [_port(22, "ssh", "OpenSSH 7.9p1")])),
      checks=[C_fc("v1.txt", text="OpenSSH"), C_fc("v2.txt", text="OpenSSH")],
      hints=["1) nmap -sV 10.10.0.6 > v1.txt", "2) nmap -sV 10.10.0.7 > v2.txt"],
      solution="nmap -sV 10.10.0.6 > v1.txt && nmap -sV 10.10.0.7 > v2.txt"),

    L(1079, "Fiche de pivot",
      story="Fiche de pivot pour .7 : son scan -sV + l'utilisateur 'sauve', dans pivot.txt. "
            "Une fiche = technique (scan) + acces (user). Complete et propre.",
      lesson="La fiche de pivot parfaite : le scan (comment entrer) + l'utilisateur (en tant que qui). "
             "Avec ca, n'importe quel agent peut refaire le saut. Documentation = professionnalisme.",
      mission="1) nmap -sV 10.10.0.7 > pivot.txt  2) echo \"user: sauve\" >> pivot.txt",
      scenario=_scen(_target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")])),
      checks=[C_fc("pivot.txt", text="OpenSSH"), C_fc("pivot.txt", text="sauve")],
      hints=["1) nmap -sV 10.10.0.7 > pivot.txt", "2) echo \"user: sauve\" >> pivot.txt"],
      solution="nmap -sV 10.10.0.7 > pivot.txt && echo \"user: sauve\" >> pivot.txt"),

    L(1080, "BOSS : pivot total",
      story="BOSS : rapport de pivot TOTAL sur .7 ! Les 2 flags (flag2 + cache) + l'utilisateur, dans rapport-pivot.txt. "
            "Deux connexions, deux flags, un rapport. Le pivot n'a plus de secret.",
      lesson="BOSS pivot : tout refaire en autonomie. ssh, ls -a, cat x2, rapport. C'est l'examen du rebond : "
             "entrer, fouiller, reunir les preuves. Valide ca, et tu sais traverser.",
      mission="Sur .7 : ramene flag2.txt + .cache/vieux.txt + note l'utilisateur, le tout dans rapport-pivot.txt.",
      scenario=_scen(_target("10.10.0.7", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["sauve"],
                             fs={"home": {"sauve": {"flag2.txt": "FLAG{pivot-2}\n",
                                                    ".cache": {"vieux.txt": "FLAG{pivot-cache}\n"}}}})),
      checks=[C_fc("rapport-pivot.txt", text="FLAG{pivot-2}"), C_fc("rapport-pivot.txt", text="FLAG{pivot-cache}"),
              C_fc("rapport-pivot.txt", text="sauve")],
      hints=["1) ssh sauve@10.10.0.7, cat flag2.txt, cat .cache/vieux.txt, exit",
             "2) echo les 2 flags + 'sauve' dans rapport-pivot.txt"],
      solution="ssh + cat flag2.txt + cat .cache/vieux.txt + exit + echo tout > rapport-pivot.txt",
      xp=25, boss=True),

    # ============ JOUR 109 : escalation de privilees (1081-1090) ============
    L(1081, "Les binaires SUID",
      story="Escalade de privilees, lecon 1 : les binaires SUID (droit 's') s'executent en tant que ROOT ! "
            "Trouve-les : 'find . -perm -4000'. Un SUID mal configure = une porte vers root.",
      lesson="'find . -perm -4000' : traquer les SUID. Un programme SUID-root lance par toi tourne en ROOT : "
             "si tu peux le detourner, tu deviens root. D'ou la chasse permanente aux SUID suspects.",
      mission="Traque : find . -perm -4000 > suid.txt (outil-priv doit y figurer).",
      setup=[F("outil-priv", "binaire special\n", mode="4755"), F("notes.txt", "rien\n")],
      checks=[C_fe("suid.txt"), C_fc("suid.txt", text="outil-priv")],
      hints=["find . -perm -4000 > suid.txt", "-4000 = le bit SUID. Les 's' de 'ls -l' : rws !"],
      solution="find . -perm -4000 > suid.txt"),

    L(1082, "Que permet sudo ?",
      story="Lecon 2 : que peux-tu lancer en sudo SANS mot de passe ? 'sudo -n -l' liste tes droits "
            "(le -n evite de demander le mot de passe). Les sudoers mal configures = jackpot.",
      lesson="'sudo -n -l > sudo.txt' : lister ses droits sudo, sans bloquer. '(ALL) NOPASSWD: ALL' = tu es root "
             "deguise. Meme un seul programme autorise peut suffire (voir GTFOBins, le grimoire des binaires).",
      mission="Liste tes droits : sudo -n -l > sudo.txt 2>&1",
      checks=[C_fe("sudo.txt"), C_cmd(r"\bsudo\b")],
      hints=["sudo -n -l > sudo.txt 2>&1", "-n = ne jamais demander le mot de passe. -l = lister."],
      solution="sudo -n -l > sudo.txt 2>&1"),

    L(1083, "Fichiers modifiables",
      story="Lecon 3 : quels fichiers peux-tu MODIFIER ? Un script root modifiable par toi = tu ecris dedans "
            "ce que tu veux... et root l'execute ! Traque avec 'find -writable'.",
      lesson="'find . -writable -type f' : les fichiers que TU peux ecrire. En privesc, on cherche les fichiers "
             "sensibles (scripts, configs, cron) modifiables : chacun est une marche vers root.",
      mission="Traque : find . -writable -type f > ins.txt (note.txt doit y figurer).",
      setup=[F("note.txt", "modifiable\n")],
      checks=[C_fe("ins.txt"), C_fc("ins.txt", text="note.txt")],
      hints=["find . -writable -type f > ins.txt", "-writable = 'que je peux modifier'."],
      solution="find . -writable -type f > ins.txt"),

    L(1084, "Le PATH piege",
      story="Lecon 4 : ton PATH ! Si un dossier modifiable par toi est DANS le PATH avant /bin, tu peux y deposer "
            "un faux 'ls'... que root lancera ! Affiche ton PATH dans path.txt.",
      lesson="'echo $PATH' : la liste des dossiers fouilles pour trouver les commandes. Un dossier inscriptible "
             "dans le PATH + un script root qui appelle 'ls' sans chemin = hijack ! Le PATH se surveille.",
      mission="Affiche : echo $PATH > path.txt",
      checks=[C_fe("path.txt"), C_fc("path.txt", text="/")],
      hints=["echo $PATH > path.txt", "$PATH = les dossiers fouilles, separes par ':'."],
      solution="echo $PATH > path.txt"),

    L(1085, "Connais tes groupes",
      story="Lecon 5 : tes GROUPES ! Membre de 'docker' ? Tu es root (docker = root deguise). De 'lxd', 'adm', "
            "'disk' ? Chacun ouvre une voie. Verifie avec 'id' dans moi.txt.",
      lesson="'id' en privesc : lire ses groupes comme des cles. docker/lxd/disk/adm/sudo : des groupes qui menent "
             "a root. Un groupe anodin + une astuce connue = escalade. D'ou l'enumeration systematique.",
      mission="Verifie : id > moi.txt",
      checks=[C_fe("moi.txt"), C_fc("moi.txt", text="uid=")],
      hints=["id > moi.txt", "Lis tes groupes : une voie vers root s'y cache peut-etre."],
      solution="id > moi.txt"),

    L(1086, "Le noyau, quelle version ?",
      story="Lecon 6 : la version du NOYAU ! Les vieux noyaux ont des exploits publics (DirtyPipe, DirtyCow...). "
            "'uname -r' dans noyau.txt : la premiere etape du ciblage.",
      lesson="'uname -r' : version du noyau. Ensuite on cherche 'Linux 5.x exploit' : si le noyau est vieux et "
             "vulnerable, un exploit public donne root. D'ou les mises a jour ! (Et les audits de version.)",
      mission="Version : uname -r > noyau.txt",
      checks=[C_fe("noyau.txt"), C_fc("noyau.txt", text=".")],
      hints=["uname -r > noyau.txt", "Vieux noyau = exploits connus. A jour = tranquille."],
      solution="uname -r > noyau.txt"),

    L(1087, "Les configs oubliees",
      story="Lecon 7 : les fichiers de CONFIG (.conf, .cfg, .ini) cachent des mots de passe en clair ! "
            "Traque les *.conf avec find. (Ici : juste les lister, la lecture c'est pour les vrais audits.)",
      lesson="'find . -name \"*.conf\"' : traquer les configs. Base de donnees, applis, services : les mots de passe "
             "en clair dorment dans les configs oubliees. Une config lisible = des identifiants offerts.",
      mission="Traque : find . -name \"*.conf\"",
      setup=[F("app.conf", "db=local\n"), F("lisez.txt", "rien\n")],
      checks=[C_cmd(r"\bfind\b[^\n]*-name")],
      hints=["find . -name \"*.conf\"", "Les .conf : la ou dorment les mots de passe en clair."],
      solution="find . -name \"*.conf\""),

    L(1088, "Qui tourne ?",
      story="Lecon 8 : les PROCESSUS ! Un backup root qui tourne toutes les minutes ? Un script bizarre ? "
            "'ps aux' photographie tout. Capture le top 5 dans top5.txt.",
      lesson="'ps aux | head -n 5' : qui tourne, en tant que qui. Les processus root interessants (cron, backups, "
             "agents) sont des cibles : si on peut influencer ce qu'ils font, on devient root.",
      mission="Capture : ps aux | head -n 5 > top5.txt",
      checks=[C_fe("top5.txt"), C_fc("top5.txt", text="PID")],
      hints=["ps aux | head -n 5 > top5.txt", "Qui tourne ? En tant que qui ? Depuis quand ?"],
      solution="ps aux | head -n 5 > top5.txt"),

    L(1089, "La maison des autres",
      story="Lecon 9 : le dossier personnel ! Les cles SSH, les historiques, les notes... tout dort dans les homes. "
            "Liste le TIEN (jamais celui des autres sans autorisation !) dans home.txt.",
      lesson="'ls ~' : ton home. Cles (.ssh), historique (.bash_history : parfois des mots de passe tapes !), "
             "notes... En audit AUTORISE, on y cherche les oublis. Et on protege le sien pareil.",
      mission="Liste : ls ~ > home.txt",
      checks=[C_fe("home.txt"), C_nempty("home.txt")],
      hints=["ls ~ > home.txt", "~ = ton home. Clés, historique, notes : tout y dort."],
      solution="ls ~ > home.txt"),

    L(1090, "BOSS : enumeration privesc",
      story="BOSS : enumeration PRIVESQ... PRIVES-C complete ! SUID + identite, dans rapport.txt. "
            "C'est la checklist de tout pentester qui vient d'entrer : SUID, id, sudo, noyau...",
      lesson="BOSS : 'find -perm -4000' + 'id' dans un rapport. L'enumeration privesc systematique : SUID, sudo, "
             "groupes, noyau, cron, fichiers modifiables. On enumere AVANT d'exploiter. Toujours.",
      mission="1) find . -perm -4000 > rapport.txt  2) id >> rapport.txt",
      setup=[F("outil-priv", "binaire special\n", mode="4755")],
      checks=[C_fc("rapport.txt", text="outil-priv"), C_fc("rapport.txt", text="uid="),
              C_fc("rapport.txt", text="(")],
      hints=["1) find . -perm -4000 > rapport.txt", "2) id >> rapport.txt"],
      solution="find . -perm -4000 > rapport.txt && id >> rapport.txt",
      xp=25, boss=True),

    # ============ JOUR 110 : examen d'agent (1091-1100) ============
    L(1091, "Examen : le scan",
      story="EXAMEN FINAL, epreuve 1/5 : la cible 10.10.0.9 ! Scanne-la : retrouve les ports 22 et 80 "
            "dans scan.txt. Sans faute, agent. Le jury observe.",
      lesson="Examen : nmap de base, sans filet. Les ports 22 (SSH) et 80 (web) : les deux portes classiques. "
             "Trouve-les, prouve-les. C'est parti.",
      mission="Scanne : nmap 10.10.0.9 > scan.txt (22 et 80 doivent y figurer).",
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1"),
                                           _port(80, "http", "Apache httpd 2.4.41")],
                             users=["agent"], fs={"home": {"agent": {
                                 "flag1.txt": "FLAG{examen-1}\n",
                                 "note.txt": "hash du coffre (md5) : ad015ef45d838cbf619d2f9f7bbdad86\n"}}})),
      checks=[C_fc("scan.txt", text="22"), C_fc("scan.txt", text="80")],
      hints=["nmap 10.10.0.9 > scan.txt", "Epreuve 1/5 : sans faute !"],
      solution="nmap 10.10.0.9 > scan.txt"),

    L(1092, "Examen : l'intrusion",
      story="Epreuve 2/5 : ENTRE ! SSH en agent sur .9, lis flag1.txt, ramene dans flag1.txt (local). "
            "Propre, rapide, sans bruit.",
      lesson="Examen : ssh + exfiltration. La boucle que tu as repetee 10 fois : connexion, lecture, retour, "
             "preuve locale. Montre au jury que c'est un reflexe.",
      mission="SSH + flag1.txt local (FLAG{examen-1}).",
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {
                                 "flag1.txt": "FLAG{examen-1}\n",
                                 "note.txt": "hash du coffre (md5) : ad015ef45d838cbf619d2f9f7bbdad86\n"}}})),
      checks=[C_cmd(r"\bssh\b"), C_fc("flag1.txt", text="FLAG{examen-1}")],
      hints=["ssh agent@10.10.0.9, cat flag1.txt, exit", "Puis : echo FLAG{...} > flag1.txt"],
      solution="ssh agent@10.10.0.9, cat flag1.txt, exit, echo > flag1.txt"),

    L(1093, "Examen : le craquage",
      story="Epreuve 3/5 : sur .9, une note donne un hash MD5 du coffre ! Recupere-le (ssh + cat note), "
            "craque-le avec john (mots.txt fourni), note le mot dans password.txt.",
      lesson="Examen : chaine complete. Lire le hash a distance, le recopier en local, john, noter. "
             "Quatre etapes, zero erreur. Les examens aiment les chaines.",
      mission="1) Lis note.txt via SSH  2) echo \"chef:HASH\" > hash.txt  3) john --wordlist=mots.txt hash.txt  4) echo pirate > password.txt",
      setup=[F("mots.txt", "chat\nchien\npirate\ncorbeau\nrenard\nloup\ntigre\nours\naigle\nrequin\n")],
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {
                                 "note.txt": "hash du coffre (md5) : ad015ef45d838cbf619d2f9f7bbdad86\n"}}})),
      checks=[C_cmd(r"\bjohn\b"), C_fc("password.txt", text="pirate")],
      hints=["1) ssh agent@10.10.0.9, cat note.txt, exit (recopie le hash !)",
             "2) echo \"chef:ad015ef45d838cbf619d2f9f7bbdad86\" > hash.txt",
             "3) john --wordlist=mots.txt hash.txt, 4) echo pirate > password.txt"],
      solution="ssh+cat note, echo chef:HASH > hash.txt, john, echo pirate > password.txt"),

    L(1094, "Examen : forensics",
      story="Epreuve 4/5 : mini-log d'attaque (4 lignes) ! Trouve l'IP la plus frequente "
            "(pipeline cut/sort/uniq/sort/head) dans top.txt. Rapide !",
      lesson="Examen : la pipeline forensics, de memoire. Filtrer, extraire, trier, compter, classer, top 1. "
             "Si tu la tapes sans reflechir, tu es un analyste.",
      mission="Top IP : grep Failed mini.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt",
      setup=[F("mini.log",
               "Sep 10 04:01:01 srv sshd[1]: Failed password for root from 203.0.113.50 port 11 ssh2\n"
               "Sep 10 04:01:02 srv sshd[2]: Failed password for root from 203.0.113.50 port 12 ssh2\n"
               "Sep 10 04:01:03 srv sshd[3]: Failed password for root from 203.0.113.50 port 13 ssh2\n"
               "Sep 10 04:01:04 srv sshd[4]: Failed password for root from 198.51.100.7 port 21 ssh2\n")],
      checks=[C_fc("top.txt", text="203.0.113.50")],
      hints=["grep Failed mini.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt",
             "De memoire, agent. Tu l'as fait 10 fois."],
      solution="grep Failed mini.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 > top.txt"),

    L(1095, "Examen : decodage",
      story="Epreuve 5/5 : un message base64 attend ! Decode message.b64 dans flag-final.txt. "
            "Derniere epreuve technique avant le rapport...",
      lesson="Examen : base64 -d, les yeux fermes. Decoder, verifier le FLAG{...}, archiver. "
             "Simple, rapide, sans faute : comme tout le reste de l'examen.",
      mission="Decode : base64 -d message.b64 > flag-final.txt (FLAG{examen-final} attendu).",
      setup=[F("message.b64", "RkxBR3tleGFtZW4tZmluYWx9\n")],
      checks=[C_fe("flag-final.txt"), C_fc("flag-final.txt", text="FLAG{examen-final}")],
      hints=["base64 -d message.b64 > flag-final.txt", "Derniere epreuve technique. Respire."],
      solution="base64 -d message.b64 > flag-final.txt"),

    L(1096, "Le site de l'examen",
      story="Bonus : le site de l'examen (site2/) cache un flag ! robots.txt indique /secret/... "
            "Ratisse avec grep -r dans web.txt. Les bonus font les mentions.",
      lesson="Bonus : enumeration web express. robots.txt (piste) + grep -r (ratissage). "
             "Les mentions 'Tres Bien' se gagnent sur les bonus.",
      mission="Ratisse : grep -r FLAG site2/ > web.txt (FLAG{examen-web} attendu).",
      setup=[D("site2/secret"), F("site2/robots.txt", "User-agent: *\nDisallow: /secret/\n"),
             F("site2/secret/drapeau.txt", "FLAG{examen-web}\n")],
      checks=[C_fe("web.txt"), C_fc("web.txt", text="FLAG{examen-web}")],
      hints=["grep -r FLAG site2/ > web.txt", "Bonus = mention. Ratisse !"],
      solution="grep -r FLAG site2/ > web.txt"),

    L(1097, "Le SUID de l'examen",
      story="Bonus 2 : un binaire SUID traine (examen-suid) ! Trouve-le avec find -perm -4000 "
            "dans suid-ex.txt. Les bonus s'accumulent...",
      lesson="Bonus : chasse au SUID, de memoire. 'find . -perm -4000' : si tu le tapes sans hesiter, "
             "l'enumeration privesc est ancree. Les bonus aiment les reflexes.",
      mission="Traque : find . -perm -4000 > suid-ex.txt (examen-suid attendu).",
      setup=[F("examen-suid", "binaire\n", mode="4755"), F("rien.txt", "rien\n")],
      checks=[C_fe("suid-ex.txt"), C_fc("suid-ex.txt", text="examen-suid")],
      hints=["find . -perm -4000 > suid-ex.txt", "De memoire. Les reflexes paient."],
      solution="find . -perm -4000 > suid-ex.txt"),

    L(1098, "Dossier partiel",
      story="Le jury veut un DOSSIER : flag1 (via SSH sur .9) + mot de passe du coffre (john + mots.txt), "
            "dans dossier.txt. Deux preuves, un fichier.",
      lesson="Dossier partiel : combiner deux exfiltrations. SSH + john, les deux epreuves reines, "
             "reunies. Un dossier, c'est des preuves RANGEES.",
      mission="SSH flag1 + john (mots.txt) : les deux dans dossier.txt (FLAG{examen-1} + pirate).",
      setup=[F("mots.txt", "chat\nchien\npirate\ncorbeau\nrenard\nloup\ntigre\nours\naigle\nrequin\n")],
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {
                                 "flag1.txt": "FLAG{examen-1}\n",
                                 "note.txt": "hash du coffre (md5) : ad015ef45d838cbf619d2f9f7bbdad86\n"}}})),
      checks=[C_fc("dossier.txt", text="FLAG{examen-1}"), C_fc("dossier.txt", text="pirate")],
      hints=["1) ssh : cat flag1.txt + cat note.txt (recopie le hash !), exit",
             "2) echo \"chef:HASH\" > hash.txt, john --wordlist=mots.txt hash.txt",
             "3) echo les 2 preuves > dossier.txt"],
      solution="ssh (flag1+hash), echo hash, john, echo preuves > dossier.txt"),

    L(1099, "Dossier complet",
      story="Le dossier GROSSIT : flag1 (SSH) + flag-final (base64) + flag-web (site2), dans dossier-full.txt. "
            "Trois epreuves, trois preuves. Le jury hoche la tete...",
      lesson="Dossier complet : trois sources, un fichier. SSH, decodage, web : l'agent polyvalent "
             "reunit tout. Le jury aime les dossiers epais (et propres).",
      mission="Reunis FLAG{examen-1} + FLAG{examen-final} + FLAG{examen-web} dans dossier-full.txt.",
      setup=[F("message.b64", "RkxBR3tleGFtZW4tZmluYWx9\n"),
             D("site2/secret"), F("site2/robots.txt", "User-agent: *\nDisallow: /secret/\n"),
             F("site2/secret/drapeau.txt", "FLAG{examen-web}\n")],
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1")], users=["agent"],
                             fs={"home": {"agent": {"flag1.txt": "FLAG{examen-1}\n"}}})),
      checks=[C_fc("dossier-full.txt", text="FLAG{examen-1}"), C_fc("dossier-full.txt", text="FLAG{examen-final}"),
              C_fc("dossier-full.txt", text="FLAG{examen-web}")],
      hints=["1) ssh : cat flag1.txt, exit", "2) base64 -d message.b64", "3) grep -r FLAG site2/",
             "4) echo les 3 flags > dossier-full.txt"],
      solution="ssh flag1 + base64 -d + grep site2 + echo tout > dossier-full.txt"),

    L(1100, "MEGA-BOSS : AGENT CYBER",
      story="MEGA-BOSS FINAL : le RAPPORT FINAL d'agent ! 5 preuves dans rapport-final.txt : les 3 flags "
            "(examen-1, examen-final, examen-web) + le mot de passe (pirate) + l'IP attaquante (203.0.113.50). "
            "Tout ce que tu sais, en un dossier. Pour le titre d'AGENT CYBER.",
      lesson="MEGA-BOSS : SSH + john + forensics + base64 + web, reunis. Cinq epreuves, cinq preuves, un rapport. "
             "Reussis ca, et tu n'es plus un joueur : tu es un AGENT. Remise des insignes immediate.",
      mission="1) SSH : flag1 + hash  2) john : pirate  3) forensics : IP  4) base64 : flag-final  5) web : flag-web. Tout dans rapport-final.txt.",
      setup=[F("mots.txt", "chat\nchien\npirate\ncorbeau\nrenard\nloup\ntigre\nours\naigle\nrequin\n"),
             F("message.b64", "RkxBR3tleGFtZW4tZmluYWx9\n"),
             D("site2/secret"), F("site2/secret/drapeau.txt", "FLAG{examen-web}\n"),
             F("mini.log",
               "Sep 10 04:01:01 srv sshd[1]: Failed password for root from 203.0.113.50 port 11 ssh2\n"
               "Sep 10 04:01:02 srv sshd[2]: Failed password for root from 203.0.113.50 port 12 ssh2\n"
               "Sep 10 04:01:03 srv sshd[3]: Failed password for root from 203.0.113.50 port 13 ssh2\n"
               "Sep 10 04:01:04 srv sshd[4]: Failed password for root from 198.51.100.7 port 21 ssh2\n")],
      scenario=_scen(_target("10.10.0.9", [_port(22, "ssh", "OpenSSH 8.9p1"),
                                           _port(80, "http", "Apache httpd 2.4.41")],
                             users=["agent"], fs={"home": {"agent": {
                                 "flag1.txt": "FLAG{examen-1}\n",
                                 "note.txt": "hash du coffre (md5) : ad015ef45d838cbf619d2f9f7bbdad86\n"}}})),
      checks=[C_fc("rapport-final.txt", text="FLAG{examen-1}"), C_fc("rapport-final.txt", text="FLAG{examen-final}"),
              C_fc("rapport-final.txt", text="FLAG{examen-web}"), C_fc("rapport-final.txt", text="pirate"),
              C_fc("rapport-final.txt", text="203.0.113.50")],
      hints=["1) ssh agent@10.10.0.9 : cat flag1.txt + cat note.txt (hash !), exit",
             "2) echo \"chef:HASH\" > hash.txt && john --wordlist=mots.txt hash.txt -> pirate",
             "3) grep Failed mini.log | cut -d' ' -f11 | sort | uniq -c | sort -nr | head -n 1 -> IP",
             "4) base64 -d message.b64 -> flag-final, 5) grep -r FLAG site2/ -> flag-web",
             "6) echo les 5 preuves > rapport-final.txt. Pour le titre !"],
      solution="ssh (flag1+hash) + john (pirate) + forensics (IP) + base64 + web, tout > rapport-final.txt",
      xp=100, boss=True),
]
