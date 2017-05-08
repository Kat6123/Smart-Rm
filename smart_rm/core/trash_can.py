# -*- coding: utf-8 -*-
import os.path
import subprocess

from smart_rm.politics import name_conflicts
# from smart_rm.politics import clean
from smart_rm.core.mover import Mover
from smart_rm.core.smart_remove import TrashInfo
from smart_rm.utils import (
    SM_REMOVE_SOLVE_NAME_CONFLICT,
    TRASH_LOCATION,
    INFO_FILE_EXPANSION,
    get_trash_files_and_info_paths,
    remove_directory_content,
    remove_file,
    get_correct_path,
    make_trash_if_not_exist
)


class TrashCan(object):
    def __init__(
        self,
        trash_location=TRASH_LOCATION,
        mover=None
    ):
        self.trash_location = get_correct_path(trash_location)
        self.trash_files_location, self.trash_info_location = (
            get_trash_files_and_info_paths(self.trash_location)
        )

        if mover is None:
            self.mover = Mover()
        else:
            self.mover = mover

        self.info_reader = TrashInfo(self.trash_info_location)

    def restore(self, item_path):
        make_trash_if_not_exist(self.trash_info_location)

        path_basename = os.path.basename(item_path)

        restore_path = self.info_reader.read(path_basename)[0]

        if self.mover.move(
            os.path.join(self.trash_files_location, path_basename),
            os.path.dirname(restore_path)
        ):
            remove_file(
                os.path.join(
                    self.trash_info_location, path_basename
                    + INFO_FILE_EXPANSION
                )
            )

    def _check_hash(self):
        pass

    def clear_trash(self):
        remove_directory_content(self.trash_files_location)
        remove_directory_content(self.trash_info_location)

    def view_content(self):
        subprocess.call(["ls", self.trash_location])


class AdvancedTrashCan(object):
    def __init__(
        self,
        trash_location=TRASH_LOCATION,
        # clean_trash_politic="",
        check_hash=False,
        dry_run=False,
        solve_samename_files_politic=SM_REMOVE_SOLVE_NAME_CONFLICT
    ):

        self.trash = TrashCan(
            trash_location=trash_location,
            mover=getattr(
                name_conflicts, solve_samename_files_politic)(dry_run=dry_run),
            # cleaner=getattr(
            #     name_conflicts, solve_samename_files_politic)(dry_run=dry_ru
        )

    def clean(self):
        self.trash.clear_trash()

    def restore_files(self, paths):
        for path in paths:
            self.trash.restore(path)

    def view_content(self):
        self.trash.view_content()
