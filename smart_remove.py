# -*- coding: utf-8 -*-
from error import Error
from os import (
    listdir,
    mkdir
)
from os.path import (
    exists,
    abspath,
    basename,
    join
)
from ConfigParser import ConfigParser


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
        #trashinfo_config.set("Trash Info", "Date")

        with open(trashinfo_file, "w") as fp:
            trashinfo_config.write(fp)


def view_content(location):
    check_basket(location)

    files = listdir(location["files"])          # try?
    for file in files:
        print file
