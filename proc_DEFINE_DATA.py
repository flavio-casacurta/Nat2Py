
import os
import re
from Util.HOFs import *
from Util.homogenize import homogenize
from Util.Constantes_Figurativas import *
from Util.DataPatterns import *


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

    def_global = 'dd_global = {}'
    ref_global = {}

    def_parameter = 'dd_parameter = {}'
    ref_parameter = {}

    def_local = 'dd_local = {}'
    ref_local = {}

    for line in lines:
        match = DataPatterns.row_pattern.match(line.strip())
        if not match:
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



