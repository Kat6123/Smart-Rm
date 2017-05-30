# -*- coding: utf-8 -*-
import ConfigParser

import simple_rm.constants as const
from simple_rm.check import get_correct_path


class Config(object):
    def __init__(self):
        self.remove = {
            "aim": const.REMOVE_FILE_MODE,
            "mode": const.PAY_ATTENTION_IF_NOT_WRITE_ACCESS_MODE
        }

        self.path_to = {
            "trash": get_correct_path(const.TRASH_LOCATION),
            "log_file": None
        }

        self.settings = {
            "dry_run": False,
            "silent": False,
            "check_hash": False
        }

        self.policies = {
            "clean": const.DEFAULT_CLEAN_POLICY,
            "clean_parametr": None,
            "solve_name_conflict": const.SOLVE_NAME_CONFLICT_POLICY,
            "max_size": const.MAX_TRASH_SIZE_IN_BYTES,
            "max_time_in_trash": const.MAX_TIME_IN_TRASH
        }

    def update(self, dict_config):
        for attribute in self.__dict__:
            new = dict_config.get(attribute)
            if new:
                self.__dict__[attribute].update(new)


def set_parser_for_remove(parser):
    parser.add_argument(
        '-d', '--dir', dest='rm_empty_directory', action='store_true',
        help='Remove empty directories')
    parser.add_argument(
        '-r', '-R', '--recursive', dest='rm_directory_recursively',
        action='store_true', help='Remove directories and '
        'their contents recursively')

    parser.add_argument(
        'path', nargs='+', help='Files to be deleted')

    parser.add_argument(
        '-i', '--interactive', dest='ask_before_remove',
        action='store_true', help='Prompt before every removal')
    parser.add_argument(
        '-f', '--force', action='store_true',
        dest='force_remove', help='Never prompt')

    parser.add_argument(
        '--regex', action='store', help='Let remove by regular expression'
    )


def get_config_dict_from_remove_parser_namespace(namespace):
    result = {
        "remove": {},
        "path_to": {},
        "settings": {}
    }

    if namespace.rm_directory_recursively:
        result["remove"]["aim"] = const.REMOVE_TREE_MODE
    elif namespace.rm_empty_directory:
        result["remove"]["aim"] = const.REMOVE_EMPTY_DIRECTORY_MODE

    if namespace.ask_before_remove:
        result["remove"]["mode"] = const.INTERACTIVE_MODE
    elif namespace.force_remove:
        result["remove"]["mode"] = const.FORCE_MODE

    if namespace.log_file_path:
        result["path_to"]["log_file"] = namespace.log_file_path
    if namespace.imitation:
        result["settings"]["dry_run"] = True
    if namespace.silent_mode:
        result["settings"]["silent"] = True

    return result


def set_parser_for_trash(parser):
    parser.add_argument(
        '--clear', dest='clear_trash', action='store_true',
        help='Clear trash')
    parser.add_argument(
        '--content', dest='view_trash_content', action='store_true',
        help='View trash content')
    parser.add_argument(
        '--restore', dest='restore_from_trash',
        nargs='+', help='Restore files from trash')

    parser.add_argument(
        '--check_hash', action='store_true',
        dest='check_hash', help='Check hash when restore from trash'
    )


def set_parser_with_common_flags(parser):
    parser.add_argument(
        '--config', dest='config_file_path', action='store',
        help='Path to configuration file for this launch')
    parser.add_argument(
        '--log', dest='log_file_path', action='store',
        help='Path to log file for this launch')
    parser.add_argument(
        '--log_level', action='store_const',
        const=const.LOG_LEVEL,
        help='Path to log file for this launch')

    parser.add_argument(
        '-s', '--silent', dest='silent_mode', action='store_true',
        help='Launch in silent mode')
    parser.add_argument(
        '--dry_run', action='store_true',
        dest='imitation', help='Launch in dry-run mode')
    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true',
        help='Give full description')


def get_config_dict_from_trash_parser_namespace(namespace):
    result = {
        "path_to": {},
        "settings": {}
    }

    if namespace.check_hash:
        result["settings"]["check_hash"] = True
    if namespace.imitation:
        result["settings"]["dry_run"] = True
    if namespace.silent_mode:
        result["settings"]["silent"] = True

    if namespace.log_file_path:
        result["path_to"]["log_file"] = namespace.log_file_path

    return result


def get_config_from_file(file_path):
    result = {}

    config = ConfigParser.ConfigParser()
    config.read(file_path)

    result["remove"] = dict(config.items("Remove"))
    result["path_to"] = dict(config.items("Path to"))
    result["policies"] = dict(config.items("Policies"))

    settings = dict(config.items("Settings"))
    result["settings"] = {
        key: True if settings[key] == "True" else False for key in settings
    }
    try:
        max_size = int(result["policies"]["max_size"])
        result["policies"]["max_size"] = max_size
    except ValueError:
        result["policies"]["max_size"] = const.MAX_TRASH_SIZE_IN_BYTES
    return result
