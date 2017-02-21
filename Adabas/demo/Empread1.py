""" Reading Demo Employees File
    Adapt the following variables:
        DBID, FNR
        MULTIFETCH > 1 : use Multifetch (experimental)
$Date: 2008-08-29 18:20:18 +0200 (Fri, 29 Aug 2008) $
$Rev: 75 $
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
import datetime

#DBID=8;FNR=11 # Employees file MF
DBID=12;FNR=11 # Employees file PC
DATELEN=6      # standard length of date fields OS: 8 MF: 6
STARTISN=0
RCOUNT=1100
MULTIFETCH=1    # number of records per call: MULTI FETCH if > 1

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
            String('jobtitle'  , 25),
            Uint1('adlineCnt'),
            Uint1('leaveCnt'),
            Uint1('langCnt'),
)
empx1 = Datamap( 'AdressLine',
            String('adline'    ,  20),
)
empx2 = Datamap( 'LeaveBooked',
            String('start'    ,  DATELEN),
            String('end'      ,  DATELEN),
)
empx3 = Datamap( 'LanguageSpoken',
            String('lang'    ,  3),
)

empsize=emp.getsize()
empx1size=empx1.getsize()
empx2size=empx2.getsize()
empx3size=empx3.getsize()

print 'One employees record has %d bytes' % empsize




name=''
dept=''

#MULTIFETCH=int(raw_input('Enter MULTIFETCH number:'))
if MULTIFETCH <=1:
    MULTIFETCH=1


while name == '' and dept=='':
    name=raw_input('Enter EMPTEL Selection values for NAME:')
    dept=raw_input('Enter EMPTEL Selection values for DEPARTMENT (e.g. SALE10):')


print '\nSelect Employees-Telephonelist file %d on database %d'  % (FNR, DBID)

if len(name) > 0:
    print '     with name=%s' % name
else:
    print '     with dept=%s' % dept


rbl1=8192 # empsize*MULTIFETCH
ibl1=4+16*MULTIFETCH
c1=Adabas(rbl=rbl1,fbl=64,sbl=32,vbl=128,ibl=ibl1,multifetch=MULTIFETCH)
#c1.dumprb=1;c1.dumpib=1;c1.dumpcb=1
c1.dbid=DBID
c1.cb.fnr=FNR
c1.cb.cid='EMPL'

# not for Multifetch:
empx1.buffer=c1.rb
empx2.buffer=c1.rb
empx3.buffer=c1.rb


if name != '':
    name=name.strip().upper()[:20]  # remove blanks and limit to 20
    ln=len(name)
    c1.vb.write(name)
    if ln < 20:
        c1.vb.write(' '*(20-ln))    # fill with blanks
    c1.vb.write(name)
    if ln < 20:
        c1.vb.write('\xff'*(20-ln)) # fill with high vals

    print 'name=%s' % repr(name)
    desc='AE,20'

if dept != '':
    dept=dept.strip().upper()[:6]  # remove blanks and limit
    ln=len(dept)
    c1.vb.write(dept)
    if ln < 6:
        c1.vb.write(' '*(6-ln))    # fill with blanks
    c1.vb.write(dept)
    if ln < 6:
        c1.vb.write('\xff'*(6-ln)) # fill with high vals

    print 'dept=%s' % repr(dept)
    desc='AO'

c1.sb.write(desc+',S,'+desc+'.')
dump(c1.vb,  header='Value Buffer')

c1.cb.cmd='L3'
c1.cb.op2='A'   # ascending
c1.cb.ad1=desc[:2]+' '*6

if MULTIFETCH>1:
    c1.cb.op1='M'   # M multifetch

# write to buffer starting with pos. 0
c1.fb.write('AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP,AIC,AWC,AZC,AI1-N,AW1-N,AZ1-N.')

count=0 # number of returned records
cstart=time.clock()
print datetime.datetime.now(), '--- Program Start ---'
c1.dumprb=1
try:
    # c1.dumpbefore=1;c1.dumprb=1;c1.dumpfb=1;c1.dumpcb=1
    mf=c1.multifetch(emp)     # generator

    while mf.next():       # rl has record length
        count+=1
        if min(emp.adlineCnt, emp.leaveCnt, emp.langCnt) >0:
            continue
        birthdate=emp.birth
        print '%4d %s %-30s %-3s %-6s %-15s %s %s-%s-%s %d %d %d'\
          %(c1.cb.isn, emp.persid,
              # string.capwords(emp.lastname+', '+emp.firstname+' '+emp.initial),
              emp.lastname+', '+emp.firstname+' '+emp.initial,
              emp.country,emp.areacode,emp.phone,
              emp.department,
              birthdate[0:4],birthdate[4:6],birthdate[6:8],
              emp.adlineCnt, emp.leaveCnt, emp.langCnt)
              # string.capwords(emp.jobtitle))
        empx1.offset=empsize
        empx2.offset=empsize+empx1size*max(1,emp.adlineCnt)
        empx3.offset=empx2.offset+empx2size*max(1,emp.leaveCnt)
        for i in range(max(1,emp.adlineCnt)):
            print '    ad%d: %s' %(i+1, empx1.adline)
            empx1.offset+=empx1size
        empx2.offset=empx1.offset
        for i in range(max(1,emp.leaveCnt)):
            print '    leave%d: %s - %s ' %(i+1, empx2.start, empx2.end)
            empx2.offset+=empx2size
        empx3.offset=empx2.offset
        for i in range(max(1,emp.langCnt)):
            print '    lang%d: %s' % (i+1, empx3.lang)
            empx3.offset+=empx3size

        c1.fb.value='C.'
        c1.cb.cid='cccc'
        c1.get()
        break




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
    dump(apa.ib,  header='ISN Buffer')

print datetime.datetime.now(), '--- Program End ---'
print 'Read time %f sec' % (time.clock() - cstart,)
