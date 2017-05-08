# -*- coding: utf-8 -*-
import os.path
import shutil
from smart_rm.utils.constants import APP_DIRECTORY
from smart_rm.utils.get import get_trash_files_and_info_paths


def make_app_folder_if_not_exist():
    app = os.path.expanduser(APP_DIRECTORY)
    if not os.path.exists(app):
        try:
            os.mkdir(app)
        except (OSError, shutil.Error) as error:
            raise SystemError(error.errno, error.strerror, error.filename)


def make_trash_if_not_exist(trash_location):
    if not os.path.exists(trash_location):
        try:
            os.mkdir(trash_location)
            files, info = get_trash_files_and_info_paths(trash_location)
            os.mkdir(files)
            os.mkdir(info)
        except OSError as error:
            raise SystemError(error.errno, error.strerror, error.filename)
