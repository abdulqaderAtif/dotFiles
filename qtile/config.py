from typing import List  # noqa: F401
import os
import subprocess
from os import path

from libqtile import bar, layout, widget, hook, qtile,images
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key, Match, Screen
from libqtile.lazy import lazy
from settings.path import qtile_path
from extra import multiColorTag
import colors
import subprocess

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration , PowerLineDecoration
from qtile_extras.widget import UPowerWidget
from qtile_extras.widget import Clock , PulseVolumeExtra ,BrightnessControl
from libqtile import widget
from qtile_extras import widget as qtile_extras_widget
from libqtile.bar import Bar

mod = "mod4"
terminal = "kitty"
mymenu = "rofi -show drun -theme ~/.config/rofi/config.rasi"
openedApps = "rofi -show window -theme ~/.config/rofi/windowSwitcher.rasi"
browser = "flatpak run com.google.Chrome"
files = "thunar"
screenie = "flameshot gui"
vscode = "code"
discord = "discord-ptb"
lockScreen = "i3lock --show-failed-attempts --color 000000 --image Pictures/blue-screen.png --tiling"

colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.catppuccin()

def toggle_max(qtile):
    qtile.current_window.toggle_maximize()

@hook.subscribe.client_new
def float_copyq(window):
    X_OFFSET = 20  # Offset from the left of the screen
    Y_OFFSET = 50  # Offset from the top of the screen
    ALIGNMENT = "right"  # Options: left, right, center
    if window.window.get_wm_class() and "copyq" in window.window.get_wm_class():
        window.floating = True  # Make the window float

        # Set the desired window size
        width, height = 700, 700  # Change these values if needed

        # Get the currently focused screen
        screen = window.qtile.current_screen
        screen_width = screen.width
        screen_height = screen.height

       # Determine X position based on alignment
        if ALIGNMENT == "left":
            x = screen.x + X_OFFSET
        elif ALIGNMENT == "right":
            x = screen.x + screen_width - width - X_OFFSET
        else:  # Default to center
            x = screen.x + (screen_width - width) // 2

        # Set Y position
        y = screen.y + Y_OFFSET  # Distance from top of screen

        # Move CopyQ to the active screen and set its size
        window.togroup(screen.group.name)  
        window.place(x, y, width, height, 2, None)  # Adjust x, y if needed
        window.bring_to_front()

        # Move mouse cursor to CopyQ window
        cursor_x = x + width // 2
        cursor_y = y + height // 2
        subprocess.run(["xdotool", "mousemove", str(cursor_x), str(cursor_y)])       

keys = [

    Key([mod , "mod1"], "l", lazy.spawn(lockScreen), desc="lock the screen using i3lock"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    Key([mod, "shift"], "m", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "m", lazy.function(toggle_max), desc="Toggle max layout"),
    Key([mod], "n", lazy.window.toggle_minimize(), desc="Toggle minimize on the focused window"),

    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "x", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod, "shift"], "q", lazy.spawn("rofi-power"), desc="Open Rofi Power Menu"),

    # App spawner
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn(mymenu)),
    Key([mod], "w", lazy.spawn(browser)),
    Key([mod, "shift"], "Return", lazy.spawn(files)),
    Key([mod, "shift"], "s", lazy.spawn(screenie)),
    Key([mod], "s", lazy.spawn(vscode)),
    Key([mod], "z", lazy.spawn(discord)),
    Key([mod], "c", lazy.spawn("copyq toggle")),
    Key(["mod1"], "tab", lazy.spawn(openedApps) ,desc="Rofi window switcher",),

    # Movement Keys
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    # Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "space", lazy.layout.flip()),

    # Switch focus to specific monitor (out of three)
    Key([mod], "i", lazy.to_screen(1)), # Left screen (External monitor) (secondary) (acer)
    Key([mod], "o", lazy.to_screen(0)), # Middle screen (External monitor) (primary) (devo)
    Key([mod], "p", lazy.to_screen(2)), # Right screen (Laptop screen) 

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),

    # Function Keys
    Key([], "XF86AudioLowerVolume", lazy.spawn("pulsemixer --change-volume -5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pulsemixer --change-volume +5")),

    # --- Media Keys ---
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause media"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next track"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop"), desc="Stop playback"),
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute", desc="Mute media")),

    # Brightness Down
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Brightness Up
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),

    # Switch keyboard layout
    # Key(["mod1", "shift"], lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."), # broke the system

]

