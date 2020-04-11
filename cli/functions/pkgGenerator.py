# -*- coding: UTF-8 -*-

import string

class PackagesGenerator:
    def AuthPackage(account, password):
        Package = {
            'Code' : '11',
            'Title' : 'AuthPackage',
            'Message' : None,
            'Account' : account,
            'Password' : password
            }
        return Package
    
    '''def Message(Title, Msg):
        Package = {
            'Code' : 200,
            'Title' : Title,
            'Message' : Msg
                }
        return Package'''
