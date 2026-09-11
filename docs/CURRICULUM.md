# 🗺️ Programme des 110 jours — ILearnLinux

10 niveaux par jour. Le 10ᵉ niveau de chaque jour est un **BOSS** (révision, 25 XP).
Les jours 11–100 fonctionnent en **spirale** : chaque jour rejoue les 10 défis du bloc
avec de nouvelles variantes (comme Duolingo : la répétition espacée fait apprendre).
La Saison 2 (jours 101–110) est une campagne CTF scénarisée, écrite à la main 🖊️.

## Jours 1–10 : les bases (écrits à la main 🖊️)

| Jour | Niveaux | Thème |
|---|---|---|
| 1 | 1–10 | Premier contact : `echo`, `pwd`, `whoami`, `date`, `clear`, `history`, `--help`, `>` |
| 2 | 11–20 | Explorer : `ls`, `-l -a -h -R -t`, joker `*`, `ls > fichier` |
| 3 | 21–30 | Naviguer : `cd`, `..`, `~`, `cd -`, chemins absolus/relatifs |
| 4 | 31–40 | Créer : `touch`, `mkdir -p`, `cp`, sauvegardes `.bak` |
| 5 | 41–50 | Lire : `cat`, `head`, `tail`, `wc`, `less`, fusion de fichiers |
| 6 | 51–60 | Ranger : `mv`, `cp -r`, `rmdir`, `rm`, jokers, corbeille maison |
| 7 | 61–70 | Redirections & pipes : `>`, `>>`, `2>`, `2>&1`, `\|`, `tee` |
| 8 | 71–80 | Chercher : `grep`, `-i -v -c -n -r`, `^`, `grep \| wc` |
| 9 | 81–90 | Retrouver : `find`, `-name -type -size -mtime -empty -delete` |
| 10 | 91–100 | Transformer : `sort`, `uniq`, `cut`, `tr` + grande révision, MEGA-BOSS |

## Jours 11–20 : permissions & droits (101–200)

Les 10 défis : `chmod +x` · modes numériques · `u+x` · opérations symboliques ·
`chmod -R` · lancer des scripts · lire `ls -l` · dossiers `700` · secrets `600` · liens `ln -s`.

| Jour | Niveaux | Manche |
|---|---|---|
| 11 | 101–110 | Manche 1 : premiers pas avec les droits + BOSS |
| 12 | 111–120 | Manche 2 + BOSS |
| 13 | 121–130 | Manche 3 + BOSS |
| 14 | 131–140 | Manche 4 + BOSS |
| 15 | 141–150 | Manche 5 + BOSS |
| 16 | 151–160 | Manche 6 + BOSS |
| 17 | 161–170 | Manche 7 + BOSS |
| 18 | 171–180 | Manche 8 + BOSS |
| 19 | 181–190 | Manche 9 + BOSS |
| 20 | 191–200 | Manche 10 + BOSS |

## Jours 21–30 : utilisateurs & groupes (201–300)

Les 10 défis : `whoami` · `id` · `groups` · `who` · `id -u` · `/etc/passwd` ·
recensement · `ls -l` système · `sudo` · `id root`.

| Jour | Niveaux |
|---|---|
| 21 | 201–210 |
| 22 | 211–220 |
| 23 | 221–230 |
| 24 | 231–240 |
| 25 | 241–250 |
| 26 | 251–260 |
| 27 | 261–270 |
| 28 | 271–280 |
| 29 | 281–290 |
| 30 | 291–300 |

*(+ BOSS chaque jour : niveau 210, 220, ..., 300)*

## Jours 31–40 : archives & compression (301–400)

Les 10 défis : `tar -cf` · `tar -tf` · `tar -czf` · extraction `xzf` · `gzip` ·
`gunzip` · `du -sb` · `tar -tvf` · `gzip -k` · avant/après compression.