# Create labels for groups and assign them a default layout.
groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "minus", "equal"]

#group_labels = ["󰖟", "", "", "", "", "", "", "", "ﭮ", "", "", "﨣", "F1", "F2", "F3", "F4", "F5"]
group_labels = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

# Add group names, labels, and default layouts to the groups object.
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

# Add group specific keybindings
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Mod + number to move to that group."),
        # Key(["mod1"], "Tab", lazy.screen.next_group(skip_empty = True), desc="Move to next group."),
        # Key(["mod1", "shift"], "Tab", lazy.screen.prev_group(), desc="Move to previous group."),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Move focused window to new group."),

    ])


# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# Define scratchpads
groups.append(ScratchPad("scratchpad", [
    # DropDown("term", "kitty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    # DropDown("term2", "kitty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    # DropDown("ranger", "kitty --class=ranger -e ranger", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("volume", "kitty --class=volume -e pulsemixer", width=0.3, height=0.2, x=0.7, y=0.0, opacity=0.8, background=colors[1],foreground=colors[6]),
    # DropDown("copyq", "copyq show", width=0.3, height=0.3, x=0.7, y=0.1, opacity=0.9, on_focus_lost_hide=True, wrap_pointer=True),
    # DropDown("mus", "kitty --class=mus -e flatpak run io.github.hrkfdn.ncspot", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    # DropDown("news", "kitty --class=news -e newsboat", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),

]))

# Scratchpad keybindings
keys.extend([
    # Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('term')),
    # Key([mod], "c", lazy.group['scratchpad'].dropdown_toggle("copyq")),
    Key([mod], "v", lazy.group['scratchpad'].dropdown_toggle('volume')),
    # Key([mod], "m", lazy.group['scratchpad'].dropdown_toggle('mus')),
    # Key([mod], "b", lazy.group['scratchpad'].dropdown_toggle('news')),
    # Key([mod, "shift"], "n", lazy.group['scratchpad'].dropdown_toggle('term2')),
])


def open_rofi():
    qtile.cmd_spawn("rofi -show drun -show-icons -theme ~/.config/rofi/config.rasi")


# Define layouts and layout themes
layout_theme = {
        "margin":5,
        "border_width": 5,
        "border_focus": colors[6],
        "border_normal": colors[1],
        "border_on_single": True,
        "grow_amount": 5,
    }

layouts = [
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.MonadThreeCol(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.Spiral(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Max(**layout_theme)
    # layout.Bsp(**layout_theme),
    layout.Columns(**layout_theme),
]


#################################
#################################
#################################
#
#
# BAR CONFIGURATIONS 
#
#
#################################
#################################
#################################

sep = widget.Sep(linewidth = 3, padding = 15, foreground = colors[1], background = colors[0],size_percent = 50,)
spacer1 = widget.Spacer(length=5,background=colors[0],)
spacer2 = widget.Spacer(length=1, background=colors[6],)
spacer3 = widget.Spacer(background=colors[0])
spacer4 = widget.Spacer(length=4, background=colors[0])

#################################
#################################
#################################
#
#
# BAR LEFT SIDE 
#
#
#################################
#################################
#################################

logo = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/launchMenu.svg", 
    margin=4, 
    mouse_callbacks={"Button1": open_rofi}, 
    scale=True, 
    background=colors[0],
)

OpenChrome = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/chrome.svg", 
    margin=4, 
    mouse_callbacks={"Button1": lazy.spawn(browser)}, 
    scale=True, 
    background=colors[0],
)

