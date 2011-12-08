#! /usr/bin/python
# encoding: utf-8
from __future__ import division

import time, datetime, pickle, signal
import pyxhook
import pynotify
from threading import Thread, Timer, Event

import gobject, gtk, appindicator

TOO_FAST = [
    {'chars':10, 'sec':5},
    {'chars':5, 'sec':2.5},
    {'chars':2, 'sec':0.5},
    {'chars':200, 'sec': 60},
]

TOO_FAST.sort(key=lambda x:x['sec'])

gtk.gdk.threads_init()

class UpdateLabel(Thread):
    def __init__(self, indicator):
        Thread.__init__(self)
        self.indicator = indicator

    def run(self):
        while not self.indicator.finished.is_set():
            now = time.time()
            new_label_parts = []
            for period in TOO_FAST:
                num_this_period = len([x for x in self.indicator.keypresses if now - x < period['sec']])
                ratio = num_this_period / period['chars']
                new_label_parts.append("{0}s: ×{1:.1f}".format(period['sec'], ratio))

            self.indicator.ind.set_label(" ".join(new_label_parts))
            time.sleep(0.2)


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

        self.finished = Event()

        self.updater = UpdateLabel(self)
        self.updater.start()


    def keydown(self, event):
        now = time.time()
        self.keypresses.append(now)

    def set_label(self, text):
        print text
        #self.ind.set_label(text, text)

    def cancel(self):
        self.finished.set()
        self.hm.cancel()
        


if __name__ == "__main__":
    indicator = TypeSlowerIndicator()

    try:
        gtk.main()
    finally:
        indicator.cancel()

if __name__ == '__main__':
    main()
