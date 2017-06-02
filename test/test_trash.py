#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import errno
import stat
import simple_rm.constants as const
from unittest import (
    TestCase,
    main
)

import test.constants as test_const
import simple_rm.error as errors
from simple_rm.check import get_regex_matcher
from simple_rm.trash import Trash
from test.use_os import (
    create_dir_in_dir,
    create_empty_directory,
    create_file_dir_tree_in_directory,
    create_file_in_dir,
    create_test_dir,
    create_tree_in_dir,
    names_for_trash_files_info_in_dir,
    remove_test_dir,
    remove_dir
)


class TestTrashMixin(object):
    @classmethod
    def setUpClass(cls):
        create_test_dir()

    @classmethod
    def tearDownClass(cls):
        remove_test_dir()

    def setUp(self):
        names = names_for_trash_files_info_in_dir(test_const.TEST_DIR)
        self.trash_loc, self.files, self.info = names

        self.trash = Trash(self.trash_loc)

    def tearDown(self):
        if os.path.exists(self.trash_loc):
            remove_dir(self.trash_loc)
        del self.trash, self.files, self.info, self.trash_loc


class TestTrash(TestTrashMixin, TestCase):
    def test_restore(self):
        test_dir = create_empty_directory("restore")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        info_paths = []

        for path in (file_path, dir_path, tree_path):
            info_paths.append(
                os.path.join(
                    self.info,
                    os.path.basename(path) + const.INFO_FILE_EXPANSION
                )
            )

        self.trash.remove_mode = const.REMOVE_TREE_MODE

        removed = self.trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 3):
            res = self.trash.restore(
                [os.path.basename(removed[num].path_in_trash)]
            )

            self.assertFalse(os.path.exists(removed[num].path_in_trash))
            self.assertFalse(os.path.exists(info_paths[num]))

            self.assertTrue(os.path.exists(removed[num].initial_path))

    def test_dry_run_restore(self):
        test_dir = create_empty_directory("dry_run")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        info_paths = []

        for path in (file_path, dir_path, tree_path):
            info_paths.append(
                os.path.join(
                    self.info,
                    os.path.basename(path) + const.INFO_FILE_EXPANSION
                )
            )

        self.trash.remove_mode = const.REMOVE_TREE_MODE

        removed = self.trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 3):
            self.trash.dry_run = True

            res = self.trash.restore(
                [os.path.basename(removed[num].path_in_trash)]
            )

            self.assertTrue(os.path.exists(removed[num].path_in_trash))
            self.assertTrue(os.path.exists(info_paths[num]))

            self.assertFalse(os.path.exists(removed[num].initial_path))
            self.assertListEqual(removed[num].errors, [])

            self.trash.dry_run = False

            res = self.trash.restore(
                [os.path.basename(removed[num].path_in_trash)]
            )

            self.assertFalse(os.path.exists(removed[num].path_in_trash))
            self.assertFalse(os.path.exists(info_paths[num]))

            self.assertTrue(os.path.exists(removed[num].initial_path))

    def test_restore_list_return(self):
        num = 8
        paths = []
        for n in xrange(num):
            paths.append(str(n))

        self.assertEqual(len(self.trash.restore(paths)), num)

    def test_restore_path_existance(self):
        num = 8
        paths = []
        for n in xrange(num):
            paths.append(str(n))

        for rm in self.trash.restore(paths):
            with self.assertRaises(errors.ExistError) as info:
                for err in rm.errors:
                    raise err
            ex = info.exception
            self.assertEqual(ex.errno, errno.ENOENT)

    def test_view(self):
        test_dir = create_empty_directory("view")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        result = []

        self.assertEqual(len(self.trash.view()), 0)

        self.trash.remove_mode = const.REMOVE_TREE_MODE

        for path in os.listdir(self.info):
            info_object = TrashInfo("", self.trash_location)

            info_object.read_info_with_config(
                os.path.join(seld.info, path), self._trashinfo_config
            )

            result.append(info_object)

        for res_obj, view_obj in zip(result, self.trash.view()):
            self.assertDictEqual(res_obj.__dict__, view_obj.__dict__)

    def test_clean_remove_all_policy(self):
        self.trash.clean_policy = "remove_all"

        test_dir = create_empty_directory("clean")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )

        self.trash.remove([file_path, dir_path, tree_path])

        self.assertNotEqual(len(os.listdir(self.files)), 0)
        self.assertNotEqual(len(os.listdir(self.info)), 0)

        self.trash.clean(clean_policy="remove_all")
        self.assertEqual(len(os.listdir(self.files)), 0)
        self.assertEqual(len(os.listdir(self.info)), 0)


if __name__ == '__main__':
    main()
