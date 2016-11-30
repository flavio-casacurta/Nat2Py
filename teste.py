from Util.HOFs import *
from Util.homogenize import homogenize

lines = file(r'C:\Natural\POC\Originais\define_data.TXT').readlines()

clearLines =  map(l472, filter(isNotRem, lines))

lines = homogenize(clearLines)

print lines
