#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sys import argv
from argparse import (
    ArgumentParser
)


def parser():
    parser = ArgumentParser(add_help=True)

    exclusive_modes = parser.add_mutually_exclusive_group()

    parser.add_argument('path', nargs='+',
                        help='Path to file')
    parser.add_argument('-d', '--dir', dest='rm_empty_directory',
                        action='store_true',
                        help='Remove empty directories')
    parser.add_argument('-r', '-R', '--recursive',
                        dest='rm_directory_recursively',
                        action='store_true',
                        help='Remove directories and '
                        'their contents recursively')

    exclusive_modes .add_argument('-a', '--ask',
                                  dest='ask_before_remove',
                                  action='store_true',
                                  help='Prompt before every removal')
    exclusive_modes .add_argument('-s', '--silent',
                                  dest='silent_mode',
                                  action='store_true',
                                  help='Launch in silent mode')
    parser.add_argument('-i', '--imitation',
                        dest='remove_imitation',
                        action='store_true',
                        help='Launch in dry-run mode')

    parser.add_argument('--clear',
                        dest='clear_basket',
                        action='store_true',
                        help='Clear basket')
    parser.add_argument('-b', '--basket',           # TODO: Launch without path
                        dest='view_basket_content',
                        action='store_true',
                        help='View basket content')

    return parser.parse_args(argv[1:])


def main():
    args = parser()
    print args.__dict__


if __name__ == '__main__':
    main()
