# -*- coding: utf-8 -*-
from os import (
    remove,
    rmdir,
    listdir,
    unlink
)
from os.path import (
    join,
    islink,
    isfile
)
from shutil import (
    rmtree,
    move,
    Error
)
from error import OtherOSError


def remove_file(path):
    try:
        remove(path)
    except OSError as why:
        raise OtherOSError(why.errno, why.strerror, why.filename)


def remove_dir(path):
    try:
        rmdir(path)
    except OSError as why:
        raise OtherOSError(why.errno, why.strerror, why.filename)


def remove_tree(path):
    try:
        rmtree(path)
    except Error as why:
        raise OtherOSError(why)


def remove_link(path):
    try:
        unlink(path)
    except OSError as why:
        raise OtherOSError(why.errno, why.strerror, why.filename)


def remove_directory_content(directory):
    content = listdir(directory)
    for path in content:
        abs_path = join(directory, path)
        if islink(abs_path):
            remove_link(abs_path)
        elif isfile(abs_path):
            remove_file(abs_path)
        else:
            remove_tree(abs_path)


def move_tree(src, dst):
    try:
        move(src, dst)
    except Error as why:
        raise OtherOSError(why.errno, why.strerror, why.filename)
