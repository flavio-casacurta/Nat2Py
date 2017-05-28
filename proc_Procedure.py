
import os
import re
import json
from Util.HOFs import *
from Util.homogenize import homogenize_proc, indentation
from Util.procedures import *


def proc_Procedure(lines, references):

    try:
        line_ed = lines.index(filter(isEndDefine, lines)[0])
    except IndexError:
        return False, [], [], 'Nao e um programa Natural valido'

    lines = homogenize_proc(lines[line_ed + 1:])
    procs = 'def PROCEDURE():\n'
    for line in lines:

        procs += '{}\n'.format(procCmd(line, references))

    procs = indentation(procs.splitlines())

    return True, procs

