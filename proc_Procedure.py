
import os
import re
import json
from Util.HOFs import *
from Util.homogenize import homogenize_proc
from Util.procedures import *


def proc_Procedure(lines, references):

    try:
        line_ed = lines.index(filter(isEndDefine, lines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    lines = homogenize_proc(lines[line_ed + 1:])
    procs = ''
    for line in lines:

        procs += '{}\n'.format(procCmd(line, references))

    return True, procs

