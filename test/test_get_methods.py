# -*- coding: utf-8 -*-
import os.path
import re
from unittest import (
    TestCase,
    main
)
import simple_rm.constants as const
from simple_rm.check import (
    get_correct_path,
    get_path_in_trash_info,
    get_path_in_trash,
    get_regex_matcher,
    get_trash_files_and_info_paths
)


class TestGetMethods(TestCase):
    paths = [
        "~/foo//./moo/../ooo",
        __file__,
        "file.py",
        "file$",
        "file$$",
        "file1231321",
        r"\file1"
    ]

    regex = [
        ".*",
        "file*",
        ".*$",
        r"\.*"
    ]

    def test_get_correct_path(self):
        for path in TestGetMethods.paths:
            correct_path = os.path.abspath(os.path.expanduser(path))
            self.assertEqual(get_correct_path(path), correct_path)

    def test_get_trash_files_and_info_paths(self):
        for path in TestGetMethods.paths:
            correct_path = get_correct_path(path)
            self.assertTupleEqual(
                get_trash_files_and_info_paths(correct_path),
                (os.path.join(correct_path, const.TRASH_FILES_DIRECTORY),
                 os.path.join(correct_path, const.TRASH_INFO_DIRECTORY))
            )

    def test_get_regex_matcher(self):
        for reg in TestGetMethods.regex:
            matcher = get_regex_matcher(reg)

            for path in TestGetMethods.paths:
                basename = os.path.basename(path)
                fully_matched_part = None

                matches = re.match(reg + "$", basename)
                if matches:
                    fully_matched_part = matches.group(0)
                self.assertEqual(matcher(path), fully_matched_part)

    def test_get_path_in_trash(self):
        trash = "trash"

        for path in TestGetMethods.paths:
            self.assertEqual(
                get_path_in_trash(path, trash),
                os.path.join(
                    trash, const.TRASH_FILES_DIRECTORY, os.path.basename(path)
                )
            )

    def test_get_path_in_trash_info(self):
        trash = "trash"

        for path in TestGetMethods.paths:
            self.assertEqual(
                get_path_in_trash_info(path, trash),
                os.path.join(
                    trash, const.TRASH_INFO_DIRECTORY,
                    os.path.basename(path) + const.INFO_FILE_EXPANSION
                )
            )


if __name__ == '__main__':
    main()
