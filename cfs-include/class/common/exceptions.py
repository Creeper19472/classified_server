# -*- coding:utf-8 -*-

class HackException(PermissionError):
    def __init__(self, cause='HackException'):
        self.cause = cause

    def __str__(self):
        return self.cause

class PortNotAvailable(OSError):
    def __init__(self):
        self.cause = 'The port is used or blocked'

    def __str__(self):
        return self.cause

