# -*- coding: utf-8 -*-
from shutil import move
from os import (
    listdir,
    mkdir
)
from os.path import (
    exists,
    join
)
from ConfigParser import ConfigParser
from error import Error
from remove import (
    remove_directory_content,
    remove_file)


def check_basket(basket, file, info):               # TODO: check inner folders
    try:
        if not exists(basket):
            mkdir(basket)
            mkdir(file)
            mkdir(info)
    except OSError as e:
        raise Error(e)


def manage_basket(config):
    check_basket(config.location["basket"],
                 config.location["files"],
                 config.location["info"])

    if config.recycle_basket_options["view_basket_content"]:
        view_content(config.location["files"])

    if config.recycle_basket_options["clear_basket"]:
        clear_basket(config.location["files"], config.location["info"])
    elif config.recycle_basket_options["restore_from_basket"]:
        restore_files(config.files_to_restore,
                      config.location["files"], config.location["info"])


def restore_files(files_to_restore, files_location, info_location):
    for file in files_to_restore:
        file_path_in_files = join(files_location, file)
        file_path_in_info = join(info_location, file+".trashinfo")
        path_to_restore = get_path_from_trashinfo_files(file_path_in_info)
        move(file_path_in_files, path_to_restore)
        remove_file(file_path_in_info)


def get_path_from_trashinfo_files(trashinfo_file):
    trashinfo_config = ConfigParser()
    trashinfo_config.read(trashinfo_file)

    return trashinfo_config.get("Trash Info", "Path")


def clear_basket(files_location, info_location):        # TODOOO@
    remove_directory_content(files_location)
    remove_directory_content(info_location)


def view_content(file):               # if path doesn't exist
    files = listdir(file)
    for file in files:
        print file
