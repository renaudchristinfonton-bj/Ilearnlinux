# 🐧 ILearnLinux — Deviens Admin Sys Linux en 100 jours, en jouant

> Le Duolingo du terminal : **1000 niveaux**, **100 jours**, **100% pratique**.
> Le jeu tourne dans un onglet, tu joues dans un autre, et il valide tes niveaux **automatiquement**.

Pas de QCM, pas de vidéos de 3 heures : ici tu **tapes des vraies commandes** sur ton vrai Linux,
et le jeu regarde, compte, félicite. Même les flemmards progressent : 10 petits niveaux par jour suffisent.

---

## ⚡ Installation (30 secondes)

```bash
git clone https://github.com/renaudchristinfonton-bj/Ilearnlinux.git
cd Ilearnlinux
./install.sh
```

C'est tout. Aucune dépendance à installer : **Python 3 suffit** (déjà présent sur tout Linux).
L'installeur vérifie les 1000 niveaux et te propose le mode automatique (recommandé).

## 🎮 Démarrage : 2 onglets

| Onglet 1 — 📺 LE JEU | Onglet 2 — ⌨️ LE JOUEUR (toi) |
|---|---|
| `./ilearn play`  (ou `ilearn play` si alias installé) | `source tools/hook.sh` *(une seule fois par onglet — automatique si tu as dit « o » à l'installateur)* |
| Affiche la leçon + la mission, **surveille en continu**, valide tout seul, célèbre 🎉 | Tu vas dans l'arène (`cd ...` affiché par le jeu) et tu tapes tes commandes |

Exemple de partie :

```
NIVEAU 9/1000 — JOUR 1/100 — Curieux du terminal
Leçon : Le symbole '>' redirige la sortie d'une commande vers un fichier...
Ta mission : >> echo salut > bonjour.txt
Arène (onglet JOUEUR) : cd /home/toi/IlearnLinux-arena/niveau-0009
Je surveille ton onglet JOUEUR... à toi de jouer !
Objectifs : [OK][OK]
BRAVO ! NIVEAU 9 RÉUSSI +10 XP
```

Pendant un niveau, dans l'onglet JEU : `h` = indice (−2 XP), `s` = solution, `m` = revoir la mission, `q` = pause.

## 🗺️ La progression : 100 jours, 10 blocs

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

Programme détaillé jour par jour : [`docs/CURRICULUM.md`](docs/CURRICULUM.md).

**Chaque 10ᵉ niveau est un BOSS** (révision, gros XP). Le jeu suit ton **XP**, ta **série quotidienne** 🔥,
tes **badges** et ton **rang** (de *Curieux du terminal* 🌱 à *ADMIN SYS LINUX* 👑).

## 🕹️ Commandes

```
./ilearn play        Jouer (reprend où tu t'es arrêté)
./ilearn dashboard   XP, série, carte des 100 jours, badges
./ilearn hint        Indice pour le niveau courant
./ilearn solution    Solution (XP réduits, mais on apprend quand même)
./ilearn mission     Revoir la mission en cours
./ilearn goto 250    Sauter à un niveau (pratique libre)
./ilearn reset       Tout recommencer à zéro
./ilearn doctor      Diagnostic : niveaux, outils, hook, progression
```

## 🔧 Comment ça marche ?

- **L'arène** : chaque niveau te donne un dossier propre (`~/IlearnLinux-arena/niveau-XXXX/`).
  Le jeu le prépare (fichiers de départ) et l'observe chaque seconde.
- **Le hook** : un petit script bash (`tools/hook.sh`) signale au jeu chaque commande tapée
  dans l'onglet joueur (commande + dossier courant, avec horodatage).
- **La validation** : 14 types de vérifications (fichier créé, contenu exact, permissions,
  commande tapée, dossier courant...) combinables par niveau. Zéro triche possible, zéro config.
- **La sauvegarde** : `~/.ilearnlinux/progress.json` (+ journal des commandes). Rien ne se perd.
- **La sécurité** : le jeu ne touche **jamais** à ton système. Tout se passe dans l'arène ;
  les commandes système utilisées sont en lecture seule, **aucun niveau n'exige root**.

## ❓ FAQ

**Ça marche sur quelle distribution ?**
N'importe quel Linux avec Python 3 et bash : Ubuntu, Debian, Fedora, Arch... (Windows : via WSL).

**Quels outils faut-il ?**
Ceux de base (`tar`, `gzip`, `ping`, `ip`, `ssh`...) déjà présents sur Ubuntu/Debian.
`./ilearn doctor` te dit exactement ce qui manque éventuellement.

**Le jeu ne détecte pas mes commandes ?**
Dans l'onglet JOUEUR, tape `source tools/hook.sh` (chemin complet depuis le dépôt),
puis rejoue ta commande. Le jeu te le rappelle tout seul au bout de 25 s. 😉

**Je suis bloqué !**
`h` pour un indice, `s` pour la solution. Mieux vaut voir la solution et continuer
que d'abandonner : la répétition en spirale te fera recroiser la notion.

**Je peux refaire un niveau ?**
Oui : `./ilearn goto NUMERO` te replace où tu veux, l'XP compte quand même.

**10 niveaux par jour, c'est obligatoire ?**
Non, c'est un rythme conseillé. La série quotidienne compte dès **1 niveau/jour**.
Les flemmards sont les bienvenus : petit pas chaque jour > rush puis abandon.

## 🤝 Contribuer

- Les jours 1–20 sont écrits à la main dans `game/packs/day01.py` … `day10.py` et `days11_20.py`.
- Les jours 21–100 sont générés par `game/packs/generated.py` (modèles + variantes, en cours d'enrichissement).
- Pour ajouter/enrichir un niveau : inspire-toi d'un niveau existant (même format),
  puis lance `python3 tests/selftest.py` (doit rester à 1000 niveaux valides).
- Idées bienvenues : nouveaux blocs (Docker, Git, SQL...), traductions, mode multijoueur !

## 📜 Licence

MIT — fais-en ce que tu veux, deviens admin, et partage. 🐧
