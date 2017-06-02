# -*- coding: utf-8 -*-
"""Contain library errors."""


class SmartError(EnvironmentError):
    """SmartError is super class for other module errors.

    It inherits from built-in EnvironmentError. That is why contains
    same attributes. And can be instantiated with:
        error code, message string, source file.
    For more information look 'EnvironmentError' documentation.
    """
    pass


class AccessError(SmartError):
    """Raises when file or directory has no permissions."""
    pass


class ExistError(SmartError):
    """Raises when file or directory doesn't exist"""
    pass


class ModeError(SmartError):
    """Raises when wrong paths in method remove in Trash class."""
    pass


class SysError(SmartError):
    """Raises when other errors which are connected with operation system."""
    pass
