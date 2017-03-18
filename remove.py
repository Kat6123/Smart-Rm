# -*- coding: utf-8 -*-
from error import error
from os import remove
from os import rmdir
from os import listdir
from os import mkdir
from os.path import expanduser
from os.path import exists
from os.path import join
from shutil import rmtree
from shutil import move

try:
    BUCKET = expanduser('~/.local/share/bucket/')   # check /
    FILES = join(BUCKET, 'files/')
    INFO = join(BUCKET, 'info/')
except OSError as e:
    raise error(e)


def check_bucket():                 # TODO: check inner folders
    try:
        if not(exists(BUCKET)):
            mkdir(BUCKET)
            mkdir(FILES)
            mkdir(INFO)
    except OSError as e:
        raise error(e)


def rm_file(path):
    try:
        remove(path)
    except OSError as e:
        raise error(e)


def rm_dir(path):
    try:
        rmdir(path)
    except OSError as e:
        raise error(e)


def rm_tree(path):
    try:
        rmtree(path)
    except OSError as e:
        raise error(e)


def rmb(src):
    check_bucket()                          # TODO: IOError, Error; write info
    try:
        move(src, FILES)
    except OSError as e:
        raise error(e)
    except IOError as e:
        raise error(e)


def show_bucket():
    check_bucket()                  # Or in main

    files = listdir(FILES)          # try?
    for i in files:
        print i
