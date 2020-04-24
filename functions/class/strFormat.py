# -*- coding: utf-8 -*-

import colset

multicol = colset.Colset()

class StrFormat:
    def INFO():
        return "[" + multicol.Green("INFO") + "] "

    def WARN():
        return "[" + multicol.Yellow("WARN") + "] "

    def ERROR():
        return "[" + multicol.Red("ERROR") + "] "
