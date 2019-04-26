import os
import sys
import string


CML = "CMakeLists.txt"

def __writetestcmakelistsfile_gtest__(cmakelistsfile, libname : str, testdirname : str):
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

def __writelibraryrootcmakelistsfile__(cmakelistsfile, srcdirname : str, testdirname : str):
    try:
        cmakelistsfile.write('add_subdirectory(' + srcdirname + ')\n')
        cmakelistsfile.write('add_subdirectory(' + testdirname  + ')\n')
    except Exception as e:
        print("Failed writing default CMakeLists.txt for library's root directory")
        raise e

def __writesrcdircmakelistsfile__(cmakelistsfile, libname: str):
    try:
        cmakelistsfile.write('add_library(' + libname + '\n)\n')
    except Exception as e:
        print("Failed writing default CMakeLists.txt for source code's directory")
        raise e


def iscmakelistspresent() -> bool:
    return os.path.isfile("CMakeLists.txt")


def writetestcmakelistsfile_gtest(libname : str, testdirname : str):
    with open(CML, "w") as cmakelists:
        __writetestcmakelistsfile_gtest__(cmakelists, libname, testdirname)

def writelibraryrootcmakelistsfile(srcdirname : str, testdirname : str):
    with open(CML, "w") as cmakelists:
        __writelibraryrootcmakelistsfile__(cmakelists, srcdirname, testdirname)

def writesrcdircmakelistsfile(libname: str):
    with open(CML, "w") as cmakelists:
        __writesrcdircmakelistsfile__(cmakelists, libname)

# TODO(mmiko) : How to handle potential multi-line directives ?
def addsinglelinedirective(directivename : str, directive : str):
    if not iscmakelistspresent():
        print("No CMakeLists.txt in current directory")
        return;
    newrootcmlcontent = ""
    with open(CML,'r+') as projectcmakelistsfile:
        filecontent = projectcmakelistsfile.readlines()
        filecontent.reverse()
        rfilecontent = filecontent
        directivefound = False

        # add dirirective line, either after the last one of the same type if existing, or at the very end of file otherwise
        for line in rfilecontent:
            if directivename in line:
                adddirfound = True
                index = rfilecontent.index(line)
                rfilecontent.insert(index, directive)
                break
        if not adddirfound:
            rfilecontent.insert(0, directive)

        rfilecontent.reverse()
        filecontent = rfilecontent
        f = ""
        newrootcmlcontent = f.join(filecontent)
        open(CML,"w").close()
        with open(CML, "w") as rootcmlfile:
            rootcmlfile.write(newrootcmlcontent)


def writeaddsubdir(libname: str):
    ADD_DIR_STR = "add_subdirectory"
    addsubdir = ADD_DIR_STR + "(" + libname + ")\n"
    addsinglelinedirective(ADD_DIR_STR, addsubdir)

def writeincludedirectory(libname: str):
    INC_DIR_STR = "include_directories"
    PROJ_SRC_DIR = "PROJECT_SOURCE_DIR"
    incdir = INC_DIR_STR + "(\"${" + PROJ_SRC_DIR + "}/" + libname + ")\n"
    addsinglelinedirective(INC_DIR_STR, incdir)


def addlibtoproject(libname : str):
    if not iscmakelistspresent():
        print("No CMakeLists.txt in current directory")
        return;
    writeincludedirectory(libname)
    writeaddsubdir(libname)
