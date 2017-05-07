# -*- coding: utf-8 -*-
import os.path
from smart_rm.core.mover import Mover
from smart_rm.core.remove import move_tree


class MoveAndMakeNewNameDependingOnAmount(Mover):
    def _watch(self, path, destination):
        super(MoveAndMakeNewNameDependingOnAmount, self)._watch(
            path,
            destination
        )
        if self.already_exists:
            count_of_samename_files = os.path.listdir(destination).count(
                os.path.basename(path)
            )
            self.final_path = os.path.join(
                destination,
                os.path.basename(path) + ".{0}".format(count_of_samename_files)
            )

    def _do(self):
        move_tree(self.source, self.final_path)
        return self.final_path
