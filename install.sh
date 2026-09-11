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

if ! command -v bash >/dev/null 2>&1; then
  echo "ERREUR : bash est requis."
  exit 1
fi
echo "[OK] bash : $(bash --version | head -n1)"

chmod +x "$ROOT/ilearn" "$ROOT/game/fakebin/nmap" "$ROOT/game/fakebin/ssh" "$ROOT/game/fakebin/john"
echo "[OK] lanceur + simulateurs executables"

mkdir -p "${ILEARN_HOME:-$HOME/.ilearnlinux}" "$HOME/IlearnLinux-arena"
echo "[OK] dossiers crees (~/.ilearnlinux, ~/IlearnLinux-arena)"

echo ""
echo "Verification des niveaux..."
python3 "$ROOT/game/main.py" doctor

echo ""
echo "----------------------------------------------"
echo "Optionnel : ajouter le raccourci 'ilearn' a ton ~/.bashrc ?"
read -r -p "[o/N] " answer
if [[ "$answer" =~ ^[oOyY] ]]; then
  {
    echo ""
    echo "# ILearnLinux"
    echo "alias ilearn='$ROOT/ilearn'"
  } >> "$HOME/.bashrc"
  echo "[OK] ~/.bashrc mis a jour (alias ilearn). Reouvre ton terminal."
else
  echo "OK : lance le jeu avec $ROOT/ilearn play"
fi

echo ""
echo "C'est parti ! UN SEUL terminal suffit :"
echo "  $ROOT/ilearn play   (ou 'ilearn play' avec l'alias)"
echo "Tape de vraies commandes, le mentor te guide. Bonne chance, agent !"
