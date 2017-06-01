#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os.path
import datetime
from unittest import (
    TestCase,
    main
)

import simple_rm.constants as const
from simple_rm.trash import (
    TrashInfo,
    Trash
)
from simple_rm.check import (
    get_correct_path,
    return_true
)


class TestInitializeMethods(TestCase):
    paths = [
        "~/foo//./moo/../ooo",
        __file__
    ]

    def test_trash_info_init(self):
        trash_location = "/home/user/.local"

        for path in TestInitializeMethods.paths:
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

            self.assertEqual(info.sha256_value, 0)
            self.assertEqual(info.size, 0)

            self.assertListEqual(info.errors, [])

    def test_trash_init(self):
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

        callable_object = callable
        confirm_removal = callable_object
        tr = Trash(confirm_removal=confirm_removal)
        self.assertEqual(tr.confirm_removal, confirm_removal)


if __name__ == '__main__':
    main()
