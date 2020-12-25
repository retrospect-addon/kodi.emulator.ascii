# SPDX-License-Identifier: GPL-3.0

import io
import os
from shutil import copyfile

from sakee import addoninfo
from sakee.colors import Colors
from sakee.stub import KodiStub


class File(object):  # NOSONAR
    def __init__(self, path, flags='r'):
        """ File class.

        :param str path:    The file or directory to open
        :param str flags:   The flags used to open the file
        """
        if flags not in ['r', 'w']:
            raise ValueError("flags should be 'r' or 'w'")

        self._file = io.open(path, flags + 'b')

    def close(self):
        """ Close the file. """
        self._file.close()

    # noinspection PyShadowingBuiltins
    def read(self, bytes=-1):
        """ Read from the file.

        :param int bytes:       How many bytes to read

        :return: The read bytes
        :rtype: str
        """
        # noinspection PyUnresolvedReferences
        return self._file.read(bytes).decode('utf-8')

    # noinspection PyPep8Naming
    def readBytes(self, numbytes=-1):  # NOSONAR
        """ Read from the file.

        :param int numbytes:    How many bytes to read

        :return: The read bytes
        :rtype: bytes
        """
        return self._file.read(numbytes)

    # noinspection PyPep8Naming
    def seek(self, seekBytes, iWhence=0):  # NOSONAR
        """ Seek to position in file.

        :param int seekBytes:   Position in the file
        :param int iWhence:     Where in a file to seek from (0=beginning, 1=current, 2=end position)

        :return: The current position in the file
        :rtype: int
        """
        return self._file.seek(seekBytes, iWhence)

    def size(self):
        """ Get the file size.

        :return: The file size
        :rtype: int
        """
        self._file.flush()
        return os.fstat(self._file.fileno()).st_size

    def tell(self):
        """ Get the current position in the file.

        :return: The current position in the file
        :rtype: int
        """
        return self._file.tell()

    def write(self, buffer):
        """ Write to the file.

        :param str|byte buffer:      Data to write to the file

        :return: True if successful
        :rtype bool
        """
        if isinstance(buffer, bytes):
            # noinspection PyTypeChecker
            bytes_written = self._file.write(buffer)
        else:
            # noinspection PyTypeChecker
            bytes_written = self._file.write(buffer.encode())
        return bytes_written == len(buffer)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Stat(object):  # NOSONAR
    def __init__(self, path):
        """ Stat class.

        :param str path:        The file or directory to stat
        """
        self._stat = os.stat(path)

    def st_atime(self):
        """ Returns the st_atime attribute.

        :rtype: float
        :return: The st_atime attribute
        """
        return self._stat.st_atime

    def st_ctime(self):
        """ Returns the st_ctime attribute.

        :rtype: float
        :return: The st_ctime attribute
        """
        return self._stat.st_ctime

    def st_dev(self):
        """ Returns the st_dev attribute.

        :rtype: int
        :return: The st_dev attribute
        """
        return self._stat.st_dev

    def st_gid(self):
        """ Returns the st_gid attribute.

        :rtype: int
        :return: The st_gid attribute
        """
        return self._stat.st_gid

    def st_ino(self):
        """ Returns the st_ino attribute.

        :rtype: int
        :return: The st_ino attribute
        """
        return self._stat.st_ino

    def st_mode(self):
        """ Returns the st_mode attribute.

        :rtype: int
        :return: The st_mode attribute
        """
        return self._stat.st_mode

    def st_mtime(self):
        """ Returns the st_mtime attribute.

        :rtype: float
        :return: The st_mtime attribute
        """
        return self._stat.st_mtime

    def st_nlink(self):
        """ Returns the st_nlink attribute.

        :rtype: int
        :return: The st_nlink attribute
        """
        return self._stat.st_nlink

    def st_size(self):
        """ Returns the st_size attribute.

        :rtype: int
        :return: The st_size attribute
        """
        return self._stat.st_size

    def st_uid(self):
        """ Returns the st_uid attribute.

        :rtype: int
        :return: The st_uid attribute
        """
        return self._stat.st_uid


