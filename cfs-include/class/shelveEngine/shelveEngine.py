# -*- coding: utf-8 -*-

import shelve
import sys


class shelveObj(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.shelveObj = shelve.open(self.filepath)
        self.TableName = None
        self.Table = None

    def close(self):
        self.shelveObj.close()

    def createTable(self, TableName):
        self.shelveObj[TableName] = {
            '__init__': TableName + sys.version
            }

    def locate(self, TableName):
        try:
            if bool(self.shelveObj[TableName]['__init__']) is not False:
                self.TableName = TableName
                self.Table = self.shelveObj[TableName]
            else:
                raise
        except:
            raise ValueError('Can\'t locate the Table %s. Does this table exist?' % TableName)
            
    def set(self, key, data):
        try:
            self.Table[key] = data
        except TypeError:
            raise TypeError('Failed to locate the Table. Did you located the Table?')

    def delete(self, key):
        try:
            self.Table[key] = None
        except TypeError:
            raise TypeError('Failed to locate the Table. Did you located the Table?')

    def search(self, key):
        try:
            return self.Table[key]
        except TypeError:
            raise TypeError('Failed to locate the Table. Did you located the Table?')
        except ValueError:
            return None

    def IsKeyExist(self, key):
        try:
            if bool(self.Table[key]) is not False:
                return True
            else:
                return False
        except TypeError:
            raise TypeError('Failed to locate the Table. Did you located the Table?')
        except KeyError:
            return False
