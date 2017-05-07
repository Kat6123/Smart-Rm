# -*- coding: utf-8 -*-
from smart_rm.utils import (
    TRASH_LOCATION,
    SM_REMOVE_SOLVE_NAME_CONFLICT,
    TRASH_SOLVE_NAME_CONFLICT,
    TRASH_CLEAN_POLITIC
)


class Namespace(object):
    def override(self, namespace):
        for attribute in self.__dict__:
            self.__dict__[attribute] = namespace.__dict__.get(
                attribute,
                self.__dict__[attribute]   # Default value if key is not exist
            )


class SmartRemoveNamespace(Namespace):
    def __init__(self):
        self.actions = {
            "remove_file": True,
            "remove_empty_directory": False,
            "remove_tree": False
        }

        self.path_to = {
            "trash": TRASH_LOCATION,
            "remove": []
        }

        self.modes = {
            "not_confirm_rm": False,
            "confirm_rm_if_no_write_access": True,
            "confirm_rm": False,

            "silent": False,
            "dry_run": False,
        }

        self.politics = {
            "solve_name_conflict_when_remove": SM_REMOVE_SOLVE_NAME_CONFLICT
        }

        self.regex = None


class TrashNamespace(Namespace):
    def __init__(self):
        self.actions = {
            "display": True,
            "clean": False,
            "restore": False
        }

        self.path_to = {
            "trash": TRASH_LOCATION,
            "restore": []
        }

        self.modes = {
            "check_hash": False,
            "dry_run": False,
            "silent": False
        }

        self.politics = {
            "clean": TRASH_CLEAN_POLITIC,
            "solve_name_conflict_when_restore": TRASH_SOLVE_NAME_CONFLICT
        }


class NamespaceReader(object):
    def __init__(self):
        self.namespace = Namespace()

    def get_namespace(self):
        return self.namespace
