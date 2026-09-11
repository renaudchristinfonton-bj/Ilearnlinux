# ILearnLinux — hook a activer dans l'onglet JOUEUR (UNE fois par onglet) :
#   source /chemin/vers/Ilearnlinux/tools/hook.sh
# Il signale au jeu chaque commande tapee (sans rien changer a ton shell).
# Pour l'activer automatiquement, l'installeur peut l'ajouter a ton ~/.bashrc.

__ilearn_log="${ILEARN_HOME:-$HOME/.ilearnlinux}/commands.log"
__ilearn_last=""

__ilearn_hook() {
  local rc=$?
  local last
  last=$(HISTTIMEFORMAT= history 1 2>/dev/null | sed -E 's/^[[:space:]]*[0-9]+[[:space:]]+//')
  if [ -n "$last" ] && [ "$last" != "$__ilearn_last" ]; then
    __ilearn_last="$last"
    mkdir -p "$(dirname "$__ilearn_log")"
    printf '%s\t%s\t%s\n' "$(date +%s)" "$PWD" "$last" >> "$__ilearn_log"
  fi
  return $rc
}

case "${PROMPT_COMMAND:-}" in
  *__ilearn_hook*) ;;
  *) PROMPT_COMMAND="__ilearn_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}" ;;
esac
export PROMPT_COMMAND

echo "HOOK ILearnLinux actif : joue dans cet onglet, le jeu te regarde depuis l'autre. Bon jeu !"
