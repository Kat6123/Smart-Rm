# -*- coding: utf-8 -*-
from os import (
    listdir,
    mkdir,
    rename,
    renames
)
from os.path import (
    exists,
    abspath,
    basename,
    join
)
from ConfigParser import ConfigParser
from datetime import datetime

from error import Error
from remove import remove_directory_content


def check_basket(basket, file, info):               # TODO: check inner folders
    try:
        if not exists(basket):
            mkdir(basket)
            mkdir(file)
            mkdir(info)
    except OSError as e:
        raise Error(e)


def make_trash_info_files(info_location, paths):
    trashinfo_config = ConfigParser()
    trashinfo_config.add_section("Trash Info")

    for path in paths:
        trashinfo_file = join(info_location, basename(path) + ".trashinfo")
        trashinfo_config.set("Trash Info", "Path", abspath(path))
        trashinfo_config.set("Trash Info", "Date", datetime.today())

        with open(trashinfo_file, "w") as fp:
            trashinfo_config.write(fp)


def remove(config):
    check_basket(config.location["basket"],
                 config.location["files"],
                 config.location["info"])

    for file in config.files_to_delete:
        file_remove(config.location["files"], file)
    make_trash_info_files(config.location["info"], config.files_to_delete)


def file_remove(basket_files_location, path):
    rename(path, join(basket_files_location, basename(path)))


def tree_remove(basket_files_location, path):           # TODO: go in
    renames(path, join(basket_files_location, basename(path)))


def manage_basket(config):
    check_basket(config.location["basket"],
                 config.location["files"],
                 config.location["info"])
    view_content(config.location["files"])

    if config.recycle_basket_options["clear_basket"]:
        clear_basket(config.location["files"], config.location["info"])


def clear_basket(files_location, info_location):        # TODOOO@
    remove_directory_content(files_location)
    remove_directory_content(info_location)


def view_content(file):               # if path doesn't exist
    files = listdir(file)
    for file in files:
        print file
