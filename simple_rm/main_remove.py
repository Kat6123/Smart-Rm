#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from argparse import ArgumentParser

import simple_rm.constants as const

from simple_rm.config import (
    Config,
    get_config_dict_from_remove_parser_namespace,
    get_config_from_file,
    set_parser_for_remove,
    set_parser_with_common_flags
)
from simple_rm.check import (
    get_correct_path,
    return_true
)
from simple_rm.wrapper import (
    init_trash_by_config,
    report_about_result
)
from simple_rm.logger import set_logger


def main():
    config = Config()

    parser = ArgumentParser()
    set_parser_for_remove(parser)
    set_parser_with_common_flags(parser)
    args = parser.parse_args()

    config.update(get_config_dict_from_remove_parser_namespace(args))

    if args.config_file_path:
        config.update(
            get_config_from_file(get_correct_path(args.config_file_path))
        )

    if args.regex:
        config.remove["aim"] = const.REMOVE_TREE_MODE

    trash = init_trash_by_config(config)

    log_file = args.log_file_path
    if args.imitation:
        args.verbose = True
    if args.silent_mode:
        trash.confirm_removal = return_true
        set_logger(write_to_stderr=False)
    elif args.verbose:
        set_logger(log_level="info", logfile_path=log_file)
    else:
        set_logger(logfile_path=log_file)

    report_about_result(trash.remove(args.path, regex=args.regex))


if __name__ == '__main__':
    main()
