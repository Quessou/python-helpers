from abc import *

from pyfsutils.changedir import cd

class Project(metaclass = ABCmeta) :
    __slots__ = ["projectPath"]
    def __init__(self, path):
        self.projectPath = path
        with cd(self.projectPath):
           

    @abstractmethod
    def checkprojectvalidity(self):
        assert False

