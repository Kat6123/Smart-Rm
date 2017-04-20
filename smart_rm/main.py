#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from log.logger import tune_logger
from logging import (
    debug,
    info,
    warning,
    error,
    critical,
    DEBUG,
    INFO
)


def main():
    tune_logger(log_level=DEBUG, logfile_path="file")

    debug("debug")
    info("info")
    warning("warning")
    error("error")
    critical("critical")

if __name__ == '__main__':
    main()
