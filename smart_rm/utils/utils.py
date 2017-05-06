# -*- coding: utf-8 -*-
import os.path
import re
from smart_rm.utils import (
    END_OF_STRING,
    TRASH_FILES_DIRECTORY,
    TRASH_INFO_DIRECTORY
)


def get_regex_matcher(regex):
    regex = regex + END_OF_STRING

    def match_path(path):
        matches = re.match(regex, os.path.basename(path))
        if matches:
            return matches.group(0)
    return match_path


def get_trash_files_and_info_paths(trash_location):         # ? expanduser
    return (
        os.path.join(trash_location, TRASH_FILES_DIRECTORY),
        os.path.join(trash_location, TRASH_INFO_DIRECTORY)
    )
