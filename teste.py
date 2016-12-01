from Util.HOFs import *
from Util.homogenize import homogenize

lines = file(r'define_data.TXT').readlines()

clearLines =  map(l472, filter(isNotRem, lines))

lines = homogenize(clearLines)

for line in lines:
    print line
