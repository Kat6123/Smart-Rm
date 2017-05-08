# -*- coding: utf-8 -*-
import sys
import argparse
from smart_rm.config.namespace import (
    SmartRemoveNamespace,
    TrashNamespace,
    NamespaceReader
)
from smart_rm.utils import (
    LOG_FILE_LOCATION,
    LOG_LEVEL
)


class ArgsRemoveReader(NamespaceReader):
    def __init__(self):
        self.namespace = SmartRemoveNamespace()

        self.log_level = None
        self.path_to_log = None
        self.path_to_config = None

        self.parser = argparse.ArgumentParser(add_help=True)
        self.add_actions()
        self.add_modes()

    def add_actions(self):
        """
        Add action flags

        dir, recursive - removal flags
        path - contains paths to remove
        """
        self.parser.add_argument(
            '-d', '--dir', dest='rm_empty_directory', action='store_true',
            help='Remove empty directories')
        self.parser.add_argument(
            '-r', '-R', '--recursive', dest='rm_directory_recursively',
            action='store_true', help='Remove directories and '
            'their contents recursively')

        self.parser.add_argument(
            'path', nargs='+', help='Files to be deleted')

    def add_modes(self):
        """ Add flags for configuration """

        self.parser.add_argument(
            '--config', dest='config_file_path', action='store',
            help='Path to configuration file for this launch')
        self.parser.add_argument(
            '--log', dest='log_file_path', action='store_const',
            const=LOG_FILE_LOCATION,
            help='Path to log file for this launch')
        self.parser.add_argument(
            '--log_level', action='store_const',
            const=LOG_LEVEL,
            help='Path to log file for this launch')

        self.parser.add_argument(
            '-i', '--interactive', dest='ask_before_remove',
            action='store_true', help='Prompt before every removal')
        self.parser.add_argument(
            '-f', '--force', action='store_true',
            dest='force_remove', help='Never prompt')

        self.parser.add_argument(
            '-s', '--silent', dest='silent_mode', action='store_true',
            help='Launch in silent mode')
        self.parser.add_argument(
            '--dry_run', action='store_true',
            dest='imitation', help='Launch in dry-run mode')

        self.parser.add_argument(
            '--regex', action='store', help='Let remove by regular expression'
        )

    def set_namespace_from_parse_args(self, list_to_parse=sys.argv[1:]):
        args = self.parser.parse_args(list_to_parse)

        self.namespace.path_to["remove"] = args.path

        if args.rm_directory_recursively:
            self.namespace.actions["remove_tree"] = True
        elif args.rm_empty_directory:
            self.namespace.actions["remove_empty_directory"] = True

        if args.ask_before_remove:
            self.namespace.modes["confirm_rm"] = True
        elif args.force_remove:
            self.namespace.modes["not_confirm_rm"] = True

        if args.silent_mode:
            self.namespace.modes["silent"] = True
        if args.imitation:
            self.namespace.modes["dry_run"] = True

        if args.regex:
            self.namespace.regex = args.regex

        if args.config_file_path:
            self.path_to_config = args.config_file_path
        self.path_to_log = args.log_file_path
        self.log_level = args.log_level

    def get_namespace(self):
        self.set_namespace_from_parse_args()
        return self.namespace


class ArgsTrashReader(NamespaceReader):
    def __init__(self):
        self.namespace = TrashNamespace()

        self.log_level = None
        self.path_to_log = None
        self.path_to_config = None

        self.parser = argparse.ArgumentParser(add_help=True)
        self.add_actions()
        self.add_modes()

    def add_actions(self):
        """
        Add action flags

        clear, content, restore - flags to work with trash
        """

        self.parser.add_argument(
            '--clear', dest='clear_trash', action='store_true',
            help='Clear trash')
        self.parser.add_argument(
            '--content', dest='view_trash_content', action='store_true',
            help='View trash content')
        self.parser.add_argument(
            '--restore', dest='restore_from_trash',
            nargs='+', help='Restore files from trash')

    def add_modes(self):
        self.parser.add_argument(
            '--config', dest='config_file_path', action='store',
            help='Path to configuration file for this launch')
        self.parser.add_argument(
            '--log', dest='log_file_path', action='store_const',
            const=LOG_FILE_LOCATION,
            help='Path to log file for this launch')
        self.parser.add_argument(
            '--log_level', action='store_const',
            const=LOG_LEVEL,
            help='Path to log file for this launch')

        self.parser.add_argument(
            '-s', '--silent', dest='silent_mode', action='store_true',
            help='Launch in silent mode')
        self.parser.add_argument(
            '--dry_run', action='store_true',
            dest='imitation', help='Launch in dry-run mode')

        self.parser.add_argument(
            '--check_hash', action='store_true',
            dest='check_hash', help='Check hash when restore from trash')

    def set_from_parse_args(self, list_to_parse=sys.argv[1:]):
        args = self.parser.parse_args(list_to_parse)

        if args.restore_from_trash:
            self.namespace.actions["restore"] = True
            self.namespace.path_to["restore"] = args.restore_from_trash
        if args.clear_trash:
            self.namespace.actions["clean"] = True
        if args.view_trash_content:
            self.namespace.modes["display"] = True

        if args.silent_mode:
            self.namespace.actions["silent"] = True
        if args.imitation:
            self.namespace.modes["dry_run"] = True
        if args.check_hash:
            self.namespace.modes["check_hash"] = True

        if args.config_file_path:
            self.path_to_config = args.config_file_path
        self.path_to_log = args.log_file_path
        self.log_level = args.log_level

    def get_namespace(self):
        self.set_from_parse_args()
        return self.namespace

# if silent then force!
