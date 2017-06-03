#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
from unittest import (
    TestCase,
    main
)

import simple_rm.constants as const
from simple_rm.wrapper import (
    ask_not_write_access_file,
    init_trash_by_config,
    ask_remove
)
from simple_rm.config import Config


class TestWrapperFunctions(TestCase):
    def setUp(self):
        self.config = Config()

    def tearDown(self):
        del self.config

    def test_init_trash_by_config(self):
        trash = init_trash_by_config(self.config)

        self.assertEqual(
            self.config.remove["aim"],
            trash.remove_mode
        )

        self.config.remove["mode"] = const.INTERACTIVE_MODE
        trash = init_trash_by_config(self.config)
        self.assertEqual(ask_remove, trash.confirm_removal)

        self.config.remove["mode"] = const.FORCE_MODE
        trash = init_trash_by_config(self.config)
        self.assertTrue(lambda x: True, trash.confirm_removal)

        self.config.remove["mode"] = const.ATTENTION_IF_NOT_WRITE_ACCESS_MODE
        trash = init_trash_by_config(self.config)
        self.assertEqual(
            ask_not_write_access_file,
            trash.confirm_removal
        )

        self.assertEqual(self.config.settings["dry_run"], trash.dry_run)

        self.assertEqual(
            self.config.policies["solve_name_conflict"], trash.conflict_policy
        )

        self.assertEqual(
            self.config.policies["clean"], trash.clean_policy
        )
        self.assertEqual(
            self.config.policies["clean_parametr"], trash.clean_parametr
        )


if __name__ == '__main__':
    main()
