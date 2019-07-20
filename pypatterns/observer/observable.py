from abc import *

import logging

from pyinspect.stackutils import fnname

class observable:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            fn = getattr(observer, 'onnotification', None)
            if not fn:
                logging.warning(fnname() + "register an observer which does not have onnotification method : " + observer.repr)
                return False
            self.observers.append(observer)
            return True
        else:
            logging.info(fnname() + 'Trying to add an observer already registered')

    def unregister(self, observer):
        if self.observers.contains(observer):
            self.observers.remove(observer)
            return True
        else:
            logging.info(fnname() + 'Trying to unregister an unregistered observer')
            return False

    def notifyobservers(self, event):
        for obs in self.observers:
            obs.onnotification(self, event) 
