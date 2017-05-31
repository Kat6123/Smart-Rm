# -*- coding: utf-8 -*-
import os
import shutil

import test.constants as const


def create_test_dir():
    os.mkdir(const.TEST_DIR)


def remove_test_dir():
    os.chmod(const.TEST_DIR, 0777)

    for root, dirs, files in os.walk(const.TEST_DIR):
        for file_path in files:
            os.chmod(os.path.join(root, file_path), 0777)

        for dir_path in dirs:
            os.chmod(os.path.join(root, dir_path), 0777)
    shutil.rmtree(const.TEST_DIR)


def create_file_in_dir(file_name, dir_path):
    path = os.path.join(dir_path, file_name)
    with open(path, "w"):
        pass

    return path


def create_dir_in_dir(dir_name, dir_path):
    path = os.path.join(dir_path, dir_name)
    os.mkdir(path)

    return path


def create_tree_in_dir(tree_name, dir_path):
    path = create_dir_in_dir(tree_name, dir_path)
    create_file_in_dir("file", path)
    create_dir_in_dir("dir", path)

    return path


def create_file(file_name):
    return create_file_in_dir(file_name, const.TEST_DIR)


def create_empty_directory(directory_name):
    return create_dir_in_dir(directory_name, const.TEST_DIR)


def create_tree(tree_name):
    return create_tree_in_dir(tree_name, const.TEST_DIR)
