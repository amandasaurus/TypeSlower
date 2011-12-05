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


class TypeSlowerMonitor(object):
    def __init__(self, indicator):
        self.indicator = indicator

        hm = pyxhook.HookManager()
        hm.HookKeyboard()
        hm.HookMouse()
        hm.KeyDown = self.keydown
        #hm.KeyUp = self.hook_manager_event #hm.printevent
        #hm.MouseAllButtonsDown = hm.printevent
        #hm.MouseAllButtonsUp = hm.printevent
        hm.start()
        self.hm = hm

        self.keypresses = []

        self.status_printer = StatusChecker(self, indicator)
        self.status_printer.start()

        self.dump()
        hm.join()


    def keydown(self, event):
        now = time.time()
        self.keypresses.append(now)

    def status(self):
        now = time.time()
        return str(len([x for x in self.keypresses if (now - x) <= 2]))

    def dump(self, delay=5):
        with open("/tmp/keypresses.pickle", "w") as fp:
            pickle.dump(self.keypresses, fp)

        Timer(delay, self.dump, args=[delay]).start()
        


class StatusChecker(Thread):
    def __init__(self, monitor, indicator):
        Thread.__init__(self)
        self.monitor = monitor
        self.indicator = indicator

    def run(self):
        while True:
            now = datetime.datetime.now()
            now_time = time.time()
            overs = None
            fmt = " {: 2d} of {: 2d} ({: 1.1f})"
            #fmt = " {: 2d} of {: 2d} ({: 1.1f})"
            guide = fmt.format(0, 0, 0, 0) * len(TOO_FAST)
            result = ""
            for level in TOO_FAST:
                chars, sec = level['chars'], level['sec']
                num = len([x for x in self.monitor.keypresses if (now_time - x) <= sec])
                result += fmt.format(num, chars, (num/chars), sec)

            self.indicator.set_label(result)
            time.sleep(0.5)
    

#def main():
#    monitor = TypeSlowerMonitor()
#

class TypeSlowerIndicator(object):
    def d__init__(self):

        ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)

        #ind = appindicator.Indicator ("indicator-sysmonitor",
        #  "sysmonitor",
        #    appindicator.CATEGORY_SYSTEM_SERVICES)
        ind.set_status(appindicator.STATUS_ACTIVE)
        ind.set_attention_icon("indicator-messages-new")
        #ind.set_label("init")

        menu_item = gtk.MenuItem("test")
        menu = gtk.Menu()
        menu.append(menu_item)
        menu_item.show()
        ind.set_menu(menu)

        self.ind = ind

    def __init__(self):
        ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        ind.set_status (appindicator.STATUS_ACTIVE)
        ind.set_attention_icon ("indicator-messages-new")

        # create a menu
        menu = gtk.Menu()

        # create some labels
        for i in range(3):
            buf = "Test-undermenu - %d" % i

            menu_items = gtk.MenuItem(buf)

            menu.append(menu_items)

            # this is where you would connect your menu item up with a function:

            # menu_items.connect("activate", self.menuitem_response, buf)

            # show the items
            menu_items.show()

        ind.set_menu(menu)
        self.ind = ind

    def set_label(self, text):
        print text
        #self.ind.set_label(text, text)
        


if __name__ == "__main__":
    indicator = TypeSlowerIndicator()
    # commenting this out makes the indicator not work.
    # look at how indicator-sysmonitor does it
    monitor = TypeSlowerMonitor(indicator)

    gtk.main()

if __name__ == '__main__':
    main()
