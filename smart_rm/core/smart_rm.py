# -*- coding: utf-8 -*-
from os import (
    listdir,
    strerror,
    walk,
    access,
    W_OK
)
from os.path import (
    expanduser,
    isdir,
    abspath,
    basename,
    join,
    isfile
)
from error import (
    PermissionError,
    ExistError,
    ModeError
)
from logging import (
    # debug,
    # info,
    # warning,
    error
    # critical
)
from errno import (
    EISDIR,
    ENOTEMPTY
)
from trash import (
    INFO_SECTION,
    OLD_PATH_OPTION,
    REMOVE_DATE_OPTION,
    FILE_HASH_OPTION,
    INFO_FILE_EXPANSION,
    DEFAULT_TRASH_LOCATION,
    get_trash_files_and_info_paths,
    check_trash_and_make_if_not_exist
)
from datetime import datetime
from hashlib import sha256
from ConfigParser import ConfigParser
import mover                # XXX ?
DEFAULT_SOLVE_SAMENAME_POLITIC = "Mover"


def verify_file_removal(file):
    if not isfile(file):
        raise ModeError(EISDIR, strerror(EISDIR), file)


def verify_directory_removal(directory):
    if isdir(directory) and listdir(directory):
        raise ModeError(ENOTEMPTY, strerror(ENOTEMPTY), directory)


def ask_if_file_has_not_write_access(path):
    if access(path, W_OK):
        return True
    elif AdvancedRemover._ask_remove(path, special_info="write-protected"):
        return True

        return False


def ask_remove(path, special_info=""):
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


class SmartRemover(object):
    def __init__(           # should i call super for object?
            self,
            trash_location=expanduser(DEFAULT_TRASH_LOCATION),
            confirm_removal=lambda: True,
            mover=None,
            is_relevant_file_name=lambda: True
    ):
        self.trash_location = trash_location
        self.trash_files_location, self.trash_info_location = (
            get_trash_files_and_info_paths(trash_location)
        )

        if mover is None:
            self.mover = mover.Mover()
        else:
            self.mover = mover

        self.confirm_removal = confirm_removal
        self.is_relevant_file_name = is_relevant_file_name

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section(INFO_SECTION)

    def remove_file_or_empty_directory(self, item_path):
        if isdir(item_path) and listdir(item_path):
            raise ModeError(ENOTEMPTY, strerror(ENOTEMPTY), item_path)

        if self.is_relevant_file_name(
            item_path
        ) and self.confirm_removal(
            item_path
        ):              # TODO: if path has changed? what about hash
            self._smart_remove(item_path)

    def remove_tree(self, tree):
        if isfile(tree):
            self.remove(tree)
            return

        items_to_remove = []

        for root, dirs, files in walk(tree, topdown=False):
            items_in_root_to_remove = []
            root = abspath(root)

            for file_path in files:
                if self.is_relevant_file_name(
                    file_path
                ) and self.confirm_removal(
                    file_path
                ):
                    abs_path = join(root, basename(file))
                    items_in_root_to_remove.append(abs_path)

            if self.is_relevant_file_name(root) and self.confirm_removal(root):
                if set(listdir(root)).issubset(items_to_remove):
                    items_to_remove = (
                        list(set(items_to_remove) - set(listdir(root)))
                    )
                    items_to_remove.append(root)
                else:
                    items_to_remove.extend(items_in_root_to_remove)
                    break
            else:
                items_to_remove.extend(items_in_root_to_remove)

        for item_path in items_to_remove:
            self._smart_remove(item_path)

    def make_trash_info_file(self, old_path):
        trashinfo_file = join(
            self.trash_info_location,
            basename(old_path) + INFO_FILE_EXPANSION
        )

        self._trashinfo_config.set(                 # wrap in try catch
            INFO_SECTION, OLD_PATH_OPTION, abspath(old_path)
        )
        self._trashinfo_config.set(
            INFO_SECTION, REMOVE_DATE_OPTION, datetime.today()
        )
        self._trashinfo_config.set(
            INFO_SECTION, FILE_HASH_OPTION, sha256(old_path).hexdigest()
        )

        with open(trashinfo_file, "w") as fp:
                self._trashinfo_config.write(fp)

    def _smart_remove(self, item_path):
        check_trash_and_make_if_not_exist(self.trash_location)

        if self.mover.move(item_path, self.trash_files_location):
            self.make_trash_info_file(item_path)


class AdvancedRemover(object):
    def __init__(
            self, trash_location=expanduser(DEFAULT_TRASH_LOCATION),
            confirm_rm_always=False, not_confirm_rm=False,
            confirm_if_file_has_not_write_access=True,
            dry_run=False,
            solve_samename_files_politic=DEFAULT_SOLVE_SAMENAME_POLITIC
    ):
        # XXX
        if confirm_rm_always:
            confirm_removal = ask_remove
        elif not_confirm_rm:
            confirm_removal = lambda: True
        else:
            confirm_removal = AdvancedRemover._ask_if_file_has_not_write_access

        self.remover = SmartRemover(
            confirm_removal=confirm_removal,
            trash_location=trash_location,
            mover=getattr(mover, solve_samename_files_politic)()
        )

    def remove_list(
            self, paths_to_remove,
            verify_removal=lambda: True
    ):
        for path in paths_to_remove:
            try:
                verify_removal(path)
                self.remover.remove_tree(path)
            except (PermissionError, ExistError, ModeError) as why:
                error(why)

    def remove_files(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            verify_removal=verify_file_removal
        )

    def remove_directories(self, paths_to_remove):
        self.remove_list(
            paths_to_remove,
            verify_removal=verify_directory_removal
        )

    def remove_trees(self, paths_to_remove):
        self.remove_list(paths_to_remove)
