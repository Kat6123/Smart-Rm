# -*- coding: utf-8 -*-
import os
import os.path


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
