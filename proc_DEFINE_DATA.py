
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


def proc_USING(dda, Using, imports):

    with open (r'Convertidos\{}.imp'.format(Using)) as impo:
        for imp in impo.readlines():
            if imp and imp not in imports:
                imports += imp

    using = file(r'Convertidos\{}.txt'.format(Using)).read()
    filejson = file('Convertidos/{}.json'.format(Using)).read()
    references.update(json.loads(filejson))
    return using, imports


def get_init(match, imports):
    _type = match.get('type', None)
    init = match.get('init', None)
    if _type:
        if not init:
            init = DATATYPES_NATURAL[_type]['init']
            imp = DATATYPES_NATURAL[_type]['import']
            if imp and imp not in imports:
                imports += imp
    else:
        init = '{'
    return init , imports


def get_def(dda, match, ancestors):
    ancestors.append(match['name'])
    return eval("""'{}{}'.format(dda, "['{}']" * len(ancestors))""").format(*ancestors)


def set_attrb(dda, match, ancestors, init):
    attrb = {}
    dicattr = {}
    dicattr['def'] = get_def(dda, match, ancestors)
    dicattr['level'] = int(match['level'])
    dicattr['type'] = ' ' if not match.get('type', None) else match['type']
    dicattr['redefine'] = False if not match.get('redefine', None) else True
    dicattr['length'] = 0 if not match.get('length', 0) else int(match['length'])
    dicattr['scale'] = 0 if not match.get('scale', 0) else int(match['scale'])
    dicattr['occurs'] = 0 if not match.get('occurs', 0) else int(match['occurs'])
    dicattr['two_dimension'] = 0 if not match.get('two_dimension', 0) else int(match['two_dimension'])
    dicattr['init'] = '' if init == '{' else init
    attrb['"{}"'.format(match['name'])] = dicattr
    references.update(attrb)


def dictionarize(dda, match, ancestors, spc, imports):
    init, imports = get_init(match, imports)
    set_attrb(dda, match, ancestors, init)
    occurs = match.get('occurs', None)
    two_dimension = match.get('two_dimension', None)
    vinit = init
    if occurs:
        occurs = 99 if int(occurs) > 99 else occurs
        if two_dimension:
            vinit = "[" + "{}".format((vinit,) * int(two_dimension))[1:-1] + "]"
        vinit = "[" + "{}".format((vinit,) * int(occurs))[1:-1].replace('"', '').replace("'", '') + "]"
    comma = '' if init == '{' else ','
    attrb = """{}"{}": {}{}\n""".format(' '*spc, match['name'], vinit, comma)
    return attrb, init, ancestors, imports


def proc_DEFINE_DATA(lines):

    try:
        line_dd = lines.index(filter(isDefine, lines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    try:
        line_ed = lines.index(filter(isEndDefine, lines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    lines = homogenize(lines[line_dd + 1:line_ed])
    imports = ''
    ancestors = ['']
    spc = 0
    spa = 0
    level_ant = 1

    for line in lines:

        wrd1 =  word(line, 1)
        if wrd1 in DDA:
            dda = DDA[wrd1]
            if words(line)[0] > 1 and word(line, 2) == 'USING':
                using, imports = proc_USING(wrd1, word(line, 3), imports)
                comp = 'def_{} += using'.format(dda)
                exec compile(comp, '', 'exec')
                spc = 7
            continue

        match = DataPatterns.row_pattern_redefine.match(line.strip())
        if not match:
            match = DataPatterns.row_pattern.match(line.strip())
            if not match:
                print line
                continue

        match = match.groupdict()

        level = int(match['level'])

        if level <= level_ant:
            ancestor = ancestors.pop()
            while True:
                if ancestors and level < references['"{}"'.format(ancestor)]['level']:
                    attrb = '{}{}\n'.format(' ' * (spc-1), '},')
                    comp = 'def_{} += attrb'.format(dda)
                    exec compile(comp, '', 'exec')
                    spc = spc - spa if spc > spa else spc
                if ancestors and references['"{}"'.format(ancestors[-1])]['level'] >= level:
                    ancestor = ancestors.pop()
                else:
                    break

        level_ant = level

        if 'redefine' in match:
            red = 0
            while True:
                red += 1
                if '"{}-R{}"'.format(match['redefine'], red) not in references:
                    break
            match['name'] = '{}-R{}'.format(match['redefine'], red)

        attrb, init, ancestors, imports = dictionarize(dda, match, ancestors, spc, imports)
        if init == '{':
            spa = (len(match['name']) + 5)
            spc += spa
        else:
            spc = 7 if spc == 0 else spc
        comp = 'def_{} += attrb'.format(dda)
        exec compile(comp, '', 'exec')

    level = 1
    if level <= level_ant:
        ancestor = ancestors.pop()
        while True:
            if ancestors and level < references["'{}'".format(ancestor)]['level']:
                attrb = '{}{}\n'.format(' ' * (spc-1), '},')
                comp = 'def_{} += attrb'.format(dda)
                exec compile(comp, '', 'exec')
                spc = spc - spa if spc > spa else spc
            if ancestors and references["'{}'".format(ancestors[-1])]['level'] >= level:
                ancestor = ancestors.pop()
            else:
                break

    attrb = '{}{}\n'.format(' '*6, '}')
    for dda in DDA.values():
        comp = 'def_{} += attrb'.format(dda)
        exec compile(comp, '', 'exec')

    return True, references, def_gda, def_pda, def_lda, imports

