# -*- coding: utf-8 -*-
import errno
import os
import os.path
import shutil
from smart_rm.utils.constants import (
    APP_DIRECTORY
)
from smart_rm.utils.utils import (
    get_correct_path
    get_trash_files_and_info_paths
)
from smart_rm.core.error import (
    AccessError,
    ExistError
)


def make_app_folder_if_not_exist(location=APP_DIRECTORY):
    app = os.path.abspath(os.path.expanduser(location))
    if not os.path.exists(app):
        try:
            os.mkdir(app)
            # shutil.copy(PATH_TO_COPY_DEFAULT_CONFIG, app)
        except (OSError, shutil.Error) as error:
            raise SystemError(error.errno, error.strerror, error.filename)
    # add config


def check_trash_and_make_if_not_exist(trash_location):
    trash = os.path.abspath(os.path.expanduser(trash_location))
    if not os.path.exists(os.path.abspath(trash)):
        try:
            os.mkdir(trash)
            # files, info = get_trash_files_and_info_paths(trash)
            os.mkdir(files)
            os.mkdir(info)
        except OSError as error:
            raise SystemError(error.errno, error.strerror, error.filename)


def check_path_existance(path):

    abs_path = os.path.abspath(path)

    if not os.access(os.path.dirname(abs_path), os.R_OK):
        raise AccessError(
            errno.EACCES, os.strerror(errno.EACCES), os.path.dirname(abs_path)
        )
    elif not os.path.exists(abs_path):
        raise ExistError(errno.ENOENT, os.strerror(errno.ENOENT), abs_path)
