# -*- coding:utf-8 -*-

class Blocked:
    def ReplaceBlock(text, level):
        if text.find('<blocked>') == -1:
            return text
        blockpos = []
        while True:
            blockstarts = text.find('<blocked>', blockstarts) + 8
            if blockstarts == -1:
                break
            blockends = text.find('</blocked>', blockstarts) + 9
            if blockends == -1:
                raise SyntaxError('Missing \'</blockends>\'')
            blockpos.append((blockstarts, blockends))
        return blockpos
        
print(Blocked.ReplaceBlock('<blocked>', 1))
