#!/bin/bash
# declare colors
red='\033[31m'
blue='\033[34m'
green='\033[32m'
normal='\033[0m'

if [ $USER == "root" ]; then
  echo -e $red"---DO NOT RUN THIS SCRIPT AS ROOT---"$normal
  return
fi

echo -e $blue'---Installing Dependencies (for Arch Linux)---'
echo -e '(fw-fanctrl still must already be installed)'$normal
sudo pacman -S libappindicator-gtk3 python-gobject lm-sensors # install dependencies (assume fw-fanctrl is already installed)

echo -e $blue"---Copying Over Files---"$normal
configPath=/home/$USER/.config/fw-fanctrl # fw-fanctrl config should be installed in ~/.config/fw-fanctrl
sudo cp fw-fanctrl-indicator.py *.svg $configPath # move our python and icon files to where fw-fanctrl is installed

echo -e $blue"---Modifying .service File to Reflect Current User---"$normal # we need to modify the .service file so systemd can find our .py file
sedArg1="s%INDICATOR%${configPath}/fw-fanctrl-indicator.py%g"
sedArg2="s%FW_FANCTRL%${configPath}%g"
sed -i -e ${sedArg1} fw-fanctrl-indicator.service # fingers crossed
sed -i -e ${sedArg2} fw-fanctrl-indicator.service # let's hope this works
sudo cp fw-fanctrl-indicator.service /home/$USER/.config/systemd/user/ # copy our systemd service file to where the user's services are stored

echo -e $blue"---Enabling systemd Service---\n"$normal
systemctl --user enable fw-fanctrl-indicator.service # enable the service
systemctl --user start fw-fanctrl-indicator.service # start the service
loginctl enable-linger $USER # make sure the service starts at boot

echo -e $green"fw-fanctrl-indicator installed, configured, and started! displaying status\n"$normal

systemctl --user status fw-fanctrl-indicator.service # indicate the status of the service
