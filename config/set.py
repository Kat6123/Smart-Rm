
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
        args.func(self, args)

    def _get_user_config(self, path=user_config_path):
        config = ConfigParser()
        config.read(path)
        self.location = dict(config.items("location"))
        self.modes = dict(config.items("modes"))

    def _get_json_config(self):                             # TODO
        pass


def set_config_from_basket_subparser(config, args):
    if args.clear_basket:
        config.recycle_basket_options["clear_basket"] = True
    elif args.restore_from_basket is not None:
        config.recycle_basket_options["restore_from_basket"] = True
        config.files_to_restore = get_available_basket_files(
            args.restore_from_basket, config.location["files"])
                                                     # TODO: files location
    if args.view_basket_content:
        config.recycle_basket_options["view_basket_content"] = True


def set_config_from_remove_subparser(config, args):
    config.files_to_delete = get_existance_paths(args.path)

    if args.config_file_path is not None:
        config._get_user_config(args.config_file_path)
    elif args.rm_directory_recursively:
        config.modes["rm_recursively"] = True
    elif args.rm_empty_directory:
        config.modes["rm_empty_directories"] = True

    if args.ask_before_remove:
        config.modes["ask_remove"] = True
    elif args.silent_mode:
        config.modes["silent_mode"] = True

    if args.remove_imitation:
        config.modes["remove_imitation"] = True


def set_basket_subparser(basket_subparser):
    basket_subparser.add_argument('--clear', dest='clear_basket',
                                  action='store_true', help='Clear basket')
    basket_subparser.add_argument('--content', dest='view_basket_content',
                                  action='store_true',
                                  help='View basket content')
    basket_subparser.add_argument('--restore', dest='restore_from_basket',
                                  nargs='+', help='Restore files from basket')
    basket_subparser.set_defaults(func=set_config_from_basket_subparser)


def set_remove_subparser(remove_subparser):
    exclusive_modes = remove_subparser.add_mutually_exclusive_group()

    remove_subparser.add_argument('path', nargs='+',
                                  help='Files to be deleted')
    remove_subparser.add_argument('-d', '--dir', dest='rm_empty_directory',
                                  action='store_true',
                                  help='Remove empty directories')
    remove_subparser.add_argument('-r', '-R', '--recursive',
                                  dest='rm_directory_recursively',
                                  action='store_true',
                                  help='Remove directories and '
                                  'their contents recursively')

    exclusive_modes .add_argument('-a', '--ask', dest='ask_before_remove',
                                  action='store_true',
                                  help='Prompt before every removal')
    exclusive_modes .add_argument('-s', '--silent', dest='silent_mode',
                                  action='store_true',
                                  help='Launch in silent mode')

    remove_subparser.add_argument('-i', '--imitation',
                                  dest='remove_imitation', action='store_true',
                                  help='Launch in dry-run mode')
    remove_subparser.add_argument('--config', dest='config_file_path',
                                  action='store', help='Path to configuration'
                                  ' file for this launch')

    remove_subparser.set_defaults(func=set_config_from_remove_subparser)


def parser(command_line):                             # TODO: add doc; break
    parser = ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers()

    basket_subparser = subparsers.add_parser('basket', help='Work with basket')
    remove_subparser = subparsers.add_parser('remove', help='Move to trash')

    set_basket_subparser(basket_subparser)
    set_remove_subparser(remove_subparser)

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
            available.append(path)
    return available
