
import os
import re
from Util.HOFs import *
from Util.homogenize import homogenize
from Util.warehouse import DDA
from Util.DataPatterns import *


references = {}
def_gda = '''gda = {'''
def_pda = '''pda = {'''
def_lda = '''lda = {'''
def_rda = '''rda = {'''


def proc_USING(dda, Using):
    using = file(r'Convertidos\{}.txt'.format(Using)).read()
    comp = 'def_{} += using'.format(DDA[dda])
    exec compile(comp, '', 'exec')
    filejson = file('Convertidos/{}.json'.format(Using)).read()
    references.update(json.loads(filejson))


def dictionarize(dda, field, attrb):
    comp = 'def_{} += field'.format(dda)
    exec compile(comp, '', 'exec')
    references[field]=attrb


def set_attrb(dda, match):
    attrb = {}
    dicattr = {}
    dicattr['def'] = """{}['{}']""".format(dda, match['name'])
    dicattr['type'] = ' ' if not match.get('type', None) else match['type']
    dicattr['length'] = 0 if not match.get('length', 0) else int(match['length'])
    dicattr['scale'] = 0 if not match.get('scale', 0) else int(match['scale'])
    dicattr['occurs'] = 0 if not match.get('occurs', 0) else int(match['occurs'])
    dicattr['two_dimension'] = 0 if not match.get('two_dimension', 0) else int(match['two_dimension'])
    dicattr['init'] = ' ' if not match.get('init', None) else match['init']
    attrb[match['name']] = dicattr
    references.update(attrb)



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

    redefines = False
    dda_def = ''

    for line in lines:

        wrd1 =  word(line, 1)
        if wrd1 in DDA:
            dda = dda_def = DDA[wrd1]
            if word(line, 2) == 'USING':
                proc_USING(wrd1, word(line, 3))
            continue

        match = DataPatterns.row_pattern.match(line.strip())
        if not match:
            match = DataPatterns.row_pattern_redefine.match(line.strip())
            if not match:
                print line
                continue

        match = match.groupdict()

        level = int(match['level'])

        if redefines:
            if level > level_redefines:
                attrb = get_attrb(match)
                continue
        redefines = False
        level_redefines = 0

        if 'redefine' in match:
            level_redefines = level
            redefines = True
            field = match['redefine']
            dda = 'rda'
            attrb = {}
            dictionarize(dda, field, attrb)
            continue

        if occurs:
            if level > level_occurs:
                if match['pic']:
                    occurs_length += field_length(match['pic'], match['usage'])
                continue
            logical_record_length += occurs_length * occurs
        occurs = False
        level_occurs = 0

        if match['occurs']:
            level_occurs = level
            occurs = (int(nextWord('OCCURS', line)) if 'TO' not in wrds else
                      int(nextWord('TO', line)))

        if match['pic']:
            if occurs:
                occurs_length += field_length(match['pic'], match['usage'])
            else:
                logical_record_length += field_length(match['pic'], match['usage'])



