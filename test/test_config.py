#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os.path
import argparse
from unittest import (
    TestCase,
    main
)

import simple_rm.constants as const
from simple_rm.config import (
    set_parser_for_remove,
    set_parser_for_trash,
    set_parser_with_common_flags
)


class TestConfig(TestCase):
    def test_set_parser_for_remove(self):
        parser = argparse.ArgumentParser()

        set_parser_for_remove(parser)

        nmsp = parser.parse_args(["path"])
        self.assertListEqual(nmsp.path, ["path"])
        nmsp = parser.parse_args(["path", "hello", "bonjure"])
        self.assertListEqual(nmsp.path, ["path", "hello", "bonjure"])

        self.assertFalse(nmsp.rm_empty_directory)
        nmsp = parser.parse_args(["-d", "path"])
        self.assertTrue(nmsp.rm_empty_directory)
        nmsp = parser.parse_args(["--dir", "path"])
        self.assertTrue(nmsp.rm_empty_directory)

        self.assertFalse(nmsp.rm_directory_recursively)
        nmsp = parser.parse_args(["-r", "path"])
        self.assertTrue(nmsp.rm_directory_recursively)
        nmsp = parser.parse_args(["--recursive", "path"])
        self.assertTrue(nmsp.rm_directory_recursively)

        self.assertFalse(nmsp.ask_before_remove)
        nmsp = parser.parse_args(["-i", "path"])
        self.assertTrue(nmsp.ask_before_remove)
        nmsp = parser.parse_args(["--interactive", "path"])
        self.assertTrue(nmsp.ask_before_remove)

        self.assertFalse(nmsp.force_remove)
        nmsp = parser.parse_args(["-f", "path"])
        self.assertTrue(nmsp.force_remove)
        nmsp = parser.parse_args(["--force", "path"])
        self.assertTrue(nmsp.force_remove)

        self.assertIsNone(nmsp.regex)
        nmsp = parser.parse_args(["--regex", "regex", "path"])
        self.assertEqual(nmsp.regex, "regex")

    def test_set_parser_for_trash(self):
        parser = argparse.ArgumentParser()

        set_parser_for_trash(parser)

        nmsp = parser.parse_args([])
        self.assertFalse(nmsp.clear_trash)
        self.assertFalse(nmsp.view_trash_content)
        self.assertIsNone(nmsp.restore_from_trash)

        nmsp = parser.parse_args(["--clear"])
        self.assertTrue(nmsp.clear_trash)

        nmsp = parser.parse_args(["--content"])
        self.assertTrue(nmsp.view_trash_content)

        nmsp = parser.parse_args(["--restore", "file1", "file2"])
        self.assertListEqual(nmsp.restore_from_trash, ["file1", "file2"])

    def test_set_parser_with_common_flags(self):
        parser = argparse.ArgumentParser()

        set_parser_with_common_flags(parser)

        nmsp = parser.parse_args([])
        self.assertIsNone(nmsp.log_level)
        self.assertIsNone(nmsp.log_file_path)
        self.assertIsNone(nmsp.config_file_path)
        self.assertFalse(nmsp.silent_mode)
        self.assertFalse(nmsp.imitation)
        self.assertFalse(nmsp.verbose)

        nmsp = parser.parse_args(
            ["--config", "path_to_conf",
             "--log", "path_to_log",
             "--log_level", "info"]
        )

        self.assertListEqual(
            [nmsp.config_file_path, nmsp.log_file_path, nmsp.log_level],
            ["path_to_conf", "path_to_log", "info"]
        )

        nmsp = parser.parse_args(["-s", "-v"])
        self.assertTrue(nmsp.silent_mode)
        self.assertTrue(nmsp.verbose)

        nmsp = parser.parse_args(["--silent", "--verbose", "--dry_run"])
        self.assertTrue(nmsp.silent_mode)
        self.assertTrue(nmsp.verbose)
        self.assertTrue(nmsp.imitation)


if __name__ == '__main__':
    main()
