# -*- coding: utf-8 -*-
from error import Error
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


def check_basket(location):                 # TODO: check inner folders
    try:
        if not exists(location["basket"]):
            mkdir(location["basket"])
            mkdir(location["files"])
            mkdir(location["info"])
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


def view_content(location):
    check_basket(location)

    files = listdir(location["files"])          # try?
    for file in files:
        print file


def remove(config):
    check_basket(config.location)

    for file in config.files_to_delete:
        file_remove(config.location["files"], file)
    make_trash_info_files(config.location["info"], config.files_to_delete)


def file_remove(basket_files_location, path):
    rename(path, join(basket_files_location, basename(path)))


def tree_remove(basket_files_location, path):           # TODO: go in
    renames(path, join(basket_files_location, basename(path)))
