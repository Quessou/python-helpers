from abc import *
import logging

from qssinspect.stackutils import fnname

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
    from qsspatterns.observer import observable
    
    o1 = observable.observable()
    do1 = dummyobserver()
    o1.register(do1)
    o1.notifyobservers(1)

    o1.unregister(do1)
    cbo = callbackobserver()
    o1.register(cbo)
    o1.notifyobservers(2)
