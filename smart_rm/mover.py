# -*- coding: utf-8 -*-
from shutil import (
    move
)
from os import (
    listdir,
    strerror,
    stat,
    getuid,
    R_OK,
    W_OK,
    X_OK,
    access
)
from os.path import (
    isdir,
    abspath,
    basename,
    join,
    exists,
    ismount,
    isfile,
    dirname,
    commonprefix
)
from error import (
    PermissionError,
    ExistError,
    OtherOSError
)
from stat import (
    S_ISBLK,
    S_ISCHR,
    S_ISFIFO,
    S_ISSOCK
)
from errno import (
    ENOENT,
    EACCES
)
from remove import (
    remove_tree,
    move_tree
)


def check_path_existance(path):
    abs_path = abspath(path)

    if not access(dirname(abs_path), R_OK):
        raise PermissionError(EACCES, strerror(EACCES), dirname(abs_path))
    elif not exists(abs_path):
        raise ExistError(ENOENT, strerror(ENOENT), abs_path)


class DryRunMixin(object):
    def __init__(
        self,
        dry_run=False
    ):
        if dry_run:
            self.move = self.dry_run
        else:
            self.move = self.execute

    def dru_run(self, *args, **kwargs):
        self._watch(*args, **kwargs)

    def execute(self, *args, **kwargs):
        self._watch(*args, **kwargs)
        return self._do()


class Mover(DryRunMixin):           # move to directory
    def __init__(self, dry_run=False):
        super(Mover, self).__init__(dry_run)

        self.source, self.destination, self.final_path = None, None, None   # ?
        self.already_exists = False

        self._special_file_modes = [S_ISBLK, S_ISCHR, S_ISFIFO, S_ISSOCK]
        sys = ["/" + path for path in listdir("/")]
        self._special_directories = ["/"] + sys

    def _watch(self, source, destination):  # Check destin has write access
        self.tune_paths(source, destination)

        check_path_existance(self.source)
        check_path_existance(self.destination)

        self.check_distance_is_directory()
        self.check_directory_access(dirname(self.source))       # Improve
        self.check_directory_access(self.destination)

        if isfile(self.source):
            self.check_special_file()
        elif isdir(self.dource):
            self.check_system_directory

        self.check_cycle()
        self.check_empty_space()

        if exists(self.final_path):
            self.already_exists = True

    def _do(self):
        if self.exists:
            raise OtherOSError(
                "Already exists {0} in {1}"
                "".format(self.source, self.destination)
            )
        move_tree(self.source, self.final_path)

        return self.final_path

    def tune_paths(self, source, destination):
        self.source = abspath(source)
        self.destination = abspath(destination)
        self.final_path = join(dirname(destination), basename(source))

    def check_distance_is_directory(self):
        if not isdir(self.destination):
            raise OtherOSError("Distance is not directory")

    def check_directory_access(self, directory):
        if not access(directory, W_OK) and access(directory, X_OK):
            raise PermissionError(EACCES, strerror(EACCES), file)

    def check_special_file(self):
        if getuid:                      # Explain!
            mode = stat(self.source).st_mode
            for special_mode in self._special_file_modes:
                if special_mode(mode):  # TODO: different types
                    raise PermissionError(
                        EACCES, "Not regular file", self.source
                    )

    def check_system_directory(self):
        if getuid:
            for special_directory in self._special_directories:
                if self.source == special_directory:
                    raise PermissionError(
                        EACCES, "System directory", self.source
                    )
            if ismount(self.source):
                raise PermissionError(EACCES, "Mount point", self.source)

    def check_cycle(self):          # Explain in doc!
        prefix = commonprefix([self.source, self.destination])
        if prefix == self.source:
            raise OtherOSError(
                "Cannot move {0} into itself {1}"
                "".format(self.source, self.destination)
            )

    def check_empty_space(self):
        pass


# need mode to choose rename or not
class MoveAndRewriteIfSamenameFilesWithoutAsking(Mover):
    def _watch(self, source, destination):
        super(MoveAndRewriteIfSamenameFilesWithoutAsking, self)._watch(
            source, destination
        )

        if self.exists:
            pass

    def _do(self):
        if self.exists:             # TODO: CHANGE!
            with open(self.final_path, "w") as target:
                with open(self.source, "r") as path:
                    target.write(path.read())
            remove_tree(self.source)
        else:
            move_tree(self.source, self.final_path)
        return self.final_path


# need message!
class MoveAndRewriteSamenameFilesWithAsking(Mover):
    def __init__(self, dry_run=False):
        super(MoveAndRewriteSamenameFilesWithAsking, self).__init__(dry_run)
        self.answer = False

    def _watch(self, path, destination):
        super(MoveAndRewriteSamenameFilesWithAsking, self)._watch(
            path, destination
        )

        if self.exists:
            self.answer = raw_input(
                "Do you want to rewrite {0} in {1}"
                "".format(basename(path), destination)
            )
        # if not answer:
        #     return

    def _do(self):
        if self.exists:
            if self.answer:     # Change
                MoveAndRewriteIfSamenameFilesWithoutAsking().execute(
                    self.source,
                    self.destination
                )
            else:
                return
        else:
            move_tree(self.source, self.final_path)
            return self.final_path


class MoveAndRaiseExceptionIfSamenameFiles(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )       # add description

        if self.exists:
            pass

    def _do(self):
        if self.exists:
            raise OtherOSError(
                "Already exists {0} in {1}"
                "".format(self.source, self.destination)
            )
        move_tree(self.source, self.final_path)
        return self.final_path


class MoveAndAskNewNameForMovableObject(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )
        if self.exists:
            new_name = raw_input("Enter new name for {0}:".format(path))
            if new_name:
                self.final_path = join(self.destination, new_name)
            else:
                raise OtherOSError(             # Or just message?
                    "Already exists {0} in {1}"
                    "".format(self.source, self.destination)
                )

    def _do(self):
        move_tree(self.source, self.final_path)
        return self.final_path


class MoveAndMakeNewNameDependingOnAmount(Mover):
    def _watch(self, path, destination):
        super(MoveAndMakeNewNameDependingOnAmount, self)._watch(
            path,
            destination
        )
        if self.exists:
            count_of_samename_files = listdir(destination).count(
                basename(path)
            )
            self.final_path = join(
                destination,
                basename(path) + ".{0}".format(count_of_samename_files)
            )

    def _do(self):
        move(self.source, self.final_path)
        return self.final_path
