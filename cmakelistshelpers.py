import os
import sys
import string


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
        cmakelistsfile.write("target_link_libraries(${" + EXC_NAME + "} gtest_main gtest pthread)\n")
        # Add test
        cmakelistsfile.write("add_test(\n")
        cmakelistsfile.write("\tNAME " + testexecutablename + "\n")
        cmakelistsfile.write("\tCOMMAND ${CMAKE_CURRENT_BINARY_DIR}/${"+EXC_NAME+"} --gtest_output=xml:${CMAKE_BINARY_DIR}/testResults/testResults_${"+EXC_NAME+"}.xml\n\t)\n")
    except Exception as e:
        print("Failed writing CMakeLists.txt for unit tests directory")
        raise e

def writelibraryrootcmakelistsfile(cmakelistsfile, srcdirname : str, testdirname : str):
    try:
        cmakelistsfile.write('add_subdirectory(' + srcdirname + ')\n')
        cmakelistsfile.write('add_subdirectory(' + testdirname  + ')\n')
    except Exception as e:
        print("Failed writing default CMakeLists.txt for library's root directory")
        raise e

def writesrcdircmakelistsfile(cmakelistsfile, libname: str):
    try:
        cmakelistsfile.write('add_library(' + libname + '\n)\n')
    except Exception as e:
        print("Failed writing default CMakeLists.txt for source code's directory")
        raise e


def iscmakelistspresent() -> bool:
    return os.path.isfile("CMakeLists.txt")
