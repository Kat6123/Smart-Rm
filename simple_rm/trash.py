# -*- coding: utf-8 -*-
import ConfigParser
import datetime
import errno
import hashlib
import os
import shutil

import simple_rm.clean as clean
import simple_rm.name_conflict as solve
import simple_rm.constants as const
from simple_rm.check import (
    check_cycle,
    check_directory_access,
    check_parent_read_rights,
    check_path_existance,
    check_path_is_directory,
    check_path_is_file,
    check_path_is_not_tree,
    check_special_file,
    check_system_directory,
    get_correct_path,
    get_path_in_trash_info,
    get_path_in_trash,
    get_regex_matcher,
    make_trash_if_not_exist,
    return_true
)
from simple_rm.error import (
    AccessError,
    ExistError,
    ModeError,
    SmartError
)


class TrashInfo(object):
    def __init__(self, path, trash_location):
        self.initial_path = get_correct_path(path)
        self.path_in_trash = get_path_in_trash(path, trash_location)

        self.deletion_date = datetime.datetime.today()
        self.sha256_value = 0
        self.size = 0

        self.errors = []

    def __str__(self):
        return (
            "Real path: {0}\n"
            "Path in trash: {1}\n"
            "Deletion date: {2}\n"
            "Hash value: {3}\n"
            "Size: {4}\n"
            "".format(
                self.initial_path, self.path_in_trash,
                self.deletion_date, self.sha256_value, self.size
            )
        )

    def write_info_with_config(self, file_path, config_parser):
        config_parser.set(                 # wrap in try catch
            const.INFO_SECTION, const.OLD_PATH_OPTION, self.initial_path
        )
        config_parser.set(
            const.INFO_SECTION, const.REMOVE_DATE_OPTION,
            self.deletion_date.strftime(const.DATE_FORMAT)
        )

        self.sha256_value = hashlib.sha256(self.initial_path).hexdigest()
        config_parser.set(
            const.INFO_SECTION, const.FILE_HASH_OPTION, self.sha256_value
        )

        self.size = clean.get_size(self.initial_path)
        config_parser.set(
            const.INFO_SECTION, const.SIZE_OPTION, self.size
        )

        with open(file_path, "w") as fp:
                config_parser.write(fp)

    def read_info_with_config(self, file_path, config_parser):
        config_parser.read(file_path)

        self.initial_path = config_parser.get(
            const.INFO_SECTION, const.OLD_PATH_OPTION
        )
        self.path_in_trash = get_path_in_trash(
            file_path.split(const.INFO_FILE_EXPANSION)[0],
            os.path.dirname(os.path.dirname(file_path))
        )

        self.deletion_date = datetime.datetime.strptime(
            config_parser.get(const.INFO_SECTION, const.REMOVE_DATE_OPTION),
            const.DATE_FORMAT
        )

        self.sha256_value = config_parser.get(
            const.INFO_SECTION, const.FILE_HASH_OPTION
        )

        self.size = config_parser.getint(
            const.INFO_SECTION, const.SIZE_OPTION
        )


