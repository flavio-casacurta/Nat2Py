
import os
import re
import json
from Util.HOFs import *
from Util.homogenize import homogenize
from Util.warehouse import DDA
from Util.warehouse import DATATYPES_NATURAL
from Util.DataPatterns import *


references = {}
def_gda = '''gda = {'''
def_pda = '''pda = {'''
def_lda = '''lda = {'''
def_rda = '''rda = {'''


def proc_USING(dda, Using):
    using = file(r'Convertidos\{}.txt'.format(Using)).read()
    filejson = file('Convertidos/{}.json'.format(Using)).read()
    references.update(json.loads(filejson))
    return using


def set_init(match):
    type = None if not match.get('type', None) else match['type']
    init = None if not match.get('init', None) else match['init']
    if type:
        if not init:
            init = DATATYPES_NATURAL[type]['init']
    else:
        init = '{'
    return init


def get_def(dda, match, ancestors):
    ancestors.append(match['name'])
    return eval("""{}'{}'.format("dda, ['{}']" * len(ancestors))""").format(*ancestors)


def set_attrb(dda, match, ancestors):
    attrb = {}
    dicattr = {}
    dicattr['def'] = get_def(dda, match, ancestors)
    dicattr['type'] = ' ' if not match.get('type', None) else match['type']
    dicattr['length'] = 0 if not match.get('length', 0) else int(match['length'])
    dicattr['scale'] = 0 if not match.get('scale', 0) else int(match['scale'])
    dicattr['occurs'] = 0 if not match.get('occurs', 0) else int(match['occurs'])
    dicattr['two_dimension'] = 0 if not match.get('two_dimension', 0) else int(match['two_dimension'])
    dicattr['init'] = set_init(match)
    attrb[match['name']] = dicattr
    references.update(attrb)


def dictionarize(dda, match, ancestors, spc):
    set_attrb(dda, match, ancestors)
    init = set_init(match)
    ac1 = '[' if match['occurs'] else ''
    fc1 = ']' if match['occurs'] else ''
    ac2 = '[' if match['two_dimension'] else ''
    fc2 = ']' if match['two_dimension'] else ''
    comma = '' if init == '{' else ','
    attrb = """{}'{}': {}{}{}{}{}{}\n""".format(spc, match['name'], ac1, ac2, init, fc1, fc2, comma)
    return attrb, init, ancestors


def proc_DEFINE_DATA(lines):
    clearLines =  map(l472, filter(isNotRem, lines))

    try:
        line_dd = clearLines.index(filter(isDefine, clearLines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    try:
        line_ed = clearLines.index(filter(isEndDefine, clearLines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    lines = homogenize(clearLines[line_dd + 1:line_ed])

    ancestors = ['']
    spc = ' ' * 7
    redefines = False
    level_redefines = 0
    dda_def = ''
    level_ant = 1

    for line in lines:

        wrd1 =  word(line, 1)
        if wrd1 in DDA:
            dda = dda_def = DDA[wrd1]
            if words(line)[0] > 1 and word(line, 2) == 'USING':
                using = proc_USING(wrd1, word(line, 3))
                comp = 'def_{} += using'.format(dda)
                exec compile(comp, '', 'exec')
            continue

        match = DataPatterns.row_pattern.match(line.strip())
        if not match:
            match = DataPatterns.row_pattern_redefine.match(line.strip())
            if not match:
                print line
                continue

        match = match.groupdict()

        level = int(match['level'])
        if level <= level_ant:
            ancestors.pop()
            level_ant = level

        if redefines:
            if level > level_redefines:
                continue
        redefines = False
        dda = dda_def
        level_redefines = 0

        if 'redefine' in match:
            level_redefines = level
            redefines = True
            ancestors = match['redefine']
            dda = 'rda'
            attrb, init, ancestors = dictionarize(dda, match, ancestors, spc)
            continue

        attrb, init, ancestors = dictionarize(dda, match, ancestors, spc)
        if init == '{':
            spc = ' ' * (len(match['name'])+12)
        comp = 'def_{} += attrb'.format(dda)
        exec compile(comp, '', 'exec')

    return references, def_gda, def_pda, def_lda, def_rda

