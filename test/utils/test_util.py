# -*- coding: utf-8 -*-
import os.path
import re
from unittest import (
    TestCase,
    main
)
from smart_rm.utils.constants import (
    TRASH_FILES_DIRECTORY,
    TRASH_INFO_DIRECTORY
)
from smart_rm.utils.util import *


class TestUtil(TestCase):
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
        for path in TestUtil.paths:
            correct_path = os.path.abspath(os.path.expanduser(path))
            self.assertEqual(get_correct_path(path), correct_path)

    def test_get_trash_files_and_info_paths(self):
        for path in TestUtil.paths:
            correct_path = get_correct_path(path)
            self.assertTupleEqual(
                get_trash_files_and_info_paths(correct_path),
                (os.path.join(correct_path, TRASH_FILES_DIRECTORY),
                 os.path.join(correct_path, TRASH_INFO_DIRECTORY))
            )

    def test_get_regex_matcher(self):
        for reg in TestUtil.regex:
            matcher = get_regex_matcher(reg)

            for path in TestUtil.paths:
                basename = os.path.basename(path)
                fully_matched_part = None

                matches = re.match(reg + "$", basename)
                if matches:
                    fully_matched_part = matches.group(0)
                self.assertEqual(matcher(path), fully_matched_part)


if __name__ == '__main__':
    main()
