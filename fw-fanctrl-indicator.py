#!/usr/bin/python
# requires libappindicator-gtk3 to be installed (either through your package manager or pip)

import os
import gi
import json

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import AppIndicator3 as appindicator

# colored text printing
red = '\033[91m'
normal = '\033[0m'

# use the location of this python file to find the config
configPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}config.json"
# use the location of the this python file to find the icons
iconPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}fan-white.svg"
defaultIcon = "computer-laptop-symbolic"

tempIcons = {
    '80': "temperature-cold-symbolic",
    '90': "temperature-normal-symbolic",
    "100": "temperature-warm-symbolic"
}

DEFAULT_ICON = "computer-laptop-symbolic"
UPDATE_TIME = 5  # update every 5 seconds

# initialize global variables
temp = 0
speed = 0  # speed in percent
strategy = ""
strategyList = []

print("---Starting fw-fanctrl-indicator---")
print('configPath:', configPath)
print('iconPath:', iconPath)


def main():
    global indicator, strategyList
    indicator = appindicator.Indicator.new("customtray",
                                           DEFAULT_ICON,
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_title("fw-fanctrl")
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    if os.path.exists(iconPath):  # check if the icon exists
        # set the icon
        indicator.set_icon_full(iconPath, 'Custom Icon')
    else:
        # warn the user icon is not found and default to DEFAULT_ICON
        print(red + "Icon File not Found!"
              + normal
              + " - Reverting to default:", defaultIcon)
    indicator.set_menu(menu())
    glib.timeout_add_seconds(UPDATE_TIME, updateMenu)
    gtk.main()


def menu():
    global statsItem, speed, temp, strategy
    menu = gtk.Menu()

    # workaround because "or" sees 0 as None
    if speed is None:
        speed = "--"

    statsItem = gtk.ImageMenuItem(
        label=f"CPU: {temp or "--"}°C | Fan: {speed}%")
    statsIcon = getTempIcon(temp, True)
    statsItem.set_image(statsIcon)
    statsItem.set_always_show_image(True)
    menu.append(statsItem)
    statsItem.show()

    # create a menu separator after to separate the stats
    menu.append(gtk.SeparatorMenuItem())

    updateState()
    updateStats()

    # read the strategyList created by buildStrategyList
    for i in strategyList:
        # add a checkmark to current strategy
        if i == strategy:
            emoji = gtk.Image.new_from_icon_name(
                "checkmark-symbolic", gtk.IconSize.MENU)
            command = gtk.ImageMenuItem(label=i)
            command.set_image(emoji)
            command.set_always_show_image(True)
            # use a lambda to pass the current strategy into the function call
            command.connect('activate', lambda _, s=i: strategyClick(s))
            menu.append(command)  # add the command to the menu
        else:  # if the strategy is not the current strategy
            command = gtk.MenuItem(label=i)  # create the menu item
            # use a lambda to pass the current strategy into the function call
            command.connect('activate', lambda _, s=i: strategyClick(s))
            menu.append(command)  # append the menu item to the menu

    exittray = gtk.ImageMenuItem(label='exit tray')  # create the exit tray
    exitImg = gtk.Image.new_from_icon_name("application-exit",
                                           gtk.IconSize.MENU)
    exittray.set_image(exitImg)
    exittray.connect('activate', quit)  # connect it to our quit() function

    # create a menu separator after to separate exit button
    menu.append(gtk.SeparatorMenuItem())

    menu.append(exittray)  # add it to the menu

    menu.show_all()  # show everything
    return menu  # return the menu for GTK to read


def updateMenu():
    indicator.set_menu(menu())
    return True


def strategyClick(clickedStrategy):
    # run fw-fanctrl with the strategy as the argument
    os.system(f'fw-fanctrl use {clickedStrategy}')
    updateMenu()


def getTempIcon(temp, returnImage):
    for i in tempIcons:
        if temp <= int(i):
            if returnImage:
                return gtk.Image.new_from_icon_name(tempIcons[i],
                                                    gtk.IconSize.MENU)
            else:
                return tempIcons[i]
    if returnImage:
        # if the temp is hotter, use a warning symbol
        return gtk.Image.new_from_icon_name("dialog-warning-symbolic",
                                            gtk.IconSize.MENU)
    else:
        return "dialog-warning-symbolic"


def updateStats():
    global speed, temp

    # workaround because "or" sees 0 as None
    if speed is None:
        speed = "--"

    # update the stats bar
    statsItem.set_label(f"CPU: {temp or "--"}°C | Fan: {speed}%")
    # update the tooltip
    indicator.set_title(f"{temp or "--"}°C {speed}%")
    statsIcon = getTempIcon(temp, True)  # get the stats icon
    statsItem.set_image(statsIcon)  # update the image
    # set the icon
    indicator.set_icon_full(getTempIcon(temp, False), 'Custom Icon')

    return True


def updateState():  # update our state from `fw-fanctrl`
    # get fw-fanctrl status in JSON
    statusJSON = os.popen("fw-fanctrl --output-format JSON print").read()

    try:
        state = json.loads(statusJSON)
    except json.decoder.JSONDecodeError:
        print("ERROR: `fw-fanctrl` is not outputting JSON")
        exit(1)

    global temp, speed, strategy, strategyList

    temp = state["movingAverageTemperature"]
    speed = state["speed"]
    strategy = state["strategy"]

    strategyList = []  # start off strategy list as empty

    for i in state["configuration"]["data"]["strategies"]:
        # add each strategy from the config file to strategyList
        strategyList.append(i)


def quit(_):
    gtk.main_quit()
    exit()


if __name__ == "__main__":
    main()
