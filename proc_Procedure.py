
import os
import re
import json
from Util.HOFs import *
from Util.homogenize import homogenize_proc


def proc_USING(dda, Using, imports):

    with open (r'Convertidos\{}.imp'.format(Using)) as impo:
        for imp in impo.readlines():
            if imp and imp not in imports:
                imports += imp

    using = file(r'Convertidos\{}.txt'.format(Using)).read()
    filejson = file('Convertidos/{}.json'.format(Using)).read()
    references.update(json.loads(filejson))
    return using, imports


def proc_Procedure(lines):

    try:
        line_ed = lines.index(filter(isEndDefine, lines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    lines = homogenize_proc(lines[line_ed + 1:])
    imports = ''
    ancestors = ['']
    spc = 0
    spa = 0

    for line in lines:

        wrd1 =  word(line, 1)

    return True

