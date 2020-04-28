# -*- coding:utf-8 -*-

class Blocked:
    def ReplaceBlock(text, level):
        if text.find('<blocked>') == -1:
            return text
        blockpos = []
        blockends = 0
        while True:
            blockstarts = text.find('<blocked>')
            if blockstarts == -1:
                break
            blockends = text.find('</blocked>', blockstarts)
            if blockends == -1:
                raise SyntaxError('Missing \'</blockends>\'')
            else:
                blockends = blockends + 10
            text = text.replace(text[blockstarts:blockends], '[数据删除]')
        return text
