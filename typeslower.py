#! /usr/bin/python
from __future__ import division

import time, datetime, pickle, signal
import pyxhook
from threading import Thread, Timer

TOO_FAST = [
    {'chars':10, 'sec':5}
]


class TypeSlowerMonitor(object):
    def __init__(self):
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

        #self.status_printer = StatusPrinter(self)
        #self.status_printer.start()

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
        


class StatusPrinter(Thread):
    def __init__(self, monitor):
        Thread.__init__(self)
        self.monitor = monitor

    def run(self):
        while True:
            now = datetime.datetime.now()
            now_time = time.time()
            result = "%s " % now
            for level in TOO_FAST:
                chars, sec = level['chars'], level['sec']
                num = len([x for x in self.monitor.keypresses if (now_time - x) <= sec])
                result += " %d of %d (%.1f) in %ds" % (num, chars, (num/chars), sec)

            #print result
            time.sleep(1 - (datetime.datetime.now().microsecond / 1000000))
    

def main():
    monitor = TypeSlowerMonitor()

if __name__ == '__main__':
    main()
