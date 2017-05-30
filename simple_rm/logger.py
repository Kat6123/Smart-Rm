# -*- coding: utf-8 -*-
import logging

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "notset": logging.NOTSET
}


def set_logger(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    log_level="warning",
    write_to_stderr=True,
    logfile_path=None
):
    """
    Tune logger

    Set logger which write to:
    1) stderr by default
    2) specified logfile
    3) or both
    It is possible to set own format and log level.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVELS[log_level])
    formatter = logging.Formatter(format)

    if write_to_stderr or logfile_path:
        if write_to_stderr:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        if logfile_path:                # If not exist?
            file_handler = logging.FileHandler(logfile_path)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    else:
        root_logger.disabled = True
