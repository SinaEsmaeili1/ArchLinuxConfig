-- Hyprland loads this file when it is started without a config, and it prefers
-- it over hyprland.conf. HyDE loads it too, last, as the override layer below.
-- The block keeps the two apart: hyde.lua sets `hyde` on its first line, so it
-- runs only when this file is the entry point and HyDE has not been loaded.
-- Removing it leaves a session with a cursor and nothing else.
if not hyde then
	local share = os.getenv("XDG_DATA_HOME") or (os.getenv("HOME") .. "/.local/share")
	local entry = share .. "/hypr/hyde.lua"
	local handle = io.open(entry, "r")
	if not handle then
		error("HyDE is not installed at " .. entry .. ". Run install.sh -r, or point Hyprland at your own config.")
	end
	handle:close()
	dofile(entry)
end

-- Other Lua files next to this one can be pulled in with require("name").

hl.bind("SUPER + SHIFT + B", hl.dsp.exec_cmd("hyde-shell waybar --select"), {
    description = "[Waybar] select layout/style",
})

hl.bind("SUPER + R", hl.dsp.exec_cmd("/home/el/.local/bin/toggle-black-hole-recording"), {
    description = "[Screen Recording] toggle black hole region recording",
})

hl.bind("SUPER + SHIFT + Z", hl.dsp.exec_cmd("/home/el/.local/bin/audio-output-menu"), {
    description = "[Audio] choose sound output",
})

-- Caps Lock is an extra Esc (for leaving insert mode in Neovim);
-- Shift + Caps Lock still toggles Caps Lock.
hl.config({
	input = {
		kb_options = "caps:escape_shifted_capslock",
	},
})

-- Your Hyprland configuration. HyDE never overwrites this file.
--
-- It loads after HyDE's own binds, so settings here take precedence. Replacing
-- a bind needs more than that: see below. HyDE's defaults live in
-- ~/.local/share/hypr/lua/ and are overwritten on every update, so edits there
-- do not survive.
--
-- Adding a keybind:
--
--     hl.bind("SUPER + SPACE", hl.dsp.exec_cmd(hyde.sh.gamelauncher()), {
--         description = "[Utilities] game launcher",
--     })
--
-- Replacing one of HyDE's: bind the same combination again and yours takes
-- over, but copy its flags across as well. A bind counts as the same one only
-- when its flags match, and `description` is not a flag — miss one and both
-- binds stay live on that combination. Copy the whole options table from
-- ~/.local/share/hypr/lua/key_binds.lua and change only what you need:
--
--     hl.bind("F9", hl.dsp.exec_cmd(hyde.sh.volumecontrol("-o", "m")), {
--         locked = true,
--         description = "[Hardware Controls|Audio] un/mute output",
--     })
--
-- Press SUPER + / to see what is actually loaded, your own binds included.
-- The full reference is KEYBINDINGS.md in the HyDE repository.
--
-- Other Lua files next to this one can be pulled in with require("name").

-- Monitors: let Hyprland pick the scale from each screen's resolution and
-- physical size, instead of the fixed numbers nwg-displays writes into
-- monitors.lua. These run after HyDE (and after monitors.lua, which it
-- requires), so they win — and they survive the next nwg-displays run.
--
-- "auto" only ever picks a scale whose logical size is a whole number of
-- pixels, which is what the old 1.43333 on eDP-2 was not: Hyprland rejected it
-- and silently fell back to 1.33333, so the saved layout no longer matched the
-- real one and the two screens overlapped by 134 px.
--
-- Anything plugged in later and not named below is covered by the first rule.

hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })

-- Laptop on the left, 4K on its right, bottom edges level
-- (eDP-2 2560x1600 → 1.6 → 1600x1000; HDMI-A-1 3840x2160 → 1.5 → 2560x1440).
hl.monitor({ output = "eDP-2", mode = "preferred", position = "0x440", scale = "auto" })
hl.monitor({ output = "HDMI-A-1", mode = "preferred", position = "1600x0", scale = "auto" })
