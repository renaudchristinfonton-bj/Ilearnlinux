#!/bin/bash
# ILearnLinux — installation en 30 secondes.
#   git clone <ton-depot> && cd Ilearnlinux && ./install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "  ILearnLinux — installation"
echo "=============================================="

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERREUR : python3 est requis."
  echo "  Ubuntu/Debian : sudo apt update && sudo apt install python3"
  exit 1
fi
echo "[OK] python3 : $(python3 --version)"

chmod +x "$ROOT/ilearn"
echo "[OK] lanceur executable"

mkdir -p "${ILEARN_HOME:-$HOME/.ilearnlinux}" "$HOME/IlearnLinux-arena"
echo "[OK] dossiers crees (~/.ilearnlinux, ~/IlearnLinux-arena)"

echo ""
echo "Verification des 1000 niveaux..."
python3 "$ROOT/game/main.py" doctor

echo ""
echo "----------------------------------------------"
echo "Optionnel : ajouter le raccourci 'ilearn' + le hook joueur a ton ~/.bashrc ?"
echo "  (recommande : le hook sera actif dans chaque nouveau terminal)"
read -r -p "[o/N] " answer
if [[ "$answer" =~ ^[oOyY] ]]; then
  {
    echo ""
    echo "# ILearnLinux"
    echo "alias ilearn='$ROOT/ilearn'"
    echo "[ -f '$ROOT/tools/hook.sh' ] && source '$ROOT/tools/hook.sh' >/dev/null"
  } >> "$HOME/.bashrc"
  echo "[OK] ~/.bashrc mis a jour (alias ilearn + hook auto). Reouvre ton terminal."
else
  echo "OK, mode manuel :"
  echo "  - jeu   : $ROOT/ilearn play"
  echo "  - joueur: source $ROOT/tools/hook.sh  (a taper UNE fois par onglet joueur)"
fi

echo ""
echo "C'est parti ! Ouvre DEUX onglets de terminal :"
echo "  Onglet JEU    : $ROOT/ilearn play"
echo "  Onglet JOUEUR : source $ROOT/tools/hook.sh  (puis joue !)"
