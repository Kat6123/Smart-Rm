# -*- coding: utf-8 -*-
from shutil import move
from os import (
    listdir,
    rename,
    walk,
    #devnull
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
from basket import check_basket
#from sys import stdout

from error import Error


class OutputManager(object):
    def __init__(self, opened_file):
        self.text = []
        self.stream = opened_file       # Rename?

    def add_line(self, string):
        self.text.append(string + "\n")

    def write(self):
        self.stream.writelines(self.text)
        self.stream.flush()
        self.text = []

    def clear(self):
        self.text = []


class SmartRemover(object):     # TODO: handle errors! file not found and pass
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

        self.errors = []
        #self.output = OutputManager(fp)

    def make_trash_info_file(self, path):
        self.errors = []

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
        if islink(dir) or isfile(dir):
            self.file_remove(dir)
            return

        if isdir(dir) and not listdir(dir):
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

        for root, dirs, files in walk(tree, topdown=False):
            #print root, dirs, files
            items_in_root_to_remove = []
            root = abspath(root)

            for file in files:
                if self.confirm_file_deletion(file):
                    abs_path = join(root, basename(file))
                    items_in_root_to_remove.append(abs_path)

            if self.confirm_dir_deletion(root):   # XXX set ? if basename
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
                move(item, join(self.files_location, basename(item)))
            except OSError as e:
                raise Error(e)

            self.make_trash_info_file(item)

    def remove_items_from_list(self, list, mode):
        """

        Try to remove each item in list.
        Depending on string value of 'mode':
            file = remove only files, other - ignored
            directory = remove files and empty directories
            recursive = remove all items
        """
        if mode == "file":
            action = self.file_remove
        elif mode == "directory":
            action = self.empty_directory_remove
        elif mode == "recursive":
            action = self.tree_remove

        for path in list:
            action(path)


class RemoveManager(object):
    def __init__(self, config):
        self.basket_location = config.location["basket"]
        self.basket_files_location = config.location["files"]
        self.basket_info_location = config.location["info"]

        check_basket(self.basket_location, self.basket_files_location,
                     self.basket_info_location)

        self.smart_remover = SmartRemover(self.basket_files_location,
                                          self.basket_info_location)

        self.ask_file_deletion = config.messages["ask_file_remove"]
        self.ask_dir_deletion = config.messages["ask_dir_remove"]

        self.items_to_delete = config.files_to_delete

        self.modes = {}
        self.modes["recursive"] = config.modes["rm_recursively"]
        self.modes["directories"] = config.modes["rm_empty_directories"]

        self.modes["interactive"] = config.modes["ask_remove"]
        self.modes["silent"] = config.modes["silent_mode"]
        self.modes["dry-run"] = config.modes["remove_imitation"]

    def make_interactive(self):
        self.smart_remover.confirm_file_deletion = self.ask_file_deletion
        self.smart_remover.confirm_dir_deletion = self.ask_dir_deletion

    def make_silent(self):             # TODO: end ?
        #null = open(devnull, "w")
        #stdout = null
        pass

    def make_dry_run(self):
        pass

    def remove_recursive(self):
        self.smart_remover.remove_items_from_list(
            self.items_to_delete, "recursive")

    def remove_directories(self):
        self.smart_remover.remove_items_from_list(
            self.items_to_delete, "directory")

    def remove_files(self):
        self.smart_remover.remove_items_from_list(
            self.items_to_delete, "file")

    def remove_using_all_config_parametres(self):
        if self.modes["interactive"]:
            self.make_interactive()
        elif self.modes["silent"]:
            self.make_silent()

        if self.modes["dry-run"]:
            self.make_dry_run()

        if self.modes["recursive"]:
            self.remove_recursive()
        elif self.modes["directories"]:
            self.remove_directories()
        else:
            self.remove_files()
