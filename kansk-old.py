#! /usr/bin/python
# -*- coding: utf-8 -*-
import signal
import urllib2
import glib

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'kanskappindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, testbar(), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    glib.timeout_add_seconds(10, update_bar())
    
    notify.init(APPINDICATOR_ID)
    gtk.main()
        def update_bar():
         temp = fetch_bar().split(";")[0]
         indicator.set_label(temp,"")
         print ('1')


    
def testbar():
    try:
        url_bar = 'http://kansk24.org/temp/rs.txt'
        content = urllib2.urlopen(url_bar).read()
        bars = content.split()
        if float(bars[47]) < float(bars[24]):
            return "go-down"
        else:
            return "go-up"
        
    except:
            return "edit-delete"   
        
    
    
    
def build_menu():
    menu = gtk.Menu()
    item_bar = gtk.MenuItem('Давление')
    item_bar.connect('activate', bar)
    menu.append(item_bar)
    item_quit = gtk.MenuItem('Выход')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    item_about = gtk.MenuItem('Об авторе')
    item_about.connect('activate', onabout)
    menu.append(item_about)
    menu.show_all()
    return menu

def fetch_bar():
    try:
        url_bar = 'http://kansk24.org/temp/term.txt'
        content = urllib2.urlopen(url_bar).read()
        return content
    except:
        return 'None'
    
def bar(_):
    notify.Notification.new(fetch_bar(), None).show()
     
def quit(source):
    notify.uninit()
    gtk.main_quit()

def onabout(source):
        ad=gtk.AboutDialog()
        ad.set_name("Об авторе")
        ad.set_version("0.1")
        ad.set_copyright('Copyrignt (c) 2015 dedo')
        ad.set_comments('Bar in KANSK')
        ad.set_license(''+
        'This program is free software: you can redistribute it and/or modify it\n'+
        'under the terms of the GNU General Public License as published by the\n'+
        'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
        'any later version.\n\n'+
        'This program is distributed in the hope that it will be useful, but\n'+
        'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
        'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
        'more details.\n\n'+
        'You should have received a copy of the GNU General Public License along with\n'+
        'this program.  If not, see <http://www.gnu.org/licenses/>.')
        ad.set_website('http://dedo24.ru')
        ad.set_website_label('dedomorozoff')
        ad.set_authors(['dedomorozoff <dedomorozoff@gmail.com'])
        ad.run()
        ad.destroy()
                
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
