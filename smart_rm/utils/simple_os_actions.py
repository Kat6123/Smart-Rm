# -*- coding: utf-8 -*-
import logging
import os
import os.path
import shutil

from smart_rm.core.error import SystemError


def remove_file(path):
    try:
        os.remove(path)
    except OSError as error:
        raise SystemError(error.errno, error.strerror, error.filename)


def remove_dir(path):
    try:
        os.rmdir(path)
    except OSError as error:
        raise SystemError(error.errno, error.strerror, error.filename)


def remove_tree(path):
    try:
        shutil.rmtree(path)
    except (shutil.Error, OSError) as error:
        raise SystemError(error)


def remove_link(path):
    try:
        os.unlink(path)
    except OSError as error:
        raise SystemError(error.errno, error.strerror, error.filename)


def remove_directory_content(directory):
    content = os.path.listdir(directory)
    for path in content:
        abs_path = os.path.join(directory, path)
        if os.path.islink(abs_path):
            remove_link(abs_path)
        elif os.path.isfile(abs_path):
            remove_file(abs_path)
        else:
            os.path.remove_tree(abs_path)


def move_tree(src, dst):
    logging.info("Try move {0} to {1}".format(src, dst))

    try:
        shutil.move(src, dst)
    except (shutil.Error, OSError) as error:
        raise SystemError(error.errno, error.strerror, error.filename)

    logging.info("Moved")
