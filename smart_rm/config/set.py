#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# from ConfigParser import ConfigParser
from argparse import ArgumentParser
from sys import argv


class Parser(object):
    def __init__(self):
        self.parser = ArgumentParser(add_help=True)

        self.action_group = self.parser.add_argument_group()
        self.config_group = self.parser.add_argument_group()
        self.add_action_flags()
        self.add_config_flags()

    def add_action_flags(self):
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

    def parse_args(self, list_to_parse=argv[1:]):
        return self.parser.parse_args(list_to_parse)
