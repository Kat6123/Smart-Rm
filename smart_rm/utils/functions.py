import errno
import os
import os.path
import re
from smart_rm.utils.constants import END_OF_STRING
from smart_rm.core.error import (
    AccessError,
    ExistError
)


def check_path_existance(path):
    abs_path = os.path.abspath(path)

    if not os.access(os.path.dirname(abs_path), os.R_OK):
        raise AccessError(
            errno.EACCES, os.strerror(errno.EACCES), os.path.dirname(abs_path)
        )
    elif not os.path.exists(abs_path):
        raise ExistError(errno.ENOENT, os.strerror(errno.ENOENT), abs_path)


def get_regex_matcher(regex):
    regex = regex + END_OF_STRING

    def match_path(path):
        matches = re.match(regex, os.path.basename(path))
        if matches:
            return matches.group(0)
    return match_path
