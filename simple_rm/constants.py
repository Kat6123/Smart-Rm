# -*- coding: utf-8 -*-

REMOVE_FILE_MODE = "file"
REMOVE_EMPTY_DIRECTORY_MODE = "directory"
REMOVE_TREE_MODE = "tree"

INTERACTIVE_MODE = "interactive"
FORCE_MODE = "force"
ATTENTION_IF_NOT_WRITE_ACCESS_MODE = "not_write_access"

LOG_LEVEL = "warning"

ROOT = "/"

TRASH_FILES_DIRECTORY = "files"
TRASH_INFO_DIRECTORY = "info"

INFO_SECTION = "Trash info"
FILE_HASH_OPTION = "Hash"
OLD_PATH_OPTION = "Path"
SIZE_OPTION = "Size"
REMOVE_DATE_OPTION = "Date"
DATE_FORMAT = "%d.%m.%Y  %H:%M"
TIME_DELTA_FORMAT = "%W months %d days %H hours %M minutes"

INFO_FILE_EXPANSION = ".trashinfo"

APP_DIRECTORY = "~/.smart_remove"
DEFAULT_CONFIG_NAME = "config.cfg"
LOG_FILE_LOCATION = "/var/log/smart_rm.log"
PATH_TO_COPY_DEFAULT_CONFIG = "config/configuration"
TRASH_LOCATION = "~/.local/share/trash"

END_OF_STRING = "$"
EMPTY_STRING = ""

DEFAULT_CLEAN_POLICY = "remove_all"
MAX_TRASH_SIZE_IN_BYTES = 2 ** 30
MAX_TIME_IN_TRASH = "12 months 1 days 1 hours 1 minutes"
CLEAN_POLICY_TEMPLATE = "get_object_list_by_{0}_policy"
CLEAN_POLICY_VALIDATION_TEMPLATE = "get_valid_clean_parametr_by_{0}_policy"

SOLVE_NAME_CONFLICT_POLICY = "give_new_name_depending_on_same_amount"
