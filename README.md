# Arch Linux config

My Arch Linux setup on the Hyprland compositor, kept in Git so I can rebuild my desktop on any machine. It started from JaKooLit's Hyprland dotfiles and HyDE, and I've tuned it from there.

![fastfetch in kitty: Arch Linux on Hyprland, with an Intel Core Ultra 9 275HX and an NVIDIA RTX 5060](screenshots/fastfetch.png)

## What's in here

Everything here lives in `~/.config`.

| Folder | What it sets up |
|---|---|
| `hypr/` | Hyprland: keybinds, monitors, workspaces, idle and the lock screen (hypridle, hyprlock), wallpaper effects, and my own settings and scripts in `UserConfigs/` and `UserScripts/` |
| `waybar/` | The status bar |
| `rofi/`, `wofi/` | The app launcher and menus |
| `quickshell/`, `noctalia/` | Desktop shell widgets |
| `swaync/`, `mako/` | Notifications |
| `wlogout/`, `swaylock/` | The logout menu and the lock screen |
| `wallust/` | Color themes made from the wallpaper |
| `kitty/`, `starship.toml`, `zshrc.txt` | The terminal, the prompt and zsh |
| `fastfetch/` | The system summary in the screenshot |
| `btop/`, `cava/` | The system monitor and the audio visualizer |
| `gtk-3.0/`, `Kvantum/`, `qt5ct/`, `qt6ct/`, `nwg-look/` | One theme across GTK and Qt apps |
| `nwg-displays/` | The monitor layout |

My Neovim config has its own repo: [SinaEsmaeili1/nvim](https://github.com/SinaEsmaeili1/nvim). Folders ending in `-backup-back-up_0102_1606` are older copies of the same configs.

## Using it

Copy the folders you want into `~/.config`. They expect the same apps to be installed, so take what fits your setup rather than the whole tree.
