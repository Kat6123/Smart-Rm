# -*- coding: utf-8 -*-
import sys
import argparse
from namespace import NamespaceReader


class ArgsReader(NamespaceReader):
    def __init__(self):
        super(ArgsReader, self).__init__()
        self.parser = argparse.ArgumentParser(add_help=True)

        self.path_to_log = ""           # add from constants
        self.path_to_config = ""

        self.action_group = self.parser.add_argument_group()
        self.config_group = self.parser.add_argument_group()
        self.add_action_flags()
        self.add_config_flags()

    def add_action_flags(self):
        """
        Add action flags

        dir, recursive - removal flags
        path - contains paths to remove
        clear, content, restore - flags to work with trash
        """
        self.action_group.add_argument(
            '-d', '--dir', dest='rm_empty_directory', action='store_true',
            help='Remove empty directories')
        self.action_group.add_argument(
            '-r', '-R', '--recursive', dest='rm_directory_recursively',
            action='store_true', help='Remove directories and '
            'their contents recursively')

        self.action_group.add_argument(
            'path', nargs='+', help='Files to be deleted')

        self.action_group.add_argument(
            '--clear', dest='clear_trash', action='store_true',
            help='Clear trash')
        self.action_group.add_argument(
            '--content', dest='view_trash_content', action='store_true',
            help='View trash content')
        self.action_group.add_argument(
            '--restore', dest='restore_from_trash',
            nargs='+', help='Restore files from trash')

    def add_config_flags(self):
        """ Add flags for configuration """
        self.config_group.add_argument(
            '--config', dest='config_file_path', action='store',
            help='Path to configuration file for this launch')
        self.config_group.add_argument(
            '--log', dest='log_file_path', action='store',
            help='Path to log file for this launch')

        self.config_group.add_argument(
            '-i', '--interactive', dest='ask_before_remove',
            action='store_true', help='Prompt before every removal')
        self.config_group.add_argument(
            '-f', '--force', action='store_true',
            dest='force_remove', help='Never prompt')

        self.config_group.add_argument(
            '-s', '--silent', dest='silent_mode', action='store_true',
            help='Launch in silent mode')
        self.config_group.add_argument(
            '--dry_run', action='store_true',
            dest='remove_imitation', help='Launch in dry-run mode')

    def set_from_parse_args(self, list_to_parse=sys.argv[1:]):
        args = self.parser.parse_args(list_to_parse)

        if args.rm_directory_recursively:
            self.namespace.actions["remove"]["tree"] = True
        elif args.rm_empty_directory:
            self.namespace.actions["remove"]["directory"] = True

        if args.ask_before_remove:
            self.namespace.modes["confirm_rm_always"] = True
        elif args.force_remove:
            self.namespace.modes["not_confirm_rm"] = True

        if args.silent_mode:
            self.namespace.modes["silent"] = True
        if args.remove_imitation:
            self.namespace.modes["dry_run"] = True

        if args.log_file_path:
            self.path_to_log = args.log_file_path

        # if args.config_file_path:
        #     self.path_to_log = args.log_file_path
        self.file_paths_to["remove"] = args.path


# if silent then force!