groupbox =  widget.GroupBox(
    font="JetBrainsMono Nerd Font ",
    fontsize=20,
    padding_x=5,
    padding_y=5,
    margin_x=10,
    rounded=False,
    center_aligned=True,
    disable_drag=True,
    borderwidth=3,
    highlight_method="line",
    hide_unused = True,
    active=colors[6],
    inactive=colors[1],
    highlight_color=colors[0],
    this_current_screen_border=colors[6],
    other_current_screen_border=colors[6],
    this_screen_border=colors[3],
    other_screen_border=colors[3],
    background=colors[0],
    foreground=colors[3],
)

def my_parse_text(window_title):

    name_map = {
        "Code": "VS Code",
        "Discord": "Discord",
        "Google Chrome": "Chrome",
        "Thunar": "Thunar",
        "kitty": "Terminal",
    }
    wm_class = window_title.split('.')[-1]
    if wm_class in name_map:
        return name_map[wm_class]
    
    for name, short_name in name_map.items():
        if name in window_title:
            return short_name
            
    return window_title.split(" ")[0]

currentApp = widget.TaskList(
    theme_mode = 'fallback',
    theme_path = '/usr/share/icons/Papirus' ,
    font = "JetBrainsMono Nerd Font",
    fontsize = 18,
    foreground=colors[2],
    background=colors[0],
    margin_x=0,
    spacing = 0,
    icon_size = 25,
    txt_maximized = ' + ',
    txt_minimized = ' - ',
    padding_y=0,
    padding_x= 10,
    border=colors[6],
    rounded=True,

    # Underline and color for urgent windows
    urgent_alert_method='text',
    markup_urgent='<span underline="low" foreground="#FF0000">{}</span>', 

    parse_text=my_parse_text,

    # Underline customization
    markup=True,  # This must be enabled
    markup_focused='<span>{}</span>', # No Underline focused window
    markup_unfocused='<span>{}</span>', # No underline for other windows
                    
    # Remove the default border/block highlight
    highlight_method='text', # Set to text so it only uses markup
                    
)

#################################
#################################
#################################
#
#
# BAR MIDDLE
#
#
#################################
#################################
#################################

clockIcon = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/clock_time_icon.ico", 
    margin=3,
)

clock = widget.Clock(
    font="JetBrainsMono Nerd Font",
    format=" %A %d, %B %m, %H:%M:%S",
    foreground=colors[2], 
    background=colors[0], 
    fontsize = 15,
)

#################################
#################################
#################################
#
#
# BAR RIGHT SIDE 
#
#
#################################
#################################
#################################

tray = qtile_extras_widget.Systray(
    background=colors[0],
    padding = 10,
)

clipboard = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/clipboard.svg", 
    margin=6, 
    mouse_callbacks={"Button1": lazy.spawn("copyq toggle")}, 
    scale=True, 
    background=colors[0],
)

# --- needs fix --- # broke the system
keyboardLayouts = widget.KeyboardLayout(
    configured_keyboards=["us", "ar"],
    display_map={"us": "US", "ar": "AR"},
    mouse_callbacks={},
    fontsize=14,
    background=colors[0],
    foreground=colors[2],  
)


pulseVolumeExtra = qtile_extras_widget.PulseVolumeExtra(
    mode = 'both',
    theme_path= "~/.config/qtile/Assets/VolumeIcons/",
    mouse_callbacks={"Button3": lazy.group['scratchpad'].dropdown_toggle('volume')},  # Open sound settings 
    mute_command="pulsemixer --toggle-mute",
    hide_interval = 1.5,
    bar_background = colors[0],
    bar_colour = colors[6],
    bar_colour_normal = colors[6],
    bar_colour_high = colors[6],
    bar_colour_loud = colors[6],
    bar_text_fontsize = 18,
    bar_text_font = "JetBrainsMono Nerd Font",
    bar_height = 15,
    icon_size= 26,
)

