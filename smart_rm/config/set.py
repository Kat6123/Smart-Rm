
# -*- coding: utf-8 -*-
#from ConfigParser import ConfigParser
from argparse import ArgumentParser
from sys import argv


class Config(object):
    """
    Contains launch configuration

    Config object contains 4 parts: actions, paths, modes, politics,
    which are presented as dictionaries with relevant names.
    """

    def __init__(self,
                 user_config_file_path="smart_rm.conf",
                 json_config_file_path="smart_rm.json",
                 args_list_to_parse=argv[1:]):

        self.actions = dict.fromkeys(["remove", "basket"], {})
        self.actions.remove = {
            "file": True, "directory": False, "tree": False}
        self.actions.basket = dict.fromkeys(  # TODO clean always True?
            ["browse_content", "clean", "restore_files"], False)

        self.file_paths_to = dict.fromkeys(
            ["config", "log", "basket", "remove", "restore"])

        self.modes = dict.fromkeys(
            ["interactive", "dry_run", "silent",
             "get_statistic", "follow_sym_link",
             "check_hash_when_restore"], False)

        self.politics = dict.fromkeys(
            ["basket_cleaning", "conflict_resolution"], {})


class Parser(object):
    def __init__(self):
        self.parser = ArgumentParser(add_help=True)

        self.action_group = self.parser.add_argument_group()
        self.config_group = self.parser.add_argument_group()
        self._add_action_flags()
        self._add_config_flags()

    def _add_action_flags(self):
        """
        Add action flags

        dir, recursive - removal flags
        path - contains paths to remove
        clear, content, restore - flags to work with basket
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
            '--clear', dest='clear_basket', action='store_true',
            help='Clear basket')
        self.action_group.add_argument(
            '--content', dest='view_basket_content', action='store_true',
            help='View basket content')
        self.action_group.add_argument(
            '--restore', dest='restore_from_basket',
            nargs='+', help='Restore files from basket')

    def _add_config_flags(self):
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
            '-s', '--silent', dest='silent_mode', action='store_true',
            help='Launch in silent mode')
        self.config_group.add_argument(
            '--dry_run', action='store_true',
            dest='remove_imitation', help='Launch in dry-run mode')

        self.config_group.add_argument(
            '-f', '--force', action='store_true',
            dest='force_remove', help='Never prompt')

        self.config_group.add_argument(
            '-l', '--link', action='store_true',
            dest='follow_link', help='Follow symbolic links')

    def parse_args(self, list_to_parse=argv[1:]):
        return self.parser.parse_args(list_to_parse)
