# -*- coding: utf-8 -*-


class SmartError(EnvironmentError):
    pass


class AccessError(SmartError):
    pass


class ExistError(SmartError):
    pass


class ModeError(SmartError):
    pass


class SystemError(SmartError):
    pass
