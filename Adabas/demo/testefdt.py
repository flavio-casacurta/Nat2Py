from adabas.api import *

DBID=12
FNR=11

a = Adabas(rbl=64)
a.dbid=DBID
a.dumpcb=1

a.open()

rdfdt = readFDT(DBID,FNR,printfdt=False)
print ''
a.close()
