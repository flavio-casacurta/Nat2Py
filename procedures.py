# -*- coding: utf-8 -*-

from Util.warehouse import COMMANDS_NATURAL
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
    for trgt in targets:
        if references[trgt]['type'] == 'C':
            return ''
        target += '{} = '.format(references[trgt]['def'])

    for srcs in sources:



