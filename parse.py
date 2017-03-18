# -*- coding: utf-8 -*-
from argparse import ArgumentParser


def parser():
    parser = ArgumentParser(add_help=True)

    parser.add_argument('path', help='')                # TODO: add many pathes
    parser.add_argument('-d', '--dir', dest='dir',
                        action='store_true',
                        help='remove empty directories')
    parser.add_argument('-r', '-R', '--recursive',
                        dest='rec',
                        action='store_true',
                        help='remove directories and '
                        'their contents recursively')
    parser.add_argument('-b', '--bucket',               # TODO: change
                        dest='bukt',
                        action='store_true',
                        help='remove to bucket')
    parser.add_argument('--show', action='store_true',  # TODO: Not need path
                        help='show bucket content')

    return parser
