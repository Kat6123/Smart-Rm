#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import errno
import simple_rm.constants as const
from unittest import (
    TestCase,
    main,
    skip
)

import simple_rm.error as errors
from simple_rm.trash import Trash
from test.use_os import (
    create_file_in_dir,
    create_dir_in_dir,
    create_tree_in_dir,
    create_file_dir_tree_in_directory,
    create_empty_directory,
    names_for_trash_files_info_in_dir,
    create_test_dir,
    remove_test_dir
)
from simple_rm.check import (
    get_correct_path,
    return_true
)


class TestTrash(TestCase):
    @classmethod
    def setUpClass(cls):
        create_test_dir()

    @classmethod
    def tearDownClass(cls):
        remove_test_dir()
        # pass

    def test_init(self):
        trash_location = "trash_loc"
        tr = Trash(trash_location=trash_location)
        self.assertEqual(tr.trash_location, get_correct_path(trash_location))

        tr = Trash(remove_mode="abracadabra")
        self.assertEqual(tr.remove_mode, const.REMOVE_FILE_MODE)

        for mode in ("file", "directory", "tree"):
            tr = Trash(remove_mode=mode)
            self.assertEqual(tr.remove_mode, mode)

        for dry_run in (True, False):
            tr = Trash(dry_run=dry_run)
            self.assertEqual(tr.dry_run, dry_run)

        confirm_removal = "str"
        tr = Trash(confirm_removal=confirm_removal)
        self.assertEqual(tr.confirm_removal, return_true)

        callable_object = TestTrash
        confirm_removal = callable_object
        tr = Trash(confirm_removal=confirm_removal)
        self.assertEqual(tr.confirm_removal, confirm_removal)

    def test_remove_file_mode(self):
        test_dir = create_empty_directory("file_mode")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )

        trash_loc, files, info = names_for_trash_files_info_in_dir(test_dir)

        trash = Trash(trash_loc, remove_mode=const.REMOVE_FILE_MODE)

        removed = trash.remove([file_path, dir_path, tree_path])

        self.assertFalse(os.path.exists(file_path))
        self.assertTrue(os.path.exists(removed[0].path_in_trash))

        for num in xrange(1, 3):
            self.assertTrue(os.path.exists(removed[num].initial_path))
            self.assertFalse(os.path.exists(removed[num].path_in_trash))
            with self.assertRaises(errors.ModeError) as info:
                for error in removed[num].errors:
                    raise error
            ex = info.exception
            self.assertEqual(ex.errno, errno.EISDIR)

    def test_remove_directory_mode(self):
        test_dir = create_empty_directory("dir_mode")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )

        trash_loc, files, info = names_for_trash_files_info_in_dir(test_dir)

        trash = Trash(
            trash_loc, remove_mode=const.REMOVE_EMPTY_DIRECTORY_MODE,
            )

        removed = trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 2):
            self.assertFalse(os.path.exists(removed[num].initial_path))
            self.assertTrue(os.path.exists(removed[num].path_in_trash))

        self.assertTrue(os.path.exists(tree_path))
        self.assertFalse(os.path.exists(removed[2].path_in_trash))
        with self.assertRaises(errors.ModeError) as info:
            for error in removed[2].errors:
                raise error
        ex = info.exception
        self.assertEqual(ex.errno, errno.ENOTEMPTY)

    def test_remove_tree_mode(self):
        test_dir = create_empty_directory("tree_mode")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        trash_loc, files, info = names_for_trash_files_info_in_dir(test_dir)

        trash = Trash(trash_loc, remove_mode=const.REMOVE_TREE_MODE)

        removed = trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 3):
            self.assertFalse(os.path.exists(removed[num].initial_path))
            self.assertTrue(os.path.exists(removed[num].path_in_trash))

    def test_remove_list(self):
        test_dir = create_empty_directory("list")
        files = []
        directories = []
        trees = []

        for num in xrange(0, 3):
            files.append(create_file_in_dir("file{0}".format(num),  test_dir))
            directories.append(
                create_dir_in_dir("dir{0}".format(num), test_dir)
            )
            trees.append(create_tree_in_dir("tree{0}".format(num), test_dir))

        trash_loc, fl, info = names_for_trash_files_info_in_dir(test_dir)

        trash = Trash(trash_loc, remove_mode=const.REMOVE_FILE_MODE)

        removed_files = trash.remove(files)

        trash.remove_mode = const.REMOVE_EMPTY_DIRECTORY_MODE
        removed_directories = trash.remove(directories)

        trash.remove_mode = const.REMOVE_TREE_MODE
        removed_trees = trash.remove(trees)

        file_list = [removed_files, removed_directories, removed_trees]
        for lt in file_list:
            for num in xrange(0, 3):
                self.assertFalse(os.path.exists(lt[num].initial_path))
                self.assertTrue(os.path.exists(lt[num].path_in_trash))


if __name__ == '__main__':
    main()
