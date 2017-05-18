# -*- coding: utf-8 -*-


class TrashInfo(object):
    def __init__(self):
        self.initial_path = ""
        self.path_in_trash = ""

        self.deletion_date = ""
        self.sha256_value = ""

        self.errors = []


class Trash(object):
    def __init__(self):
        self.trash_location = ""
        self.mode = ""
        self.regex = ""
        self.clean_politic = ""
        self.conflict_name_poitic = ""
        self.confirm_removal = ""
        self.dry_run = ""

    def setup(self):
        pass

    def remove(self):
        pass

    def restore(self):
        pass

    def view(self):
        pass

    def clean(self):
        pass
