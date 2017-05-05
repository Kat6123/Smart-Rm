# -*- coding: utf-8 -*-
import errno
import os
import os.path
import stat
from error import (
    AccessError,
    ExistError,
    SystemError
)
from remove import (
    move_tree
)


class DryRunMixin(object):
    def __init__(
        self,
        dry_run=False
    ):
        if dry_run:         # ? move to
            self.move = self.dry_run
        else:
            self.move = self.execute

    def dru_run(self, *args, **kwargs):
        self._watch(*args, **kwargs)

    def execute(self, *args, **kwargs):
        self._watch(*args, **kwargs)
        return self._do()


class Mover(DryRunMixin):           # shutil.move to directory
    def __init__(self, dry_run=False):
        super(Mover, self).__init__(dry_run)

        self.source, self.destination, self.final_path = None, None, None   # ?
        self.already_exists = False

        self._special_file_modes = [
            stat.S_ISBLK, stat.S_ISCHR,
            stat.S_ISFIFO, stat.S_ISSOCK
        ]
        sys = ["/" + path for path in os.listdir("/")]
        self._special_directories = ["/"] + sys

    def _watch(self, source, destination):
        self.tune_paths(source, destination)

        check_path_existance(self.source)
        check_path_existance(self.destination)

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
            self.already_exists = True

    def _do(self):
        if self.already_exists:
            raise SystemError(
                "Already exists {0} in {1}"
                "".format(self.source, self.destination)
            )
        move_tree(self.source, self.final_path)

        return self.final_path

    def tune_paths(self, source, destination):
        self.source = os.path.abspath(source)
        self.destination = os.path.abspath(destination)
        self.final_path = (
            os.path.join(
                self.destination,
                os.path.basename(self.source)
            )
        )

    def check_distance_is_directory(self):
        if not os.path.isdir(self.destination):
            raise SystemError(
                "Distance {0} is not directory"
                "".format(os.path.basename(self.destination))
            )

    def check_directory_access(self, directory):
        if not os.access(directory, os.W_OK) and os.access(directory, os.X_OK):
            raise AccessError(
                errno.EACCES, os.strerror(errno.EACCES), file
            )

    def check_special_file(self):
        if os.getuid:                      # Explain!
            mode = os.stat(self.source).st_mode
            for special_mode in self._special_file_modes:
                if special_mode(mode):  # TODO: different types
                    raise AccessError(
                        errno.EACCES, "Not regular file", self.source
                    )

    def check_system_directory(self):
        if os.getuid:
            for special_directory in self._special_directories:
                if self.source == special_directory:
                    raise AccessError(
                        errno.EACCES, "System directory", self.source
                    )
            if os.path.ismount(self.source):
                raise AccessError(errno.EACCES, "Mount point", self.source)

    def check_cycle(self):          # Explain in doc!
        prefix = os.path.commonprefix([self.source, self.destination])
        if prefix == self.source:
            raise SystemError(
                "Cannot move {0} into itself {1}"
                "".format(self.source, self.destination)
            )

    def check_empty_space(self):
        pass
