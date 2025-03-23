# fw-fanctrl-indicator

A GTK 3 system tray indicator for the fw-fanctrl service

Creates a system tray widget using GTK3 and the AppIndicator bindings
Created for Arch Linux, but any other distro could work if you modify `install.sh`


# Supported Desktop Environments
| Desktop Environment | Working? |  Notes  | Last Tested Version |
|:--------------------|:---------|:--------|:--------------------|
| KDE                 | ✅ Yes   | none    | 6.2.4               |
| GNOME               | Untested | none    | none                |
| Budgie              | Untested | none    | none                |
| XFCE                | Untested | none    | none                |

# Requirements

- [fw-fanctrl](https://github.com/TamtamHero/fw-fanctrl) 
- [libappindicator-gtk3](https://archlinux.org/packages/extra/x86_64/libappindicator-gtk3/) (`install.sh` automatically installs)
- [python-gobject](https://archlinux.org/packages/extra/x86_64/python-gobject/) (`install.sh` automatically installs)
 
# Installation

1. `git clone https://github.com/WheatleyFromPortal2/fw-fanctrl-indicator.git`
2. `cd fw-fanctrl-indicator`
3. `./install.sh` (DO NOT RUN AS ROOT)

# Manual Installation (for distros other than Arch Linux)

1. `git clone https://github.com/WheatleyFromPortal2/fw-fanctrl-indicator.git`
2. `cd fw-fanctrl-indicator`
3. install `libappindicator-gtk3` and `python-gobject`
    - Use your distros' package manager or pip
4. Move `fw-fanctrl-indicator.py`, `fan-black.svg` and `fan-white.svg` to wherever your `fw-fanctrl` `config.json` is
    - `config.json` is often in `~/.config/fw-fanctrl`
5. Enable the systemd service
    - copy `fw-fanctrl-indicator.service` to `~/.config/systemd/user`
        - If you're not using systemd, you will need to write your own service file
    - run `systemctl --user enable fw-fanctrl-indicator.service` to enable the service
    - run `systemctl --user start fw-fanctrl-indicator.service` to start the service
    - run `loginctl enable-linger $USER` to make sure the service starts at boot
    - run `systemctl --user status fw-fanctrl-indicator.service` to check its status
