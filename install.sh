#!/usr/bin/env bash
# Puts this config into ~/.config. Whatever was there first is saved in
# ~/.config-backup-<date and time>, so nothing is lost. Run it after the base
# tools are installed (step 2 in README.md).
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
BACKUP="$HOME/.config-backup-$(date +%Y%m%d-%H%M%S)"
ITEMS=(hypr waybar kitty rofi dunst wlogout fastfetch fish gtk-3.0 Kvantum qt5ct qt6ct xsettingsd kdeglobals btop cava hyde)

mkdir -p "$CONFIG" "$BACKUP" "$HOME/.local/bin"
for item in "${ITEMS[@]}"; do
  if [[ -e "$CONFIG/$item" ]]; then
    cp -a "$CONFIG/$item" "$BACKUP/"
  fi
  # A folder is merged into the one already there, so the base tools' other files stay.
  cp -a "$SRC/$item" "$CONFIG/"
done
install -m 755 "$SRC/bin/audio-output-menu" "$HOME/.local/bin/audio-output-menu"

# A few files name my home folder (/home/el). Point them at yours.
if [[ "$HOME" != "/home/el" ]]; then
  for item in "${ITEMS[@]}"; do
    # grep exits 1 when a folder has no match; that is fine, anything else is not.
    { grep -rlZ --binary-files=without-match '/home/el' "$CONFIG/$item" || [[ $? -eq 1 ]]; } |
      xargs -0 -r sed -i "s|/home/el|$HOME|g"
  done
fi

echo "Done. Your previous config is saved in $BACKUP"
echo "Log out and back in, then follow step 4 in README.md."
