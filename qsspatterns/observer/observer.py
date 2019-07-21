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
        self.value = "ok"

    def onnotification(self, observed, event):
        print(str(event) + " " + self.value)


if __name__ == "__main__":
    from qsspatterns.observer import observable
    
    o1 = observable.observable()
    do1 = dummyobserver()
    o1.register(do1)
    o1.notifyobservers(1)