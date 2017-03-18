# -*- coding: utf-8 -*-


class error(Exception):         # TODO:
    def __init__(self, _error):
        super(error, self).__init__(str(_error))
