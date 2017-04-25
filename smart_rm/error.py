# -*- coding: utf-8 -*-


class SmartRMError(EnvironmentError):
    pass


class PermissionError(SmartRMError):
    pass


class ExistError(SmartRMError):
    pass


class ModeError(SmartRMError):
    pass


class OtherOSError(SmartRMError):
    pass
