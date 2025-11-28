#!/bin/bash
set -euo pipefail

# --- helpers ---------------------------------------------------------------
log() { printf "[autostart] %s\n" "$*" >&2; }

# --- early wait: let X come up ------------------------------------------------
sleep 2

# --- keyboard layout ------------------------------------------------------
setxkbmap -layout "us,ar" -option "grp:alt_shift_toggle"

# --- display logic (X11 only) --------------------------------------------
if [ "${XDG_SESSION_TYPE:-x11}" != "x11" ]; then
  log "Not X11 (XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-unset}), skipping xrandr."
else
  LAPTOP_OUT="DP-4"        # internal panel 1920x1080
  LEFT_OUT="DP-0.2.1"      # Acer 2560x1440 @60
  MID_OUT="DP-0.3.1"       # Devo 2560x1440 @120

  is_connected() { xrandr --query | awk '/ connected/{print $1}' | grep -qx "$1"; }

  laptop_connected=false; is_connected "$LAPTOP_OUT" && laptop_connected=true
  left_connected=false;   is_connected "$LEFT_OUT"   && left_connected=true
  mid_connected=false;    is_connected "$MID_OUT"    && mid_connected=true

  external_present=false
  $left_connected || $mid_connected && external_present=true

  if $external_present; then
    log "External monitor(s) detected. Applying DESKTOP layout (Devo primary)."
    XR=()

    # Left (Acer) 1440p@60
    $left_connected && XR+=( --output "$LEFT_OUT" --mode 2560x1440 --rate 60 --pos 0x0 )

    # Middle (Devo) 1440p@120
    if $mid_connected; then
      if $left_connected; then
        XR+=( --output "$MID_OUT" --mode 2560x1440 --rate 120 --pos 2560x0 )
      else
        XR+=( --output "$MID_OUT" --mode 2560x1440 --rate 120 --pos 0x0 )
      fi
    fi

    # Laptop 1080p@240 on the right-most, vertically centered
    if $laptop_connected; then
      if $left_connected && $mid_connected; then      LX=5120
      elif $left_connected || $mid_connected; then    LX=2560
      else                                            LX=0
      fi
      XR+=( --output "$LAPTOP_OUT" --mode 1920x1080 --rate 240 --pos ${LX}x360 )
    fi

    # Power off disconnected known outputs
    ! $left_connected && XR+=( --output "$LEFT_OUT" --off )
    ! $mid_connected  && XR+=( --output "$MID_OUT"  --off )

    # ------------ PRIMARY SELECTION -----------------------
    # If any external is present:
    #   - Prefer Devo (MID_OUT) as primary when connected.
    #   - Else fall back to Left (Acer) as primary.
    #   - Only use laptop as primary if it's the *only* display (handled in the else branch).
    if $mid_connected; then
      XR+=( --output "$MID_OUT" --primary )
    elif $left_connected; then
      XR+=( --output "$LEFT_OUT" --primary )
    fi
    # ------------------------------------------------------

    xrandr "${XR[@]}"
  else
    log "No externals detected. Applying LAPTOP-ONLY layout (Laptop primary)."
    if $laptop_connected; then
      xrandr \
        --output "$LAPTOP_OUT" --primary --mode 1920x1080 --rate 60 --pos 0x0 \
        --output "$LEFT_OUT" --off \
        --output "$MID_OUT"  --off
    else
      log "Warning: laptop panel ($LAPTOP_OUT) not found; leaving displays unchanged."
    fi
  fi
fi


# --- power: keep screen awake --------------------------------------------
xset -dpms || true
xset s off || true

# --- qtile restart (safe, background) ------------------------------------
qtile cmd-obj -o cmd -f restart &

# --- wallpaper ------------------------------------------------------------
~/.fehbg &    # if you maintain it
feh --bg-scale /home/abdoo/Pictures/Wallpapers/8-bit-graphics-pixels-scene-with-city-night.jpg  &

# --- compositor: ensure single instance ----------------------------------
while pgrep -u "$UID" -x picom >/dev/null; do sleep 1; done
picom --experimental-backends -b &



# --- tray & utilities -----------------------------------------------------
nm-applet &                              # Network Manager
dunst &                                  # Notifications
clipman store &                          # Clipboard history
/usr/libexec/polkit-gnome-authentication-agent-1 &  # Polkit
blueman-applet &                         # Bluetooth Manager
copyq &                                  # Clipboard manager
gxkb &                                   # keyboard layout indicator
