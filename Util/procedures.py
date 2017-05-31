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
    occtw = {}
    for n, trgt in enumerate(targets):
        fieldref= field_ref(trgt, references)
        target += fieldref[0] + ' '
        occtw[n] = fieldref[1]
    if source.startswith('(AD='):
        source = AD[''.join(source.split('=')[1])[:-1]]
    else:
        if source.startswith('LEFT') or source.startswith('RIGHT'):
            source = ''.join(source.split()[1:])
        elif source.startswith('EDITED'):
            source = ''.join(source.split('(EM=')[0]).split()[1]
        source = field_ref(source, references)[0]
    ret = ''
    for n, trgt in enumerate(target.split()):
        if trgt.strip() == source:
            ret += """# removido >>> {}\n""".format(line)
        else:
            if trgt[-2] == '*':
                ret += geraLoopMove(trgt, source, occtw[n])
            else:
                ret += "{} = {}\n".format(trgt, source)
    return ret[:-1]


def procDEFINE(line, references):
    return "def {}():".format(line.split()[-1].replace('-', '_'))


def procELSE(line, references):
    return 'else:'


def procEXAMINE(line, references):
    match = DataPatterns.row_pattern_examine.match(line.strip())
    if not match:
        return "#EXAMINE not match >>> " + line
    match = match.groupdict()
    fieldref = field_ref(match['operando1'], references)
    operando1 = fieldref[0]
    occtw = fieldref[1]
    occ, tw = occtw
    arg1 = field_ref(match['arg1'], references)[0]
    arg2 = field_ref(match['arg2'], references)[0]
    ret = ''
    if operando1[-2] == '*':
        ret += "for ndx1 in xrange({}):\n".format(occ)
        if int(tw):
            ret += """for ndx2 in xrange({}):\n""".format(tw)
            operando1 = operando1.replace('[*,*]', '[ndx1][ndx2]')
        else:
            operando1 = operando1.replace('[*]', '[ndx1]')
    ret += "{}.replace({}, {})\n".format(operando1, arg1, arg2)
    ret += "END-FOR\nEND-FOR\n" if int(tw) else "END-FOR\n" if int(occ) else ""
    return ret[:-1]

def procFOR(line, references):
    match = DataPatterns.row_pattern_for.match(line.strip())
    if not match:
        return "#FOR not match >>> " + line
    match = match.groupdict()
    operando1 = field_ref(match['operando1'], references)[0]
    start = field_ref(match['start'], references)[0]
    start = int(start) - 1 if start.isdigit() else "int({})-1".format(start)
    stop = field_ref(match['stop'], references)[0]
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
        operando1 = field_ref(match['operando1'], references)[0] if match['operando1'] else ''
        operando2 = field_ref(match['operando2'], references)[0] if match['operando2'] else ''
        line = '{} {} {} {}'.format(word(line,1).lower(), operando1,
                                    LOGICAL_OPERATORS[match['operator']], operando2)
    return line

procAND = procIF
procOR = procIF


def procIGNORE(line, references):
    return 'continue'


def procPERFORM(line, references):
    return "{}()".format(line.split()[-1].replace('-', '_'))


def procREINPUT(line, references):
    match = DataPatterns.row_pattern_reinput.match(line.strip())
    if not match:
        return 'return False'
    match = match.groupdict()
    fld = field_ref(match['mark'], references)[0] + ' ,' if match['mark'] else ''
    return """return False, {}'{}'""".format(fld, match['msg'])


def reMask(line, references):
    cmd = word(line, 1).lower()
    if ' EQ ' in line:
        oper = ""
        fld = "".join("".join(line.split("EQ")[0]).strip().split()[1:])
    elif ' NE ' in line:
        oper = "not"
        fld = "".join("".join(line.split("NE")[0]).strip().split()[1:])
    fld = field_ref(fld, references)[0]
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
        for i in idx.split(','):
            if i.isdigit():
                idx = idx.replace(i, str(int(i) - 1), 1)
            else:
                ix = '{}'.format(references.get(u'{}'.format(i),
                                 references.get('"{}"'.format(i),
                                 {})).get('def', i))
                idx = idx.replace(i, ix, 1)
        idx = '[{}]'.format(idx)
    field = "{}{}".format(references.get(u'{}'.format(fld),
                          references.get('"{}"'.format(fld),
                          {})).get('def', fld), idx)
    occurs = '{}'.format(references.get(u'{}'.format(fld),
                         references.get('"{}"'.format(fld),
                         {})).get('occurs', 0))
    two_dimension = '{}'.format(references.get(u'{}'.format(fld),
                                references.get('"{}"'.format(fld),
                                {})).get('two_dimension', 0))
    return (field, (occurs, two_dimension))


def type_ref(fld, references):
    fld = fld.split('(')[0]
    fld_type = "{}".format(references.get(u'{}'.format(fld),
                           references.get('"{}"'.format(fld),
                           {})).get('type', 'A'))
    return fld_type


def geraLoopMove(target, source, occtw):
    occ, tw = occtw
    ret = """for ndx1 in xrange({}):\n""".format(occ)
    if int(tw):
        ret += """for ndx2 in xrange({}):\n""".format(tw)
        target = target.replace('[*,*]', '[ndx1][ndx2]')
        if isinstance(source, str):
            source = source.replace('[*,*]', '[ndx1][ndx2]')
    else:
        target = target.replace('[*]', '[ndx1]')
        if isinstance(source, str):
            source = source.replace('[*]', '[ndx1]')
    ret += "{} = {}\n".format(target, source)
    ret += "END-FOR\nEND-FOR\n" if int(tw) else "END-FOR\n"
    return ret


