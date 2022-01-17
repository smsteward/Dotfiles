#!/usr/bin/env bash

lxsession &
picom -b
redshift &
xinput set-prop 8 289 1
xscreensaver &
xautolock -time 60 -locker "systemctl suspend" &
