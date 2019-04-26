#!/bin/python3


from changedir import cd
import sys
import string
import errno, os
from pathchecks import is_pathname_valid, isValidFilename 

def argumentsValid(arg1 : str, arg2 : str) -> bool:
    if (os.path.isdir(arg1) and isValidFilename(arg2) and is_pathname_valid(arg1 + arg2)):
        return True
    elif (os.path.isdir(arg2) and isValidFilename(arg1) and is_pathname_valid(arg2 + arg1)):
        return True
    return False


def writetestcmakelistsfile_gtest(cmakelistsfile, libname : str, testdirname : str):
    try:
        EXC_NAME = "EXECUTABLE_NAME"
        testexecutablename = testdirname + libname.capitalize()
        # Set variable EXECUTABLE_NAME
        cmakelistsfile.write("set(" + EXC_NAME + ' ' + testexecutablename + ')\n\n') 
        # Declare executable
        cmakelistsfile.write("add_executable(${" + EXC_NAME + "} " + testexecutablename.lower() + ".cpp)\n\n"  )
        # Add dependencies
        cmakelistsfile.write("target_link_libraries(${" + EXC_NAME + "} " + libname +")\n")
        cmakelistsfile.write("target_link_libraries(${" + EXC_NAME + "}  gtest_main gtest pthread)\n")
        # Add test
        cmakelistsfile.write("add_test(\n")
        cmakelistsfile.write("\tNAME " + testexecutablename + "\n")
        cmakelistsfile.write("\tCOMMAND ${CMAKE_CURRENT_BINARY_DIR}/${"+EXC_NAME+"} --gtest_output=xml:${CMAKE_BINARY_DIR}/testResults/testResults_${"+EXC_NAME+"}.xml\n\t)\n")
    except Exception as e:
        print("lol")

def writelibraryrootcmakelistsfile(cmakelistsfile, srcdirname : str, testdirname : str):
    try:
        rootcmakelistsfile.write('add_subdirectory(' + srcdirname + ')\n')
        rootcmakelistsfile.write('add_subdirectory(' + testdirname  + ')\n')
    except Exception as e:
        sys.exit("Failed writing default CMakeLists.txt for library's root directory")

def writesrcdircmakelistsfile(cmakelistsfile, libname: str):
    try:
        libcmakelistsfile.write('add_library(' + libname + '\n)\n')
    except Exception as e:
        sys.exit("Failed writing default CMakeLists.txt for source code's directory")

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
    print("args ok")
    try:
        with cd(path): # Going into root src directory
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




    except PermissionError as pe:
        sys.exit("Permission denied")
    except FileNotFoundError as fnfe:
        sys.exit("Directory not found")
    except FileExistsError as fee:
        sys.exit("Directory with this library name already exists")
    

