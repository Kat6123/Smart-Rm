# -*- coding: utf-8 -*-
import ConfigParser
import errno
import hashlib
import os
import shutil
from datetime import datetime

from simple_rm.constants import *
from simple_rm.check import *
from simple_rm.error import *


class TrashInfo(object):
    def __init__(self, path, trash_location):
        self.initial_path = get_correct_path(path)
        self.path_in_trash = get_path_in_trash(path, trash_location)

        self.deletion_date = datetime.today()
        self.sha256_value = hashlib.sha256(path).hexdigest()

        self.errors = []

    def __str__(self):
        return (
            "Real path: {0}\n"
            "Path in trash: {1}\n"
            "Deletion date: {2}\n"
            "Hash value: {3}\n"
            "Errors {4}\n"
            "".format(
                self.initial_path, self.path_in_trash,
                self.deletion_date, self.sha256_value,
                "\n".join([str(error) for error in self.errors])
            )
        )

    def write_info_with_config(self, file_path, config_parser):
        config_parser.set(                 # wrap in try catch
            INFO_SECTION, OLD_PATH_OPTION, self.initial_path
        )
        config_parser.set(
            INFO_SECTION, REMOVE_DATE_OPTION, self.deletion_date
        )
        config_parser.set(
            INFO_SECTION, FILE_HASH_OPTION, self.sha256_value
        )

        with open(file_path, "w") as fp:
                config_parser.write(fp)

    def read_info_with_config(self, file_path, config_parser):
        config_parser.read(file_path)

        self.initial_path = config_parser.get(INFO_SECTION, OLD_PATH_OPTION)
        self.path_in_trash = get_path_in_trash(
            file_path, os.path.dirname(os.path.dirname(file_path))
        )

        self.deletion_date = config_parser.get(
            INFO_SECTION, REMOVE_DATE_OPTION
        )

        self.sha256_value = config_parser.get(INFO_SECTION, FILE_HASH_OPTION)


