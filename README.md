# 🐧 ILearnLinux — Du terminal à Agent Cyber, en jouant

> Le Duolingo du terminal : **1100 niveaux**, **110 jours**, **100% pratique**.
> **Un seul terminal suffit** : tu tapes de vraies commandes, le jeu exécute, le mentor guide, les XP pleuvent.

Pas de QCM, pas de vidéos de 3 heures : ici tu **tapes des vraies commandes** sur ton vrai Linux
(`ls`, `grep`, `nmap`, `ssh`, `john`...), tu résous des **missions façon CTF** (flags, scans, intrusions,
craquage, forensics), et le jeu valide **automatiquement**. 10 petits niveaux par jour suffisent.

---

## ⚡ Installation (30 secondes)

```bash
git clone https://github.com/renaudchristinfonton-bj/Ilearnlinux.git
cd Ilearnlinux
./install.sh
```

C'est tout. Aucune dépendance : **Python 3 suffit** (déjà présent sur tout Linux).
L'installeur vérifie les 1100 niveaux, les outils et les simulateurs, puis te propose un alias `ilearn`.

## 🎮 Jouer : un seul terminal !

```bash
./ilearn play        (ou 'ilearn play' avec l'alias)
```

Exemple de partie :

```
 NIVEAU 1023/1100 - JOUR 103 - Agent Cyber stagiaire
Histoire : Un flag dort sur la cible : /home/agent/flag.txt. Connecte-toi, lis-le...
Ta mission : >> Sur la cible : lis flag.txt, recopie-le dans reponse.txt (local).
Dossier de mission : /home/toi/IlearnLinux-arena/niveau-1023
agent@cyber:~$ ssh agent@10.10.0.5
Welcome to Ubuntu 22.04 LTS (GNU/Linux)
agent@10-10-0-5:~$ cat flag.txt
FLAG{ssh-1}
agent@10-10-0-5:~$ exit
agent@cyber:~$ echo FLAG{ssh-1} > reponse.txt
  Objectifs : [OK]
BRAVO ! NIVEAU 1023 REUSSI +10 XP
```

Tu te trompes ? Le **mentor** réagit (erreur expliquée, piste concrète) et t'offre un indice
automatiquement si tu bloques vraiment. Pendant un niveau : `aide`, `mission`, `cours`,
`indice`, `solution`, `quitter` (+ `history`, `clear`).

## 🗺️ La progression : 110 jours, 2 saisons

**Saison 1 — Admin Sys Linux (jours 1–100, niveaux 1–1000)**

| Jours | Niveaux | Thème |
|---|---|---|
| 1–10 | 1–100 | Bases : terminal, `ls`, `cd`, fichiers, lecture, `mv`/`rm`, redirections, `grep`, `find`, tri |
| 11–20 | 101–200 | Permissions, droits, `chmod`, scripts exécutables, liens symboliques |
| 21–30 | 201–300 | Utilisateurs, groupes, identités, `sudo`, `/etc/passwd` |
| 31–40 | 301–400 | Archives & compression : `tar`, `gzip`, sauvegardes |
| 41–50 | 401–500 | Système & matériel : noyau, disques, mémoire, CPU |
| 51–60 | 501–600 | Processus : `ps`, jobs, `kill`, `top`, `nohup` |
| 61–70 | 601–700 | Réseau local : `ping`, `ip`, DNS, ports, `curl` |
| 71–80 | 701–800 | SSH : clés, empreintes, `scp`, config |
| 81–90 | 801–900 | Scripting shell : variables, boucles, tests, fonctions |
| 91–100 | 901–1000 | Admin pro : logs, dépannage, incidents + **MEGA-BOSS final** 👑 |

**Saison 2 — Agent Cyber (jours 101–110, niveaux 1001–1100)** 🕵️

| Jour | Niveaux | Mission |
|---|---|---|
| 101 | 1001–1010 | Bienvenue à l'agence : flags, `file`, hashes, base64, `strings` |
| 102 | 1011–1020 | Reconnaissance : scans `nmap`, ports, versions, OS |
| 103 | 1021–1030 | Connexion `ssh` : clés, intrusions, exfiltration de flags |
| 104 | 1031–1040 | Chasse aux flags : `find -exec`, `grep -o`, double-base64 |
| 105 | 1041–1050 | Mots de passe : `john`, wordlists, sel, secrets aléatoires |
| 106 | 1051–1060 | Forensics : journaux `auth.log`, top attaquants, rapports |
| 107 | 1061–1070 | Énumération web : `robots.txt`, `.git`, backups, secrets |
| 108 | 1071–1080 | Pivot réseau : rebonds de machine en machine |
| 109 | 1081–1090 | Escalade de privilèges : SUID, `sudo`, groupes, noyau |
| 110 | 1091–1100 | **EXAMEN D'AGENT** : mini-CTF + **MEGA-BOSS final** 👑 |

