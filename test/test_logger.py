#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from unittest import (
    TestCase,
    main
)
from logging import (
    debug,
    info,
    warning,
    error,
    critical,
    DEBUG,
    INFO
)
from logger import tune_logger
from sys import stderr
from os import remove
from contextlib import contextmanager
#%(levelname)-8s [%(asctime)s] %(message)s


class TestLogger(TestCase):
    def setUp(self):
        self.stderr_file_name = "stderr"
        self.logfile = "logfile"

    def tearDown(self):
        remove(self.stderr_file_name)
        remove(self.logfile)
        del self.stderr_file_name
        del self.logfile

    def test_levels(self):          # TODO
        tune_logger(log_level=DEBUG, logfile_path=self.logfile)
        self._write_logs()
        with (
              open(self.stderr_file_name, "r") as std,
              open(self.logfile, 'r') as logfile)):
            self.assertEqual(self.fixture, range(1, 10))

    def _write_logs(self):
        with(
            redirected(stderr_name=self.stderr_file_name),
            open(self.logfile, 'w')
        ):
            debug("debug")
            info("info")
            warning("warning")
            error("error")
            critical("critical")


@contextmanager
def redirected(stderr_name):
    saved_stderr = stderr
    stderr = open(stderr_name, 'w')
    yield
    stderr = saved_stderr

if __name__ == '__main__':
    main()
