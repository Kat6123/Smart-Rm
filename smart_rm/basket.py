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
    move_tree,
    dry_run
)
_remove_import = [
    remove_directory_content,
    remove_tree,
    remove_file,
    move_tree
]
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
        for func in _remove_import:
            func = dry_run(dry_run)(func)

    def clean(self):
        pass

    def move_file_to_basket(self, file):
        pass

    def restore_files(self, paths):
        pass

    def view_content(self):
        self.basket.view_content()


class DryRunMixin(object):
    def dru_run(self, *args, **kwargs):
        self._watch(*args, **kwargs)

    def execute(self, *args, **kwargs):
        self._watch(*args, **kwargs)
        return self._do(*args, **kwargs)


class Mover(DryRunMixin):        # Enough to inherit fron DryRunMixin
    def __init__(self):
        self.source, self.destination, self.target_path = "", ""
        self.exists = False

    def _watch(self, path, destination):
        self.path = path
        self.destination = destination
        self.target_path = join(dirname(destination), basename(path))
        if exists(self.target_path):
            self.exists = True


# need mode to choose rename or not
class MoveAndRewriteIfSamenameFilesWithoutAsking(Mover):
    def _watch(self, path, destination):
        super(MoveAndRewriteIfSamenameFilesWithoutAsking, self)._watch(
            path, destination
        )

        if self.exists:
            pass

    def _do(self):
        if self.exists:             # TODO: CHANGE!
            with open(self.target_path, "w") as target:
                with open(self.path, "r") as path:
                    target.write(path.read())
            remove_tree(self.path)
        else:
            move_tree(self.path, self.target_path)
        return self.target_path


# need message!
class MoveAndRewriteSamenameFilesWithAsking(Mover):
    def __init__(self):
        super(MoveAndRewriteSamenameFilesWithAsking, self).__init__()
        self.answer = False

    def _watch(self, path, destination):
        super(MoveAndRewriteSamenameFilesWithAsking, self, path, destination)

        if self.exists:
            self.answer = raw_input(
                "Do you want to rewrite {0} in {1}"
                "".format(basename(path), destination)
            )
        # if not answer:
        #     return

    def _do(self):
        if self.exists:
            if self.answer:     # Change
                MoveAndRewriteIfSamenameFilesWithoutAsking().execute(
                    self.path,
                    self.destination
                )
            else:
                return
        else:
            move_tree(self.path, self.target_path)
            return self.target_path


class MoveAndRaiseExceptionIfSamenameFiles(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )       # add description

        if self.exists:
            pass

    def _do(self):
        if self.exists:
            raise OtherOSError(
                "Already exists {0} in {1}".format(self.path, self.destination)
            )
        move_tree(self.path, self.target_path)
        return self.target_path


class MoveAndAskNewNameForMovableObject(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )
        if self.exists:
            new_name = raw_input("Enter new name for {0}:".format(path))
            if new_name:
                self.target_path = join(self.destination, new_name)
            else:
                raise OtherOSError(             # Or just message?
                    "Already exists {0} in {1}"
                    "".format(self.path, self.destination)
                )

    def _do(self):
        move_tree(self.path, self.target_path)
        return self.target_path


class MoveAndMakeNewNameDependingOn(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )
        if self.exists:
            count_of_samename_files = listdir(destination).count(
                basename(path)
            )
            self.target_path = join(
                destination,
                basename(path) + ".{0}".format(count_of_samename_files)
            )

    def _do(self):
        move(self.path, self.target_path)
        return self.target_path
