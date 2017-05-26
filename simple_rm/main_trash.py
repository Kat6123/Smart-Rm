#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
from simple_rm.config import (
    Config,
    ArgumentParser
)
from trash import Trash


def main():
    config = Config()
    parser = ArgumentParser()
    config.override(parser.get_config())

    trash = Trash(
        trash_location=config.path_to["trash"],
        remove_mode=config.remove_mode
    )

    if parser.args.
    trash.remove(parser.args.path)


if __name__ == '__main__':
    main()
