#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from smart_rm.core.trash_can import AdvancedTrashCan
from smart_rm.config.namespace import TrashNamespace
from smart_rm.config.readers.commad_line_args_reader import ArgsTrashReader
from smart_rm.log.logger import tune_logger
from smart_rm.utils import make_app_folder_if_not_exist


def main():
    namespace = TrashNamespace()

    make_app_folder_if_not_exist()
    # default_namespace = ""
    #
    # namespace.override(default_namespace)

    args_reader = ArgsTrashReader()
    args_namespace = args_reader.get_namespace()

    # if args_reader.path_to_config:
    #     special_config_namespace = ""

    # namespace.override(special_config_namespace)
    namespace.override(args_namespace)

    if namespace.modes["silent"]:
        tune_logger(
            write_to_stderr=False,
            log_level=args_reader.log_level,
            logfile_path=args_reader.path_to_log
        )
        namespace.modes["force"] = True
    else:
        tune_logger(
            # log_level=args_reader.log_level,
            logfile_path=args_reader.path_to_log
        )

    trash = AdvancedTrashCan(
        namespace.path_to["trash"]
    )

    if namespace.actions["display"]:
        trash.view_content()
    elif namespace.actions["restore"]:
        trash.restore_files(namespace.path_to["remove"])
    elif namespace.actions["clean"]:
        trash.clean()


if __name__ == '__main__':
    main()
