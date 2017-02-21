""" Read by descriptor in Demo Employees file by NAME or DEPTartment
    MULTIFETCH number is prompted
    Adapt DBID, FNR

$Date: 2008-08-29 16:48:48 +0200 (Fri, 29 Aug 2008) $
$Rev: 68 $
"""

#  Copyright 2004-2008 Software AG
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import string
import adabas
from adabas.api import *
from adabas.datamap import *
from adabas.dump import *

DBID=8;FNR=11 # Employees file mf
#DBID=12;FNR=11 # Employees file pcmm2
STARTISN=0
RCOUNT=1100
MULTIFETCH=8    # number of records per call: MULTI FETCH if > 1
USEACBX=1
# define the mapping of data in record buffer to attributes
# of EmpTel class

emp = Datamap( 'EmployeeTeleLine',
            String('persid'    ,  8),
            String('firstname' , 20),
            String('initial'   , 20),
            String('lastname'  , 20),
            String('birth'     ,  8),
            String('country'   ,  3),
            String('areacode'  ,  6),
            String('phone'     , 15),
            String('department',  6),
            String('jobtitle'  , 25))

name=''
dept=''

MULTIFETCH=int(raw_input('Enter MULTIFETCH number:'))


empsize=emp.getsize()
print 'One employees record has %d bytes' % empsize

if MULTIFETCH <=1:
    MULTIFETCH=1

rbl1=empsize*MULTIFETCH

if USEACBX:
    mbl1=4+16*MULTIFETCH
    c1=Adabasx(rbl=rbl1,fbl=64,sbl=32,vbl=128,mbl=mbl1,multifetch=MULTIFETCH)
    c1.dumprb=1;c1.dumpcb=1;c1.dumpmb=1;c1.dumpfb=c1.dumpsb=c1.dumpvb=1
    c1.acb=c1.acbx
else:
    ibl1=4+16*MULTIFETCH
    c1=Adabas(rbl=rbl1,fbl=64,sbl=32,vbl=128,ibl=ibl1,multifetch=MULTIFETCH)
    c1.dumpcb=1;c1.dumprb=1;c1.dumpib=1

c1.cb.dbid=DBID
c1.cb.fnr=FNR
c1.cb.cid='EMPL'

print '\nSelect Employees file %d on database %d'  % (FNR, DBID)

while name == '' and dept=='':
    name=raw_input('Enter EMPTEL Selection values for NAME:')
    if len(name) > 0:
        print '     with name=%s' % name
        c1.searchfield('AE,20', 20, name)
        break

    dept=raw_input('Enter EMPTEL Selection values for DEPARTMENT (e.g. SALE10):')
    if len(dept) > 0:
        print '     with department=%s' % dept
        c1.searchfield('AO', 6, name)
        break

c1.sb.write('.')
dump(c1.vb,  header='Value Buffer')

c1.cb.cmd='L3'
c1.cb.op2='A'          # ascending
c1.cb.ad1=c1.sb[0:2]   # search descriptor

if MULTIFETCH>1:
    c1.cb.op1='M'   # M multifetch

# write to buffer starting with pos. 0
c1.fb.write('AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP.')

count=0 # number of returned records
cstart=time.clock()

try:
    c1.dumpbefore=1
    mf=c1.multifetch(emp)     # generator

    while mf.next():       # rl has record length
        count+=1
        birthdate=emp.birth
        #"""
        print '%4d %s %-30s %-3s %-6s %-15s %s %s-%s-%s %s'\
          %(c1.cb.isn, emp.persid,
              # string.capwords(emp.lastname+', '+emp.firstname+' '+emp.initial),
              emp.lastname+', '+emp.firstname+' '+emp.initial,
              emp.country,emp.areacode,emp.phone,
              emp.department,
              birthdate[0:4],birthdate[4:6],birthdate[6:8],
              string.capwords(emp.jobtitle))
        #"""

except DataEnd:
    print 'Sequential Read by desciptor returned', count, 'record(s).'
    pass
except DatabaseError, (line, apa):
    print line
    dump(apa.acb, header='Control Block')
    dump(apa.sb,  header='Search Buffer')
    dump(apa.vb,  header='Value Buffer')
    dump(apa.fb,  header='Format Buffer')
    dump(apa.rb,  header='Record Buffer')
    dump(apa.mb,  header='Multifetch Buffer')

print 'Read time %f sec' % (time.clock() - cstart,)
