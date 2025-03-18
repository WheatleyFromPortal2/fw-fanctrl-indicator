#!/bin/bash

sudo pacman -S libappindicator-gtk3 python-gobject # install dependencies (assume fw-fanctrl is already installed)
read -p "Enter the path for your fw-fanctrl install - ex. /home/YOUR_USER/.config/fw-fanctrl: " configPath
sudo cp fw-fanctrl-indicator.py *.svg $configPath # move our python and icon files to where fw-fanctrl is installed
sedArg1="s%FW_FANCTRL_INDICATOR%${configPath}/fw-fanctrl-indicator.py%g"
sedArg2="s%FW_FANCTRL%${configPath}%g"
sed -e -e ${sedArg1} fw-fanctrl-indicator.service # fingers crossed
sed -i -e ${sedArg2} fw-fanctrl-indicator.service # let's hope this works

sudo cp fw-fanctrl-indicator.service /etc/systemd/system/ # copy our systemd service file to where the services are stored

sudo systemctl enable fw-fanctrl-indicator.service # enable the service
sudo systemctl start fw-fanctrl-indicator.service # start the service

echo "fw-fanctrl-indicator installed, configured, and started!"
