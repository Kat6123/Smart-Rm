#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from simple_rm.config import (
    Config,
    get_config_dict_from_trash_parser_namespace,
    get_config_from_file,
    set_parser_for_trash,
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
    set_parser_for_trash(parser)
    set_parser_with_common_flags(parser)
    args = parser.parse_args()

    config.update(get_config_dict_from_trash_parser_namespace(args))

    if args.config_file_path:
        config.update(
            get_config_from_file(get_correct_path(args.config_file_path))
        )

    trash = init_trash_by_config(config)

    log_file = args.log_file_path

    if args.imitation or args.view_trash_content:
        args.verbose = True
    if args.silent_mode:
        trash.confirm_removal = return_true
        set_logger(write_to_stderr=False)
    elif args.verbose or not (args.restore_from_trash or args.clear_trash):
        set_logger(log_level="info", logfile_path=log_file)
    else:
        set_logger(logfile_path=log_file)

    if args.restore_from_trash:
        report_about_result(trash.restore(args.restore_from_trash))
    elif args.clear_trash:
        report_about_result(trash.clean())
    else:
        report_about_result(trash.view())


if __name__ == '__main__':
    main()