def copy(source, destination):
    """ Copy file to destination, returns true/false.

    :param str source:          The file to copy
    :param str destination:     The destination

    :return: True if successful
    :rtype bool
    """
    return copyfile(source, destination) == destination


# noinspection PyPep8Naming
def rename(file, newFile):  # NOSONAR
    """ file, newFile

    :param str file:        File to rename
    :param str newFile:     New filename, including the full path.

    :return: True if successed
    :rtype: bool

    """
    try:
        os.rename(file, newFile)
        return True
    except:
        return False


def delete(file):
    """ Delete a file.

    :param str file:        File to delete

    :return: True if successful
    :rtype bool
    """
    try:
        os.remove(file)
        return True
    except OSError:
        return False


def exists(path):
    """ Check for a file or folder existence.

    :param str path:            File or folder (folder must end with slash or backslash)

    :return: True if the file exists
    :rtype bool
    """
    return os.path.exists(path)


def listdir(path):
    """ Lists content of a folder.

    :param str path:            Folder to get list from

    :return: Directory content list (directories, files)
    :rtype (list[str], list[str])
    """
    files = []
    dirs = []
    if not exists(path):
        return dirs, files
    for filename in os.listdir(path):
        fullname = os.path.join(path, filename)
        if os.path.isfile(fullname):
            files.append(filename)
        if os.path.isdir(fullname):
            dirs.append(filename)
    return dirs, files


# noinspection PyPep8Naming
def makeLegalFilename(path):  # NOSONAR
    """ Returns a legal filename or path as a string.

    :param str path:            Filename or path to make legal.

    :return: Legal filename or path as a string
    :rtype str
    """
    return os.path.normpath(path)


def mkdir(path):
    """ Create a directory.

    :param str path:            Directory to create

    :return: True if successful
    :rtype bool
    """
    return os.mkdir(path)


def mkdirs(path):
    """ Create a directory and all the directories along the path.

    :param str path:            Directory to create

    :return: True if successful
    :rtype bool
    """
    if os.path.exists(path):
        return True

    try:
        os.makedirs(path)
        return os.path.exists(path)
    except OSError:
        return False


def rmdir(path):
    """ Remove a directory.

    :param str path:            Directory to remove

    :return: True if successful
    :rtype bool
    """
    return os.rmdir(path)


# noinspection PyPep8Naming
def validatePath(path):  # NOSONAR
    """ Returns the validated path.

    :param str path:            Path to format

    :return: The validated path
    :rtype str
    """
    return os.path.normpath(path)


# noinspection PyPep8Naming
def translatePath(path):  # NOSONAR
    """ Returns the translated path.

    :param str path:    Path to format

    :return: Translated path
    :rtype: str

    See http://kodi.wiki/view/Special_protocol

    E.g:
        special://home/ is mapped to: kodi/
        special://profile/ is mapped to: kodi/userdata

    Or in portable:
        special://home/ is mapped to: kodi/portable_data/
        special://profile/ is mapped to: kodi/portable_data/userdata

    """

    def get_return_path(base_path, name, *segments):
        if not base_path:
            raise ValueError("Missing __kodi_{}_path data".format(name))
        new_path = os.path.join(base_path, *[i.replace("/", os.sep) for i in segments if i and i != ''])

        if not os.path.exists(new_path):
            raise ValueError("Invalid path specified: {}".format(path, ))

        return new_path

    if path.startswith("special://profile/"):
        return_path = get_return_path(__add_on_info.kodi_profile_path,
                                      "profile",
                                      path.replace("special://profile/", ""))

    elif path.startswith("special://home/"):
        return_path = get_return_path(__add_on_info.kodi_home_path,
                                      "home",
                                      path.replace("special://home/", ""))

    elif path.startswith("special://xbmcbin/"):
        return_path = get_return_path(__add_on_info.kodi_home_path,
                                      "home",
                                      "system",
                                      path.replace("special://xbmcbin/", ""))

    elif os.path.isabs(path):
        return path

    else:
        raise ValueError("Invalid special path: %s" % (path,))

    actual_path = os.path.abspath(return_path)
    KodiStub.print_line("Mapped '{0}' -> '{1}'".format(path, actual_path), color=Colors.Blue)
    return actual_path


__add_on_info = addoninfo.get_add_on_info_from_calling_script()
