# -*- coding: utf-8 -*-
import os.path

from simple_rm.clean import permanent_remove
from simple_rm.error import SysError


def ask_new_name(info_obj):
    new_name = raw_input("Enter new name for {0}: ".format(
        os.path.basename(info_obj.path_in_trash))
    )
    if new_name:
        new_path = os.path.join(
            os.path.dirname(info_obj.path_in_trash),
            os.path.basename(new_name)
        )
        info_obj.path_in_trash = new_path
    else:
        info_obj.errors.append(
            SysError("Already exists {0}".format(info_obj.path_in_trash))
        )


def give_new_name_depending_on_same_amount(info_obj):
    old_path = info_obj.path_in_trash

    count_of_samename_files = os.listdir(os.path.dirname(old_path)).count(
        os.path.basename(old_path)
    )
    new_path = os.path.join(
        os.path.dirname(old_path),
        os.path.basename(old_path) + ".{0}".format(count_of_samename_files)
    )

    info_obj.path_in_trash = new_path


def skip(info_obj):
    info_obj.errors.append(
        SysError("Already exists {0}".format(info_obj.path_in_trash))
    )


def replace_without_confirm(info_obj):
    permanent_remove(
        info_obj, os.path.dirname(os.path.dirname(info_obj.path_in_trash))
    )


def confirm_and_replace(info_obj):
    answer = raw_input(
        "Do you want to rewrite {0}(y/n): "
        "".format(os.path.basename(info_obj.path_in_trash))
    )
    if answer == 'y':
        permanent_remove(
            info_obj, os.path.dirname(os.path.dirname(info_obj.path_in_trash))
        )
    else:
        info_obj.errors.append(
            SysError("Already exists {0}".format(info_obj.path_in_trash))
        )
