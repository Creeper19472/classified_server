# -*- coding: utf-8 -*-

import shelve
import sys

class shelveObj(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.shelveObj = shelve.open(self.filepath)

    def check(checkdata):
        pass
