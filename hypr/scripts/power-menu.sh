#!/usr/bin/env bash

lock=" Lock"
logout=" Logout"
reboot=" Reboot"
shutdown=" Shutdown"

chosen=$(printf '%s\n' "$lock" "$logout" "$reboot" "$shutdown" \
    | wofi --dmenu \
           --prompt "Power" \
           --width 400 \
           --height 550 \
           --lines 4 \
           --no-actions \
           --hide-scroll \
           --hide-search \
           --insensitive \
           --style ~/.config/wofi/power.css)

case "$chosen" in
    "$shutdown") systemctl poweroff ;;
    "$reboot") systemctl reboot ;;
    "$logout") hyprctl dispatch exit ;;
    "$lock") hyprlock ;;
esac
