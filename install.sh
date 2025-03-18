#!/bin/bash

sudo pacman -S libappindicator-gtk3 python-gobject # install dependencies (assume fw-fanctrl is already installed)
read -p "Enter the path for your fw-fanctrl install - ex. /home/YOUR_USER/.config/fw-fanctrl: " configPath
mv fw-fanctrl-indicator.py *.svg $configPath # move our python and icon files to where fw-fanctrl is installed
sed -i -e 's/CONFIG_FILE/${configPath}\/config.json/g' fw-fanctrl-indicator.service # let's hope this works

mv fw-fanctrl-indicator.service /etc/systemd/system # move our systemd service file to where the services are stored

sudo systemctl enable fw-fanctrl-indicator.service # enable the service
sudo systemctrl start fw-fanctrl-indicator.service # start the service

echo "fw-fanctrl-indicator installed, configured, and started!"
