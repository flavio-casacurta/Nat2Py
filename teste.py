import proc_DEFINE_DATA

lines = file(r'define_data.TXT').readlines()

dda, reference = proc_DEFINE_DATA.proc_DEFINE_DATA(lines)