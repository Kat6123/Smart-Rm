# -*- coding: utf-8 -*-
from shutil import (
    move
)
from os import (
    listdir,
    mkdir,
    rename
)
from os.path import (
    expanduser,
    exists,
    join,
    commonprefix,
    abspath,
    basename,
    dirname
)
from ConfigParser import ConfigParser
from remove import (
    remove_directory_content,
    remove_tree,
    remove_file,
    move_tree
)
from error import OtherOSError
from datetime import datetime
from hashlib import sha256
from logging import (
    error,
    warning
)
from politics import (
    MoveAndAskNewNameForMovableObject,
    MoveAndMakeNewNameDependingOnAmount,
    MoveAndRaiseExceptionIfSamenameFiles,
    MoveAndRewriteSamenameFilesWithAsking,
    MoveAndRewriteIfSamenameFilesWithoutAsking
)

BASKET_FILES_DIRECTORY = "files"            # is it bad?
BASKET_INFO_DIRECTORY = "info"
INFO_SECTION = "Trash info"
OLD_PATH_OPTION = "Path"
REMOVE_DATE_OPTION = "Date"
FILE_HASH_OPTION = "Hash"
INFO_FILE_EXPANSION = ".trashinfo"
DEFAULT_BASKET_LOCATION = "~/.local/share/basket"


def get_basket_files_and_info_paths(basket_location):
    return (
        join(basket_location, BASKET_FILES_DIRECTORY),
        join(basket_location, BASKET_INFO_DIRECTORY)
    )


def check_basket_and_make_if_not_exist(basket_location):
    if not exists(basket_location):
        try:
            mkdir(basket_location)
            files, info = get_basket_files_and_info_paths(basket_location)
            mkdir(files)
            mkdir(info)
        except OSError as why:
            raise OtherOSError(why.errno, why.strerror, why.filename)


class Basket(object):
    def __init__(
        self,
        basket_location=expanduser(DEFAULT_BASKET_LOCATION),
        mover=None
    ):
        self.basket_files_location,     # XXX
        self.basket_info_location =
        get_basket_files_and_info_paths(basket_location)

        if mover is None:
            self.mover = Mover()
        else:
            self.mover = mover

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section(INFO_SECTION_NAME)

    def restore_from_basket(self, item_path):
        item_path_in_files = join(self.basket_files_location, item_path)
        item_path_in_info = join(
            self.basket_info_location, item.path + INFO_FILE_EXPANSION
        )

        restore_path = self._get_restore_path_from_trashinfo_files(
            file_path_in_info
        )       # XXX check basket?

        if self.mover.move(item_path_in_files, restore_path):
            remove_file(item_path_in_info)      # else some warning

    def _get_restore_path_from_trashinfo_files(self, trashinfo_file):
        self._trashinfo_config.read(trashinfo_file)     # add try catch

        return self._trashinfo_config.get(INFO_SECTION, OLD_PATH_OPTION)

    def clear_basket(files_location, info_location):
        remove_directory_content(files_location)
        remove_directory_content(info_location)

    def view_content(self):
        # call("less {0}".format(self.basket_location))
        pass


class AdvancedBasket(object):
    def __init__(
        self,
        basket_location=expanduser("~/.local/share/basket"),
        move_basket_name_conflicts=MoveAndMakeNewNameDependingOnAmount,
        restore_name_conflicts=MoveAndRewriteSamenameFilesWithAsking,
        clean_basket_politic="",
        check_hash=False,
        dry_run=False
    ):
        if dry_run:
            solve_basket_name_conflicts = move_basket_name_conflicts()._watch
            solve_restore_name_conflicts = restore_name_conflicts()._watch
        else:
            solve_basket_name_conflicts = move_basket_name_conflicts.execute
            solve_restore_name_conflicts = restore_name_conflicts.execute

        self.basket = Basket(
            basket_location=basket_location,
            move_to_basket=solve_basket_name_conflicts,
            move_from_basket=solve_restore_name_conflicts
        )

    def clean(self):
        pass

    def move_file_to_basket(self, file):
        self.basket.move_to_basket(file)

    def restore_files(self, paths):
        self.basket.restore_file(paths)

    def view_content(self):
        self.basket.view_content()
