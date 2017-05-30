# -*- coding: utf-8 -*-
import os
import os.path
import logging

import simple_rm.constants as const
from simple_rm.check import return_true
from simple_rm.trash import Trash


def init_trash_by_config(config):
    confirm_removal = return_true

    if config.remove["mode"] == const.PAY_ATTENTION_IF_NOT_WRITE_ACCESS_MODE:
        confirm_removal = ask_if_file_has_not_write_access
    elif config.remove["mode"] == const.INTERACTIVE_MODE:
        confirm_removal = ask_remove

    result_trash = Trash(
        trash_location=config.path_to["trash"],
        remove_mode=config.remove["aim"],
        dry_run=config.settings["dry_run"],
        confirm_removal=confirm_removal,
        clean_policy=config.policies["clean"],
        clean_parametr=config.policies["clean_parametr"],
        solve_name_conflict_policy=config.policies["solve_name_conflict"],
        max_size=config.policies["max_size"],
        max_time_in_trash=config.policies["max_time_in_trash"]
    )

    return result_trash


def ask_if_file_has_not_write_access(path):
    if os.access(path, os.W_OK):
        return True
    elif ask_remove(path, special_info="write-protected"):
        return True

        return False


def ask_remove(path, special_info=""):
    if os.path.isfile(path):
        what_remove = "file"
    else:
        what_remove = "directory"
    answer = raw_input(
        "Do you want to remove {0} {1} \"{2}\"?: "
        "".format(special_info, what_remove, path)
    )
    if answer == 'y':
        return True


def report_about_result(result):
    for info_obj in result:
        if info_obj.errors:
            logging.error("\n".join([str(error) for error in info_obj.errors]))
        else:
            logging.info("\n" + str(info_obj))