| Jour | Niveaux |
|---|---|
| 31 | 301–310 |
| 32 | 311–320 |
| 33 | 321–330 |
| 34 | 331–340 |
| 35 | 341–350 |
| 36 | 351–360 |
| 37 | 361–370 |
| 38 | 371–380 |
| 39 | 381–390 |
| 40 | 391–400 |

## Jours 41–50 : système & matériel (401–500)

Les 10 défis : `uname -r` · `hostname` · `uname -m` · `df -h` · `/etc/os-release` ·
`uptime` · `free -h` · `lscpu` · `lsblk` · `/proc/version`.

| Jour | Niveaux |
|---|---|
| 41 | 401–410 |
| 42 | 411–420 |
| 43 | 421–430 |
| 44 | 431–440 |
| 45 | 441–450 |
| 46 | 451–460 |
| 47 | 461–470 |
| 48 | 471–480 |
| 49 | 481–490 |
| 50 | 491–500 |

## Jours 51–60 : processus (501–600)

Les 10 défis : `ps aux` · `ps -ef` · `&` + `jobs` · `$!` · `kill` · `pgrep` ·
`jobs -l` · `ps -p` · `top -b` · `nohup`.

| Jour | Niveaux |
|---|---|
| 51 | 501–510 |
| 52 | 511–520 |
| 53 | 521–530 |
| 54 | 531–540 |
| 55 | 541–550 |
| 56 | 551–560 |
| 57 | 561–570 |
| 58 | 571–580 |
| 59 | 581–590 |
| 60 | 591–600 |

## Jours 61–70 : réseau local (601–700)

Les 10 défis : `ping` IP · `ping` nom · `ip addr` · `ip -br` · `getent` ·
`/etc/hosts` · `ss -tln` · `resolv.conf` · `hostname` · `curl`.

| Jour | Niveaux |
|---|---|
| 61 | 601–610 |
| 62 | 611–620 |
| 63 | 621–630 |
| 64 | 631–640 |
| 65 | 641–650 |
| 66 | 651–660 |
| 67 | 661–670 |
| 68 | 671–680 |
| 69 | 681–690 |
| 70 | 691–700 |

## Jours 71–80 : SSH & copies (701–800)

Les 10 défis : `ssh-keygen` · régénérer la publique · empreintes · `600`/`644` ·
`authorized_keys` · `ssh -V` · `scp` · clés signées `-C` · `~/.ssh/config` · `scp -r`.

| Jour | Niveaux |
|---|---|
| 71 | 701–710 |
| 72 | 711–720 |
| 73 | 721–730 |
| 74 | 731–740 |
| 75 | 741–750 |
| 76 | 751–760 |
| 77 | 761–770 |
| 78 | 771–780 |
| 79 | 781–790 |
| 80 | 791–800 |

## Jours 81–90 : scripting shell (801–900)

Les 10 défis : variables · `$HOME` · écrire des scripts · `for` nombres ·
`for` fichiers · `if [ ]` · `$(...)` · fonctions · `while read` · `printenv`.

| Jour | Niveaux |
|---|---|
| 81 | 801–810 |
| 82 | 811–820 |
| 83 | 821–830 |
| 84 | 831–840 |
| 85 | 841–850 |
| 86 | 851–860 |
| 87 | 861–870 |
| 88 | 871–880 |
| 89 | 881–890 |
| 90 | 891–900 |

## Jours 91–100 : admin pro (901–1000)

Les 10 défis : `journalctl` · `systemctl` · `/var/log` · `dmesg` · chasse au glouton ·
scripts cassés · compresser les logs · compter les erreurs · top IP · `/proc/loadavg`.

| Jour | Niveaux |
|---|---|
| 91 | 901–910 |
| 92 | 911–920 |
| 93 | 921–930 |
| 94 | 931–940 |
| 95 | 941–950 |
| 96 | 951–960 |
| 97 | 961–970 |
| 98 | 971–980 |
| 99 | 981–990 |
| 100 | 991–1000 — **MEGA-BOSS FINAL** 👑 : déploiement complet |

---

# 🕵️ Saison 2 — Agent Cyber (jours 101–110, niveaux 1001–1100, écrits à la main 🖊️)

