# -*- coding: utf-8 -*-
import datetime
import os
import shutil

import simple_rm.constants as const
import simple_rm.error as errors
from simple_rm.check import get_path_in_trash_info
import logging


def sort_by_deletion_date(obj_list):
    obj_list.sort(key=lambda x: x.deletion_date)


def get_size(start_path):
    if os.path.isfile(start_path):
        total_size = os.path.getsize(start_path)
    else:
        total_size = 0
        for root, directories, files in os.walk(start_path):
            for file_path in files:
                file_full_path = os.path.join(root, file_path)
                total_size += os.path.getsize(file_full_path)
            for dir_path in directories:
                dir_full_path = os.path.join(root, dir_path)
                total_size += os.path.getsize(dir_full_path)

    return total_size


def permanent_remove(info_object, trash_location):
    trashinfo_path = get_path_in_trash_info(
        info_object.path_in_trash, trash_location
    )

    try:
        if not os.path.isdir(info_object.path_in_trash):
            os.remove(info_object.path_in_trash)
        else:
            shutil.rmtree(info_object.path_in_trash)

        os.remove(trashinfo_path)
    except (shutil.Error, OSError) as error:
        info_object.errors.append(
            errors.SysError(error.errno, error.strerror, error.filename)
        )


def get_valid_clean_parametr_by_remove_all_policy(parametr):
    return parametr


def get_object_list_by_remove_all_policy(
    obj_list,
    parametr_to_match_template
):
    return obj_list


def get_valid_clean_parametr_by_time_policy(timedelta_str):
    min_datetime = datetime.datetime.strptime(
        const.EMPTY_STRING, const.EMPTY_STRING
    )
    try:
        timedelta = datetime.datetime.strptime(
            timedelta_str, const.TIME_DELTA_FORMAT
        ) - min_datetime
    except ValueError:
        timedelta = datetime.datetime.strptime(
            const.MAX_TIME_IN_TRASH, const.TIME_DELTA_FORMAT
        ) - min_datetime

    low_bound_time = datetime.datetime.today() - timedelta

    return low_bound_time


def get_object_list_by_time_policy(obj_list, low_bound_time):
    result_list = []

    sort_by_deletion_date(obj_list)
    for obj in obj_list:
        if obj.deletion_date < low_bound_time:
            result_list.append(obj)
        else:
            break

    return result_list


def get_valid_parametr_by_size_time_policy(max_size):
    result_size = max_size
    try:
        if max_size <= 0 or max_size > const.MAX_TRASH_SIZE_IN_BYTES:
            result_size = const.MAX_TRASH_SIZE_IN_BYTES
    except ValueError:
        result_size = const.MAX_TRASH_SIZE_IN_BYTES

    return result_size


def get_object_list_by_size_time_policy(obj_list, max_size):
    total_size = sum(obj.size for obj in obj_list)
    obj_count = len(obj_list)
    pointer = 0

    sort_by_deletion_date(obj_list)

    while (total_size >= max_size and pointer < obj_count):
        total_size -= obj_list[pointer].size
        pointer += 1

    return obj_list[:pointer]