# Function to get battery info and display a notification
def show_battery_details():
    
    try:
        
        battery_status = subprocess.check_output(['acpi', '-b'], encoding='utf-8').strip()
        
        
        title = "Battery Status"
        message = battery_status.replace("Battery 0: ", "")
        name = "Battery"
        
        timeout_ms = 3500

        subprocess.run(['dunstify','-a',name, title, message , '-t', str(timeout_ms)])
    except FileNotFoundError:
        subprocess.run(['dunstify', 'Error', 'acpi not found','-t', str(timeout_ms)])
    except Exception as e:
        subprocess.run(['dunstify', 'Error', f'Could not get battery info: {e}','-t', str(timeout_ms)])

battryWidget = widget.BatteryIcon(
    theme_path = '~/.config/qtile/Assets/BatteryIcon/',
    scale = 1.2,
    update_interval=10,
    mouse_callbacks={'Button1': show_battery_details},
)

battrypercent = widget.Battery(
    format='{percent:2.0%}',
    font = "JetBrainsMono Nerd Font",
    update_interval=10,
    background=colors[0],
    foreground=colors[2],
    fontsize = 16,
)

screenBackLight = widget.Backlight(
    format='{percent:2.0%}',
    brightness_file = '/sys/class/backlight/nvidia_0/brightness',
    max_brightness_file = '/sys/class/backlight/nvidia_0/max_brightness',
    background = colors[0],
    fontsize = 16,
    font = "JetBrainsMono Nerd Font",
)

brightnessIcon = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/brightness/brightness-bright.svg", 
    margin=0, 
    scale=True, 
    background=colors[0],
)
# --- needs fix --- # not showing the bar
# brightnessControl = qtile_extras_widget.BrightnessControl(
#     fmt='{}',
#     mode = 'bar',
#     device='nvidia_0',
#     backlight_name='nvidia_0',
#     brightness_file = '/sys/class/backlight/nvidia_0/brightness',
#     max_brightness_file = '/sys/class/backlight/nvidia_0/max_brightness',
# )

powerMenu = qtile_extras_widget.Image(
    filename= "~/.config/qtile/Assets/shutdown.svg",
    margin=6,
    mouse_callbacks={"Button1": lazy.spawn("rofi-power-button")},
    background=colors[0],
)

screens = [
    Screen(
        top=bar.Bar([
            logo,
            spacer1,
            groupbox,
            currentApp,
            # clockIcon,
            clock,
            spacer3,
            
            
            tray,
            spacer4,
            clipboard,
            # keyboardLayouts, # broke the system
            spacer4,
            sep,
            spacer4,
            pulseVolumeExtra,
            spacer4,
            spacer4,
            spacer4,
            battryWidget,
            battrypercent,
            spacer4,
            brightnessIcon,
            screenBackLight,
            powerMenu,
            spacer4,

            ],
            # opacity=1, 
            background="#00000000", #use this for transparency
            margin=2,
            size=35,
            ),
        ),
    Screen(
        top=bar.Bar([
            logo,
            spacer1,
            groupbox,
            spacer3,
            clock,
            spacer3,
            
            spacer4,
            pulseVolumeExtra,
            ],
            margin=2,
            size=35,
            background="#00000000",
            ),
        ),

    Screen(
        top=bar.Bar([
            logo,
            spacer1,
            groupbox,
            spacer3,
            clock,
            spacer3,

            spacer4,
            pulseVolumeExtra,
            ],
            margin=2,
            size=35,
            background="#00000000",
            ),
        ),
    Screen(
        top=bar.Bar([
            logo,
            spacer1,
            groupbox,
            spacer3,
            clock,
            spacer3,

            spacer4,
            pulseVolumeExtra,
            ],
            margin=2,
            size=35,
            background="#00000000",
            ),
        )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class= "copyq"), # force copyq to float
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="Blueman-manager"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus=colors[8],
    border_normal=colors[1],
    border_width=3,

)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = False

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "qtile"
