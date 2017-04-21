#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from os.path import expanduser


def check_file_existance(file):
    return True


def verify_file_removal(file):
    pass


def verify_directory_removal(directory):
    pass


def verify_tree_removal(tree):
    pass


class Remover(object):
    """docstring for ."""
    def __init__(
            self, basket_location=expanduser("~/.local/share/basket"),
            confirm_rm_always=False, not_confirm_rm=False,
            confirm_rm_if_file_write_ban=True,
            dry_run=False,
            follow_sym_link=False
    ):
        # TODO: check_basket
        self.basket_location = basket_location

        self.modes["confirm_rm_always"] = confirm_rm_always
        self.modes["not_confirm_rm"] = not_confirm_rm
        self.modes[
            "confirm_rm_if_file_write_ban"
        ] = confirm_rm_if_file_write_ban
        self.dry_run = dry_run
        self.follow_sym_link = follow_sym_link

    def remove_tree(self, file):
        pass


class AdvancedRemover(object):
    """docstring for ."""
    def __init__(
        self, basket_location=expanduser("~/.local/share/basket"),
        confirm_rm_always=False, not_confirm_rm=False,
        confirm_rm_if_file_write_ban=True,
        dry_run=False,
        follow_sym_link=False
    ):
        self.remover = Remover(
            basket_location,
            confirm_rm_always, not_confirm_rm,
            confirm_rm_if_file_write_ban,
            dry_run, follow_sym_link
        )

    def remove_list(
        self, paths_to_remove,
        verify_file_remove,
        check_file_existance=check_file_existance
    ):
        for path in paths_to_remove:
            if check_file_existance(path) and verify_file_remove(path):
                self.remover.remove_tree(path)

    def remove_files(self, paths_to_remove):
        self.remove_list(paths_to_remove, verify_file_removal)

    def remove_directories(self, paths_to_remove):
        self.remove_list(paths_to_remove, verify_directory_removal)

    def remove_trees(self, paths_to_remove):
        self.remove_list(paths_to_remove, verify_tree_removal)
