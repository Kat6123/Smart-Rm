# -*- coding: utf-8 -*-
import os.path
from unittest import (
    TestCase,
    main
)
from smart_rm.mover import Mover
from smart_rm.error import OtherOSError


class TestMoverCheckMethods(TestCase):
    def setUp(self):
        self.mover = Mover()

    def tearDown(self):
        del self.mover

    def test_tune_paths(self):
        source = "source"
        destination = "destination"

        self.mover.tune_paths(source, destination)
        self.assertEqual(self.mover.source, os.path.abspath(source))
        self.assertEqual(self.mover.destination, os.path.abspath(destination))
        self.assertEqual(
            self.mover.final_path,
            os.path.join(self.mover.destination, os.path.basename(source))
        )

    def test_check_distance_is_directory(self):
        self.mover.tune_paths("source", __file__)
        with self.assertRaisesRegexp(
            OtherOSError,
            "{0}".format(os.path.basename(self.mover.destination))
        ):
            self.mover.check_distance_is_directory()

    def test_check_cycle(self):
        self.mover.tune_paths(os.path.pardir, os.path.curdir)
        with self.assertRaisesRegexp(
            OtherOSError,
            "{0}.+{1}".format(self.mover.source, self.mover.destination)
        ):
            self.mover.check_cycle()

    def test_empty_space(self):
        pass


if __name__ == '__main__':
    main()
