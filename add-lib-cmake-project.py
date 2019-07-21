#!/usr/bin/python3


from qssfsutils.changedir import cd
import sys
import string
import errno, os
from qssfsutils.pathchecks import is_pathname_valid, isValidFilename 
from qsscmake.cmakelistshelpers import *

def argumentsValid(arg1 : str, arg2 : str) -> bool:
    if (os.path.isdir(arg1) and isValidFilename(arg2) and is_pathname_valid(arg1 + arg2)):
        return True
    elif (os.path.isdir(arg2) and isValidFilename(arg1) and is_pathname_valid(arg2 + arg1)):
        return True
    return False

def handleArguments(argv : list): #TODO(mmiko) : check if it's possible to specify a return type when we have multiple return values
    if len(argv) != 3: # TODO(mmiko) : handle here the case where the user does not give enough arguments, and maybe ask him to input them interactively
        sys.exit("bad argument count : needs  two arguments")
    if not argumentsValid(argv[1], argv[2]) :
        sys.exit("invalid arguments : must give a valid path and a valid library name")
    if os.path.isdir(argv[1]) :
        path = argv[1]
        libname = argv[2]
    else:
        path = argv[2]
        libname = argv[1]

    return path, libname

if __name__ == '__main__':
    # Arguments handling
    path, libname = handleArguments(sys.argv)
    try:
        with cd(path): # Going into root src directory
            if not iscmakelistspresent():
                sys.exit("Project directory does not contain CMakeLists.txt")
            os.mkdir(libname) # Creating a directory for the library
            with cd(libname):
                # Note : we use libname as dirname here, or else C++'s #includes are really ugly, referencing "src" everywhere.
                srcdirname = libname
                testdirname = "test"
                cml = "CMakeLists.txt"
                # Create library's root CMakeLists.txt file, and filling it
                writelibraryrootcmakelistsfile(srcdirname, testdirname)    
                # Create source and test directories
                os.mkdir(srcdirname)
                os.mkdir(testdirname)
                with cd(srcdirname):
                    writesrcdircmakelistsfile(libname) 
                with cd(testdirname):
                    # Generate CMakeLists.txt for a test project
                    writetestcmakelistsfile_gtest(libname, testdirname)
                    # Generate minimalistic source test file
                    defaulttestfilename = testdirname.lower() + libname.lower() + ".cpp"
                    with open(defaulttestfilename, 'w')  as testfile:
                        testfile.write("#include <gtest/gtest.h>\n")
                        testfile.write("// TODO : add includes to library's headers here\n\n")
                        testfile.write("// TODO : add tests here\n")
            # Reference new library into root CMakeLists.txt
            addlibtoproject(libname) 
    except PermissionError as pe:
        sys.exit("Permission denied")
    except FileNotFoundError as fnfe:
        sys.exit("Directory not found")
    except FileExistsError as fee:
        sys.exit("Directory with this library name already exists")
    except LookupError as lue:
        sys.exit("Index out of bounds exception")
    except Exception as e:
        sys.exit("Failed : " + e)
    print("Done")

