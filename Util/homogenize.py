# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''
import re
from change import change
from warehouse import DDA
from warehouse import LINEFEED
from warehouse import CMDSPLIT
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

    homolines = []
    filler = 0
    for line in joinLines:
        if 'FILLER' in line:
            filler+=1
            line = re.sub('FILLER', 'FILLER_{:02}'.format(filler), line)
            pattern = re.search('(?P<length>\d+)X', line)
            if pattern:
                match = pattern.groupdict()
                sub = ' (A{})'.format(match['length'])
                line = re.sub('\s+\d+X', sub, line)
        homolines.append(line)
    return homolines


def homogenize_proc(lines):
    joinLines = []
    holder = []
    ilines = iter(lines)
    stop = False

    while True:
        if stop:
            break

        if not holder:
            try:
                line = ilines.next()
            except StopIteration:
                break

        if not holder:
            holder.append(line)

        try:
            line = ilines.next()
        except StopIteration:
            joinLines.append(" ".join(holder))
            stop = True
            continue

        if word(line, 1) not in LINEFEED:
            holder.append(" " + line.strip())
        else:
            joinLines.append(" ".join(holder))
            holder = []
            holder.append(line)

    joinLines = splitCmd(joinLines)
    joinLines = orEq(joinLines)

    return joinLines


def splitCmd(lines):
    joinLines = []

    for line in lines:
        wrd = words(line)
        for w in xrange(1, wrd[0]):
            if wrd[1][w] in CMDSPLIT:
                wrd1 = word(line, 1)
                if wrd[1][w] == wrd1:
                    lw = len(wrd1)
                    idx = line[lw:].index(wrd1) + 2
                    ll = len(wrd1 + ' ' + line[lw:idx])
                    joinLines.append(wrd1 + ' ' + line[lw:idx])
                    line = line[ll:]
                else:
                    joinLines.append(line[:line.index(wrd[1][w])].strip())
                    line = line[line.index(wrd[1][w]):]
        joinLines.append(line)

    return joinLines


def orEq(lines):
    joinLines = []
    ilines = iter(lines)
    stop = False
    if_old = ""

    while True:
        if stop:
            break
        try:
            line = ilines.next()
        except StopIteration:
            stop = True
            continue
        if line.strip().startswith('IF'):
            line = line.replace("=", "EQ")
            if_old = "".join("".join(line.split("EQ")[0]).strip().split()[1:])
        if line.strip().startswith("OR="):
            line = line.replace("OR=", "OR {} EQ".format(if_old)).strip()
        joinLines.append(line)

    return joinLines