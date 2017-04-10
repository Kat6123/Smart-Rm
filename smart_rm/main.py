#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from config.set import Config
from smart_remove import RemoveManager
from basket import manage_basket


def main():
    config = Config()
    remover = RemoveManager(config)
    remover.remove_using_all_config_parametres()
    manage_basket(config)


if __name__ == '__main__':
    main()
