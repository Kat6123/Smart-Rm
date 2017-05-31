#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import hashlib
import os.path
import datetime

from unittest import (
    TestCase,
    main
)
from simple_rm.trash import TrashInfo


class TestTrashInfo(TestCase):
    paths = [
        "~/foo//./moo/../ooo",
        __file__
    ]

    def test_init(self):
        trash_location = "/home/user/.local"

        for path in TestTrashInfo.paths:
            info = TrashInfo(path, trash_location)

            correct_path = os.path.abspath(os.path.expanduser(path))
            self.assertEqual(info.initial_path, correct_path)

            path_in_trash = os.path.join(
                trash_location, "files", os.path.basename(correct_path)
            )
            self.assertEqual(info.path_in_trash, path_in_trash)

            deletion_date = datetime.datetime.today()
            self.assertEqual(info.deletion_date.date(), deletion_date.date())
            self.assertListEqual(
                [
                    info.deletion_date.date(),
                    info.deletion_date.hour, info.deletion_date.minute
                ],
                [
                    deletion_date.date(),
                    deletion_date.hour, deletion_date.minute
                ]
            )

            sha256_value = hashlib.sha256(correct_path).hexdigest()
            self.assertEqual(info.sha256_value, sha256_value)

            self.assertListEqual(info.errors, [])


if __name__ == '__main__':
    main()
