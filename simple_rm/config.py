# -*- coding: utf-8 -*-
import argparse
import sys

from simple_rm.constants import *


class Config(object):
    def __init__(self):
        self.remove = {
            aim: REMOVE_FILE_MODE,
            mode: PAY_ATTENTION_IF_NOT_WRITE_ACCESS_MODE
        }

        self.path_to = {
            "trash": TRASH_LOCATION,
            "log_file": None
        }

        self.dry_run = False
        self.silent = False

        self.check_hash = False

        self.policies = {
            "solve_name_conflict_when_remove": SM_REMOVE_SOLVE_NAME_CONFLICT,
            "clean": TRASH_CLEAN_POLITIC,
        }

    def override(self, another_config):
        for attribute in self.__dict__:
            self.__dict__[attribute] = another_config.__dict__.get(
                attribute,
                self.__dict__[attribute]   # Default value if key is not exist
            )


class ArgumentParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True)
        self.add_actions()
        self.add_modes()

        self.args = self.parser.parse_args(sys.argv[1:])

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

    def get_config(self):
        config = Config()

        if self.args.rm_directory_recursively:
            config.remove_mode = REMOVE_EMPTY_DIRECTORY_MODE
        elif self.args.rm_empty_directory:
            config.remove_mode = REMOVE_TREE_MODE

        return config
