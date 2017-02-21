""" Employees with W fields
        Telephone Listing mod_python/APACHE web application
   Adjust settings:
     FNR DBID HTMLDIR

$Date: 2008-08-29 16:46:45 +0200 (Fri, 29 Aug 2008) $
$Rev: 67 $
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

from mod_python import apache

import string
import cStringIO
import adabas
import sys
from adabas.api import *
from adabas.datamap import *
import os
import string25  # Template class from string of Python V2.5

HTMLDIR="C:/ADA/WEB/apps/"

DBID=12;FNR=9 # EmplTel file
STARTISN=0
RCOUNT=1100

# define the mapping of data in record buffer to attributes
# of EmpTel class

# create datamap object for Employees-Telephone-List
emp=Datamap('EmplTel',
    String('personnel_id',  8),
    Utf8('firstname',      40),
    Utf8('m_initial',      40),
    Utf8('lastname',       40),
    String('birth',         8),
    String('country',       3),
    String('areacode',      6),
    String('phone',        15),
    String('department',    6),
    Utf8('jobtitle',       25)
    )

sempline=u"""
<tr %s>
  <td>%s</td>
  <td>%s</td>
  <td class="col1">%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
</tr>
"""

# assert False, str(os.environ)

f=open(HTMLDIR+'emplistu.html','r')
rawtemplate=f.read().decode('utf-8')
f.close()
page=string25.Template(rawtemplate)

def select(req,name='',dept='',dbid=DBID,fnr=FNR):

    lines=''
    extraline=''
    alter=False

    c1=Adabas(rbl=256,fbl=64,sbl=32,vbl=128,ibl=0)
    c1.cb.dbid=DBID
    c1.cb.fnr=FNR
    c1.cb.cid='1011'
    c1.fb.value='AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP.'

    #for s in sys.path:
    #  req.write('<br>'+s)

    #print '\nRead by ISN on Employees-Telephonelist file %d on database %d' \
    #      '\n     starting from ISN %d for %d records\n' \
    #      % (FNR, DBID, STARTISN, RCOUNT)

    if name=='' and dept=='':

        c1.cb.isn=STARTISN

        # use emp Datamap on record buffer
        emp.buffer=c1.rb
        emp.offset=0

        count=0

        # req.write(semplist)

        try:
            for count in range(RCOUNT):
                c1.readByIsn(getnext=1)
                # birthdate=emp.birth


                if alter:
                    alter=False
                    altx='class="altline"'
                else:
                    alter=True
                    altx='class="wline"'   # alternate for between 2 lines

                lines+=sempline % ( altx, emp.personnel_id,
                    emp.lastname+', '+emp.firstname+' '+emp.m_initial,
                    emp.country, emp.phone, emp.department, emp.jobtitle)

        except DataEnd:
            extraline+= 'Sequential Read by ISN returned '+str(count)+' record(s).'+\
                '<br\>Selection: name=%s, dept=%s' % (name, dept)
            pass
        except DatabaseError, (line, apa):
            extraline+='</table><br>Database Error:'+line
            # dump(apa.cb, header='Control Block')

    else:

        emp.buffer=c1.rb
        emp.offset=0
        # write to buffer starting with pos. 0
        c1.fb.value='AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP.'
        count=0

        # req.write(semplist)

        try:

            #
            # prepare search criterion
            #
            if name != '':
                #name=name.upper()
                if type(name) != type(u''):   # ensure name is in unicode
                    name=name.decode('utf-8')
                c1.searchfield('AE',40,name.encode('utf_8'))
            if dept != '':
                if c1.vb.tell()>0:
                    c1.sb.write(',D,') # AND with previous
                dept=dept.upper()
                c1.searchfield('AO',6,dept.encode('utf_8'))
            c1.sb.write('.')


            #
            # issue Adabas Search and sort by name
            #
            c1.find(sort='AE')

            count=c1.cb.isq
            if count>0:
                while 1:

                    #
                    # issue Adabas get next
                    #
                    c1.getnext()

                    if alter:
                        alter=False
                        altx='class="altline"'
                    else:
                        alter=True
                        altx='class="wline"'  # alternate for between 2 lines


                    lines += sempline % ( altx,
                        emp.personnel_id,
                        emp.lastname+', '+emp.firstname+' '+emp.m_initial,
                        emp.country, emp.phone, emp.department,
                        emp.jobtitle)

            else:
                c1.close()
                extraline+='No records found.'

        except DataEnd:
            extraline+='Getnext returned '+str(count)+' record(s).'\
                '<br/>Selection: name=%s, dept=%s' % (name, dept)
            c1.close()

        except DatabaseError, (line, apa):
            extraline+='Database Error dbid=%d, fnr=%d:'%(
                apa.dbid,apa.cb.fnr)+line

            f=cStringIO.StringIO()
            dump.dump(apa.acb, header='Control Block',fd=f)
            dump.dump(apa.sb, header='Search Buffer',fd=f)
            dump.dump(apa.vb, header='Value Buffer',fd=f)
            f.seek(0)
            req.write(f.read())

            c1.close()


    req.content_type="text/html"
    req.write(page.substitute(details=lines, extras=extraline).encode('utf_8'))
    # return apache.OK
