""" a1emp11.py -- Example of simple update transaction

Simple Update of Record given by ISN in File with fields AX, AY, C1

DBID and FNR

$Date: 2008-08-22 13:32:56 +0200 (Fri, 22 Aug 2008) $
$Rev: 57 $
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
import binascii
import string
import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *


FNR=11
DBID=8

c1=Adabas(fbl=64,rbl=64)
c1.dbid=DBID
c1.cb.fnr=FNR


print datetime.datetime.now(), 'Program started'
try:
    c1.open(mode=UPD)

    c1.dumpcb=c1.dumprb=1

    c1.cb.cid='abcd'
    c1.cb.isn=499
    c1.fb.value='AX1,AY1,C1.'
    c1.rb.value='000000000000A'

    c1.update(hold=1)

    c1.dumpcb=c1.dumprb=0

    c1.et()

    c1.close()

except DatabaseError, (line, apa):
    print line
    dump.dump(apa.acb, header='Control Block')
    raise
#
print datetime.datetime.now(), 'Program stopped'
