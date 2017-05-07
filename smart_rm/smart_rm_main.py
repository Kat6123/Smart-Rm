#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from smart_rm.core.smart_remove import AdvancedRemover
from smart_rm.config.namespace import SmartRemoveNamespace
from smart_rm.config.readers.command_line_args_reader import ArgsRemoveReader
from smart_rm.log.logger import tune_logger
from smart_rm.utils import make_app_folder_if_not_exist


def main():
    namespace = SmartRemoveNamespace()

    make_app_folder_if_not_exist()
    # default_namespace = ""

    # namespace.override(default_namespace)

    args_reader = ArgsRemoveReader()
    args_namespace = args_reader.get_namespace()

    # if args_reader.path_to_config:
    #     special_config_namespace = ""

    # namespace.override(special_config_namespace)
    namespace.override(args_namespace)

    if namespace.modes["silent"]:
        tune_logger(
            write_to_stderr=False,
            # log_level=args_reader.log_level,
            logfile_path=args_reader.path_to_log
        )
        namespace.modes["force"] = True
    else:
        tune_logger(
            # log_level=args_reader.log_level,
            logfile_path=args_reader.path_to_log
        )

    remover = AdvancedRemover(
        namespace.path_to["trash"],
        namespace.modes["confirm_rm"],
        namespace.modes["not_confirm_rm"],
        namespace.modes["confirm_rm_if_no_write_access"],
        namespace.modes["dry_run"],
        namespace.politics["solve_name_conflict_when_remove"],
        namespace.regex
    )

    if namespace.actions["remove_tree"]:
        remover.remove_trees(namespace.path_to["remove"])
    elif namespace.actions["remove_empty_directory"]:
        remover.remove_directories(namespace.path_to["remove"])
    elif namespace.actions["remove_file"]:
        remover.remove_files(namespace.path_to["remove"])


if __name__ == '__main__':
    main()
