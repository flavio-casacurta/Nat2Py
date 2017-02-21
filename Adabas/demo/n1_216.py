"""Simple sequence of Adabas calls using ACBX:
        Store and Read record then BT and CL

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

import datetime
import string
import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *

FNR=11;DBID=8    # Employees will do
#FNR=60;DBID=216
#FNR=20;DBID=49983

FB='AA,8,A.'
c1=Adabasx(fbl=64,rbl=64)
# c1.dbid=DBID         # ACB
c1.cb.dbid=DBID        # ACBX
c1.cb.fnr=FNR

print datetime.datetime.now(), 'Program started'

try:
    c1.dumpcb=c1.dumprb=1;c1.dumpfb=1;c1.dumpbefore=1
    c1.open(mode=UPD)
    c1.dumpcb=c1.dumprb=1;c1.dumpfb=1
    c1.cb.cid='abcd'
    c1.cb.isn=0

    c1.fb.value=FB
    c1.rb.value='ABCDEFGE'
    c1.rabd.send=8          #ACBX set send size

    c1.store()
    c1.rb.value='4'*8
    c1.rabd.send=0

    c1.get()

    print repr(c1.rb.value), 'returned size', c1.rabd.recv

    c1.bt()

    # c1.fb.value='AA.'+' '*61
    c1.close()
    c1.dumpcb=c1.dumprb=0;c1.dumpfb=0

except DatabaseError, (line, apa):
    print line
    dump.dump(apa.acbx, header='Control Block')
    raise
#
print datetime.datetime.now(), 'Program stopped'
