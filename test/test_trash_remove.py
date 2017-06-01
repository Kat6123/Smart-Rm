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


class TestTrash(TestCase):
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

    def test_remove_file_mode(self):
        test_dir = create_empty_directory("file_mode")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )

        self.trash.remove_mode = const.REMOVE_FILE_MODE

        removed = self.trash.remove([file_path, dir_path, tree_path])

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
        self.trash.remove_mode = const.REMOVE_EMPTY_DIRECTORY_MODE
        removed = self.trash.remove([file_path, dir_path, tree_path])

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
        self.trash.remove_mode = const.REMOVE_TREE_MODE

        removed = self.trash.remove([file_path, dir_path, tree_path])

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

        self.trash.remove_mode = const.REMOVE_FILE_MODE

        removed_files = self.trash.remove(files)

        self.trash.remove_mode = const.REMOVE_EMPTY_DIRECTORY_MODE
        removed_directories = self.trash.remove(directories)

        self.trash.remove_mode = const.REMOVE_TREE_MODE
        removed_trees = self.trash.remove(trees)

        file_list = [removed_files, removed_directories, removed_trees]
        for lt in file_list:
            for num in xrange(0, 3):
                self.assertFalse(os.path.exists(lt[num].initial_path))
                self.assertTrue(os.path.exists(lt[num].path_in_trash))

    def test_dry_run_mode(self):
        test_dir = create_empty_directory("dry_run")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        trash_loc, files, info = names_for_trash_files_info_in_dir(test_dir)

        trash = Trash(
            trash_loc, remove_mode=const.REMOVE_TREE_MODE, dry_run=True)

        removed = trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 3):
            self.assertTrue(os.path.exists(removed[num].initial_path))
            self.assertFalse(os.path.exists(removed[num].path_in_trash))

        trash.dry_run = False
        removed = trash.remove([file_path, dir_path, tree_path])

        for num in xrange(0, 3):
            self.assertFalse(os.path.exists(removed[num].initial_path))
            self.assertTrue(os.path.exists(removed[num].path_in_trash))

    def test_info_creating(self):
        test_dir = create_empty_directory("info_creating")
        file_path, dir_path, tree_path = create_file_dir_tree_in_directory(
            test_dir
        )
        test_paths = []
        trash_loc, files, info = names_for_trash_files_info_in_dir(test_dir)
        for path in (file_path, dir_path, tree_path):
            test_paths.append(
                os.path.join(
                    info, os.path.basename(path) + const.INFO_FILE_EXPANSION
                )
            )

        trash = Trash(trash_loc, remove_mode=const.REMOVE_TREE_MODE)

        for path in test_paths:
            self.assertFalse(os.path.exists(path))

        trash.remove([file_path, dir_path, tree_path])

        for path in test_paths:
            self.assertTrue(os.path.exists(path))

    def test_file_not_exist(self):
        file_path = "file_not_exist"

        removed = self.trash.remove([file_path])
        with self.assertRaises(errors.ExistError) as info:
            for error in removed[0].errors:
                raise error
        ex = info.exception
        self.assertEqual(ex.errno, errno.ENOENT)

    def test_parent_read_rights(self):
        parent_directory = create_empty_directory("parent_dir")

        r_file = create_file_in_dir("file_parent_right", parent_directory)
        no_r_file = create_file_in_dir("file_no_par_right", parent_directory)

        read_wright_execute_all = 0777
        no_read_wright_execute_all = 0333

        os.chmod(parent_directory, read_wright_execute_all)
        rm = self.trash.remove([r_file])
        self.assertFalse(os.path.exists(rm[0].initial_path))
        self.assertTrue(os.path.exists(rm[0].path_in_trash))

        os.chmod(parent_directory, no_read_wright_execute_all)
        rm = self.trash.remove([no_r_file])
        with self.assertRaises(errors.AccessError) as info:
            for error in rm[0].errors:
                raise error
        ex = info.exception
        self.assertEqual(ex.errno, errno.EACCES)

    def test_check_cycle(self):
        self.trash.remove_mode = const.REMOVE_TREE_MODE
        rm = self.trash.remove([self.trash_loc])
        with self.assertRaises(errors.SysError):
            for error in rm[0].errors:
                raise error

    def test_remove_special_file(self):
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

        removed = self.trash.remove(paths)
        for rm in removed:
            with self.assertRaises(errors.AccessError) as info:
                for error in rm[0].errors:
                    raise error
            ex = info.exception
            self.assertTrue(ex.errno, errno.EACCES)

    def test_remove_system_directory(self):
        special_directories = [
            os.path.join(const.ROOT, root_inner) for root_inner in os.listdir(
                const.ROOT
            )
        ] + [const.ROOT]

        self.trash.remove_mode = const.REMOVE_TREE_MODE
        removed = self.trash.remove(special_directories)
        for rm in removed:
            with self.assertRaises(errors.AccessError) as info:
                for error in rm.errors:
                    raise error
            ex = info.exception
            self.assertTrue(ex.errno, errno.EACCES)

    def test_file_regex(self):
        regex_dir = create_empty_directory("regex")
        file_template = "file.*"
        file_names = [
            "file.py",
            "file$",
            "file$$",
            "file1231321",
            r"\file1",
            "abracadabra",
            "lalal"
        ]

        file_re = get_regex_matcher(file_template)
        regex_paths = []
        file_paths = []

        for name in file_names:
            path = create_file_in_dir(name, regex_dir)
            file_paths.append(path)
            if file_re(name):
                regex_paths.append(os.path.abspath(path))

        removed = self.trash.remove(file_paths, regex=file_template)
        for rm in removed:
            self.assertIn(rm.initial_path, regex_paths)

    def test_dir_regex(self):
        regex_dir = create_empty_directory("regex_dir")
        dir_template = ".+dir123"
        dir_names = [
            "dir123",
            "ajdhadir123",
            "asjdhsjdir123skjfhkds",
            r"$$$$$dir123",
            "$$dir123",
            "abr"
        ]

        dir_re = get_regex_matcher(dir_template)
        regex_paths = []
        dir_paths = []

        for name in dir_names:
            path = create_dir_in_dir(name, regex_dir)
            dir_paths.append(path)
            if dir_re(name):
                regex_paths.append(os.path.abspath(path))

        self.trash.remove_mode = const.REMOVE_EMPTY_DIRECTORY_MODE
        removed = self.trash.remove(dir_paths, regex=dir_template)
        for rm in removed:
            self.assertIn(rm.initial_path, regex_paths)

    def test_all_tree_elem_match_regex(self):
        regex_dir = create_empty_directory("regex_tree_dir")
        all_tree_elem_match_regex_template = r"\d*tree.*"
        all_tree_elem_match_regex = create_dir_in_dir(
            "121212treeadadas", regex_dir
        )
        create_file_in_dir("436757treejhj", all_tree_elem_match_regex)
        create_file_in_dir("566887treekjhkj", all_tree_elem_match_regex)
        dir_in_all_tree_elem_match_regex = create_dir_in_dir(
            "767868treeoj9", all_tree_elem_match_regex
        )
        create_file_in_dir("12treeadad", dir_in_all_tree_elem_match_regex)

        self.trash.remove_mode = const.REMOVE_TREE_MODE
        res = self.trash.remove(
            [all_tree_elem_match_regex],
            regex=all_tree_elem_match_regex_template
        )
        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0].initial_path, os.path.abspath(all_tree_elem_match_regex)
        )

    def test_tree_match_rehex_partially(self):
        regex_dir = create_empty_directory("regex_tree_part")
        paths = []
        regex_paths = []
        tree_template = r"4+part.*"
        matcher = get_regex_matcher(tree_template)

        tree = create_dir_in_dir(
            "444part098765", regex_dir
        )
        file1_in_tree = create_file_in_dir("444partads", tree)
        file2_in_tree = create_file_in_dir("partkasjd", tree)
        dir_in_tree = create_dir_in_dir(
            "hello", tree
        )
        file_in_dir_tree = create_file_in_dir("4444parthello", dir_in_tree)
        paths = [
            tree, file1_in_tree, file2_in_tree,
            dir_in_tree, file_in_dir_tree
        ]
        for path in paths:
            if matcher(path):
                regex_paths.append(os.path.abspath(path))

        self.trash.remove_mode = const.REMOVE_TREE_MODE
        result = self.trash.remove(
            [tree],
            regex=tree_template
        )
        for res in result:
            self.assertIn(res.initial_path, regex_paths)


if __name__ == '__main__':
    main()
