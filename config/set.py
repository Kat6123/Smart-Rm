
# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from sys import argv
from os.path import (
    exists,
    join,
    abspath)


class Config(object):
    """Contains launch configuration"""
    user_config_path = "config/smart_rm.cfg"
    json_config_path = "config/smart_rm.json"
    command_line_args = argv[1:]

    def __init__(self):
        self.location = {}
        self.politics = {}

        self.files_to_delete = []
        self.files_to_restore = []

        self.recycle_basket_options = dict.fromkeys(["clear_basket",
                                                    "restore_from_basket",
                                                    "view_basket_content"],
                                                    False)
        self.modes = dict.fromkeys(["rm_recursively", "rm_empty_directories",
                                    "ask_remove", "silent_mode",
                                    "remove_imitation"], False)

        self._get_user_config()
        self._get_command_line_config()
        self._get_json_config()

    def _get_command_line_config(self):             # TODO: verification
        args = parser(self.command_line_args)            # ?

        if args.clear_basket:
            self.recycle_basket_options["clear_basket"] = True
        elif args.restore_from_basket is not None:
            self.recycle_basket_options["restore_from_basket"] = True
            self.files_to_restore = get_available_basket_files(
                args.restore_from_basket, self.location["files"])
                                                         # TODO: files location
        if args.view_basket_content:
            self.recycle_basket_options["view_basket_content"] = True

        self.files_to_delete = get_existance_paths(args.path)

        if args.config_file_path is not None:
            self._get_user_config(args.config_file_path)
        elif args.rm_directory_recursively:
            self.modes["rm_recursively"] = True
        elif args.rm_empty_directory:
            self.modes["rm_empty_directories"] = True

        if args.ask_before_remove:
            self.modes["ask_remove"] = True
        elif args.silent_mode:
            self.modes["silent_mode"] = True

        if args.remove_imitation:
            self.modes["remove_imitation"] = True

    def _get_user_config(self, path=user_config_path):
        config = ConfigParser()
        config.read(path)
        self.location = dict(config.items("location"))
        self.modes = dict(config.items("modes"))

    def _get_json_config(self):                             # TODO
        pass


def parser(command_line):                             # TODO: add doc; break
    parser = ArgumentParser(add_help=True)

    exclusive_modes = parser.add_mutually_exclusive_group()
    subparsers = parser.add_subparsers()
    basket_subparser = subparsers.add_parser('basket', help='Work with basket')

    parser.add_argument('path', nargs='+', type=file,
                        help='Files to be deleted')
    parser.add_argument('-d', '--dir', dest='rm_empty_directory',
                        action='store_true', help='Remove empty directories')
    parser.add_argument('-r', '-R', '--recursive',
                        dest='rm_directory_recursively', action='store_true',
                        help='Remove directories and '
                        'their contents recursively')

    exclusive_modes .add_argument('-a', '--ask', dest='ask_before_remove',
                                  action='store_true',
                                  help='Prompt before every removal')
    exclusive_modes .add_argument('-s', '--silent', dest='silent_mode',
                                  action='store_true',
                                  help='Launch in silent mode')

    parser.add_argument('-i', '--imitation', dest='remove_imitation',
                        action='store_true', help='Launch in dry-run mode')
    parser.add_argument('--config', dest='config_file_path',
                        type=file, action='store',
                        help='Path to configuration file for this launch')

    basket_subparser.add_argument('--clear', dest='clear_basket',
                                  action='store_true', help='Clear basket')
    basket_subparser.add_argument('--content', dest='view_basket_content',
                                  action='store_true',
                                  help='View basket content')
    basket_subparser.add_argument('--restore', dest='restore_from_basket',
                                  type=file, nargs='+',
                                  help='Restore files from basket')

    return parser.parse_args(command_line)


def get_existance_paths(paths):
    exist = []
    for path in paths:
        if exists(path):
            exist.append(abspath(path))
    return exist


def get_available_basket_files(paths_basename, basket_files_location):
    available = []

    for path in paths_basename:
        abs_path = join(basket_files_location, path)
        if exists(abs_path):
            available.append(abs_path)
    return available
