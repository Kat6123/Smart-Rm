#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from log.logger import tune_logger
from config.set import Config
from smart_rm import AdvancedRemover
# from basket import AdvancedBasket


def main():
    config = Config()

    if config.modes["silent"]:          # XXX
        tune_logger(write_to_stderr=False,
                    logfile_path=config.file_paths_to["log"])
        config.modes["not_confirm_rm"] = True
    else:
        tune_logger(logfile_path=config.file_paths_to["log"])

    remover = AdvancedRemover(
        config.file_paths_to["basket"],
        config.modes["confirm_rm_always"],
        config.modes["not_confirm_rm"],
        config.modes["confirm_if_file_has_not_write_access"],
        config.modes["dry_run"],
        config.politics["conflict_resolution"]
    )

    if config.actions["remove"]["tree"]:
        remover.remove_trees(config.file_paths_to["remove"])
    elif config.actions["remove"]["directory"]:
        remover.remove_directories(config.file_paths_to["remove"])
    elif config.actions["remove"]["file"]:
        remover.remove_files(config.file_paths_to["remove"])


if __name__ == '__main__':
    main()
