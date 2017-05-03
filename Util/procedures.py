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

    source, targets = ' '.join(words(line)[1][1:]).split('TO')[:]
    targets = targets.strip().upper()
    source = source.strip().upper()
    targets = targets.split()
    target = ''
    for trgt in targets:
        trg = trgt
        idx = ''
        if trgt.find('(') != -1:
            trg, idx = trgt.split('(')[:]
            idx = '[{}]'.format(idx[:-1])
        target += '{}{} = '.format(references['"{}"'.format(trg)]['def'], idx)

    src = source
    idx = ''
    if src.startswith('(AD='):
        source = AD[''.join(src.split('=')[1])[:-1]]
    elif src.startswith('LEFT'):
        source = src.split()[1]
    elif src.startswith('EDITED'):
        source = ''.join(src.split('(EM=')[0]).split()[1]
    elif src.find('(') != -1:
        source, idx = src.split('(')[:]
        idx = '[{}]'.format(idx[:-1])
    source = '{}{}'.format(references.get(u'{}'.format(source),
                           references.get('"{}"'.format(source),
                           {})).get('def', source), idx)
    ret = '' if target.replace('=','').strip() == source else '{}{}'.format(target, source)
    return ret

