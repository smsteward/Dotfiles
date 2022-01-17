# Stephen's Qtile config

"""Main config file for Qtile."""

# --------------------
# Package Imports
# --------------------
import socket
import os
import subprocess
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, qtile, hook
from libqtile.config import Click, Drag, Group, Key, Screen, Match
from libqtile.lazy import lazy
from libqtile.dgroups import simple_key_binder

# --------------------
# Set personal variables
# --------------------
mod = "mod4"
my_terminal = "alacritty"
my_browser = "librewolf"
my_file_manager = "pcmanfm"
my_music_player = "ytmdesktop-bin"
my_ide = "pyenv/bin/spyder"
my_email = "thunderbird"

# --------------------
# Set shortcut keys
# --------------------
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(my_terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Switching monitor focus
    Key([mod], "comma", lazy.to_screen(0), desc="Focus to monitor 1"),
    Key([mod], "period", lazy.to_screen(1), desc="Focus to monitor 2"),

    # Audio key commands
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Custom spawn commands
    Key([mod], "d", lazy.spawn("/usr/local/bin/dmenu_run")),
    Key([mod], "b", lazy.spawn(my_browser)),
    Key([mod], "f", lazy.spawn(my_file_manager)),
    Key([mod], "y", lazy.spawn(my_music_player)),
    Key([mod], "p", lazy.spawn(my_ide)),
    Key([mod], "e", lazy.spawn(my_email)),
    Key([mod], "s", lazy.spawn("/usr/lib/kscreenlocker_greet"))
    ]

# -------------------
# Define groups
# -------------------
groups = [Group("1", layout="monadtall", label="DEV"),
          Group("2", layout="monadtall", label="WWW", matches=[Match(
              wm_class=["LibreWolf", "chromium-browser"])]),
          Group("3", layout="monadtall", label="SYS", matches=[Match(
              wm_class=["pcmanfm", "Thunderbird"])]),
          Group("4", layout="monadtall", label="DOC", matches=[Match(
              wm_class=["libreoffice"])]),
          Group("5", layout="monadtall", label="MUS", matches=[Match(
              wm_class=["youtube-music-desktop-app"])]),
          Group("6", layout="max", label="VID", matches=[Match(
              wm_class=["mpv"])]),
          Group("7", layout="floating", label="GFX")]

for group in groups:
    keys.extend([Key([mod], group.name, lazy.group[group.name].toscreen()),
                 Key([mod, "shift"], group.name, lazy.window.togroup(
                     group.name, switch_group=True))])

# -------------------
# Allow mod key to change groups
# -------------------
dgroups_key_binder = simple_key_binder("mod4")

# -------------------
# Set layout theme
# -------------------
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"}

# -------------------
# Define layouts
# -------------------
layouts = [layout.MonadTall(**layout_theme),
           layout.Max(**layout_theme),
           layout.Stack(num_stacks=2),
           layout.Floating(**layout_theme)]

# -------------------
# Define colors
# -------------------
colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]


# -------------------
# Define prompt
# -------------------
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

# -------------------
# Widget settings
# -------------------
widget_defaults = dict(font="Ubuntu Bold",
                       fontsize=10,
                       padding=2,
                       background=colors[2])
extension_defaults = widget_defaults.copy()


