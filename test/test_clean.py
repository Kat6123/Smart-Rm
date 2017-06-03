#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import subprocess

from unittest import (
    TestCase,
    main
)

import simple_rm.constants as const
from simple_rm.clean import permanent_remove
from test.test_trash import TestTrashMixin
from test.use_os import (
    create_empty_directory,
    create_file_dir_tree_in_directory
)


class TestClean(TestTrashMixin, TestCase):
    def test_permanent_remove(self):
        directory = create_empty_directory("permanent")
        file_path, dir_path, tree_path = (
            create_file_dir_tree_in_directory(directory)
        )

        self.trash.remove_mode = "tree"
        removed = self.trash.remove([file_path, dir_path, tree_path])

        for rm in removed:
            print self.info
            print os.path.basename(
                rm.initial_path
            ) + const.INFO_FILE_EXPANSION
            info_path = os.path.join(
                self.info,
                os.path.basename(rm.initial_path) + const.INFO_FILE_EXPANSION
            )
            permanent_remove(rm, self.trash_loc)

            self.assertFalse(os.path.exists(rm.initial_path))
            self.assertFalse(os.path.exists(rm.path_in_trash))
            self.assertFalse(os.path.exists(info_path))


if __name__ == '__main__':
    main()
