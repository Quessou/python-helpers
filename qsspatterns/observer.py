from abc import *
import logging
from qssinspect.stackutils import fnname

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
        if observer in self.observers:
            self.observers.remove(observer)
            return True
        else:
            logging.info(fnname() + 'Trying to unregister an unregistered observer')
            return False

    def notifyobservers(self, event):
        for obs in self.observers:
            obs.onnotification(self, event)


class observer(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def onnotification(self, observed, event):
        pass


class dummyobserver(observer):
    __slots__=["value"]
    def __init__(self):
        observer.__init__(self)
        self.value = "ok"

    def onnotification(self, observed, event):
        print(str(event) + " " + self.value)


def default_callback(_, observed, event):
    print(repr(observed) + " : " + repr(event))

class callbackobserver(observer):
    _DEFAULT_CALLBACK = default_callback

    def __init__(self):
        observer.__init__(self)
        self.notification_callback = self._DEFAULT_CALLBACK

    def onnotification(self, observed, event):
        self.notification_callback(observed, event)

if __name__ == "__main__":

    o1 = observable()
    do1 = dummyobserver()
    o1.register(do1)
    o1.notifyobservers(1)

    o1.unregister(do1)
    cbo = callbackobserver()
    o1.register(cbo)
    o1.notifyobservers(2)
