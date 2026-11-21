#!/usr/bin/env python3

from pathlib import Path
import subprocess
import colorsys
import re


home = Path.home()

colors_file = home / ".config/hypr/themes/colors.conf"
theme_dir = home / ".config/hyde/themes/Rosé Pine"

palette_file = theme_dir / "wallpaper-colors.css"
adaptive_file = home / ".config/waybar/adaptive-colors.css"
kitty_file = home / ".config/kitty/adaptive-theme.conf"

# -------------------------------------------------------
# Read HyDE's generated wallpaper colors
# -------------------------------------------------------

colors = {}

pattern = re.compile(
    r"^\$wallbash_([A-Za-z0-9]+)\s*=\s*([0-9A-Fa-f]{6})"
)

for line in colors_file.read_text().splitlines():
    match = pattern.match(line.strip())

    if match:
        name, value = match.groups()
        colors[name] = value.upper()

def rgb(hex_color):
    return tuple(
        int(hex_color[i:i+2], 16) / 255
        for i in (0, 2, 4)
    )

def hsl(hex_color):
    r, g, b = rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def hex_from_hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    return "".join(
        f"{round(v * 255):02X}"
        for v in (r, g, b)
    )


def terminal_color(hex_color, min_sat=0.55, min_light=0.58):
    h, s, l = hsl(hex_color)

    s = max(s, min_sat)
    l = max(l, min_light)
    l = min(l, 0.72)

    return hex_from_hsl(h, s, l)


def terminal_ansi_color(hex_color, target_hue):
    _, s, l = hsl(hex_color)

    # Keep some character from the wallpaper,
    # but guarantee readable terminal saturation/lightness.
    s = max(s, 0.60)
    l = max(l, 0.58)
    l = min(l, 0.70)

    return hex_from_hsl(target_hue, s, l)
def hue_distance(a, b):
    ha, _, _ = hsl(a)
    hb, _, _ = hsl(b)

    d = abs(ha - hb)
    return min(d, 1.0 - d)


def luminance(hex_color):
    r, g, b = rgb(hex_color)
    return 0.2126*r + 0.7152*g + 0.0722*b


def mix(a, b, amount):
    ar, ag, ab = rgb(a)
    br, bg, bb = rgb(b)

    result = (
        ar * (1 - amount) + br * amount,
        ag * (1 - amount) + bg * amount,
        ab * (1 - amount) + bb * amount,
    )

    return "".join(
        f"{round(v * 255):02X}"
        for v in result
    )


def rgba(hex_color, alpha):
    r, g, b = (
        int(hex_color[i:i+2], 16)
        for i in (0, 2, 4)
    )

    return f"rgba({r}, {g}, {b}, {alpha})"


def text_for(hex_color):
    return "111111" if luminance(hex_color) > 0.62 else "FFFFFF"


# -------------------------------------------------------
# Background:
# choose darkest of HyDE's actual primary colors
# -------------------------------------------------------

primaries = [
    colors[f"pry{i}"]
    for i in range(1, 5)
    if f"pry{i}" in colors
]

if not primaries:
    raise RuntimeError("No wallbash primary colors found")

base = min(primaries, key=luminance)


# -------------------------------------------------------
# Accent candidates:
# use middle/bright accents from EVERY wallpaper family
# -------------------------------------------------------


candidates = []

# Use the ACTUAL wallpaper primary colors first
for group in range(1, 5):
    key = f"pry{group}"

    if key not in colors:
        continue

    value = colors[key]
    hue, saturation, lightness = hsl(value)

    # Don't use near-black colors as accents
    if lightness < 0.18:
        continue

    score = (
        saturation * 3.5
        + lightness * 0.35
    )

    candidates.append(
        (score, hue, saturation, lightness, value)
    )


# Also allow HyDE accent shades as secondary candidates
for group in range(1, 5):
    for shade in range(4, 7):

        key = f"{group}xa{shade}"

        if key not in colors:
            continue

        value = colors[key]
        hue, saturation, lightness = hsl(value)

        if lightness < 0.18:
            continue

        score = (
            saturation * 2.0
            - abs(lightness - 0.55)
        )

        candidates.append(
            (score, hue, saturation, lightness, value)
        )
