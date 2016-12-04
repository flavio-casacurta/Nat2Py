# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''
from warehouse import DDA

from HOFs import *
def homogenize(dda):
    clearLines = filter(isNotBlank, dda)
    joinLines = []
    holder = []
    ilines = iter(clearLines)
    stop = False

    while True:
        if stop:
            break

        if not holder:
            try:
                line = ilines.next()
            except StopIteration:
                break

        if word(line, 1) in DDA:
            joinLines.append(line)
            continue

        if not holder:
            holder.append(line if not holder else line.strip())
        try:
            line = ilines.next()
        except StopIteration:
            joinLines.append(" ".join(holder))
            stop = True
            continue
        if not word(line, 1).isdigit():
            holder.append(line if not holder else line.strip())
        else:
            joinLines.append(" ".join(holder))
            holder = []
            holder.append(line if not holder else line.strip())


    return joinLines
