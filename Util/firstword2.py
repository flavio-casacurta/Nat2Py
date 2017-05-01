#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from DirFileList import *
from HOFs import *

path = r'C:\Natural\Originais\PGM'

ehPgm = lambda pgm: pgm[-3:].upper() == 'NSN' or pgm[-3:].upper() == 'NSP'

dirFileList = DirFileList()
dirFileList.setDirFileList(path)
pgmList = dirFileList.getDirFileList()
cmds = open(r'firstword2.txt', 'w')

for pgm in filter(ehPgm, pgmList):

    baseName = os.path.basename(pgm)
    namePgm = baseName[:baseName.index('.')]
    lines = open(pgm).readlines()
    clearLines =  map(l480, filter(both(isNotBlank, isNotRem), lines))
    lPgm = clearLines[clearLines.index(filter(isEndDefine, clearLines)[0])+1:]
    for line in lPgm:
        cmds.write('{} - {}\n'.format(namePgm, line.split()[0]))
cmds.close()
