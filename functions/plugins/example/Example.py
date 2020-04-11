# -*- coding: UTF-8 -*-

### EXAMPLE PLUGIN ###

# This is a example plugin.

### EXAMPLE PLUGIN ###

# Note: All four fields are required, but their order is not limited.

import sys

lists = ['Plug1', 'Plug2']


def Plug1():
    return 'aa'

def Plug2():
    return 'bb'

def main():
    for i in lists:
        Replace = i.replace('\'', '')
        exec(Replace + '()')
