# -*- coding: utf-8 -*-
from shutil import move
from os import (
    listdir,
    mkdir,
    rename,
    renames,
    walk
)
from os.path import (
    isdir,
    abspath,
    basename,
    join,
    islink,
    isfile
)
from ConfigParser import ConfigParser
from datetime import datetime

from error import Error


class SmartRemover(object):
    def _default_remove_permission(path):
        return True

    def __init__(self, basket_files_location, basket_info_location,
                 confirm_file_deletion=_default_remove_permission,
                 confirm_dir_deletion=_default_remove_permission):

        self.files_location = basket_files_location
        self.info_location = basket_info_location

        self.confirm_file_deletion = confirm_file_deletion
        self.confirm_dir_deletion = confirm_dir_deletion

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section("Trash Info")

    def make_trash_info_file(self, path):
        trashinfo_file = join(self.info_location,
                              basename(path) + ".trashinfo")
        self._trashinfo_config.set("Trash Info", "Path", abspath(path))
        self._trashinfo_config.set("Trash Info", "Date", datetime.today())

        with open(trashinfo_file, "w") as fp:
            self._trashinfo_config.write(fp)

    def file_remove(self, file):
        if islink(file) or isfile(file):
            if self.confirm_file_deletion(file):
                try:
                    rename(file, join(self.files_location, basename(file)))
                except OSError as e:
                    raise Error(e)

                self.make_trash_info_file(file)
        else:
            pass

    def empty_directory_remove(self, dir):
        if not islink(dir) and isdir(dir) and not listdir(dir):
            if self.confirm_dir_deletion(dir):
                try:
                    rename(dir, join(self.files_location, basename(dir)))
                except OSError as e:
                    raise Error(e)

                self.make_trash_info_file(dir)
        else:
            pass

    def tree_remove(self, tree):
        if islink(tree) or isfile(tree):
            self.file_remove(tree)
            return

        items_to_remove = []

        for root, dirs, files in walk(tree):
            items_in_root_to_remove = []

            for file in files:
                if self.confirm_file_deletion(file):
                    items_in_root_to_remove.append(file)

            if self.confirm_dir_deletion(root):   # XXX
                if set(listdir(root)).issubset(items_to_remove):
                    items_to_remove = list(set(items_to_remove)
                                           - set(listdir(root)))
                    items_to_remove.append(root)
                else:
                    items_to_remove.extend(items_in_root_to_remove)
                    break
            else:
                items_to_remove.extend(items_in_root_to_remove)

        for item in items_to_remove:
            try:
                renames(item, join(self.files_location, basename(item)))
            except OSError as e:
                raise Error(e)

            self.make_trash_info_file(item)


class RemoveManager(object):
    def __init__(self, config):
        self.basket_location = config.location["basket"]
        self.basket_files_location = config.location["files"]
        self.basket_info_location = config.location["info"]

        self.confirm_file_deletion = config.messages["ask_file_remove"]
        self.confirm_dir_deletion = config.messages["ask_directory_remove"]

        #check_basket(self.basket_location, self.basket_files_location,
        #             self.basket_info_location)

        #if config.modes[rm_recursively]:
        #    pass

        for file in config.files_to_delete:
            pass
        #file_remove(config.location["files"], file)
        #make_trash_info_files(config.location["info"], config.files_to_delete)
