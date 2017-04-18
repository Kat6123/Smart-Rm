
# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from argparse import ArgumentParser
from sys import argv
from os.path import (
    exists,
    join
)


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
