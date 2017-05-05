# -*- coding: utf-8 -*-


class RMNamespace(object):
    def __init__(self):
        self.actions = dict.fromkeys(["remove", "trash"], {})
        self.actions["remove"] = {
            "file": True, "directory": False, "tree": False}
        self.actions["trash"] = dict.fromkeys(  # TODO clean always True?
            ["browse_content", "clean", "restore_files"], False
        )

        self.file_paths_to = dict.fromkeys(
            ["trash", "remove", "restore"]
        )

        self.modes = dict.fromkeys(
            ["confirm_rm_always", "not_confirm_rm",
             "silent", "dry_run",
             "get_statistic", "check_hash_when_restore"], False)
        self.modes["confirm_if_file_has_not_write_access"] = True

        self.politics = dict.fromkeys(
            ["trash_cleaning", "conflict_resolution"], {}
        )

    def override_by_another_namespace(self, namespace):
        for attribute in self.__dict__:
            self.__dict__[attribute] = namespace.__dict__.get(
                attribute,
                self.__dict__(attribute)   # Default value if key is not exist
            )


class NamespaceReader(object):
    def __init__(self):
        self.namespace = RMNamespace()

    def get_namespace(self):
        return self.namespace
