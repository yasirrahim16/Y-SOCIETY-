#!/bin/bash
pkill -f termux-x11
pkill -f pulseaudio
rm -rf /data/data/termux/files/usr/tmp/.X11-unix/*

pulseaudio --start --exit-idle-time=-1 2>/dev/null

termux-x11 :1 -xstartup "proot-distro login ubuntu --shared-tmp -- env DISPLAY=:1 XDG_CONFIG_DIRS=/etc/xdg dbus-launch --exit-with-session xfce4-session" &

sleep 3
am start -n com.termux.x11/com.termux.x11.MainActivity




