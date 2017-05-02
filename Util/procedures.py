# -*- coding: utf-8 -*-

from Util.warehouse import COMMANDS_NATURAL, AD
from Util.HOFs import *

def procCmd(line, references):
    firstWord = word(line,1)
#    if firstWord in COMMANDS_NATURAL:
    if firstWord in 'MOVE':
        return eval('proc{}(line, references)'.format(firstWord))
    else:
        return line

def procMOVE(line, references):
    sources, targets = ' '.join(words(line)[1][1:]).split('TO')[:]
    sources = sources.split()
    targets = targets.split()
    target = ''
    for trgt in targets:
        trg = trgt
        idx = ''
        if trgt.find('(') != -1:
            trg, idx = trgt.split('(')[:]
            idx = '[{}]'.format(idx[:-1])
        target += '{}{} = '.format(references['"{}"'.format(trg)]['def'], idx)

    for srcs in sources:
        src = srcs
        idx = ''
        if srcs.startswith('(AD='):
            source = AD[''.join(srcs.split('=')[1])[:-1]]
            break
        elif srcs.find('(') != -1:
            src, idx = trgt.split('(')[:]
            idx = '[{}]'.format(idx[:-1])
        try:
            source = '{}{} = '.format(references['"{}"'.format(src)]['def'], idx)
        except:
            source = src

    return '{}{}'.format(target, source)

