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
    """Tune 'run' if 'watch', 'do' methods exist, depend on 'dry-run' parametr.

    Subclass should have 'watch' and 'do' methods to use mixin.

    The __init__ method accept 'dry_run' parametr and set 'run'.
    If 'dry_run' then 'run' only 'watch', otherwise 'watch' and 'do'.

    Attributes:
        dry_run (bool): set behavior.

    """
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
    """Using for movement to directory. Can move in dry run mode.

    If you want to move you should use samename method.

    The __init__ method accept 'dry_run' parametr and set method 'move'.

    Attributes:
        source (str): Path to source for 'move'. Should be absolute.
        destination (str): Path to destination for 'move'.
            Should be absolute path to folder.
        final_path (str): Path to 'source' in 'destination' folder.
        already_exists (bool): Set when move if 'final_path' already exists
            in destination folder.

    """
    special_file_modes = [
        stat.S_ISBLK, stat.S_ISCHR,
        stat.S_ISFIFO, stat.S_ISSOCK
    ]
    """List of functions.

    Let define if file is 'block', 'character device', 'named pipe' or
    'socket'.
    """
    special_directories = [
        os.path.join(ROOT, root_inner) for root_inner in os.listdir(ROOT)
    ] + [ROOT]
    """List of system folders paths. Contains root and all inside folders."""

    def __init__(self, dry_run=False):
        super(Mover, self).__init__(dry_run)

        self.source = self.destination = self.final_path = ""
        self.already_exists = False

        self.move = self.run

    def watch(self, source, destination):
        """Launch all checks and set instance attributes"""
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
        """Move 'source' to 'destination' if it doesn't exist yet.

        Returns:
            string: If has moved return 'final_path', 'None' otherwise

        Raises:
        SystemError: If 'self.already_exists' is True.

        """
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
        """Raises error if path 'parent' unreadable or if 'path' doesn't exist.

        Args:
            path (string): Absolute path.

        Raises:
            AccessError: Path directory hasn't got write access.
            ExistError: Path doesn't exist.

        """

        logging.info("Check \"{0}\" existance".format(path))

        if not os.access(os.path.dirname(path), os.R_OK):
            raise AccessError(
                errno.EACCES, os.strerror(errno.EACCES), os.path.dirname(path)
            )
        elif not os.path.exists(path):
            raise ExistError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        logging.info("Pass check")

    def check_distance_is_directory(self):
        """Check if destination is directory.

        Raises:
            SystemError: 'self.destination' is not directory

        """
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
        """Raises error if can only read 'directory'.

        Args:
            path (string): Absolute path.

        Raises:
            AccessError: If dierctory hasn't gor write and execute rights.

        """
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
        """Check if source is not regular file. Skip if 'sudo'.

        Check if 'source' is one of the type mentioned in class attribute
        'special_file_modes' doc and if without root rights.
        When launch from 'sudo' your 'uid' will be '0' and then skip.

        Raises:
            AccessError: If not sudo and not regular file.

        """
        logging.info("Check file \"{0}\" is general".format(self.source))

        if os.getuid:
            mode = os.stat(self.source).st_mode
            for special_mode in self.special_file_modes:
                if special_mode(mode):  # TODO: different types
                    raise AccessError(
                        errno.EACCES, "Not regular file", self.source
                    )

        logging.info("Pass check")

    def check_system_directory(self):          # remove
        """Check if source is system directory. Skip if 'sudo'.

        Check if 'source' is one of the directories in class attribute
        'special_directories' doc and if without root rights.
        When launch from 'sudo' your 'uid' will be '0' and then skip.

        Raises:
            AccessError: If not sudo, but special directory.

        """
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

    def check_cycle(self):
        """Check if 'source' path is beginning of 'destination' path.

        Raises:
            SystemError: If cycle of names.

        """
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
