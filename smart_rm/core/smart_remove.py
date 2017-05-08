# -*- coding: utf-8 -*-
import ConfigParser
import errno
import logging
import os
import os.path

from datetime import datetime
from hashlib import sha256

from smart_rm.politics import name_conflicts
from smart_rm.core.mover import Mover
from smart_rm.core.error import (
    AccessError,
    ExistError,
    ModeError,
    SystemError
)
from smart_rm.utils import (
    ask_if_file_has_not_write_access,
    ask_remove,
    make_trash_if_not_exist,
    default_true,
    get_correct_path,
    get_regex_matcher,
    get_trash_files_and_info_paths
)
from smart_rm.utils.constants import (
    FILE_HASH_OPTION,
    INFO_FILE_EXPANSION,
    INFO_SECTION,
    OLD_PATH_OPTION,
    REMOVE_DATE_OPTION,
    SM_REMOVE_SOLVE_NAME_CONFLICT,
    TRASH_LOCATION,
)


class TrashInfo(object):
    def __init__(self, trash_info_location):
        self.trashinfo_config = ConfigParser.ConfigParser()
        self.trashinfo_config.add_section(INFO_SECTION)

        self.trash_info_location = trash_info_location

        # self.trashinfo_config.set(INFO_SECTION, OLD_PATH_OPTION)
        # self.trashinfo_config.set(INFO_SECTION, REMOVE_DATE_OPTION)
        # self.trashinfo_config.set(INFO_SECTION, FILE_HASH_OPTION)

    def write(self, old_path, path_in_trash):
        trashinfo_file = os.path.join(
            self.trash_info_location,
            os.path.basename(path_in_trash) + INFO_FILE_EXPANSION
        )

        self.trashinfo_config.set(                 # wrap in try catch
            INFO_SECTION, OLD_PATH_OPTION, os.path.abspath(old_path)
        )
        self.trashinfo_config.set(
            INFO_SECTION, REMOVE_DATE_OPTION, datetime.today()
        )
        self.trashinfo_config.set(
            INFO_SECTION, FILE_HASH_OPTION,
            sha256(path_in_trash).hexdigest()
        )

        with open(trashinfo_file, "w") as fp:
                self.trashinfo_config.write(fp)

    def read(self, path_in_trash):
        trashinfo_file = os.path.join(
            self.trash_info_location,
            path_in_trash + INFO_FILE_EXPANSION
        )

        self.trashinfo_config.read(trashinfo_file)

        old_path = self.trashinfo_config.get(INFO_SECTION, OLD_PATH_OPTION)

        date = self.trashinfo_config.get(INFO_SECTION, REMOVE_DATE_OPTION)

        hash = self.trashinfo_config.get(INFO_SECTION, FILE_HASH_OPTION)

        return old_path, date, hash


class SmartRemover(object):
    def __init__(
            self,
            trash_location=TRASH_LOCATION,
            confirm_removal=default_true,
            is_relevant_file_name=default_true,
            mover=None,
    ):
        self.trash_location = get_correct_path(trash_location)
        self.trash_files_location, trash_info_location = (
            get_trash_files_and_info_paths(self.trash_location)
        )

        if mover is None:
            self.mover = Mover()
        else:
            self.mover = mover

        self.confirm_removal = confirm_removal
        self.is_relevant_file_name = is_relevant_file_name

        self.info_writer = TrashInfo(trash_info_location)

    def remove_file(self, file_path):
        correct_file_path = get_correct_path(file_path)

        if not os.path.isdir(correct_file_path):
            if (self.is_relevant_file_name(correct_file_path) and
                    self.confirm_removal(correct_file_path)):
                        self._smart_remove(correct_file_path)
        else:
            raise ModeError(
                errno.EISDIR, os.strerror(errno.EISDIR), correct_file_path
            )

    def remove_directory(self, directory_path):
        correct_directory_path = get_correct_path(directory_path)

        if (os.path.isdir(correct_directory_path) and
                os.listdir(correct_directory_path)):
            raise ModeError(
                errno.ENOTEMPTY,
                os.strerror(errno.ENOTEMPTY), correct_directory_path
            )

        self._smart_remove(correct_directory_path)

    def remove_tree(self, tree_path):
        correct_tree_path = get_correct_path(tree_path)

        if os.path.isfile(correct_tree_path):
            self.remove_file(correct_tree_path)
            return

        items_to_remove = []

        for root, dirs, files in os.walk(correct_tree_path, topdown=False):
            items_in_root_to_remove = []

            for file_path in files:
                if (self.is_relevant_file_name(file_path) and
                        self.confirm_removal(file_path)):
                    abs_path = os.path.join(root, os.path.basename(file_path))
                    items_in_root_to_remove.append(abs_path)

            if self.is_relevant_file_name(root) and self.confirm_removal(root):
                root_inners = [
                    os.path.join(root, file_path) for
                    file_path in os.listdir(root)
                ]

                if (set(root_inners).issubset(items_in_root_to_remove)):
                    items_to_remove = list(
                        set(items_to_remove) - set(root_inners)
                    )
                    items_to_remove.append(root)
                else:
                    items_to_remove.extend(items_in_root_to_remove)
                    break
            else:
                items_to_remove.extend(items_in_root_to_remove)

        for item_path in items_to_remove:
            self._smart_remove(item_path)

    def _smart_remove(self, item_path):
        make_trash_if_not_exist(self.trash_location)

        item_path_in_trash = self.mover.move(
            item_path, self.trash_files_location
        )

        if item_path_in_trash:
            self.info_writer.write(item_path, item_path_in_trash)


class AdvancedRemover(object):
    def __init__(
            self, trash_location=TRASH_LOCATION,
            confirm_rm=False, not_confirm_rm=False,
            confirm_rm_if_no_write_access=True,
            dry_run=False,
            solve_samename_files_politic=SM_REMOVE_SOLVE_NAME_CONFLICT,
            regex=None
    ):

        if confirm_rm:
            confirm_removal = ask_remove
        elif not_confirm_rm:
            confirm_removal = default_true
        else:
            confirm_removal = ask_if_file_has_not_write_access

        matcher = default_true
        if regex:
            matcher = get_regex_matcher(regex)

        self.remover = SmartRemover(
            trash_location=trash_location,
            confirm_removal=confirm_removal,
            mover=getattr(
                name_conflicts, solve_samename_files_politic)(dry_run=dry_run),
            is_relevant_file_name=matcher
        )

    def _remove_list(
            self, paths_to_remove, remove_method
    ):
        for path in paths_to_remove:
            try:
                if os.path.exists(get_correct_path(path)):
                    remove_method(path)
                else:
                    raise ExistError(
                        errno.ENOENT, os.strerror(errno.ENOENT), path
                    )
            except (AccessError, ExistError, ModeError, SystemError) as error:
                logging.error(error)

    def remove_files(self, paths_to_remove):
        self._remove_list(
            paths_to_remove,
            remove_method=self.remover.remove_file
        )

    def remove_directories(self, paths_to_remove):
        self._remove_list(
            paths_to_remove,
            remove_method=self.remover.remove_directory
        )

    def remove_trees(self, paths_to_remove):
        self._remove_list(
            paths_to_remove,
            remove_method=self.remover.remove_tree
        )