class Trash(object):
    def __init__(
        self,
        trash_location=const.TRASH_LOCATION,
        remove_mode=const.REMOVE_FILE_MODE,
        dry_run=False,
        confirm_removal=return_true,
        clean_policy=const.DEFAULT_CLEAN_POLICY,
        clean_parametr=None,
        solve_name_conflict_policy=const.SOLVE_NAME_CONFLICT_POLICY,
        max_size=const.MAX_TRASH_SIZE_IN_BYTES,
        max_time_in_trash=const.MAX_TIME_IN_TRASH
    ):
        self.trash_location = get_correct_path(trash_location)

        if (remove_mode == const.REMOVE_FILE_MODE or
                remove_mode == const.REMOVE_EMPTY_DIRECTORY_MODE or
                remove_mode == const.REMOVE_TREE_MODE):
            self.remove_mode = remove_mode
        else:
            self.remove_mode = const.REMOVE_FILE_MODE

        if callable(confirm_removal):
            self.confirm_removal = confirm_removal
        else:
            self.confirm_removal = return_true

        self.dry_run = dry_run

        self.clean_policy = clean_policy
        self.clean_parametr = clean_parametr

        self.conflict_policy = solve_name_conflict_policy

        self.max_size = max_size
        self.max_time_in_trash = max_time_in_trash

        self._trashinfo_config = ConfigParser.ConfigParser()
        self._trashinfo_config.add_section(const.INFO_SECTION)

    def remove(self, paths_to_remove, regex=None):
        make_trash_if_not_exist(self.trash_location)
        # self._time_clean_automatically()            # XXX ?

        result_info_objects = []
        regex_matcher = return_true
        if regex:
            regex_matcher = get_regex_matcher(regex)

        for path in paths_to_remove:
            path_info_object = TrashInfo(path, self.trash_location)
            correct_path = path_info_object.initial_path
            try:
                self._run_remove_checks(correct_path, self.trash_location)
            except SmartError as error:
                path_info_object.errors.append(error)
                result_info_objects.append(path_info_object)
                continue

            items_to_remove = self._get_paths_to_remove_from_tree(
                correct_path, regex_matcher
            )

            for item in items_to_remove:
                if item == correct_path:
                    info_object = path_info_object
                else:
                    info_object = TrashInfo(item, self.trash_location)

                try:            # XXX
                    self._run_access_checks(
                        info_object.initial_path,
                        self.trash_location
                    )
                except SmartError as error:
                    info_object.errors.append(error)
                    result_info_objects.append(path_info_object)
                    continue

                if not self.dry_run:
                    make_trash_if_not_exist(self.trash_location)
                    if check_path_existance(info_object.path_in_trash):
                        method_to_solve = getattr(solve, self.conflict_policy)
                        method_to_solve(info_object)

                    # future_size = self.max_size - info_object.size
                    # self.clean(
                    #     clean_policy="size_time",
                    #     clean_parametr=future_size
                    # )
                    # if (clean.get_size(self.trash_location) + info_object.size
                    #         > self.max_size):
                    #     info_object.errors.append(
                    #         SystemError("File is too large")
                    #     )

                    if not info_object.errors:
                        self._smart_remove(info_object)

                # result_info_objects.append(path_info_object)
                result_info_objects.append(info_object)

        return result_info_objects

    def restore(self, paths_to_restore):
        self._time_clean_automatically()
        result_info_objects = []                # regex?

        for path in paths_to_restore:
            path_in_trash = os.path.join(
                self.trash_location, const.TRASH_FILES_DIRECTORY, path
            )
            path_in_info = os.path.join(
                self.trash_location, const.TRASH_INFO_DIRECTORY,
                path + const.INFO_FILE_EXPANSION
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

                if not self.dry_run:
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
            self.trash_location, const.TRASH_INFO_DIRECTORY
        )

        for path in os.listdir(trashinfo_path):         # XXX
            info_object = TrashInfo("", self.trash_location)

            info_object.read_info_with_config(
                os.path.join(trashinfo_path, path), self._trashinfo_config
            )
            # Add try catch
            result.append(info_object)

        return result

    def clean(self, clean_policy=None, clean_parametr=None):
        if not clean_policy:
            clean_policy = self.clean_policy
        if not clean_parametr:
            clean_parametr = self.clean_parametr
        objects_in_trash = self.view()
        try:
            get_remove_objects_function = getattr(
                clean,
                const.CLEAN_POLICY_TEMPLATE.format(clean_policy)
            )
            valid_clean_parametr = getattr(
                clean,
                const.CLEAN_POLICY_VALIDATION_TEMPLATE.format(clean_policy)
            )(clean_parametr)
        except AttributeError:
            get_remove_objects_function = getattr(
                clean, const.CLEAN_POLICY_TEMPLATE.format(
                    const.DEFAULT_CLEAN_POLICY
                )
            )
            valid_clean_parametr = getattr(
                clean,
                const.CLEAN_POLICY_VALIDATION_TEMPLATE.format(
                    const.DEFAULT_CLEAN_POLICY
                )
            )(clean_parametr)

        objects_for_remove = get_remove_objects_function(
            objects_in_trash, valid_clean_parametr
        )
        if not self.dry_run:
            for obj in objects_in_trash:
                clean.permanent_remove(obj, self.trash_location)

        return objects_for_remove

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

        if (self.remove_mode == const.REMOVE_FILE_MODE and
                not check_path_is_file(source)):
                raise ModeError(
                    errno.EISDIR, os.strerror(errno.EISDIR), source
                )
        elif (self.remove_mode == const.REMOVE_EMPTY_DIRECTORY_MODE and
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

    def _get_paths_to_remove_from_tree(self, correct_path, regex_matcher):
        if (os.path.isfile(correct_path) and
                regex_matcher(correct_path) and
                self.confirm_removal(correct_path)):
            return [correct_path]

        items_to_remove = []

        for root, dirs, files in os.walk(correct_path, topdown=False):
            for file_path in files:
                if (regex_matcher(file_path) and
                        self.confirm_removal(file_path)):
                    abs_path = os.path.join(root, os.path.basename(file_path))
                    items_to_remove.append(abs_path)

            if regex_matcher(root) and self.confirm_removal(root):
                root_inners = [
                    os.path.join(root, file_path) for
                    file_path in os.listdir(root)
                ]

                if len(root_inners) == 0:
                    items_to_remove.append(root)
                elif (set(root_inners).issubset(items_to_remove)):
                    items_to_remove = list(
                        set(items_to_remove) - set(root_inners)
                    )
                    items_to_remove.append(root)

        return items_to_remove

    def _smart_remove(self, info_object):
        try:
            trashinfo_path = get_path_in_trash_info(
                info_object.path_in_trash, self.trash_location
            )
            info_object.write_info_with_config(
                trashinfo_path, self._trashinfo_config
            )
            shutil.move(
                info_object.initial_path,
                info_object.path_in_trash
            )
        except (shutil.Error, OSError) as error:
            info_object.errors.append(
                SystemError(error.errno, error.strerror, error.filename)
            )

    def _time_clean_automatically(self):
        self.clean(clean_policy="time", clean_parametr=self.max_time_in_trash)

    def _size_clean_automatically(self):
        self.clean(clean_policy="size_time", clean_parametr=self.max_size)
