# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''
RESERV = 'GLOBAL LOCAL PARAMETER'

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
        try:
            line = ilines.next()
        except StopIteration:
            break
        if word(line, 1) in RESERV:
            joinLines.append(line)
            continue

        holder.append(line if not holder else line.strip())
        try:
            line = ilines.next()
        except StopIteration:
            joinLines.append(" ".join(holder))
            stop = True
            continue
        if not word(line, 1).isdigit():
            holder.append(line if not holder else line.strip())
            joinLines.append(" ".join(holder))
            holder = []
        else:
            joinLines.append(" ".join(holder))
            holder = []
            holder.append(line if not holder else line.strip())


    return joinLines
