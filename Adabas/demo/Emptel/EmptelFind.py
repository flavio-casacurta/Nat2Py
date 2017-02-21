""" Find in Demo Employees file by NAME, DEPTartment or MAKE
    Adapt DBID, FNR and AUTOFNR
    Note: when using FIND with MAKE and AUTOFNR != 12, file number in
          search criterium must be changed in searchfield() parms

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

# DBID=8;FNR=11 # Employees MF
#DBID=241;FNR=11 # Employees MF
DBID=12;FNR=11 # Employees PC
AUTOFNR=12

emp=Datamap('EmplTel',
    String('personnel_id',  8),
    String('firstname',    20),
    String('m_initial',    20),
    String('lastname',     20),
    String('birth',         8),
    String('country',       3),
    String('areacode',      6),
    String('phone',        15),
    String('department',    6),
    String('jobtitle',     25)
    )

name='SMITH'
dept=''
make='FORD'

while name == '' and dept=='':
    name=raw_input('Enter Employee selection values for NAME:')
    dept=raw_input('Enter Employee selection values for DEPARTMENT (e.g. SALE10):')
    make=raw_input('Enter Vehicles selection values for MAKE (e.g. FORD):')

print '\nSelect Employees (file %d on database %d)'  % (FNR, DBID)

if len(name) > 0:
    print '     with name=%s' % name
if len(dept) > 0:
    print '     with dept=%s' % dept
if len(make) > 0:
    print '     coupled to Vehicles via personnel_id with make=%s' % make


c1=Adabas(rbl=150,fbl=64,sbl=128,vbl=256,ibl=0)
c1.dbid=DBID
c1.cb.fnr=FNR
c1.cb.cid='EMPL'
emp.buffer=c1.rb
emp.offset=0

# write to buffer starting with pos. 0
c1.fb.value='AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP.'
count=0
cstart=time.clock()

try:
    #
    # prepare search criterion
    #
    c1.vb.seek(0)
    c1.sb.seek(0)
    if make !='':
        make=make.upper()
        c1.searchfield('(0011,AA,0012,AC)/0012/',0,'')  # soft coupling
        c1.searchfield('AD',20,make)                    # make search crit
        c1.searchfield(',D,/0011/',0,'')                   # switch to main file
    if name != '':
        name=name.upper()
        c1.searchfield('AE',20,name)
    if dept != '':
        sbl=c1.sb.tell()
        if sbl>0 and c1.sb[sbl-1]!='/':   # search crit but not only soft coupling
            c1.sb.write(',D,') # AND with previous
        dept=dept.upper()
        c1.searchfield('AO',6,dept)
    c1.sb.write('.')

    #
    # issue Adabas Search and sort by name
    #
    c1.dumpcb=c1.dumpsb=c1.dumpvb=1
    c1.find(sort='AE')

    count=c1.cb.isq
    if count>0:
        while 1:
            #
            # issue Adabas get next
            #
            c1.dumpcb=c1.dumpsb=c1.dumpvb=0
            c1.getnext()

            print \
                emp.personnel_id, \
                string.capwords(emp.lastname+', '+emp.firstname+' '+emp.m_initial), \
                emp.country, emp.phone, emp.department, \
                string.capwords(emp.jobtitle)
    else:
        c1.close()
        print '\nNo records found.'

except DataEnd:
    print 'Getnext returned '+str(count)+' record(s).'\
          '\nSelection: dbid=%s, fnr=%s, name=%s, dept=%s, make=%s' % (
          c1.dbid,c1.cb.fnr,name,dept,make)
    c1.close()

except DatabaseError, (line, apa):
    print 'Database Error: %s, dbid=%s, fnr=%s'%(line,apa.dbid,apa.cb.fnr)

    dump.dump(apa.acb, header='Control Block')
    dump.dump(apa.fb, header='Format Buffer')
    dump.dump(apa.sb, header='Search Buffer')
    dump.dump(apa.vb, header='Value Buffer')

print 'Run time %f sec' % (time.clock() - cstart,)
