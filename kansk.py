#! /usr/bin/python3
# -*- coding: utf-8 -*-
import signal
import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from gi.repository import GLib

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


class IndicatorKansk:


    def __init__(self):
        APPINDICATOR_ID = 'kanskappindicator'
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.testbar(self), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.update_bar()
        GLib.timeout_add_seconds(300,self.handler_timeout)
        

    def get_bar(self):
        try:
            url_bar = 'http://kansk24.org/temp/term.txt'
            content = urllib2.urlopen(url_bar).read()
            content = content.decode("utf-8")
            temp = content.split(";")[0]
            timen = time.strftime("%H:%M:%S")
            o = timen + " " + temp
            print(o)
            return temp
        except:
            return "None"

    
    def update_bar(self):  
        temp = self.get_bar()
        self.indicator.set_label(temp, "")
       
        
        
        
    def handler_timeout(self):
        """This will be called every few seconds by the GLib.timeout.
        """
        # read, parse and put bar in the label
        self.update_bar()
        # return True so that we get called again
        # returning False will make the timeout stop
        
        return True


    
    def testbar(self,content):
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
        
    
    
    
    def build_menu(self):
        menu = gtk.Menu()
        item_bar = gtk.MenuItem('Давление')
        item_bar.connect('activate', self.bar)
        menu.append(item_bar)
        item_quit = gtk.MenuItem('Выход')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        item_about = gtk.MenuItem('Об авторе')
        item_about.connect('activate', self.onabout)
        menu.append(item_about)
        menu.show_all()
        return menu

    
    def bar(self,evt):
        notify.init(APPINDICATOR_ID)
        notify.Notification.new(self.fetch_bar(), None).show()
     
    def quit(self, evt):
        notify.uninit()
        gtk.main_quit()

    def onabout(self, evt):
        print('About clicking')
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
        
    def main(self):
        gtk.main()  
                  
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = IndicatorKansk()
    indicator.main()
