#!/bin/python3


from changedir import cd
import sys
import string
import errno, os
from pathchecks import is_pathname_valid, isValidFilename 
from cmakelistshelpers import *

def argumentsValid(arg1 : str, arg2 : str) -> bool:
    if (os.path.isdir(arg1) and isValidFilename(arg2) and is_pathname_valid(arg1 + arg2)):
        return True
    elif (os.path.isdir(arg2) and isValidFilename(arg1) and is_pathname_valid(arg2 + arg1)):
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("bad argument count : needs  two arguments")
    if not argumentsValid(sys.argv[1], sys.argv[2]) :
        sys.exit("invalid arguments : must give a valid path and a valid library name")
    if os.path.isdir(sys.argv[1]) :
        path = sys.argv[1]
        libname = sys.argv[2]
    else:
        path = sys.argv[2]
        libname = sys.argv[1]
    try:
        with cd(path): # Going into root src directory
            if not iscmakelistspresent():
                sys.exit("Project directory does not contain CMakeLists.txt")
            os.mkdir(libname) # Creating a directory for the library
            with cd(libname):
                srcdirname = "src"
                testdirname = "test"
                cml = "CMakeLists.txt"
                # Create library's root CMakeLists.txt file, and filling it
                with open(cml,'w') as rootcmakelistsfile:
                    writelibraryrootcmakelistsfile(rootcmakelistsfile, srcdirname, testdirname)    
                # Create source and test directories
                os.mkdir(srcdirname)
                os.mkdir(testdirname)
                with cd(srcdirname):
                    with open(cml, 'w') as libcmakelistsfile:
                       writesrcdircmakelistsfile(libcmakelistsfile, libname) 
                with cd(testdirname):
                    with open(cml, 'w') as testcmakelistsfile:
                        writetestcmakelistsfile_gtest(testcmakelistsfile, libname, testdirname)
                    defaulttestfilename = testdirname.lower() + libname.lower() + ".cpp"
                    with open(defaulttestfilename, 'w')  as testfile:
                        testfile.write("#include <gtest/gtest.h>\n")
                        testfile.write("// TODO : add includes to library's headers here\n\n")
                        testfile.write("// TODO : add tests here\n")
            # Reference new library into root CMakeLists.txt
            newrootcmlcontent = ""
            with open(cml,'r+') as projectcmakelistsfile:
                INC_DIR_STR = "include_directories"
                ADD_DIR_STR = "add_subdirectory"
                PROJ_SRC_DIR = "PROJECT_SOURCE_DIR"
                
                filecontent = projectcmakelistsfile.readlines()
                filecontent.reverse()
                rfilecontent = filecontent
                incdirfound = False
                adddirfound = False
                incdir = INC_DIR_STR + "(\"${" + PROJ_SRC_DIR + "}/" + libname + ")\n"
                addsubdir = ADD_DIR_STR + "(" + libname + ")\n"
                # add include_directories line
                for line in rfilecontent:
                    if INC_DIR_STR in line:
                        incdirfound = True
                        index = rfilecontent.index(line)
                        rfilecontent.insert(index, incdir)
                        break
                if not incdirfound:
                   rfilecontent.insert(0, incdir)

                # add add_subdirectory line
                for line in rfilecontent:
                    if ADD_DIR_STR in line:
                        adddirfound = True
                        index = rfilecontent.index(line)
                        rfilecontent.insert(index, addsubdir)
                        break
                if not adddirfound:
                   rfilecontent.insert(0, addsubdir)
                rfilecontent.reverse()
                filecontent = rfilecontent
                f = ""
                newrootcmlcontent = f.join(filecontent)
            open("cml","w").close()
            with open(cml, "w") as rootcmlfile:
                rootcmlfile.write(newrootcmlcontent)
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