Campagne CTF scénarisée : recrutement par l'agence, missions (scans `nmap`, intrusions
`ssh`, flags, craquage `john`, forensics, énumération web, pivot, privesc) et examen final.
Les cibles `nmap`/`ssh` sont simulées par le jeu (sorties réalistes) ; tout le reste
exécute de VRAIES commandes Linux.

## Jour 101 : bienvenue à l'agence (1001–1010)

Les 10 défis : premier flag · `file` · `md5sum` · `sha256sum` · `base64 -d` ·
`base64` · `strings` · `grep -r` · `ls -a` · **BOSS** dossier d'enquête.

## Jour 102 : reconnaissance (1011–1020)

Les 10 défis : premier scan · port 80 · 3 ports · `nmap -sV` · `nmap -O` ·
cible éteinte · port filtré · `-sV -O` · 2 cibles · **BOSS** audit express.

## Jour 103 : connexion SSH (1021–1030)

Les 10 défis : `ssh-keygen` · 1re connexion · flag distant · `/var/www` ·
`whoami` distant · flag planqué · code du coffre · `root` refusé · `ssh -i` ·
**BOSS** intrusion complète.

## Jour 104 : chasse aux flags (1031–1040)

Les 10 défis : `.planque` · `find -name` · ratissage · `find -exec` ·
`grep` dans les logs · `strings | grep` · double-base64 · fichier à espaces ·
`grep -o | wc -l` · **BOSS** grand inventaire.

## Jour 105 : mots de passe (1041–1050)

Les 10 défis : `john` + MD5 · `john` + SHA-1 · `john` + SHA-256 · identifier un hash ·
le sel · `/dev/urandom` · grosse wordlist · `0 cracked` · `wc -l` · **BOSS** craquage pro.

## Jour 106 : forensics (1051–1060)

Les 10 défis : filtrer `auth.log` · `grep -c` · top attaquant (`cut/sort/uniq`) ·
connexions légitimes · extraire les IP · classement complet · `tail` ·
qui était visé · casier de l'attaquant · **BOSS** rapport d'incident.

## Jour 107 : énumération web (1061–1070)

Les 10 défis : `ls -R` · `robots.txt` · `.git` exposé · `.bak` oublié ·
ratissage `grep -r` · mot de passe en commentaire · config `.git` · fichiers `~` ·
`grep -a` dans une image · **BOSS** audit web.

## Jour 108 : pivot réseau (1071–1080)

Les 10 défis : reco `.6` · fiche `.7` · indice sur `.6` · saut vers `.7` ·
bannière · flag oublié sur `.7` · double scan · versions des deux ·
fiche de pivot · **BOSS** pivot total.

## Jour 109 : escalade de privilèges (1081–1090)

Les 10 défis : SUID (`-perm -4000`) · `sudo -n -l` · `-writable` · `$PATH` ·
`id` et groupes · `uname -r` · `*.conf` · `ps aux` · `ls ~` ·
**BOSS** énumération privesc.

## Jour 110 : examen d'agent (1091–1100)

Épreuve 1/5 scan · 2/5 intrusion · 3/5 craquage · 4/5 forensics · 5/5 décodage ·
bonus web · bonus SUID · dossier partiel · dossier complet ·
**MÉGA-BOSS FINAL** 👑 : rapport d'agent complet (100 XP) → titre d'**AGENT CYBER**.

---

**Rangs** : 1+ Curieux du terminal 🌱 · 51+ Explorateur ⌨️ · 151+ Bidouilleur 🛠️ ·
301+ Power User ⚡ · 501+ Sorcier du shell 🧙 · 751+ Gardien du système 🛡️ ·
901+ Futur Admin Sys 🚀 · 1000 ADMIN SYS LINUX 👑 · 1001+ Agent Cyber stagiaire 🕵️ ·
1041+ Agent Cyber 💻 · 1081+ Agent Cyber confirmé 🎖️ · 1100 AGENT CYBER D'ÉLITE 👑
