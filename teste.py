import proc_DEFINE_DATA

lines = file(r'define_data.TXT').readlines()

ret, references, def_gda, def_pda, def_lda, def_rda = proc_DEFINE_DATA.proc_DEFINE_DATA(lines)

print ret
