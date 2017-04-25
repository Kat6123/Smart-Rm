#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from os import (
    listdir,
    strerror,
    stat,
    walk,
    getuid,
    R_OK,
    W_OK,
    X_OK,
    access
)
from os.path import (
    expanduser,
    isdir,
    abspath,
    basename,
    join,
    exists,
    ismount,
    isfile,
    dirname
)
from basket import Basket
from error import (
    PermissionError,
    ExistError,
    ModeError
)
from stat import (
    S_ISBLK,
    S_ISCHR,
    S_ISFIFO,
    S_ISSOCK
)
from logging import (
    debug,
    # info,
    # warning,
    error
    # critical
)
from errno import (
    EISDIR,
    ENOENT,
    ENOTEMPTY,
    EACCES
)


def check_path_existance(path):
    abs_path = abspath(path)
    if not access(dirname(abs_path), R_OK):
        raise PermissionError(EACCES, strerror(EACCES), path)
    elif not exists(abs_path):
        raise ExistError(ENOENT, strerror(ENOENT), abs_path)


def default_true(path):
    return True


class Remover(object):
    """docstring for ."""
    def __init__(
            self,
            check_file_existance=check_path_existance,
            confirm_removal=default_true,
            # check_file_access=default_true,
            move_file_to_basket=default_true,       # TODO what default?
            is_relevant_file_name=default_true
    ):
        self.check_file_existance = check_file_existance
        self.confirm_removal = confirm_removal
        # self.check_file_access = Remover.check_file_access
        self.move_file_to_basket = Remover.move_file_to_basket
        self.is_relevant_file_name = is_relevant_file_name

    def remove(self, item_path):
        self.check_file_existance(item_path)

        if isdir(item_path) and listdir(item_path):
            raise ModeError(ENOTEMPTY, strerror(ENOTEMPTY), item_path)
        if self.confirm_removal(item_path):
            if (
                not access(dirname(item_path), W_OK) or
                not access(dirname(item_path), X_OK)
            ):
                raise PermissionError(EACCES, strerror(EACCES), item_path)
            # self.move_file_to_basket(item_path)

    def remove_tree(self, tree):
        if isfile(tree):
            self.remove(tree)
            return

        items_to_remove = []

        for root, dirs, files in walk(tree, topdown=False):
            items_in_root_to_remove = []
            root = abspath(root)

            for file in files:
                if self.is_relevant_file_name(file):
                    if self.confirm_removal(file):
                        abs_path = join(root, basename(file))
                        items_in_root_to_remove.append(abs_path)

            if self.confirm_removal(root):   # XXX set ? if basename + relev
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
            self.move_file_to_basket(item)

    @staticmethod
    def check_file_access(file):
        path_parent = dirname(file)
        if not access(path_parent, W_OK) and access(path_parent, X_OK):
            raise PermissionError(EACCES, strerror(EACCES), file)

    @staticmethod
    def move_file_to_basket(file):
        pass


class AdvancedRemover(object):
    def __init__(
            self, basket_location=expanduser("~/.local/share/basket"),
            confirm_rm_always=False, not_confirm_rm=False,
            dry_run=False
    ):
        # XXX
        if confirm_rm_always:
            confirm_removal = AdvancedRemover._ask_remove
        elif not_confirm_rm:
            confirm_removal = default_true
        else:
            confirm_removal = AdvancedRemover._ask_if_file_has_not_write_access

        self.basket = Basket(
            basket_location=basket_location,
            dry_run=dry_run,
        )
        move_to_basket = self.basket.move_to_basket

        self.remover = Remover(
            confirm_removal=confirm_removal,    # confirm_removal,
            move_file_to_basket=move_to_basket
        )

        self._special_file_modes = [S_ISBLK, S_ISCHR, S_ISFIFO, S_ISSOCK]
        sys = ["/" + path for path in listdir("/")]
        self._special_directories = ["/"] + sys

    def remove_list(
            self, paths_to_remove,
            verify_removal=default_true
    ):
        for path in paths_to_remove:
            try:
                path = abspath(path)
                check_path_existance(path)
                verify_removal(path)

                if isfile(path):
                    self._check_special_file(path)
                elif isdir(path):
                    self._check_system_directory(path)

                self.remover.remove_tree(path)
            except (PermissionError, ExistError, ModeError) as why:
                error(why)

    def remove_files(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            verify_removal=AdvancedRemover._verify_file_removal
        )

    def remove_directories(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            verify_removal=AdvancedRemover._verify_directory_removal
        )

    def remove_trees(self, paths_to_remove):
        self.remove_list(paths_to_remove)

    def _check_special_file(self, path):
        if getuid:          # TODO explain!
            mode = stat(path).st_mode
            for special_mode in self._special_file_modes:
                if special_mode(mode):  # TODO: different types
                    raise PermissionError(EACCES, "Not regular file", path)

    def _check_system_directory(self, path):
        if getuid:
            for special_directory in self._special_directories:
                if path == special_directory:
                    raise PermissionError(EACCES, "System directory", path)
            if ismount(path):
                raise PermissionError(EACCES, "Mount point", path)

    @staticmethod
    def _verify_file_removal(file):
        if not isfile(file):
            raise ModeError(EISDIR, strerror(EISDIR), file)

    @staticmethod
    def _verify_directory_removal(directory):
        if isdir(directory) and listdir(directory):
            raise ModeError(ENOTEMPTY, strerror(ENOTEMPTY), directory)

    @staticmethod
    def _ask_if_file_has_not_write_access(path):
        if access(path, W_OK):
            return True
        elif AdvancedRemover._ask_remove(path, special_info="write-protected"):
            return True

        return False

    @staticmethod
    def _ask_remove(path, special_info=""):
        if isfile(path):
            what_remove = "file"
        else:
            what_remove = "directory"
        answer = raw_input(
            "Do you want to remove {0} {1} \"{2}\"?: "
            "".format(special_info, what_remove, path)
        )
        if answer == 'y':
            return True
