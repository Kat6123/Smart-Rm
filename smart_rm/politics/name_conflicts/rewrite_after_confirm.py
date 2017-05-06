# -*- coding: utf-8 -*-
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
