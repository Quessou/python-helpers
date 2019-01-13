#!/bin/python3

from changedir import cd
import os

def ls(path):
    if(os.path.isdir(path)):
        with cd(path):
            print("  ".join(os.listdir('.')))
    else:
        print('Given path is not a directory')
    
