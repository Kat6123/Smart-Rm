# -*- coding: utf-8 -*-
from os import linesep


class Error (Exception):         # TODO:
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        result = linesep.join(self.errors)
        return result
