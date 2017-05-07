# -*- coding: utf-8 -*-
import errno
import logging
import os
import os.path
import stat

from smart_rm.core.error import (
    AccessError,
    ExistError,
    SystemError
)
from smart_rm.utils.simple_os_actions import move_tree
from smart_rm.utils.constants import ROOT


class DryRunMixin(object):
    def __init__(
        self,
        dry_run=False
    ):
        if dry_run:
            self.run = self._dry_run
        else:
            self.run = self._execute

    def _dry_run(self, *args, **kwargs):
        self.watch(*args, **kwargs)

    def _execute(self, *args, **kwargs):
        self.watch(*args, **kwargs)
        return self.do()


class Mover(DryRunMixin):
    special_file_modes = [
        stat.S_ISBLK, stat.S_ISCHR,
        stat.S_ISFIFO, stat.S_ISSOCK
    ]

    special_directories = [
        os.path.join(ROOT, root_inner) for root_inner in os.listdir(ROOT)
    ] + [ROOT]

    def __init__(self, dry_run=False):
        super(Mover, self).__init__(dry_run)

        self.source = self.destination = self.final_path = ""
        self.already_exists = False

        self.move = self.run

    def watch(self, source, destination):
        logging.info("Start checking")

        self.tune_paths(source, destination)

        self.check_path_existance(self.source)
        self.check_path_existance(self.destination)

        self.check_distance_is_directory()
        self.check_directory_access(os.path.dirname(self.source))  # Improve
        self.check_directory_access(self.destination)

        if os.path.isfile(self.source):
            self.check_special_file()
        elif os.path.isdir(self.source):
            self.check_system_directory

        self.check_cycle()
        self.check_empty_space()

        if os.path.exists(self.final_path):
            logging.warning("Already exists \"{0}\"".format(self.final_path))
            self.already_exists = True

        logging.info("Stop checking")

    def do(self):
        if self.already_exists:
            raise SystemError(
                "Already exists \"{0}\" in \"{1}\""
                "".format(self.source, self.destination)
            )
        move_tree(self.source, self.final_path)

        return self.final_path

    def tune_paths(self, source, destination):
        self.source = source
        self.destination = destination
        self.final_path = (
            os.path.join(
                self.destination,
                os.path.basename(self.source)
            )
        )

    def check_path_existance(self, path):
        logging.info("Check \"{0}\" existance".format(path))

        if not os.access(os.path.dirname(path), os.R_OK):
            raise AccessError(
                errno.EACCES, os.strerror(errno.EACCES), os.path.dirname(path)
            )
        elif not os.path.exists(path):
            raise ExistError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        logging.info("Pass check")

    def check_distance_is_directory(self):
        logging.info(
            "Check distance \"{0}\" is directory"
            "".format(self.destination)
        )

        if not os.path.isdir(self.destination):
            raise SystemError(
                "Distance \"{0}\" is not directory"
                "".format(os.path.basename(self.destination))
            )

        logging.info("Pass check")

    def check_directory_access(self, directory):
        logging.info(
            "Check directory \"{0}\" has \"write\" and \"execute\" access"
            "".format(directory)
        )

        if not (os.access(directory, os.W_OK) and
                os.access(directory, os.X_OK)):
            raise AccessError(
                errno.EACCES, os.strerror(errno.EACCES), directory
            )

        logging.info("Pass check")

    def check_special_file(self):
        logging.info("Check file \"{0}\" is general".format(self.source))

        if os.getuid:                      # Explain!
            mode = os.stat(self.source).st_mode
            for special_mode in self.special_file_modes:
                if special_mode(mode):  # TODO: different types
                    raise AccessError(
                        errno.EACCES, "Not regular file", self.source
                    )

        logging.info("Pass check")

    def check_system_directory(self):          # remove
        logging.info(
            "Check system directory \"{0}\"".format(self.source)
        )

        if os.getuid:
            for special_directory in self.special_directories:
                if self.source == special_directory:
                    raise AccessError(
                        errno.EACCES, "System directory", self.source
                    )
            if os.path.ismount(self.source):
                raise AccessError(errno.EACCES, "Mount point", self.source)

        logging.info("Pass check")

    def check_cycle(self):          # Explain in doc!
        logging.info("Check name cycle \"{0}\"".format(self.source))

        prefix = os.path.commonprefix([self.source, self.destination])
        if prefix == self.source:
            raise SystemError(
                "Cannot move \"{0}\" into itself \"{1}\""
                "".format(self.source, self.destination)
            )

        logging.info("Pass check")

    def check_empty_space(self):
        pass
