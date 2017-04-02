# -*- coding: utf-8 -*-


class Error (Exception):         # TODO:
    def __init__(self, _error):
        super(Error, self).__init__(str(_error))
