# -*- coding: utf-8 -*-
from os import (
    mkdir,
)
from os.path import (
    expanduser,
    exists,
    join,
    abspath
)
from ConfigParser import ConfigParser
from remove import (
    remove_directory_content,
    remove_file
)
from error import OtherOSError
# from logging import (
#     error,
#     warning
# )
import mover

TRASH_FILES_DIRECTORY = "files"            # is it bad?
TRASH_INFO_DIRECTORY = "info"
INFO_SECTION = "Trash info"
OLD_PATH_OPTION = "Path"
REMOVE_DATE_OPTION = "Date"
FILE_HASH_OPTION = "Hash"
INFO_FILE_EXPANSION = ".trashinfo"
DEFAULT_TRASH_LOCATION = "~/.local/share/trash"


def get_trash_files_and_info_paths(trash_location):
    return (
        join(trash_location, TRASH_FILES_DIRECTORY),
        join(trash_location, TRASH_INFO_DIRECTORY)
    )


def check_trash_and_make_if_not_exist(trash_location):
    if not exists(abspath(trash_location)):
        try:
            mkdir(trash_location)
            files, info = get_trash_files_and_info_paths(trash_location)
            mkdir(files)
            mkdir(info)
        except OSError as why:
            raise OtherOSError(why.errno, why.strerror, why.filename)


class TrashCan(object):
    def __init__(
        self,
        trash_location=expanduser(DEFAULT_TRASH_LOCATION),
        mover=None
    ):
        self.trash_files_location, self.trash_info_location = (
            get_trash_files_and_info_paths(trash_location)
        )

        if mover is None:
            self.mover = mover.Mover()
        else:
            self.mover = mover

        self._trashinfo_config = ConfigParser()
        self._trashinfo_config.add_section(INFO_SECTION)

    def restore_from_trash(self, item_path):
        item_path_in_files = join(self.trash_files_location, item_path)
        item_path_in_info = join(
            self.trash_info_location, item_path + INFO_FILE_EXPANSION
        )

        restore_path = self._get_restore_path_from_trashinfo_files(
            item_path_in_info
        )       # XXX check trash?

        if self.mover.move(item_path_in_files, restore_path):
            remove_file(item_path_in_info)      # else some warning

    def _get_restore_path_from_trashinfo_files(self, trashinfo_file):
        self._trashinfo_config.read(trashinfo_file)     # add try catch

        return self._trashinfo_config.get(INFO_SECTION, OLD_PATH_OPTION)

    def _check_hash(self):
        pass

    def clear_trash(files_location, info_location):
        remove_directory_content(files_location)
        remove_directory_content(info_location)

    def view_content(self):
        # call("less {0}".format(self.trash_location))
        pass


class AdvancedTrashCan(object):
    def __init__(
        self,
        trash_location=expanduser(DEFAULT_TRASH_LOCATION),
        # clean_trash_politic="",
        check_hash=False,
        # dry_run=False
    ):

        self.trash = TrashCan(
            trash_location=trash_location
        )

    def clean(self):
        pass

    def move_file_to_trash(self, file):
        self.trash.move_to_trash(file)

    def restore_files(self, paths):
        self.trash.restore_file(paths)

    def view_content(self):
        self.trash.view_content()
