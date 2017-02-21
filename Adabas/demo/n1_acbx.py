"""Store and Read record then BT and CL using ACBX

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

import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *

#FNR=11;DBID=12              # Employees local DB12
FNR=11;DBID=8                # Employees mf
FB='AA,8,A.'

c1=Adabasx(fbl=64,rbl=64)   # allocate set of buffers ACBX,
                            # abd+format and record buffer

c1.dumpcb=c1.dumpfb=c1.dumprb=c1.dumpbefore=1 # print Adabas buffers

try:
    # print Adabas call buffers before and after
    c1.cb.dbid=DBID         # for ACBX; c1.dbid=DBID for ACB
    c1.cb.fnr=FNR           # set control block fields

    c1.open(mode=UPD)       # issue OP

    c1.cb.cid='abcd'
    c1.cb.isn=0
    c1.fb.value=FB          # put data into format buffer
    c1.rb.value='AACDEFGE'  # ..            record buffer
    c1.rabd.send=8          # set send size for record buffer

    c1.store()              # issue N1

    c1.rb.value=' '*8       # reset rb
    # c1.rabd.send=0        # send size zero!
    c1.rabd.send=8          # send size !

    c1.get()                # issue L1

    print repr(c1.rb.value), 'returned size', c1.rabd.recv

    c1.bt()                 # issue backout
    c1.close()              # issue close

except DatabaseError, (line, apa):
    print line
    dump.dump(apa.acbx, header='Control Block')
    raise
