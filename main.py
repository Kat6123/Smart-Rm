#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from config.set import Config
from smart_remove import(
    manage_remove,
    manage_basket)


def main():
    config = Config()
    manage_remove(config)
    manage_basket(config)


if __name__ == '__main__':
    main()
