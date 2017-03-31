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

    def _get_command_line_config(self):
        pass

    def _get_user_config(self, path=user_config_path):
        config = ConfigParser()
        config.read(path)
        self.location = dict(config.items("location"))
        self.modes = dict(config.items("modes"))

    def _get_json_config(self):                             # TODO
        pass
