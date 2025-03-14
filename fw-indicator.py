#!/usr/bin/python
# copied from https://fosspost.org/custom-system-tray-icon-indicator-linux with import modified
# requires libappindicator-gtk3 to be installed (either through your package manager or pip)
import os, gi, json

home = os.getenv('HOME')
configPath = f'{home}/.config/fw-fanctrl/config.json'
iconPath = f'{home}/code/fw-fanctrl-indicator/fan-white.svg'

print('---Starting fw-fanctrl-indicator---')
print('configPath:', configPath)
print('iconPath:', iconPath)

gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

def main():
    global indicator, strategyList, currentStrategy
    indicator = appindicator.Indicator.new("customtray", "computer-laptop-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
    strategyList, currentStrategy = buildStrategyList()
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    if os.path.exists(iconPath):
        indicator.set_icon_full(iconPath, 'Custom Icon')
    else:
        print('\033[91m' + 'Icon File not Found!' + '\033[0m' + " - Reverting to default computer-laptop-symbolic") 
        print("")
    indicator.set_menu(menu())
    gtk.main()

def menu():
    menu = gtk.Menu()
    for i in strategyList:
        displayStrategy = ''
        if i == currentStrategy: # this is to distinguish the current strategy
            menu.append(gtk.SeparatorMenuItem())
            command = gtk.MenuItem(label='[' + i + ']') 
            command.connect("activate", lambda _, s=i: strategyClick(s)) # use a lambda function to pass the current strategy into the function call
            menu.append(command)
            menu.append(gtk.SeparatorMenuItem())
        else:
            command = gtk.MenuItem(label=i)
            command.connect("activate", lambda _, s=i: strategyClick(s)) # use a lambda function to pass the current strategy into the function call
            menu.append(command)
    exittray = gtk.MenuItem(label='Exit Tray')
    exittray.connect('activate', quit)
    menu.append(exittray)
  
    menu.show_all()
    return menu

def updateMenu():
    print('updating menu')
    indicator.set_menu(menu())
    gtk.main()

def buildStrategyList(): # make "strategyList", a list with all the strategies from the config file
    strategyList = []
    
    config = ''
    try:
        with open(configPath, 'r') as configFile:
            config = json.load(configFile)
    except FileNotFoundError:
            print('\033[91m' + 'Config File not Found!' + '\033[0m')
            exit()
    for i in config['strategies']:
        strategyList.append(i)
    global currentStrategy
    currentStrategy = config['defaultStrategy']
    return strategyList, currentStrategy
    
def strategyClick(strategy):
    
    print(f'fw-fanctrl {strategy}')
    os.system(f'fw-fanctrl {strategy}')
    global currentStrategy
    currentStrategy = strategy
    updateMenu()

def quit(_):
    gtk.main_quit()


if __name__ == "__main__":
  main()
