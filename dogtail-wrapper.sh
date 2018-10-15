#!/bin/bash

set -xe

Xvfb :1 -screen 0 1024x768x16 &> /tmp/dogtail-root/xvfb.log &
export DISPLAY=:1.0

# xvfb takes some time to start
sleep 0.5

# Enable Assistive Technology support
gsettings set org.gnome.desktop.interface toolkit-accessibility true

$@
status=$?

kill -9 $(pgrep Xvfb) || true
exit $status
