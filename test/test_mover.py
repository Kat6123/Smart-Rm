# -*- coding: utf-8 -*-
import os
import os.path
import shutil
from unittest import (
    TestCase,
    main,
    skip
)
from smart_rm.core.mover import Mover
from smart_rm.core.error import SystemError


class TestSpecialChecksMixin(object):   # ? Need tests for mover separate fun
    method = None
    test_dir = "smart_rm_test_directory"
    directory = "directory"
    @classmethod
    def setUpClass(cls):
        os.mkdir(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_check_path_existance(self):
        directory
        simple_file = "file"

        open(simple_file, "w").close()
        open(os.path.join(self.test_dir, simple_file), "w").close()


class TestMoverMethods(TestSpecialChecksMixin, TestCase):
    def setUp(self):
        self.mover = Mover()

    def tearDown(self):
        del self.mover

    def test():
        pass
    # @skip
    # def test_tune_paths(self):
    #     source = "source"
    #     destination = "destination"
    #
    #     self.mover.tune_paths(source, destination)
    #     self.assertEqual(self.mover.source, os.path.abspath(source))
    #     self.assertEqual(self.mover.destination, os.path.abspath(destination))
    #     self.assertEqual(
    #         self.mover.final_path,
    #         os.path.join(self.mover.destination, os.path.basename(source))
    #     )
    #
    # @skip
    # def test_check_distance_is_directory(self):
    #     self.mover.tune_paths("source", __file__)
    #     with self.assertRaisesRegexp(
    #         SystemError,
    #         "{0}".format(os.path.basename(self.mover.destination))
    #     ):
    #         self.mover.check_distance_is_directory()
    #
    # @skip
    # def test_check_cycle(self):
    #     self.mover.tune_paths(os.path.pardir, os.path.curdir)
    #     with self.assertRaisesRegexp(
    #         SystemError,
    #         "{0}.+{1}".format(self.mover.source, self.mover.destination)
    #     ):
    #         self.mover.check_cycle()
    #
    # def test_empty_space(self):
    #     pass


if __name__ == '__main__':
    main()
