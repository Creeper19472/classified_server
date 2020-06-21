# -*- coding: utf-8 -*-

import colset, time 

multicol = colset.Colset()

class StrFormat:
    def INFO():
        return "[" + time.asctime() + multicol.Green(" INFO") + "] "

    def WARN():
        return "[" +  time.asctime() + multicol.Yellow(" WARN") + "] "

    def ERROR():
        return "[" +  time.asctime() + multicol.Red(" ERROR") + "] "
