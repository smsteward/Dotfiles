#!/usr/bin/env bash

lxsession &
picom -b
nitrogen --restore &
redshift &
xinput set-prop 8 289 1
xscreensaver &
xautolock -time 60 -locker "systemctl suspend" &
