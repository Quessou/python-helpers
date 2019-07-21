import os

def changedir(path):
    os.chdir(path)

class cd:
    __slots__=['__newDir','__savedDir']
    def __init__(self, newDir):
        if(os.path.isdir(newDir)) :
            self.__newDir = os.path.expanduser(newDir)
        else:
            print('invalid path')

    def __enter__(self):
        if(os.path.isdir(self.__newDir)):
            self.__savedDir = os.getcwd()
            changedir(self.__newDir)
        else:
            print('invalid path')

    def __exit__(self, etype, value, traceback):
        changedir(self.__savedDir)


# TODO(mmiko) : write tests here
