# -*- coding: utf-8 -*-
import datetime
import errno
import ConfigParser
import os
import os.path
import hashlib
from smart_rm.core import (
    AccessError,
    ExistError,
    ModeError
)
from smart_rm.utils import (
    DEFAULT_TRASH_LOCATION,
    FILE_HASH_OPTION,
    INFO_FILE_EXPANSION,
    INFO_SECTION,
    OLD_PATH_OPTION,
    REMOVE_DATE_OPTION
)


class SmartRemover(object):
    def __init__(
            self,
            trash_location=DEFAULT_TRASH_LOCATION,
            confirm_removal=lambda: True,
            mover=None,
            is_relevant_file_name=lambda: True
    ):
        self.trash_location = trash_location
        self.trash_files_location, self.trash_info_location = (
            get_trash_files_and_info_paths(trash_location)
        )

        if mover is None:
            self.mover = Mover()
        else:
            self.mover = mover

        self.confirm_removal = confirm_removal
        self.is_relevant_file_name = is_relevant_file_name

        self._trashinfo_config = ConfigParser.ConfigParser()
        self._trashinfo_config.add_section(INFO_SECTION)

    def remove_file_or_empty_directory(self, item_path):
        if os.path.isdir(item_path) and os.path.os.path.listdir(item_path):
            raise ModeError(
                errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY), item_path
            )

        if self.is_relevant_file_name(
            item_path
        ) and self.confirm_removal(
            item_path
        ):              # TODO: if path has changed? what about hash
            self._smart_remove(item_path)

    def remove_tree(self, tree):
        if os.path.isfile(tree):
            self.remove(tree)
            return

        items_to_remove = []

        for root, dirs, files in os.walk(tree, topdown=False):
            items_in_root_to_remove = []
            root = os.path.abspath(root)

            for file_path in files:
                if self.is_relevant_file_name(
                    file_path
                ) and self.confirm_removal(
                    file_path
                ):
                    abs_path = os.path.join(root, basename(file))
                    items_in_root_to_remove.append(abs_path)

            if self.is_relevant_file_name(root) and self.confirm_removal(root):
                if (
                    set(os.path.os.path.listdir(
                        root)).issubset(items_to_remove)):
                    items_to_remove = (
                        list(set(items_to_remove) - set(os.path.listdir(root)))
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
        trashinfo_file = os.path.join(
            self.trash_info_location,
            basename(old_path) + INFO_FILE_EXPANSION
        )

        self._trashinfo_config.set(                 # wrap in try catch
            INFO_SECTION, OLD_PATH_OPTION, os.path.abspath(old_path)
        )
        self._trashinfo_config.set(
            INFO_SECTION, REMOVE_DATE_OPTION, datetime..today()
        )
        self._trashinfo_config.set(
            INFO_SECTION, FILE_HASH_OPTION,
            hashlib.sha256(old_path).hexdigest()
        )

        with open(trashinfo_file, "w") as fp:
                self._trashinfo_config.write(fp)

    def _smart_remove(self, item_path):
        check_trash_and_make_if_not_exist(self.trash_location)

        if self.mover.move(item_path, self.trash_files_location):
            self.make_trash_info_file(item_path)


class AdvancedRemover(object):
    def __init__(
            self, trash_location=DEFAULT_TRASH_LOCATION,
            confirm_rm=False, not_confirm_rm=False,
            confirm_rm_if_no_write_access=True,
            dry_run=False,
            solve_samename_files_politic=DEFAULT_SOLVE_SAMENAME_POLITIC
    ):
        # XXX
        if confirm_rm:
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
            except (AccessError, ExistError, ModeError) as error:
                error(error)

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
