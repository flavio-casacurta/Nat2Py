import proc_DEFINE_DATA
import proc_Procedure
from print_dict import Print_Dict
from Util.change import change
from Util.HOFs import *


lines = file(r'C:\Python\MyTools\Nat2PyBath\Work\POC.XXX.ALTERACAO.TXT').readlines()
lines = filter(isNotBlank, map(l480, filter(isNotRem, lines)))

ret, references, def_gda, def_pda, def_lda, imports = proc_DEFINE_DATA.proc_DEFINE_DATA(lines)

ret, procs = proc_Procedure.proc_Procedure(lines, references)

Print_Dict(r'references.txt')(references)

dic = {'@GLOBAL': def_gda
        ,'@PARAMETER': def_pda
        ,'@LOCAL': def_lda
        ,'@IMPORTS': imports
        ,'@PROCEDURE': procs}

template = open(r'C:\Python\MyTools\Nat2PyBath\Templates\pgm_template.py').read()
prog = change(dic, template)
progWrite = open(r'Convertidos\pgmteste.py', 'w')
progWrite.write(prog)
progWrite.close()

