# -*- coding:utf-8 -*-

class Blocked:
    def ReplaceBlock(text, level):
        if text.find('<blocked>') == -1:
            return text
        for i in :
            blockstarts = text.find('<blocked>')
            blockends = text.find('</blocked>', blockstarts)
