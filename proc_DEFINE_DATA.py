
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


    for line in lines:

        wrd1 =  word(line, 1)
        if wrd1 in DDA:
            dic = DDA[wrd1]
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

        if not match['level']:
            continue

        level = int(match['level'])

        if redefines:
            if level > level_redefines:
                continue
        redefines = False
        level_redefines = 0

        if match['redefines']:
            level_redefines = level
            redefines = True
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



