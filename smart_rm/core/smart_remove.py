# -*- coding: utf-8 -*-
import datetime
import errno
import ConfigParser
import logging
import os
import os.path
import hashlib
from smart_rm.politics import name_conflicts
from smart_rm.core.mover import Mover
from smart_rm.core.error import (
    AccessError,
    ExistError,
    ModeError
)
from smart_rm.utils import (
    ask_remove,
    ask_if_file_has_not_write_access,
    default_true,
    get_trash_files_and_info_paths,
    get_regex_matcher,
    get_correct_path,
    check_trash_and_make_if_not_exist,
    verify_file_removal,
    verify_directory_removal,
    check_path_existance
)
from smart_rm.utils.constants import (
    TRASH_LOCATION,
    SM_REMOVE_SOLVE_NAME_CONFLICT,
    FILE_HASH_OPTION,
    INFO_FILE_EXPANSION,
    INFO_SECTION,
    OLD_PATH_OPTION,
    REMOVE_DATE_OPTION,
)


class SmartRemover(object):
    def __init__(
            self,
            trash_location=TRASH_LOCATION,
            confirm_removal=lambda: True,
            mover=None,
            is_relevant_file_name=lambda: True
    ):
        self.trash_location = get_correct_path(trash_location)
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
            self.remove_file_or_empty_directory(tree)
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
                    abs_path = os.path.join(root, os.path.basename(file))
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

    def make_trash_info_file(self, old_path, path_in_trash):
        trashinfo_file = os.path.join(
            os.path.expanduser(self.trash_info_location),
            os.path.basename(path_in_trash) + INFO_FILE_EXPANSION
        )

        self._trashinfo_config.set(                 # wrap in try catch
            INFO_SECTION, OLD_PATH_OPTION, os.path.abspath(old_path)
        )
        self._trashinfo_config.set(
            INFO_SECTION, REMOVE_DATE_OPTION, datetime.datetime.today()
        )
        self._trashinfo_config.set(
            INFO_SECTION, FILE_HASH_OPTION,
            hashlib.sha256(path_in_trash).hexdigest()
        )

        with open(trashinfo_file, "w") as fp:
                self._trashinfo_config.write(fp)

    def _smart_remove(self, item_path):
        check_trash_and_make_if_not_exist(self.trash_location)

        item_path_in_trash = self.mover.move(
            item_path, self.trash_files_location
        )

        if item_path_in_trash:
            self.make_trash_info_file(item_path, item_path_in_trash)


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
            confirm_removal=confirm_removal,
            trash_location=trash_location,
            mover=getattr(name_conflicts, solve_samename_files_politic)(),
            is_relevant_file_name=matcher
        )

    def remove_list(
            self, paths_to_remove,
            verify_removal=lambda: True
    ):
        for path in paths_to_remove:
            try:
                check_path_existance(os.path.abspath(path))
                verify_removal(os.path.abspath(path))
                self.remover.remove_tree(path)
            except (AccessError, ExistError, ModeError) as error:
                logging.error(error)

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
