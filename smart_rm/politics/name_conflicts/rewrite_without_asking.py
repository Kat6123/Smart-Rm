# -*- coding: utf-8 -*-
# need mode to choose rename or not


class MoveAndRewriteIfSamenameFilesWithoutAsking(Mover):
    def _watch(self, source, destination):
        super(MoveAndRewriteIfSamenameFilesWithoutAsking, self)._watch(
            source, destination
        )

        if self.already_exists:
            pass

    def _do(self):
        if self.already_exists:             # TODO: CHANGE!
            with open(self.final_path, "w") as target:
                with open(self.source, "r") as path:
                    target.write(path.read())
            remove_tree(self.source)
        else:
            move_tree(self.source, self.final_path)
        return self.final_path
