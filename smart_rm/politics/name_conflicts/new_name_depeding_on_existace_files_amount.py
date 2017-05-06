# -*- coding: utf-8 -*-


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
