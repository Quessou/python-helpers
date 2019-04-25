#!/bin/python3

from changedir import cd
import os
import sys
import string
import errno, os

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123

def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Specific Windows processing
        # Removes the Drive letter, which will be stored into "_", and keeps the rest in "pathname".
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    else:
        return True

def isValidFilename(filename : str) -> bool:
    validchars = set(string.ascii_letters + string.digits + string.punctuation.replace("/",""))
    fn = set(filename)
    print(validchars)
    print(fn)
    return filename != "." and filename != "/" and fn.issubset(validchars)

def argumentsValid(arg1 : str, arg2 : str) -> bool:
    if (os.path.isdir(arg1) and isValidFilename(arg2) and is_pathname_valid(arg1 + arg2)):
        return True
    elif (os.path.isdir(arg2) and isValidFilename(arg1) and is_pathname_valid(arg2 + arg1)):
        return True
    return False


def writetestcmakelistsfile_gtest(cmakelistsfile, libname : str, testdirname : str) -> bool:
    try:
        print("coucou")
    except Exception as e:
        print("lol")

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
                testDirectoryName = "test"
                # Create library's root CMakeLists.txt file, and filling it
                with open("CMakeLists.txt",'w') as rootcmakelistsfile:
                    rootcmakelistsfile.write('add_subdirectory(' + libname + ')\n')
                    rootcmakelistsfile.write('add_subdirectory(' + testDirectoryName  + ')\n')
                os.mkdir(libname)
                os.mkdir(testDirectoryName)
                with cd(libname):
                    with open("CMakeLists.txt", 'w') as libcmakelistsfile:
                        libcmakelistsfile.write('add_library(' + libname + '\n)\n')
                with cd(testDirectoryName):
                    with open("CMakeLists.txt", 'w') as testcmakelistsfile:
                        writetestcmakelistsfile_gtest(testcmakelistsfile, libname, testDirectoryName)




    except PermissionError as pe:
        sys.exit("Permission denied")
    except FileNotFoundError as fnfe:
        sys.exit("Directory not found")
    except FileExistsError as fee:
        sys.exit("Directory with this library name already exists")
    

