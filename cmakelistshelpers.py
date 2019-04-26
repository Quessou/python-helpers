import os
import sys
import string


CML = "CMakeLists.txt"

# TODO(mmiko) : add versions of these methods that do not take a FILE into parameter
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

def writeaddsubdir(libname: str):
    if not iscmakelistspresent():
        print("No CMakeLists.txt in current directory")
        return;
    newrootcmlcontent = ""
    with open(CML,'r+') as projectcmakelistsfile:
        ADD_DIR_STR = "add_subdirectory"

        filecontent = projectcmakelistsfile.readlines()
        filecontent.reverse()
        rfilecontent = filecontent
        adddirfound = False
        addsubdir = ADD_DIR_STR + "(" + libname + ")\n"

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
        open(CML,"w").close()
        with open(CML, "w") as rootcmlfile:
            rootcmlfile.write(newrootcmlcontent)

def writeincludedirectory(libname: str):
    if not iscmakelistspresent():
        print("No CMakeLists.txt in current directory")
        return;
    newrootcmlcontent = ""
    with open(CML,'r+') as projectcmakelistsfile:
        INC_DIR_STR = "include_directories"
        PROJ_SRC_DIR = "PROJECT_SOURCE_DIR"

        filecontent = projectcmakelistsfile.readlines()
        filecontent.reverse()
        rfilecontent = filecontent
        incdirfound = False
        incdir = INC_DIR_STR + "(\"${" + PROJ_SRC_DIR + "}/" + libname + ")\n"
        # add include_directories line
        for line in rfilecontent:
            if INC_DIR_STR in line:
                incdirfound = True
                index = rfilecontent.index(line)
                rfilecontent.insert(index, incdir)
                break
        if not incdirfound:
            rfilecontent.insert(0, incdir)

        rfilecontent.reverse()
        filecontent = rfilecontent
        f = ""
        newrootcmlcontent = f.join(filecontent)
        open(CML,"w").close()
        with open(CML, "w") as rootcmlfile:
            rootcmlfile.write(newrootcmlcontent)
    


def addlibtoproject(libname : str):
    if not iscmakelistspresent():
        print("No CMakeLists.txt in current directory")
        return;
    writeincludedirectory(libname)
    writeaddsubdir(libname)