Programme détaillé jour par jour : [`docs/CURRICULUM.md`](docs/CURRICULUM.md).

**Chaque 10ᵉ niveau est un BOSS** (révision, gros XP). Le jeu suit ton **XP**, ta **série quotidienne** 🔥,
tes **badges** et ton **rang** (de *Curieux du terminal* 🌱 à *AGENT CYBER D'ÉLITE* 👑).

## 🕹️ Commandes

```
./ilearn play        Jouer (reprend où tu t'es arrêté)
./ilearn dashboard   XP, série, carte des 110 jours, badges
./ilearn hint        Indice pour le niveau courant
./ilearn solution    Solution (XP réduits, mais on apprend quand même)
./ilearn mission     Revoir la mission en cours
./ilearn goto 250    Sauter à un niveau (pratique libre)
./ilearn reset       Tout recommencer à zéro
./ilearn doctor      Diagnostic : niveaux, outils, simulateurs, progression
```

## 🔧 Comment ça marche ?

- **Un vrai bash persistant** : tes commandes s'exécutent pour de vrai dans le dossier
  de mission (`~/IlearnLinux-arena/niveau-XXXX/`), préparé à chaque niveau. Zéro simulation
  pour le système : `ls`, `grep`, `find`, `tar`, `ps`, `sudo -n`... tout est réel.
- **Des cibles simulées réalistes** : `nmap`, `ssh` et `john` sont des simulateurs pédagogiques
  fournis par le jeu (dans `game/fakebin/`) : vraies sorties, vraies options, machines-cibles
  avec fichiers et flags — sans rien installer ni casser.
- **La validation** : 14 types de vérifications (fichier créé, contenu exact, permissions,
  commande tapée, dossier courant...) combinables par niveau. Les objectifs se cochent en direct.
- **Le mentor** : explique chaque erreur (fichier introuvable, permission, faute de frappe...),
  offre des indices automatiques après 4 puis 8 fautes. Jamais de frustration.
- **La sauvegarde** : `~/.ilearnlinux/progress.json`. XP, série quotidienne, historique : rien ne se perd.
- **La sécurité** : le jeu bloque les commandes destructrices (`rm -rf /`, fork-bomb, `mkfs`,
  `dd` vers `/dev`...) avant exécution. **Aucun niveau n'exige root**, aucun `sudo` interactif.

## ❓ FAQ

**Ça marche sur quelle distribution ?**
N'importe quel Linux avec Python 3 et bash : Ubuntu, Debian, Fedora, Arch... (Windows : via WSL).

**Quels outils faut-il ?**
Ceux de base (`tar`, `gzip`, `ping`, `ip`, `ssh-keygen`...) déjà présents sur Ubuntu/Debian,
plus les simulateurs inclus dans le jeu (`nmap`, `ssh`, `john`).
`./ilearn doctor` te dit exactement ce qui manque éventuellement.

**Je suis bloqué !**
Tape `indice` (ou attends : le mentor aide tout seul après 4 fautes), `solution` en dernier recours.
Mieux vaut voir la solution et continuer que d'abandonner : la répétition en spirale te fera
recroiser la notion. Et `cours` réaffiche la leçon.

**Je peux refaire un niveau ?**
Oui : `./ilearn goto NUMERO` te replace où tu veux, l'XP compte quand même.

**10 niveaux par jour, c'est obligatoire ?**
Non, c'est un rythme conseillé. La série quotidienne compte dès **1 niveau/jour**.
Petit pas chaque jour > rush puis abandon.

## 🤝 Contribuer

- Les jours 1–30 et 101–110 sont écrits à la main (`game/packs/`).
- Les jours 31–100 sont générés par `game/packs/generated.py` (modèles + variantes, en cours d'enrichissement).
- Pour ajouter/enrichir un niveau : inspire-toi d'un niveau existant (même format),
  puis lance `python3 tests/selftest.py` (doit rester à 1100 niveaux valides, 100% vert).
- Idées bienvenues : nouveaux blocs (Docker, Git, SQL...), traductions, mode multijoueur !

## 📜 Licence

MIT — fais-en ce que tu veux, deviens agent, et partage. 🐧
