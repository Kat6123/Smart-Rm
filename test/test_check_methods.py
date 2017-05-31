# -*- coding: utf-8 -*-
import os
import os.path
import stat
import shutil

import simple_rm.constants as const
import test.constants as test_const
from unittest import (
    TestCase,
    main
)
from simple_rm.check import (
    check_cycle,
    check_directory_access,
    check_parent_read_rights,
    check_path_existance,
    check_path_is_file,
    check_path_is_not_tree,
    check_special_file,
    check_system_directory,
    create_not_exist_file,
    make_trash_if_not_exist,
    return_true
)
from test.use_os import (
    create_dir_in_dir,
    create_empty_directory,
    create_file_in_dir,
    create_test_dir,
    remove_test_dir
)


def set_rights(rights):
    def inner():
        if rights == "root":
            return 0
        else:
            return 1
    return inner


class TestChecksWithoutOS(TestCase):
    def test_check_cycle(self):
        destination = "/home/user/.local/trash/"

        no_cycle = "/home/user/.local/trash/files"
        self.assertTrue(check_cycle(no_cycle, destination))

        cycle = "/home/user/.local/"
        self.assertFalse(check_cycle(cycle, destination))

    def test_check_path_is_file(self):
        path_to_file = __file__
        path_to_directory = os.path.dirname(path_to_file)

        self.assertTrue(check_path_is_file(path_to_file))
        self.assertFalse(check_path_is_file(path_to_directory))

    def test_check_path_existance(self):
        path_exists = __file__
        strange_path = "/lala/lala/lala/lala/laala/lalla/alal"

        self.assertTrue(check_path_existance(path_exists))
        self.assertFalse(check_path_existance(strange_path))


class TestChecksWithOS(TestCase):
    @classmethod
    def setUpClass(cls):
        create_test_dir()

    @classmethod
    def tearDownClass(cls):
        remove_test_dir()

    def test_check_path_is_not_tree(self):
        empty_directory = create_empty_directory("empty_dir")

        self.assertTrue(check_path_is_not_tree(empty_directory))
        self.assertTrue(check_path_is_not_tree(__file__))
        self.assertFalse(check_path_is_not_tree(os.path.dirname(__file__)))

    def test_check_directory_access(self):
        access_directory = create_empty_directory("acces_dir")

        read_wright_execute_all = 0777
        read_wright_no_execute_all = 0666
        read_no_wright_execute_all = 0555
        read_no_wright_no_execute_all = 0444
        no_read_wright_execute_all = 0333

        os.chmod(access_directory, read_wright_execute_all)
        self.assertTrue(check_directory_access(access_directory))

        os.chmod(access_directory, read_wright_no_execute_all)
        self.assertFalse(check_directory_access(access_directory))

        os.chmod(access_directory, read_no_wright_execute_all)
        self.assertFalse(check_directory_access(access_directory))

        os.chmod(access_directory, read_no_wright_no_execute_all)
        self.assertFalse(check_directory_access(access_directory))

        os.chmod(access_directory, no_read_wright_execute_all)
        self.assertTrue(check_directory_access(access_directory))

    def test_check_parent_read_rights(self):
        parent_directory = create_empty_directory("parent_dir")

        read_wright_execute_all = 0777
        no_read_wright_execute_all = 0333

        test_paths = []

        empty_dir = create_dir_in_dir("empty", parent_directory)
        test_paths.append(empty_dir)

        file_in_dir = create_file_in_dir("file", parent_directory)
        test_paths.append(file_in_dir)

        tree_dir = create_dir_in_dir("tree", parent_directory)
        file_in_tree = create_file_in_dir("file", tree_dir)
        test_paths.append(tree_dir)
        os.chmod(tree_dir, read_wright_execute_all)

        for path in test_paths:
            os.chmod(parent_directory, read_wright_execute_all)
            self.assertTrue(check_parent_read_rights(path))

            os.chmod(parent_directory, no_read_wright_execute_all)
            self.assertFalse(check_parent_read_rights(path))

        os.chmod(parent_directory, read_wright_execute_all)
        self.assertTrue(check_parent_read_rights(file_in_tree))

        os.chmod(parent_directory, no_read_wright_execute_all)
        self.assertTrue(check_parent_read_rights(file_in_tree))

    def test_check_special_directory(self):
        special_directories = [
            os.path.join(const.ROOT, root_inner) for root_inner in os.listdir(
                const.ROOT
            )
        ] + [const.ROOT]

        os.getuid = set_rights("root")
        for directory in special_directories:
            self.assertTrue(check_system_directory(directory))

        os.path.ismount = return_true
        self.assertTrue(check_system_directory("strange_path"))

        os.getuid = set_rights("not_root")
        for directory in special_directories:
            self.assertFalse(check_system_directory(directory))

        os.path.ismount = return_true
        self.assertFalse(check_system_directory("strange_path"))

    def test_check_special_file(self):
        special_names = ["fifo", "socket"]
        special_modes = [
            stat.S_IFIFO,
            stat.S_IFSOCK
        ]
        paths = []

        for num in xrange(len(special_modes)):
            path = os.path.join(
                test_const.TEST_DIR, special_names[num]
            )
            os.mknod(path, special_modes[num])
            paths.append(path)

        os.getuid = set_rights("root")
        for path in paths:
            self.assertTrue(check_special_file(path))
        self.assertTrue(check_special_file(__file__))

        os.getuid = set_rights("not_root")
        for path in paths:
            self.assertFalse(check_special_file(path))
        self.assertTrue(check_special_file(__file__))

    def test_create_if_not_exist(self):
        test_path = create_empty_directory("create")

        if os.path.exists(test_path):
            shutil.rmtree(test_path)

        self.assertFalse(os.path.exists(test_path))
        create_not_exist_file(test_path)
        self.assertTrue(os.path.exists(test_path))

    def test_make_trash_if_not_exist(self):
        trash = create_empty_directory("trash_loc")

        make_trash_if_not_exist(trash)
        self.assertTrue(os.path.exists(trash))

        self.assertTrue(os.path.exists(
            os.path.join(trash, const.TRASH_FILES_DIRECTORY)))

        self.assertTrue(os.path.exists(
            os.path.join(trash, const.TRASH_INFO_DIRECTORY)))


if __name__ == '__main__':
    main()
