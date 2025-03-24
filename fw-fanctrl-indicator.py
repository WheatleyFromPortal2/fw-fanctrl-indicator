#!/usr/bin/python
# initial code copied from https://fosspost.org/custom-system-tray-icon-indicator-linux with import modified
# requires libappindicator-gtk3 to be installed (either through your package manager or pip)
import os, gi, json

red = '\033[91m'
normal = '\033[0m'

configPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}config.json" # use the location of this python file to find the config (because it should be installed there)
iconPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}fan-white.svg" # use the location of the this python file to find the icons (because they should be installed there)
defaultIcon = "computer-laptop-symbolic"

print("---Starting fw-fanctrl-indicator---")
print('configPath:', configPath)
print('iconPath:', iconPath)

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, GLib

def main():
    global indicator, strategyList, currentStrategy
    indicator = appindicator.Indicator.new("customtray", "computer-laptop-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
    strategyList, currentStrategy = buildStrategyList()
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    if os.path.exists(iconPath): # check if the icon exists
        indicator.set_icon_full(iconPath, 'Custom Icon') # set the icon
    else:
        print(red + "Icon File not Found!" + normal + " - Reverting to default:", defaultIcon)  # warn the user icon is not found, instead it will default to "computer-laptop-symbolic"
    indicator.set_menu(menu())
    gtk.main()

def menu():
    global statsItem
    menu = gtk.Menu()

    temp, RPM = getStats()
    if RPM is None: # workaround because "or" sees 0 as None
        RPM = "--"
    statsItem = gtk.MenuItem(label=f"CPU: {temp or "--"}°C | Fan: {RPM}rpm")
    menu.append(statsItem)
    statsItem.show()
    menu.append(gtk.SeparatorMenuItem()) # create a menu separator after to separate the stats
    updateStats()
    for i in strategyList: # read the strategyList created by buildStrategyList
        if i == currentStrategy: # this is to distinguish the current strategy
            emoji = gtk.Image.new_from_icon_name("checkmark-symbolic", gtk.IconSize.MENU)
            command = gtk.ImageMenuItem(label=i) # add brackets to the current strategy to distingish
            command.set_image(emoji)
            command.set_always_show_image(True)
            command.connect('activate', lambda _, s=i: strategyClick(s)) # use a lambda function to pass the current strategy into the function call
            menu.append(command) # add the command to the menu
        else: # strategy is not the current strategy
            command = gtk.MenuItem(label=i) # create the menu item
            command.connect('activate', lambda _, s=i: strategyClick(s)) # use a lambda function to pass the current strategy into the function call
            menu.append(command) # append the menu item to the menu

    exittray = gtk.MenuItem(label='Exit Tray') # create the exit tray command
    exittray.connect('activate', quit) # connect it to our quit() function
    menu.append(exittray) # add it to the menu
  
    menu.show_all() # show everything
    return menu # return the menu for GTK to read

def updateMenu():
    print('updating menu')
    indicator.set_menu(menu())
    gtk.main()

def buildStrategyList(): # make a list with all the strategies from the config file
    strategyList = [] # make sure these variables can be used throughout the function
    config = '' # make sure these variables can be used throughout the function

    try:
        with open(configPath, 'r') as configFile:
            config = json.load(configFile)
    except FileNotFoundError as err:
            print(red + 'Config File not Found! err:' + normal, err)
            exit()
    for i in config['strategies']:
        strategyList.append(i) # add each strategy from the config file to strategyList
    global currentStrategy
    currentStrategy = config['defaultStrategy'] # guess that the current strategy is the default, since we can't read from fw-fanctrl, just change the strategy
    return strategyList, currentStrategy
    
def strategyClick(strategy):
    print(f'fw-fanctrl {strategy}')
    os.system(f'fw-fanctrl {strategy}') # run fw-fanctrl with the strategy as the argument
    global currentStrategy
    currentStrategy = strategy
    updateMenu()

def updateStats():
    temp, RPM = getStats()
    if RPM is None: # workaround because "or" sees 0 as None
        RPM = "--"
    statsItem.set_label(f"CPU: {temp or "--"}°C | Fan: {RPM}rpm")
    GLib.timeout_add(1000, updateStats)
    

def getStats(): # return CPU Temp and RPM of system fan
    sensorsJSON = os.popen("sensors -j").read() # run the command "sensors -j" and store the result in sensorsJSON
    try:
        sensors = json.loads(sensorsJSON) # try to parse the result into JSON 
    except json.decoder.JSONDecodeError as err:
        print(red + "loading 'sensors -j' as JSON failed; err:" + normal, err)
        return None, None
    try:
        temp = int(sensors["cros_ec-isa-0000"]["F75303_CPU"]["temp2_input"])
    except KeyError as err:
        print(red + "getting temp failed; err:" + normal, err)
        temp = None
    try:
        RPM = int(sensors["cros_ec-isa-0000"]["fan1"]["fan1_input"])
    except KeyError as err:
        print(red + "getting RPM failed; err:" + normal, err)
        RPM = None

    return temp, RPM

def quit(_):
    gtk.main_quit()


if __name__ == "__main__":
  main()
