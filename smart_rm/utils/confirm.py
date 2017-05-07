# -*- coding: utf-8 -*-
import errno
import os
import os.path
from smart_rm.core.error import ModeError


def ask_if_file_has_not_write_access(path):
    if os.access(path, os.W_OK):
        return True
    elif ask_remove(path, special_info="write-protected"):
        return True

        return False


def ask_remove(path, special_info=""):
    if os.path.isfile(path):
        what_remove = "file"
    else:
        what_remove = "directory"
    answer = raw_input(
        "Do you want to remove {0} {1} \"{2}\"?: "
        "".format(special_info, what_remove, path)
    )
    if answer == 'y':
        return True


def verify_file_removal(file):
    if not os.path.isfile(file):
        raise ModeError(errno.EISDIR, os.strerror(errno.EISDIR), file)


def verify_directory_removal(directory):
    if os.path.isdir(directory) and os.path.listdir(directory):
        raise ModeError(
            errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY), directory
        )
