from abc import *
import logging
from qssinspect.stackutils import fnname

class Observable:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            fn = getattr(observer, 'on_notification', None)
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
            obs.on_notification(self, event)


class Observer(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def on_notification(self, observed, event):
        pass


class DummyObserver(Observer):
    __slots__=["value"]
    def __init__(self):
        Observer.__init__(self)
        self.value = "ok"

    def on_notification(self, observed, event):
        print(str(event) + " " + self.value)


def default_callback(_, observed, event):
    print(repr(observed) + " : " + repr(event))

class CallbackObserver(Observer):
    _DEFAULT_CALLBACK = default_callback

    def __init__(self):
        Observer.__init__(self)
        self.notification_callback = self._DEFAULT_CALLBACK

    def on_notification(self, observed, event):
        self.notification_callback(observed, event)

if __name__ == "__main__":

    o1 = Observable()
    do1 = DummyObserver()
    o1.register(do1)
    o1.notifyobservers(1)

    o1.unregister(do1)
    cbo = CallbackObserver()
    o1.register(cbo)
    o1.notifyobservers(2)
