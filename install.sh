#!/bin/bash
if [$USER == root]; then
  echo "---DO NOT RUN THIS SCRIPT AS ROOT---"
  return
fi

sudo pacman -S libappindicator-gtk3 python-gobject # install dependencies (assume fw-fanctrl is already installed)
#read -p "Enter the path for your fw-fanctrl install - ex. /home/YOUR_USER/.config/fw-fanctrl: " configPath
configPath=/home/$USER/.config/fw-fanctrl
sudo cp fw-fanctrl-indicator.py *.svg $configPath # move our python and icon files to where fw-fanctrl is installed
sedArg1="s%INDICATOR%${configPath}/fw-fanctrl-indicator.py%g"
sedArg2="s%FW_FANCTRL%${configPath}%g"
sed -i -e ${sedArg1} fw-fanctrl-indicator.service # fingers crossed
sed -i -e ${sedArg2} fw-fanctrl-indicator.service # let's hope this works
sed -i -e "s%NOT_ROOT%${USER}%g" fw-fanctrl-indicator.service # don't run the indicator as root :facepalm: 

sudo cp fw-fanctrl-indicator.service /home/$USER/.config/systemd/user/ # copy our systemd service file to where the user's services are stored

systemctl --user enable fw-fanctrl-indicator.service # enable the service
systemctl --user start fw-fanctrl-indicator.service # start the service

echo "fw-fanctrl-indicator installed, configured, and started!"

sudo systemctl status fw-fanctrl-indicator.service
