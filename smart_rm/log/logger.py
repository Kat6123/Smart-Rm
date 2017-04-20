#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from logging import (
    INFO,
    getLogger,
    Formatter,
    StreamHandler,
    FileHandler)


def tune_logger(
        format=u'%(levelname)-8s [%(asctime)s] %(message)s',
        log_level=INFO,
        write_to_stderr=True,
        logfile_path=""
):
    """
    Tune logger

    Set logger which write to:
    1) stderr by default
    2) specified logfile
    3) or both
    It is possible to set own format and log level.
    """
    root_logger = getLogger()
    root_logger.setLevel(log_level)

    formatter = Formatter(format)

    if write_to_stderr:
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if logfile_path:                # If not exist?
        file_handler = FileHandler(logfile_path)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
