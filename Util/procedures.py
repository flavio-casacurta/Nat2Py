# -*- coding: utf-8 -*-

from Util.warehouse import COMMANDS_NATURAL, AD, MASKS
from Util.HOFs import *

def procCmd(line, references):
    firstWord = word(line,1)
    if firstWord in COMMANDS_NATURAL:
        return eval('proc{}(line, references)'.format(firstWord))
    else:
        return line


def procMOVE(line, references):

    source, targets = ' '.join(words(line)[1][1:]).split(' TO ')[:]
    targets = targets.strip().upper()
    source = source.strip().upper()
    targets = targets.split()
    target = ''
    for trgt in targets:
        idx = ''
        if trgt.find('(') != -1:
            trgt, idx = trgt.split('(')[:]
            idx = idx[:-1]
            idx = '{}'.format(references.get(u'{}'.format(idx),
                              references.get('"{}"'.format(idx),
                              {})).get('def', idx))
            idx = '[{}]'.format(idx)
        target += '{}{} = '.format(references.get(u'{}'.format(trgt),
                                   references.get('"{}"'.format(trgt),
                                   {})).get('def', trgt), idx)

    if source.startswith('LEFT') or source.startswith('RIGHT'):
        source = source.split()[1]
    src = source
    idx = ''
    if src.startswith('(AD='):
        source = AD[''.join(src.split('=')[1])[:-1]]
    elif src.startswith('EDITED'):
        source = ''.join(src.split('(EM=')[0]).split()[1]
    elif src.find('(') != -1:
        source, idx = src.split('(')[:]
        idx = idx[:-1]
        idx = '{}'.format(references.get(u'{}'.format(idx),
                          references.get('"{}"'.format(idx),
                          {})).get('def', idx))
        idx = '[{}]'.format(idx)
    source = '{}{}'.format(references.get(u'{}'.format(source),
                           references.get('"{}"'.format(source),
                           {})).get('def', source), idx)
    ret = '' if target.replace('=','').strip() == source else '{}{}'.format(target, source)
    return ret


def procIF(line, references):
    if "MASK" in line:
        line = reMask(line, references)
    return line


procAND = procIF
procOR = procIF


def reMask(line, references):
    idx = ""
    cmd = word(line, 1).lower()
    if 'EQ' in line:
        oper = ""
        fld = "".join("".join(line.split("EQ")[0]).strip().split()[1:])
    elif 'NE' in line:
        oper = "not"
        fld = "".join("".join(line.split("NE")[0]).strip().split()[1:])
    if fld.find('(') != -1:
        fld, idx = fld.split('(')[:]
        idx = idx[:-1]
        idx = '{}'.format(references.get(u'{}'.format(idx),
                          references.get('"{}"'.format(idx),
                          {})).get('def', idx))
        idx = '[{}]'.format(idx)
    fld = "{}{}".format(references.get(u'{}'.format(fld),
                        references.get('"{}"'.format(fld),
                        {})).get('def', fld), idx)
    mask = ''.join(line.split("MASK")[1:]).strip()
    newMask = MASKS.get(mask, None)
    if newMask:
        ret = """{} {} {}({}):""".format(cmd, oper, newMask, fld)
    elif mask[1:-1] == '{}'.format('N'*(len(mask)-2)):
        newMask = "mask_full_num"
        ret = """{} {} {}({},{}):""".format(cmd, oper, newMask, fld, len(mask)-2)
    else:
        newMask = mask.replace("N","\d").replace("'","")
        ret = """{} {} re.match({},{}):""".format(cmd, oper, newMask, fld)

    return ret