# -*- coding: utf-8 -*-

from Util.warehouse import *
from Util.HOFs import *
from Util.change import change
from Util.DataPatterns import *

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
        target += field_ref(trgt, references) + ' '

    if source.startswith('(AD='):
        source = AD[''.join(source.split('=')[1])[:-1]]
    else:
        if source.startswith('LEFT') or source.startswith('RIGHT'):
            source = ''.join(source.split()[1:])
        elif source.startswith('EDITED'):
            source = ''.join(source.split('(EM=')[0]).split()[1]
        source = field_ref(source, references)
    ret = ''
    for trgt in target.split():
        if target.strip() == source:
            ret += """# removido >>> {}\n""".format(line)
        else:
            ret += "{} = {}\n".format(trgt, source)
    return ret[:-1]


def procELSE(line, references):
    return 'else:'


def procEXAMINE(line, references):
    match = DataPatterns.row_pattern_examine.match(line.strip())
    if not match:
        return "#EXAMINE not match >>> " + line
    match = match.groupdict()
    operando1 = field_ref(match['operando1'], references)
    arg1 = field_ref(match['arg1'], references)
    arg2 = field_ref(match['arg2'], references)
    return """{}.replace({}, {})""".format(operando1, arg1, arg2)

def procFOR(line, references):
    match = DataPatterns.row_pattern_for.match(line.strip())
    if not match:
        return "#FOR not match >>> " + line
    match = match.groupdict()
    operando1 = field_ref(match['operando1'], references)
    start = field_ref(match['start'], references)
    start = int(start) - 1 if start.isdigit() else "int({})-1".format(start)
    stop = field_ref(match['stop'], references)
    stop = int(stop) if stop.isdigit() else "int({})".format(stop)
    return """for {} in xrange({}, {}):""".format(operando1, start, stop)


def procIF(line, references):
    line = change(OPERATORS_REPLACE, line)
    if "MASK" in line:
        line = reMask(line, references)
    else:
        match = DataPatterns.row_pattern_if.match(line.strip())
        if not match:
            return line
        match = match.groupdict()
        operando1 = field_ref(match['operando1'], references) if match['operando1'] else ''
        operando2 = field_ref(match['operando2'], references) if match['operando2'] else ''
        line = '{} {} {} {}'.format(word(line,1).lower(), operando1,
                                    LOGICAL_OPERATORS[match['operator']], operando2)
    return line

procAND = procIF
procOR = procIF


def procIGNORE(line, references):
    return 'continue'


def procREINPUT(line, references):
    match = DataPatterns.row_pattern_reinput.match(line.strip())
    if not match:
        return 'return False'
    match = match.groupdict()
    fld = field_ref(match['mark'], references)+ ' ,' if match['mark'] else ''
    return """return False, {}'{}'""".format(fld, match['msg'])


def reMask(line, references):
    cmd = word(line, 1).lower()
    if ' EQ ' in line:
        oper = ""
        fld = "".join("".join(line.split("EQ")[0]).strip().split()[1:])
    elif ' NE ' in line:
        oper = "not"
        fld = "".join("".join(line.split("NE")[0]).strip().split()[1:])
    fld = field_ref(fld, references)
    mask = ''.join(line.split("MASK")[1:]).strip()
    newMask = MASKS.get(mask, None)
    if newMask:
        ret = """{} {} {}({})""".format(cmd, oper, newMask, fld)
    elif mask[1:-1] == '{}'.format('N'*(len(mask)-2)):
        newMask = "mask_full_num"
        ret = """{} {} {}({},{})""".format(cmd, oper, newMask, fld, len(mask)-2)
    else:
        newMask = mask.replace("N","\d").replace("'","")
        ret = """{} {} re.match({},{})""".format(cmd, oper, newMask, fld)

    return ret


def field_ref(fld, references):
    idx = ""
    if fld.find('(') != -1:
        fld, idx = fld.split('(')[:]
        idx = idx[:-1]
        idx = '{}'.format(references.get(u'{}'.format(idx),
                          references.get('"{}"'.format(idx),
                          {})).get('def', idx))
        idx = '[{}]'.format(idx)
    field = "{}{}".format(references.get(u'{}'.format(fld),
                          references.get('"{}"'.format(fld),
                          {})).get('def', fld), idx)
    return field


def type_ref(fld, references):
    fld = fld.split('(')[0]
    fld_type = "{}".format(references.get(u'{}'.format(fld),
                          references.get('"{}"'.format(fld),
                          {})).get('type', 'A'))
    return fld_type