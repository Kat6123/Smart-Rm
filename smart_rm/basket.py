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
    remove_file
)
from error import OtherOSError
from datetime import datetime
from hashlib import sha256
from logging import (
    error,
    warning
)
# from subprocess import call


class Basket(object):
    def __init__(
        self,
        basket_location=expanduser("~/.local/share/basket"),
    ):
        self.basket_location = basket_location
        self.file = join(self.basket_location, "files")
        self.info = join(self.basket_location, "info")

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section("Trash Info")

        self._move=""

    def move_to_basket(self, path):         # XXX fix dry_run
        path = abspath(path)

        self._check_basket()
        self._check_cycle(path)
        self._check_empty_space()

        if self._move(self.basket_location, path):
            self._make_trash_info_file(path)

    def _check_cycle(self, path):
        prefix = commonprefix([path, self.file])
        if prefix == path:
            raise OtherOSError(
                "Cannot move a directory {0} into itself {1}"
                "".format(path, self.file)
            )

    def _check_basket(self):         # TODO: check inner folders
        try:
            if not exists(self.basket_location):
                mkdir(self.basket_location)
                mkdir(self.file)
                mkdir(self.info)
        except OSError as why:
            raise OtherOSError(why.errno, why.strerror, why.filename)

    def _check_empty_space(self):
        pass

    def restore_file(self, file):
        file_path_in_files = join(self.file, file)
        file_path_in_info = join(self.info, file + ".trashinfo")

        path_to_restore = self._get_path_from_trashinfo_files(
            file_path_in_info
        )       # XXX check basket?

        # self._check_basket()          # XXX similar to move code
        # self._check_cycle(path)
        # self._check_empty_space()
        if self._restore(file_path_in_files, path_to_restore):
            remove_file(file_path_in_info)      # else some warning

    def _get_path_from_trashinfo_files(self, trashinfo_file):
        self._trashinfo_config.read(trashinfo_file)

        return self._trashinfo_config.get("Trash Info", "Path")

    def clear_basket(files_location, info_location):
        remove_directory_content(files_location)
        remove_directory_content(info_location)

    def view_content(self):
        # call("less {0}".format(self.basket_location))
        pass

    def _make_trash_info_file(self, path):
        trashinfo_file = join(self.info, basename(path) + ".trashinfo")
        self._trashinfo_config.set("Trash Info", "Path", abspath(path))
        self._trashinfo_config.set("Trash Info", "Date", datetime.today())
        self._trashinfo_config.set(
            "Trash Info", "Hash", sha256(path).hexdigest()
        )

        with open(trashinfo_file, "w") as fp:
            self._trashinfo_config.write(fp)


class AdvancedBasket(object):
    def __init__(
        self,
        basket_location=expanduser("~/.local/share/basket"),
        solve_name_conflicts_when_move_to_basket="",
        solve_name_conflicts_when_restore="",
        clean_basket_politic="",
        check_hash=False,
    ):

        self.basket = Basket(
            basket_location=basket_location,
            check_hash=check_hash
        )

    def clean(self):
        pass

    def move_file_to_basket(self, file):
        pass

    def restore_files(self, paths):
        pass

    def view_content(self):
        self.basket.view_content()


# need mode to choose rename or not; what to do with dry_run?
def rewrite_samename_files_without_asking(path, destination, dry_run=False):
    target_path = join(dirname(destination), basename(path))
    remove_tree(target_path)
    move(path, target_path)
    return target_path


# need message!
def rewrite_samename_files_with_asking(path, destination):
    answer = raw_input(
        "Do you want to rewrite {0} in {1}".format(basename(path), destination)
    )
    if answer:
        return rewrite_samename_files_without_asking(path, destination)
    else:
        raise_exception_if_samename_files(path, destination)


def raise_exception_if_samename_files(path, destination):
    raise OtherOSError(
        "Already exists {0} in {1}".format(basename(path), destination)
    )


def ask_new_name_for_movable_object(path, destination):
    new_name = raw_input("Enter new name for {0}:".format(path))
    new_path = join(destination, new_name)

    if new_name:
        move(path, new_path)
        return new_path
    else:
        raise_exception_if_samename_files(path, destination)


def new_name_for_movable_object_depending_on_amount_of_samename_files(
    path,
    destination
):
    count_of_samename_files = listdir(destination).count(basename(path))
    new_path = join(
        destination,
        basename(path) + ".{0}".format(count_of_samename_files)
    )
    move(path, new_path)
    return new_path
