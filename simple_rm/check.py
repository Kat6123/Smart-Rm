# -*- coding: utf-8 -*-
# import logging
import os
import re
import stat

import simple_rm.constants as const

special_file_modes = [
    stat.S_ISBLK, stat.S_ISCHR,
    stat.S_ISFIFO, stat.S_ISSOCK
]

special_directories = [
    os.path.join(const.ROOT, root_inner) for root_inner in os.listdir(
        const.ROOT
    )
] + [const.ROOT]


def make_trash_if_not_exist(trash_location):
    create_not_exist_file(trash_location)
    files, info = get_trash_files_and_info_paths(trash_location)

    create_not_exist_file(files)
    create_not_exist_file(info)


def create_not_exist_file(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError as error:
            raise SysError(error.errno, error.strerror, error.filename)


def get_path_in_trash(path, trash_location):
    return os.path.join(
        trash_location, const.TRASH_FILES_DIRECTORY, os.path.basename(path)
    )


def get_path_in_trash_info(path, trash_location):
    return os.path.join(
        trash_location, const.TRASH_INFO_DIRECTORY,
        os.path.basename(path) + const.INFO_FILE_EXTENSION
    )


def get_correct_path(path):
    return os.path.abspath(os.path.expanduser(path))


def get_regex_matcher(regex):
    regex = regex + const.END_OF_STRING

    def match_path(path):
        matches = re.match(regex, os.path.basename(path))
        if matches:
            return matches.group(0)
    return match_path


def get_trash_files_and_info_paths(trash_location):
    return (
        os.path.join(trash_location, const.TRASH_FILES_DIRECTORY),
        os.path.join(trash_location, const.TRASH_INFO_DIRECTORY)
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


def return_true(x):
    return True
