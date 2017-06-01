#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
from unittest import (
    TestCase,
    main
)

import simple_rm.constants as const
from simple_rm.wrapper import (
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
            self.config.path_to["trash"],
            trash.trash_location
        )

        self.assertEqual(
            self.config.remove["aim"],
            trash.remove_mode
        )

        self.assertEqual(self.config.dry_run, trash.dry_run)

        self.config.remove["mode"] = const.INTERACTIVE_MODE
        trash = init_trash_by_config(self.config)
        self.assertEqual(ask_remove, trash.confirm_removal)

        self.config.remove["mode"] = const.FORCE_MODE
        trash = init_trash_by_config(self.config)
        test_paths = ["abracadabra", "alalala",
                      __file__, os.path.basename(__file__)]
        for path in test_paths:
            self.assertTrue(trash.confirm_removal(path))

        # (
        #     self.config.remove["mode"]=
        #     const.PAY_ATTENTION_IF_NOT_WRITE_ACCESS_MODE
        # )
        # trash = init_trash_by_config(self.config)
        # self.assertEqual(
        #     ask_if_file_has_not_write_access,
        #     trash.confirm_removal
        # )


if __name__ == '__main__':
    main()
