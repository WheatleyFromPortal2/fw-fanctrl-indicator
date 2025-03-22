#!/usr/bin/python
# initial code copied from https://fosspost.org/custom-system-tray-icon-indicator-linux with import modified
# requires libappindicator-gtk3 to be installed (either through your package manager or pip)
import os, gi, json

configPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}config.json" # use the location of this python file to find the config (because it should be installed there)
iconPath = f"{__file__.replace("fw-fanctrl-indicator.py", '')}fan-white.svg" # use the location of the this python file to find the icons (because they should be installed there)

print("---Starting fw-fanctrl-indicator---")
print('configPath:', configPath)
print('iconPath:', iconPath)

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

def main():
    global indicator, strategyList, currentStrategy
    indicator = appindicator.Indicator.new("customtray", "computer-laptop-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
    strategyList, currentStrategy = buildStrategyList()
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    if os.path.exists(iconPath): # check if the icon exists
        indicator.set_icon_full(iconPath, 'Custom Icon') # set the icon
    else:
        print('\033[91m' + "Icon File not Found!" + '\033[0m' + " - Reverting to default computer-laptop-symbolic")  # warn the user icon is not found, instead it will default to "computer-laptop-symbolic"
    indicator.set_menu(menu())
    gtk.main()

def menu():
    menu = gtk.Menu()
    for i in strategyList: # read the strategyList created by buildStrategyList
        if i == currentStrategy: # this is to distinguish the current strategy
            menu.append(gtk.SeparatorMenuItem()) # create a menu separator before to distinguish the current strategy
            command = gtk.MenuItem(label='[' + i + ']') # add brackets to the current strategy to distingish
            command.connect('activate', lambda _, s=i: strategyClick(s)) # use a lambda function to pass the current strategy into the function call
            menu.append(command) # add the command to the menu
            menu.append(gtk.SeparatorMenuItem()) # create a menu separator after to distinguish the current strategy
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
    except FileNotFoundError:
            print('\033[91m' + 'Config File not Found!' + '\033[0m')
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

def quit(_):
    gtk.main_quit()


if __name__ == "__main__":
  main()
