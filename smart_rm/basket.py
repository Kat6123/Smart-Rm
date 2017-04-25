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
from logging import error
# from subprocess import call


class Basket(object):
    def __init__(
        self,
        basket_location=expanduser("~/.local/share/basket"),
        dry_run=False,
        same_name_politics=""
    ):
        self.basket_location = basket_location
        self.file = join(self.basket_location, "files")
        self.info = join(self.basket_location, "info")

        self.dry_run = dry_run
        self.same_name_politics = same_name_politics

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section("Trash Info")

    def move_to_basket(self, path):         # XXX fix dry_run
        path = abspath(path)

        self._check_basket()
        self._check_cycle(path)
        self._check_empty_space()

        if not self.dry_run:
            self._make_trash_info_file(path)
            try:
                error(join(self.file, basename(path)))
                error(path)
                rename(path, join(self.file, basename(path)))
            except OSError as why:
                raise OtherOSError(why.errno, why.strerror, why.filename)

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

    def _check_name_conflicts(self, path):
        pass

    def _check_empty_space(self):
        pass

    def restore_files(self, files_to_restore):
        for file in files_to_restore:
            file_path_in_files = join(self.file, file)
            file_path_in_info = join(self.info, file + ".trashinfo")

            path_to_restore = self._get_path_from_trashinfo_files(
                file_path_in_info
            )       # XXX check basket?
            move(file_path_in_files, path_to_restore)
            remove_file(file_path_in_info)

    def _get_path_from_trashinfo_files(self, trashinfo_file):
        self._trashinfo_config.read(trashinfo_file)

        return self._trashinfo_config.get("Trash Info", "Path")

    def clear_basket(files_location, info_location):        # TODOOO@
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


# need mode to choose rename or not
def rewrite_samename_files_without_asking(path, destination):
    target_path = join(dirname(destination)), basename(path)
    remove_tree(target_path)
    move(path, target_path)


def rewrite_samename_files_with_asking(path, destination):
    new_name = raw_input("Enter new name for {0}:".format(path))

    if new_name:
        move(path, join(destination, new_name))
