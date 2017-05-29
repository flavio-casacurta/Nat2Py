# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''
import re
from change import change
from warehouse import *
from HOFs import *
from DataPatterns import *

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
    homoocurs = []
    level_ant = 1
    occurs_gr = 0
    for line in homolines:
        match = DataPatterns.row_pattern_redefine.match(line.strip())
        if not match:
            match = DataPatterns.row_pattern.match(line.strip())
            if match:
                match = match.groupdict()
                level = int(match['level'])
                if not match['length'] and not match['type'] and match['occurs']:
                    occurs_gr = match['occurs']
                    line = line.replace("(1:{})".format(occurs_gr), "")
                    level_ant = level
                else:
                    if level <= level_ant:
                        occurs_gr = 0
                if level > level_ant:
                    if occurs_gr:
                        occ1 = "1:{}".format(occurs_gr)
                        if match['occurs']:
                            occ2 = "1:{}".format(match['occurs'])
                            line = line.replace(occ2, occ1 + ',' + occ2)
                        else:
                            line = line.replace(')', '/'+occ1 + ')')
        homoocurs.append(line)
    return homoocurs


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


def indentation(lines):
    sp = 0
    indentLines = ""

    for line in lines:
        firstWord = word(line, 1).lower()
        if firstWord in INDENT:
            init = INDENT.get(firstWord, {}).get('init', None)
            if isinstance(init, int):
                sp = sp + init if init and sp else init if sp > 0 else sp
            addsub = INDENT.get(firstWord, {}).get('ad', None)
        else:
            addsub = None
        if firstWord.startswith('end'):
            line = ''
        else:
            line = """{}{}\n""".format(' '*sp, line.strip())
        indentLines += line
        if addsub:
            sp += addsub

    return indentLines
