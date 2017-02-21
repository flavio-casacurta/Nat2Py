""" adalist_LBLA.py - list images is part of the
LOB Demo Center mod_python/APACHE web application

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
import adabas
import sys
from time import sleep,time
from adabas.api import *
from adabas.datamap import *
from struct import *

STARTISN=0
RCOUNT=1100

# define the mapping of data in record buffer to attributes
# for records of Adabas image file

rec=Datamap( 'AdaList',
        String( 'name',     25),
        String( 'extension', 4),
        String( 'size',      8),
        String( 'length',    2),
    )

#
#    HTML template pieces
#
shead="""
<html>
<head><meta HTTP-EQUIV="content-type" CONTENT="text/html">
  <title>ADABAS list of JPG or GIF files</title></head>
<body>
<font face=arial,sans-serif color=#000000>
 <table width=100%><tr>
  <td><img src="../../Images/adabas2006.jpg" height="70" >
  </td><td><font size=+2> ADABAS list of JPG or GIF files </font></td>
 </tr></table>
"""

simglist2="""
<p><p>
<table cellpadding=0 cellspacing=0 border=0 width=100%>
  <tr><td bgcolor=#ffcc33><img width=1 height=1 alt=""></td>
 </tr></table>
<table border=0 cellpadding=3 cellspacing=0 width="100%">
<tr bgcolor=#fff8c0><font size=-1><b>
<td nowrap width=01%> ISN </td>
<td nowrap width=01%>Size [bytes]</td>
<td nowrap width=01%>Name</td>
<td nowrap width=01%>Extension</td>
<td nowrap width=01%>Thumbnail</td>
</b></font></tr>
"""

simgline="""
<tr bgcolor=#f0f0f0 valign=top><font face=arial,sans-serif>
  <td nowrap align=left>
    <a href="../menu_LBLA.py/l1ADAimg?DBID=%s&FNR=%s&ISN=%s&TYPE=%s" target="_blank"> %s </a></td>
  <td nowrap align=left>%s</td>
  <td nowrap align=left>%s</td>
  <td nowrap align=left>%s</td>
  <td nowrap align=left>
    <a href="../menu_LBLA.py/l1ADAimg?DBID=%s&FNR=%s&ISN=%s&TYPE=%s" target="_blank">
      <img src="../menu_LBLA.py/l2ADAimg?DBID=%s&FNR=%s&ISN=%s" width="40" height="30">  </a> </td>
</font></tr>
"""

simgline2="""
<tr bgcolor=#f0f0f0 valign=top><font face=arial,sans-serif>
  <td nowrap align=left> <a href="../menu_LBLA.py/l1ADAimg?DBID=%s&FNR=%s&ISN=%s&TYPE=%s" target="_blank"> %s </a></td>
  <td nowrap align=left>%s</td>
  <td nowrap align=left>%s</td>
  <td nowrap align=left>%s</td>
</font></tr>
"""

stail="""
</font>
<br clear=all></center><p><hr class=z>
     <center>
      <img src="../../Images/adabas.gif" width="150" height="32" ><br>
      <font size=-1><a href="http://www.softwareag.com/adabas/" target="_blank" >powered</a><br>
        &copy;&nbsp;2007 Software AG
      </font>
     </center>
</body></html>
"""

def select(req,DBID,FNR):

    req.content_type="text/html"
    req.write(shead)

    c1=Adabas(rbl=64,fbl=16,sbl=0,vbl=0,ibl=0)
    c1.cb.dbid=int(DBID)
    c1.cb.fnr=int(FNR)
    c1.cb.cid='LBLA'
    c1.fb.value='A1,A2,A3.'

    c1.cb.isn=STARTISN
    rec.buffer=c1.rb

    # write to buffer starting with pos. 0
    count=0
    counter=0
    req.write(simglist2)

    for count in range(RCOUNT):
        try:
            c1.readByIsn(getnext=1)
            # req.write ('\nget rsp= %s  isn= %s \n' % (c1.cb.rsp,c1.cb.isn) )

            if rec.extension in [ 'jpg', 'jpeg' , 'gif' , 'JPG' , 'JPEG' , 'GIF' ] :

                req.write(simgline \
                  %(  DBID, \
                      FNR,
                      c1.cb.isn, \
                      rec.extension, \
                      c1.cb.isn, \
                      rec.size , \
                      rec.name, \
                      rec.extension , \
                      DBID,
                      FNR,
                      c1.cb.isn, \
                      rec.extension, \
                      DBID,
                      FNR,
                      c1.cb.isn ), \
                  )
                time.sleep(0.08)
            else:
                req.write(simgline2 \
                  %(  DBID, \
                      FNR,  \
                      c1.cb.isn, \
                      rec.extension, \
                      c1.cb.isn, \
                      rec.size , \
                      rec.name, \
                      rec.extension ), \
                  )

        except DataEnd:
            req.write('</table><br>Sequential Read by ISN returned '+str(count)+' record(s).')
            req.write(stail)
            return

        except DatabaseError, (line, c1):
            req.write('</table><br>Database Error:'+line )
            return

        except InterfaceError, (line):
            counter=counter + 1
            if counter == 100:
                req.write('counter= %d' % (counter) )
                req.write('\n')
                req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
                return
            sleep(0.5)

        # c1.close()


