from Util.HOFs import *
from Util.DataPatterns import *
line = '02601 #AX-PARAM-VAL-ANT (P13,2)'
match = DataPatterns.row_pattern.match(l472(line))
match = match.groupdict()
match

line = '04301 #TL1-OPE      (A1/1:10)'
match = DataPatterns.row_pattern.match(l472(line))
match = match.groupdict()
match