class Trash(object):
    def __init__(
        self,
        trash_location=TRASH_LOCATION,
        remove_mode=REMOVE_FILE_MODE,
        regex=None,
        dry_run=False,
        confirm_removal=lambda x: True
    ):
        self.trash_location = get_correct_path(trash_location)

        if (remove_mode == REMOVE_FILE_MODE or
                remove_mode == REMOVE_EMPTY_DIRECTORY_MODE or
                remove_mode == REMOVE_TREE_MODE):
            self.remove_mode = remove_mode
        else:
            self.remove_mode = REMOVE_FILE_MODE

        self.clean_policy = ""
        self.conflict_name_policy = ""
        self.confirm_removal = confirm_removal
        self.dry_run = dry_run

        if regex:
            self._regex_matcher = get_regex_matcher(regex)
        else:
            self._regex_matcher = lambda x: True

        self._trashinfo_config = ConfigParser.ConfigParser()
        self._trashinfo_config.add_section(INFO_SECTION)

    def setup(self):
        pass

    def remove(self, paths_to_remove):          # What about generator
        result_info_objects = []                # regex?

        for path in paths_to_remove:
            path_info_object = TrashInfo(path, self.trash_location)
            correct_path = path_info_object.initial_path

            try:
                self._run_remove_checks(correct_path, self.trash_location)
            except SmartError as error:
                path_info_object.errors.append(error)
                result_info_objects.append(path_info_object)
                continue            # ? Need to?

            items_to_remove = self._get_paths_to_remove_from_tree(correct_path)

            for item in items_to_remove:
                if item == correct_path:
                    info_object = path_info_object
                else:
                    info_object = TrashInfo(item, self.trash_location)

                if not self.dry_run:
                    self._smart_remove(info_object)

                result_info_objects.append(path_info_object)

        return result_info_objects

    def restore(self, paths_to_restore):
        result_info_objects = []                # regex?

        for path in paths_to_restore:
            path_in_trash = os.path.join(
                self.trash_location, TRASH_FILES_DIRECTORY, path
            )
            path_in_info = os.path.join(
                self.trash_location, TRASH_INFO_DIRECTORY,
                path + INFO_FILE_EXPANSION
            )

            path_info_object = TrashInfo("", self.trash_location)
            path_info_object.path_in_trash = path_in_trash

            try:
                if not check_path_existance(path_in_trash):
                    raise ExistError(
                        errno.ENOENT, os.strerror(errno.ENOENT), path_in_trash
                    )
                self._run_access_checks(path_in_trash, self.trash_location)
            except SmartError as error:
                path_info_object.errors.append(error)
                result_info_objects.append(path_info_object)
                continue

            make_trash_if_not_exist(self.trash_location)
            try:
                path_info_object.read_info_with_config(
                    path_in_info, self._trashinfo_config
                )

                shutil.move(
                    path_in_trash,
                    os.path.dirname(path_info_object.initial_path)
                )
                os.remove(path_in_info)
            except (shutil.Error, OSError) as error:
                path_info_object.errors.append(
                    SystemError(error.errno, error.strerror, error.filename)
                )

            result_info_objects.append(path_info_object)

        return result_info_objects

    def view(self):
        result = []
        make_trash_if_not_exist(self.trash_location)

        trashinfo_path = os.path.join(
            self.trash_location, TRASH_INFO_DIRECTORY
        )

        for path in os.listdir(trashinfo_path):         # XXX
            info_object = TrashInfo("", self.trash_location)

            info_object.read_info_with_config(
                os.path.join(trashinfo_path, path), self._trashinfo_config
            )
            # Add try catch
            result.append(info_object)

        return result

    def clean(self):
        pass

    def _run_access_checks(self, source, destination):
        if not check_path_is_directory(destination):
            raise SystemError(
                "Distance \"{0}\" is not directory"
                "".format(os.path.basename(destination))
            )

        for path in (os.path.dirname(source), destination):
            if not check_directory_access(path):
                raise AccessError(
                    errno.EACCES, os.strerror(errno.EACCES), path
                )

    def _run_remove_checks(self, source, destination):
        for path in (source, destination):
            if not check_parent_read_rights(path):
                raise AccessError(
                    errno.EACCES, os.strerror(errno.EACCES),
                    os.path.dirname(path)
                )

            if not check_path_existance(path):
                raise ExistError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        if (self.remove_mode == REMOVE_FILE_MODE and
                not check_path_is_file(source)):
                raise ModeError(
                    errno.EISDIR, os.strerror(errno.EISDIR), source
                )
        elif (self.remove_mode == REMOVE_EMPTY_DIRECTORY_MODE and
                not check_path_is_not_tree(source)):
            raise ModeError(
                errno.ENOTEMPTY,
                os.strerror(errno.ENOTEMPTY), source
            )

        if os.path.isfile(source) and not check_special_file(source):
            raise AccessError(
                errno.EACCES, "Not regular file", source
            )
        elif os.path.isdir(source) and not check_system_directory(source):
            raise AccessError(
                errno.EACCES, "System directory", source
            )

        if not check_cycle(source, destination):
            raise SystemError(
                "Cannot move \"{0}\" into itself \"{1}\""
                "".format(source, destination)
            )       # Add check same name exists

    def _get_paths_to_remove_from_tree(self, correct_path):
        if (os.path.isfile(correct_path) and
                self._regex_matcher(correct_path) and
                self.confirm_removal(correct_path)):
            return [correct_path]

        items_to_remove = []

        for root, dirs, files in os.walk(correct_path, topdown=False):
            items_in_root_to_remove = []

            for file_path in files:
                if (self._regex_matcher(file_path) and
                        self.confirm_removal(file_path)):
                    abs_path = os.path.join(root, os.path.basename(file_path))
                    items_in_root_to_remove.append(abs_path)

            if self._regex_matcher(root) and self.confirm_removal(root):
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

        return items_to_remove

    def _smart_remove(self, info_object):
        try:
            self._run_access_checks(
                info_object.initial_path,
                self.trash_location
            )
        except SmartError as error:
            path_info_object.errors.append(error)
            return

        make_trash_if_not_exist(self.trash_location)
        try:
            trashinfo_path = get_path_in_trash_info(
                info_object.initial_path, self.trash_location
            )
            info_object.write_info_with_config(
                trashinfo_path, self._trashinfo_config
            )

            shutil.move(
                info_object.initial_path,
                os.path.dirname(info_object.path_in_trash)
            )
        except (shutil.Error, OSError) as error:
            info_object.errors.append(
                SystemError(error.errno, error.strerror, error.filename)
            )
