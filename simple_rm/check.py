# -*- coding: utf-8 -*-
# import logging
import os
import re
import shutil
import stat

from simple_rm.constants import *     # XXX:
from simple_rm.error import *


special_file_modes = [
    stat.S_ISBLK, stat.S_ISCHR,
    stat.S_ISFIFO, stat.S_ISSOCK
]

special_directories = [
    os.path.join(ROOT, root_inner) for root_inner in os.listdir(ROOT)
] + [ROOT]


def make_app_folder_if_not_exist():
    app = os.path.expanduser(APP_DIRECTORY)
    if not os.path.exists(app):
        try:
            os.mkdir(app)
        except (OSError, shutil.Error) as error:
            raise SystemError(error.errno, error.strerror, error.filename)


def make_trash_if_not_exist(trash_location):
    if not os.path.exists(trash_location):
        try:
            os.mkdir(trash_location)
            files, info = get_trash_files_and_info_paths(trash_location)
            os.mkdir(files)
            os.mkdir(info)
        except OSError as error:
            raise SystemError(error.errno, error.strerror, error.filename)


def get_path_in_trash(path, trash_location):
    return os.path.join(
        trash_location, TRASH_FILES_DIRECTORY, os.path.basename(path)
    )


def get_path_in_trash_info(path, trash_location):
    return os.path.join(
        trash_location, TRASH_INFO_DIRECTORY,
        os.path.basename(path) + INFO_FILE_EXPANSION
    )


def get_correct_path(path):
    return os.path.abspath(os.path.expanduser(path))


def get_regex_matcher(regex):
    regex = regex + END_OF_STRING

    def match_path(path):
        matches = re.match(regex, os.path.basename(path))
        if matches:
            return matches.group(0)
    return match_path


def get_trash_files_and_info_paths(trash_location):
    return (
        os.path.join(trash_location, TRASH_FILES_DIRECTORY),
        os.path.join(trash_location, TRASH_INFO_DIRECTORY)
    )


def check_cycle(source_path, destination_path):
    prefix = os.path.commonprefix([source_path, destination_path])
    if prefix == source_path:
        return False

    return True


def check_path_is_file(file_path):
    if os.path.isdir(file_path):
        return False

    return True


def check_path_existance(path):
    if not os.path.exists(path):
        return False

    return True


def check_path_is_directory(path):      # Remove!
    if not os.path.isdir(path):
        return False

    return True


def check_path_is_not_tree(path):
    if (os.path.isdir(path) and os.listdir(path)):
        return False

    return True


def check_directory_access(directory_path):
    if not (os.access(directory_path, os.W_OK) and
            os.access(directory_path, os.X_OK)):
            return False

    return True     # Stop


def check_parent_read_rights(path):
    if not os.access(os.path.dirname(path), os.R_OK):
        return False

    return True


def check_special_file(file_path):
    if os.getuid():                      # Explain!
        mode = os.stat(file_path).st_mode
        for special_mode in special_file_modes:
            if special_mode(mode):  # TODO: different types
                return False

    return True


def check_system_directory(directory_path):
    if os.getuid():
        for special_directory in special_directories:
            if directory_path == special_directory:
                return False
        if os.path.ismount(directory_path):
            return False

    return True
