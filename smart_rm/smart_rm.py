"""docstring ."""
# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# from os.path import expanduser
# from shutil import move
from os import (
    listdir,
    # rename,
    walk
)
from os.path import (
    expanduser,
    # isdir,
    abspath,
    basename,
    join
    # islink,
    # isfile
)
# from ConfigParser import ConfigParser
# from datetime import datetime


def default_true(path):
    return True


class Remover(object):
    """docstring for ."""
    def __init__(
            self, basket_location=expanduser("~/.local/share/basket"),
            check_file_existance=default_true,
            confirm_removal=default_true,
            check_file_access=default_true,
            move_file_to_basket=default_true,
            is_relevant_file_name=default_true,
            follow_link=False
    ):
        self.basket_location = basket_location
        self.check_file_existance = check_file_existance
        self.confirm_removal = confirm_removal
        self.check_file_access = check_file_access
        self.move_file_to_basket = move_file_to_basket
        self.is_relevant_file_name = is_relevant_file_name
        self.follow_link = follow_link

    def remove(self, item_path):
        # TODO: check_file_location, is relevant
        self.check_file_existance(item_path)
        self.confirm_removal(item_path)
        self.check_file_access(item_path)
        self.move_file_to_basket(item_path)

    def remove_tree(self, tree):
        # if islink(tree) or isfile(tree):
        #     self.remove(tree)
        #     return
        items_to_remove = []

        for root, dirs, files in walk(tree, topdown=False):
            items_in_root_to_remove = []
            root = abspath(root)

            for file in files:
                if self.is_relevant_file_name(file):
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


class AdvancedRemover(object):
    """docstring for ."""
    def __init__(
            self, basket_location=expanduser("~/.local/share/basket"),
            confirm_rm_always=False, not_confirm_rm=False,
            # confirm_rm_if_file_write_ban=True,
            dry_run=False,
            follow_sym_link=False
    ):
        if confirm_rm_always:
            confirm_removal = AdvancedRemover.interactive_mode
        elif confirm_rm_if_file_write_ban:
            confirm_removal = AdvancedRemover.ask_if_file_has_not_write_access

        self.remover = Remover(
            basket_location,
            confirm_removal=confirm_removal,
            follow_link=follow_sym_link
        )

    def remove_list(
            self, paths_to_remove,
            verify_file_remove,
            check_file_existance=check_file_existance   # pylint?
    ):
        for path in paths_to_remove:
            if AdvancedRemover.check_file_existance(path)
            and verify_file_remove(path):
                self.remover.remove_tree(path)

    def remove_files(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            AdvancedRemover.verify_file_removal
        )

    def remove_directories(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            AdvancedRemover.verify_directory_removal
        )

    def remove_trees(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            AdvancedRemover.verify_tree_removal
        )

    @staticmethod
    def check_file_existance(path):
        pass

    @staticmethod
    def verify_file_removal(file):
        """"""
        pass

    @staticmethod
    def verify_directory_removal(directory):
        """docstring ."""
        pass

    @staticmethod
    def verify_tree_removal(tree):
        pass

    @staticmethod
    def interactive_mode(path):
        pass

    @staticmethod
    def ask_if_file_has_not_write_access(path):
        pass
