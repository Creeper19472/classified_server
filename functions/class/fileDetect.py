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
                raise SyntaxError('Missing \'</blocked>\'')
            else:
                blockends = blockends + 10
            if level >= 5:
                text = text.replace(text[blockstarts:blockends], text[blockstarts+9:blockends-10])
            else:
                text = text.replace(text[blockstarts:blockends], '[数据删除]')
        return text
