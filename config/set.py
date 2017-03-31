# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from sys import argv


class Config(object):
    """Contains launch configuration"""
    user_config_path = "config/smart_rm.cfg"
    json_config_path = "config/smart_rm.json"

    def __init__(self):
        self.location = {}
        self.modes = {}
        self.politics = {}
        self.recycle_basket_options = {}

        self._get_user_config()
        self._get_command_line_config()
        self._get_json_config()

    def _get_command_line_config(self):             # TODO: verification
        args = parser()
        #if args.config

    def _get_user_config(self, path=user_config_path):
        config = ConfigParser()
        config.read(path)
        self.location = dict(config.items("location"))
        self.modes = dict(config.items("modes"))

    def _get_json_config(self):                             # TODO
        pass


def parser():                                            # TODO: add doc; break
    parser = ArgumentParser(add_help=True)

    exclusive_modes = parser.add_mutually_exclusive_group()

    parser.add_argument('path', nargs='+', help='Files to be deleted')  # TODO:
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

    parser.add_argument('--clear', dest='clear_basket',
                        action='store_true', help='Clear basket')
    parser.add_argument('--content', dest='view_basket_content',
                        action='store_true', help='View basket content')

    parser.add_argument('--config', dest='config_file_path', action='store',
                        help='Path to configuration file for this launch')

    return parser.parse_args(argv[1:])
