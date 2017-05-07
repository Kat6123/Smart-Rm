# -*- coding: utf-8 -*-


class MoveAndRaiseExceptionIfSamenameFiles(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )       # add description

        if self.already_exists:
            pass

    def _do(self):
        if self.already_exists:
            raise SystemError(
                "Already exists {0} in {1}"
                "".format(self.source, self.destination)
            )
        move_tree(self.source, self.final_path)
        return self.final_path
