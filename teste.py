import proc_DEFINE_DATA
from print_dict import Print_Dict
from Util.change import change

lines = file(r'C:\Natural\POC_SERPRO\Originais\POC.XXX.ALTERACAO.TXT').readlines()

ret, references, def_gda, def_pda, def_lda, imports = proc_DEFINE_DATA.proc_DEFINE_DATA(lines)

print ret

Print_Dict(r'references.txt')(references)

dic = {'@GLOBAL': def_gda
        ,'@PARAMETER': def_pda
        ,'@LOCAL': def_lda
        ,'@IMPORTS': imports}

template = open(r'C:\Python\MyTools\Nat2Py\Templates\pgm_template.py').read()
prog = change(dic, template)
progWrite = open(r'Convertidos\pgmteste.py', 'w')
progWrite.write(prog)
progWrite.close()

