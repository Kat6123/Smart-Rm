# -*- coding: utf-8 -*-


class MoveAndAskNewNameForMovableObject(Mover):
    def _watch(self, path, destination):
        super(MoveAndRaiseExceptionIfSamenameFiles, self)._watch(
            path,
            destination
        )
        if self.already_exists:
            new_name = raw_input("Enter new name for {0}:".format(path))
            if new_name:
                self.final_path = join(self.destination, new_name)
            else:
                raise SystemError(             # Or just message?
                    "Already exists {0} in {1}"
                    "".format(self.source, self.destination)
                )

    def _do(self):
        move_tree(self.source, self.final_path)
        return self.final_path
