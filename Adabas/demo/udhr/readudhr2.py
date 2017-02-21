""" Read uhdr data from database - MU1-25/4K version

    Adjust settings:
        FNR DBID

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

FNR=47;DBID=8
RBL=4032

import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *
import os,sys
import string
import cStringIO
import os.path
import unicodedata

from mod_python import apache
import string25  # Template class from string of Python V2.5



thisfile=os.path.basename(__file__)

HTMLDIR="C:/ADA/WEB/apps/"

FB ='AA,32,A,WW1-25,160.'
FBB='AA,32,A,WW1,240.'

sline="""
<tr %s>
  <td><a href="../%s/select?isn=%d">%s</a></td>
  <td>%s</td>
</tr>
"""
stable1="""<div><table><tbody><tr class="byello">
  <td style="white-space: nowrap; width: 1%;">Language</td>
  <td style="width: 80%;">Text</td>
    """
stable2="</tbody></table></div>"


def test_rtl(utf8_string):
    """ Test first characters of utf8_string for right-to-left direction
    The input string is in utf_8 encoding
    """
    x=utf8_string[0:40].decode('utf_8','replace')

    for c in x:
        if unicodedata.bidirectional(c)[0] in ('A','R'):
            return 1
    return 0


f=open(HTMLDIR+'readudhr.html','r')
rawtemplate=f.read()
f.close()
page=string25.Template(rawtemplate)


def select(req,name='',dbid=str(DBID),fnr=str(FNR),isn='0',acbx='0'):

    lines=''
    extraline=''
    ACBX=0
    if acbx!='0':
        ACBX=1

    try:
        if ACBX:
            c1=Adabasx(fbl=64,sbl=3,vbl=32,rbl=RBL) # allocate set of buffers ACBX,
            c1.acb=c1.acbx
        else:
            c1=Adabas(fbl=64,sbl=3,vbl=32,rbl=RBL) # allocate set of buffers ACBX,
                                 # abd+format and record buffer
        c1.cb.dbid=int(dbid)

        c1.open() # issue OP

        c1.cb.fnr=int(fnr)
        c1.cb.cid='1019'

        c1.fb.value=FB
        if ACBX:
            c1.fabd.send=len(FB)

        udh=Datamap('udhr_record',
            String('language', 32),
            Unicode('decla', RBL-32),      # stored in Unicode
            buffer=c1.rb)

        if name != '':
            c1.searchfield('AA.',32,name.capitalize())
            if ACBX:
                c1.sabd.send=3
                c1.vabd.send=32

            c1.read(descriptor='AA')
        else:
            c1.getiseq(isn=int(isn))

        language=udh.language

        c1.rb.seek(32+4)
        lines=cStringIO.StringIO()
        lines.write(udh.decla.encode('utf8'))
        lines.seek(0)
        text='<p></p>'.join(lines.readlines())

        xrtl=''
        if test_rtl(text):
            # right-to-left language: align to right <text>
            xrtl='class="rtl"'

        lines = '<p></p><em>%s</em><p></p><div %s>%s</div>'%(language,xrtl,text)

        c1.close()

    except DatabaseError, (line, apa):
        extraline+='Database Error dbid=%d, fnr=%d, reading language %s:'%(
            apa.cb.dbid,apa.cb.fnr,name)+line

        f=cStringIO.StringIO()
        dump.dump(apa.acb, header='Control Block',fd=f)
        dump.dump(apa.fb, header='Format Buffer',fd=f)
        dump.dump(apa.sb, header='Search Buffer',fd=f)
        dump.dump(apa.vb, header='Value Buffer',fd=f)
        f.seek(0)
        extraline+='<pre>'+f.read()+'</pre>'
        apa.close()


    req.content_type="text/html"
    req.write(page.substitute(details=lines, extras=extraline,
        dbid=dbid, file=fnr,
        formpost='/apps/%s/browse'%thisfile)) # .encode('utf_8'))
    # return apache.OK


def browse(req,name='',dbid=str(DBID),fnr=str(FNR),maxlines=str(20),dbug=''):

    lines=[stable1,]
    extraline=''
    f=cStringIO.StringIO()

    try:
        c1=Adabas(fbl=64,sbl=3,vbl=32,rbl=272) # allocate set of buffers ACBX,
                                 # abd+format and record buffer
        c1.cb.dbid=int(dbid)

        c1.open(wcharset='UTF-8') # issue OP

        c1.cb.fnr=int(fnr)
        c1.cb.cid='1020'

        c1.fb.value=FBB

        udh=Datamap('udhr_record',
            String('language', 32),
            String('decla', 240),      # stored in UTF-8
            buffer=c1.rb)

        c1.searchfield('AA.',32,name.capitalize())

        for linum in range(int(maxlines)):

            c1.read(descriptor='AA')

            language=udh.language

            if dbug=='1':
                print language >> f
                dump.dump(c1.acb, header='Control Block',fd=f)
                dump.dump(c1.fb, header='Format Buffer',fd=f)
                dump.dump(c1.rb, header='Record Buffer',fd=f)
                dump.dump(c1.sb, header='Search Buffer',fd=f)
                dump.dump(c1.vb, header='Value Buffer',fd=f)

            texts=cStringIO.StringIO()
            i2=udh.decla.rfind(' ',0,80)
            texts.write(udh.decla[0:i2])  # cut before last space
            texts.seek(0)
            text=texts.readline().strip() # read one line, strip new line

            if linum%2:
                altx='class="altline"'
            else:
                altx='class="wline"'  # alternate for between 2 lines

            lines.append(sline % ( altx, thisfile, c1.cb.isn, language, text) )

        c1.close()

    except DatabaseError, (line, apa):
        f.write('Database Error dbid=%d, fnr=%d, reading language %s:'%(
            apa.cb.dbid,apa.cb.fnr,name)+line)

        dump.dump(apa.acb, header='Control Block',fd=f)
        dump.dump(apa.fb, header='Format Buffer',fd=f)
        dump.dump(apa.sb, header='Search Buffer',fd=f)
        dump.dump(apa.vb, header='Value Buffer',fd=f)
        # apa.close()
        pass
    except DataEnd:
        c1.close()
        pass

    lines.append(stable2) # close table

    if f.tell()>0:
        f.seek(0)
        extraline+='<pre>'+f.read()+'</pre>'

    req.content_type="text/html"
    req.write(page.substitute(details=''.join(lines), extras=extraline,
        dbid=dbid, file=fnr,
        formpost='/apps/%s/browse'%thisfile)) # .encode('utf_8'))
    # return apache.OK
