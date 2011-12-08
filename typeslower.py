#! /usr/bin/python
from __future__ import division

import time, datetime, pickle, signal
import pyxhook
import pynotify
from threading import Thread, Timer

import gobject, gtk, appindicator

TOO_FAST = [
    {'chars':10, 'sec':5},
    #{'chars':200, 'sec':60},
]

gtk.gdk.threads_init()


class TypeSlowerIndicator(object):
    def __init__(self):
        self.keypresses = []

        self.hm = pyxhook.HookManager()
        self.hm.HookKeyboard()
        self.hm.HookMouse()
        self.hm.KeyDown = self.keydown

        self.hm.start()

        ind = appindicator.Indicator ("indicator-sysmonitor",
          "sysmonitor",
            appindicator.CATEGORY_SYSTEM_SERVICES)

        ind.set_status(appindicator.STATUS_ACTIVE)
        ind.set_attention_icon("indicator-messages-new")
        ind.set_label("init")

        menu_item = gtk.MenuItem("test")
        menu = gtk.Menu()
        menu.append(menu_item)
        menu_item.show()
        ind.set_menu(menu)

        self.ind = ind


    def keydown(self, event):
        print "Keydown"
        now = time.time()
        self.keypresses.append(now)

    def set_label(self, text):
        print text
        #self.ind.set_label(text, text)
        


if __name__ == "__main__":
    indicator = TypeSlowerIndicator()

    gtk.main()

if __name__ == '__main__':
    main()
