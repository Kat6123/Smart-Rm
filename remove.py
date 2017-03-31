# -*- coding: utf-8 -*-
from error import Error
from os import (
    remove,
    rmdir
)

from shutil import rmtree


def rm_file(path):
    try:
        remove(path)
    except OSError as e:
        raise Error(e)


def rm_dir(path):
    try:
        rmdir(path)
    except OSError as e:
        raise Error(e)


def rm_tree(path):
    try:
        rmtree(path)
    except OSError as e:
        raise Error(e)
