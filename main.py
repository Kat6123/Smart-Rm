#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from sys import argv
from error import error
from parse import parser
from remove import rm_file
from remove import rm_dir
from remove import rm_tree
from remove import rmb
from remove import show_bucket


def main():
    args = parser().parse_args(argv[1::])

    try:
        if args.show:
            show_bucket()
        elif args.bukt:
            rmb(args.path)
        elif args.rec:
            rm_tree(args.path)
        elif args.dir:
            rm_dir(args.path)
        else:
            rm_file(args.path)
    except error as e:
        print e


if __name__ == '__main__':
    main()