candidates.sort(reverse=True)


if not candidates:
    raise RuntimeError("No Wallbash accents found")


accent1 = candidates[0][4]
hue1 = candidates[0][1]


# Pick another strong color that's actually different
accent2 = accent1

for candidate in candidates[1:]:

    hue2 = candidate[1]

    distance = abs(hue1 - hue2)
    distance = min(distance, 1 - distance)

    # ~36 degree hue difference
    if distance > 0.10:
        accent2 = candidate[4]
        break


# Slightly tint the dark base toward the wallpaper accent
main_bg = mix(base, accent1, 0.16)

main_fg = text_for(main_bg)
active_fg = text_for(accent1)
hover_fg = text_for(accent2)


# -------------------------------------------------------
# Generate CSS
# -------------------------------------------------------

css = f"""/* AUTO-GENERATED FROM CURRENT WALLPAPER */
/* Do not manually edit */

@define-color bar-bg {rgba(main_bg, 0.82)};

@define-color main-bg #{main_bg};
@define-color main-fg #{main_fg};

@define-color wb-act-bg #{accent1};
@define-color wb-act-fg #{active_fg};

@define-color wb-hvr-bg #{accent2};
@define-color wb-hvr-fg #{hover_fg};
"""


term_red = terminal_ansi_color(
    colors.get("pry3", accent1), 0.00
)

term_yellow = terminal_ansi_color(
    colors.get("pry4", accent1), 0.15
)

term_green = terminal_ansi_color(
    colors.get("pry2", accent2), 0.33
)

term_cyan = terminal_ansi_color(
    colors.get("4xa4", accent2), 0.50
)

term_blue = terminal_ansi_color(
    colors.get("2xa4", accent2), 0.62
)

term_magenta = terminal_ansi_color(
    colors.get("3xa4", accent1), 0.83
)

kitty_css = f"""# AUTO-GENERATED FROM CURRENT WALLPAPER
# Do not manually edit

background #{main_bg}
foreground #{main_fg}

cursor #{accent1}
cursor_text_color #{active_fg}

selection_background #{accent2}
selection_foreground #{hover_fg}

url_color #{accent2}

active_tab_background #{accent1}
active_tab_foreground #{active_fg}

inactive_tab_background #{main_bg}
inactive_tab_foreground #{main_fg}

active_border_color #{accent1}
inactive_border_color #{accent2}

# black
color0 #{base}
color8 #{main_bg}

# red
color1 #{term_red}
color9 #{term_red}

# green
color2 #{term_green}
color10 #{term_green}

# yellow
color3 #{term_yellow}
color11 #{term_yellow}

# blue
color4 #{term_blue}
color12 #{term_blue}

# magenta
color5 #{term_magenta}
color13 #{term_magenta}

# cyan
color6 #{term_cyan}
color14 #{term_cyan}

# white
color7 #{main_fg}
color15 #FFFFFF"""


theme_dir.mkdir(parents=True, exist_ok=True)
adaptive_file.parent.mkdir(parents=True, exist_ok=True)

palette_file.write_text(css)
adaptive_file.write_text(css)
kitty_file.write_text(kitty_css)

print()
print("Wallpaper → Waybar")
print("-------------------")
print(f"Base       #{base}")
print(f"Background #{main_bg}")
print(f"Accent 1   #{accent1}")
print(f"Accent 2   #{accent2}")
print()

# Restart Waybar after generating the new palette
subprocess.run(
    [
        "systemctl",
        "--user",
        "restart",
        "hyde-Hyprland-bar.service",
    ],
    check=False,
)
# Reload Kitty with the newly generated colors
subprocess.run(
    ["pkill", "-USR1", "-x", "kitty"],
    check=False,
)
# -------------------------------------------------------
# Update Hyprland window borders
# -------------------------------------------------------

hypr_lua = f"""
hl.config({{
    general = {{
        col = {{
            active_border = {{
                colors = {{
                    "rgba({accent1}ff)",
                    "rgba({accent2}ff)"
                }},
                angle = 45
            }},
            inactive_border = "rgba({main_bg}aa)"
        }}
    }}
}})
"""

subprocess.run(
    [
        "hyprctl",
        "eval",
        hypr_lua,
    ],
    check=False,
)