# -------------------
# Define list of widgets
# -------------------
def init_widgets_list():
    """Return list of widgets for top bar."""
    widgets_list = [widget.Image(filename="~/.config/qtile/icons/python.png",
                    scale="False",
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(
                        my_terminal)}),
                    widget.Sep(linewidth=0,
                               padding=6,
                               foreground=colors[2],
                               background=colors[0]),
                    widget.GroupBox(font="Ubuntu Bold",
                                    fontsize=9,
                                    margin_y=3,
                                    margin_x=0,
                                    padding_y=5,
                                    padding_x=3,
                                    borderwidth=3,
                                    active=colors[2],
                                    inactive=colors[7],
                                    rounded=False,
                                    highlight_colors=colors[1],
                                    highlight_method="line",
                                    this_current_screen_border=colors[6],
                                    this_screen_border=colors[4],
                                    other_current_screen_border=colors[6],
                                    other_screen_border=colors[4],
                                    foreground=colors[2],
                                    background=colors[0]),
                    widget.TextBox(text='|',
                                   font="Ubuntu Mono",
                                   background=colors[0],
                                   foreground="474747",
                                   padding=2,
                                   fontsize=14),
                    widget.CurrentLayoutIcon(
                        custom_icon_paths=[os.path.expanduser(
                            "~/.config/qtile/icons")],
                        foreground=colors[2],
                        background=colors[0],
                        padding=0,
                        scale=0.7),
                    widget.CurrentLayout(foreground=colors[2],
                                         background=colors[0],
                                         padding=5),
                    widget.TextBox(text="|",
                                   font="Ubuntu Mono",
                                   background=colors[0],
                                   foreground="474747",
                                   padding=2,
                                   fontsize=14),
                    widget.WindowName(foreground=colors[6],
                                      background=colors[0],
                                      padding=0),
                    widget.Sep(linewidth=0,
                               padding=6,
                               foreground=colors[2],
                               background=colors[0]),
                    widget.Prompt(background=colors[0],
                                  foreground=colors[2],
                                  font="Ubuntu Bold",
                                  fontsize=10,
                                  padding=5,
                                  prompt="Enter command: "),
                    widget.Systray(
                            background=colors[0],
                            padding=5),
                    widget.Sep(linewidth=0,
                            padding=6,
                            foreground=colors[2],
                            background=colors[0]),
                    widget.TextBox(
                        text="",
                        background=colors[0],
                        foreground=colors[6],
                        font="Ubuntu Mono",
                        padding=0,
                        fontsize=37),
                    widget.OpenWeather(
                            fontsize=12,
                            metric=False,
                            location="Durham",
                            background=colors[6],
                            foreground=colors[1],
                            coordinates={"longitude": "-78.938671",
                                         "latitude": "35.898763"},
                            update_interval=300,
                            format="{location_city}: {main_temp} °{units_temperature} {weather_details}"),
                    widget.TextBox(
                            text="",
                            background=colors[6],
                            foreground=colors[9],
                            font="Ubuntu Mono",
                            padding=0,
                            fontsize=37),
                    widget.PulseVolume(
                            fontsize=12,
                            background=colors[9],
                            foreground=colors[1],
                            padding=5,
                            step=5,
                            fmt="Vol: {}",
                            volume_app="pactl",
                            update_interval=0.2,
                            check_mute_command="pactl get-sink-mute @DEFAULT_SINK@",
                            get_volume_command="pactl get-sink-volume @DEFAULT_SINK@"),
                    widget.TextBox(
                       text="",
                       font="Ubuntu Mono",
                       background=colors[9],
                       foreground=colors[3],
                       padding=0,
                       fontsize=37
                       ),
                    widget.Net(interface="wlp5s0",
                            fontsize=12,
                               format="  {down} ↓↑ {up}",
                               foreground=colors[1],
                               background=colors[3],
                               padding=5),
                    widget.TextBox(
                        text="",
                        font="Ubuntu Mono",
                        background=colors[3],
                        foreground=colors[4],
                        padding=0,
                        fontsize=37),
                    widget.CPU(
                        fontsize=12,
                        format="  {freq_current}GHz {load_percent}%",
                        background=colors[4],
                        foreground=colors[1],
                        padding=5),
                    widget.TextBox(
                        text="",
                        font="Ubuntu Mono",
                        foreground=colors[6],
                        background=colors[4],
                        padding=0,
                        fontsize=37),
                    widget.Memory(
                       fontsize=12,
                       format="  {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}",
                       foreground=colors[1],
                       background=colors[6],
                       padding=5
                       ),
                    widget.TextBox(
                       text="",
                       font="Ubuntu Mono",
                       background=colors[6],
                       foreground=colors[9],
                       padding=0,
                       fontsize=37
                       ),
                    widget.Clock(
                        fontsize=12,
                        foreground=colors[1],
                        background=colors[9],
                        format="%A, %B %d - %H:%M "
                        ),
                    ]
    return widgets_list


# -------------------
# Define the screens and top bar
# -------------------
def init_widgets_screen1():
    """Define widgets for monitor 1."""
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    """Define widgets for monitor 2."""
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


def init_screens():
    """Return the top bar on both screens."""
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0,
                               size=24), wallpaper="~/Pictures/Wallpaper/awesome.jpg",
                               wallpaper_mode="stretch"),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0,
                               size=24), wallpaper="~/Pictures/Wallpaper/awesome.jpg",
                               wallpaper_mode="stretch")]


# -------------------
# Put the widgets on the screen
# -------------------
if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


# -------------------
# Moving windows around
# -------------------
def window_to_prev_group(qtile):
    """Move window to previous group in group list."""
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    """Move window to next group in group list."""
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    """Move window to previous screen."""
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    """Move window to next screen."""
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    """Switch screens."""
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


# -------------------
# Special mouse actions for floating windows
# -------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# -------------------
# Miscellaneous settings
# -------------------
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# -------------------
# Floating layout rules
# -------------------
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(title="pinentry-qt"),
    Match(title="pinentry")
        ])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True


# -------------------
# Startup hooks
# -------------------
@hook.subscribe.startup_once
def start_once():
    """Qtile startup hook."""
    home = os.path.expanduser("~")
    subprocess.call([home+"/.config/qtile/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
