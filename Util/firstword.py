#!/usr/bin/env python
# -*- coding: utf-8 -*-


from DirFileList import *
from HOFs import *

path = r'C:\Natural\Originais\PGM'

ehPgm = lambda pgm: pgm[-3:].upper() == 'NSN' or pgm[-3:].upper() == 'NSP'

dirFileList = DirFileList()
dirFileList.setDirFileList(path)
pgmList = dirFileList.getDirFileList()
setcmd = set()

for pgm in filter(ehPgm, pgmList):
    lines = open(pgm).readlines()
    clearLines =  map(l480, filter(isNotRem, lines))
    clearLines =  filter(isNotBlank, clearLines)
    lPgm = clearLines[clearLines.index(filter(isEndDefine, clearLines)[0])+1:]
    for line in lPgm:
        setcmd.add(line.split()[0])

with open(r'firstword.txt', 'w') as cmds:
    for s in setcmd:
        cmds.write(s + '\n')
