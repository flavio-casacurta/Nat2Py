""" ticker.py -- Store Timestamp into Ticker File every 60 seconds


The Ticker file has the following field

    01,TI,20,A,DE,NU

Each minute will have a separate record with ISN=minute of day.
At most there will be 1440 ISNs.

If the interval is other than 60 the number of records changes by
factor i/60.


Usage: python [-O] ticker.py --dbid <dbid> --fnr <fnr> --repeat <num>
                                                       --interval <sec>

                -O          run optimzied, debug code not generated
                -d <dbid>   dbid
                -f <fnr>    file number of ticker file
                -r <num>    specifies the number of ticks to write
                            otherwise runs forever
                -i <sec>    interval in seconds (default = 60)

 Options:

    -h, --help              display this help

 Example (short parameter form):
    python ticker.py -d 241 -f 12 -r 5

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

import time
import string
import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *
import getopt

def usage():
    print __doc__

FNR=0
DBID=0
COUNT=1987543210    # very high number
SLEEPINT=60         # sleep interval in seconds


try:
    opts, args = getopt.getopt(sys.argv[1:],
      'hd:f:i:r:',
      ['help','dbid=','fnr=','interval=','repeat='])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt in ('-d', '--dbid'):
        DBID=int(arg)
    elif opt in ('-f', '--fnr'):
        FNR=int(arg)
    elif opt in ('-i', '--interval'):
        SLEEPINT=int(arg)
    elif opt in ('-r', '--repeat'):
        COUNT=int(arg)

if FNR==0 or DBID==0 or COUNT <0:
    usage()
    sys.exit(2)


lastTic = -1
lastHour = -1
lastMin = -1

#fields = '01,TI,20,A,DE,NU %'
c1=Adabas(fbl=64,rbl=128)
c1.dbid=DBID
c1.cb.fnr=FNR


count=COUNT


try:
    c1.open(mode=UPD)

    c1.cb.cid=12
    c1.fb.value='TI,20,A.'   # set format

    while count>0:
        t=time.localtime()
        if lastHour != t[3]:
            lastHour = t[3]
            print time.strftime('\n %Y-%m-%d %H:', t),
            lastMin = -1
        x = t[5] +60*t[4] + 3600*t[3]  # sec + 60*minute + 3600*hour
        currTic = int(x/SLEEPINT)
        if lastTic < currTic:
            lastTic = currTic
            newRecord=0
            try:
                c1.get(isn=currTic+1, hold=1)
            except DatabaseError, (line, apa):
                if apa.cb.rsp == 113:
                    newRecord=1
                else:
                    raise
            c1.rb[0:20]=time.strftime(' %Y-%m-%d %H:%M:%S',t)
            if newRecord == 0:
                c1.update()
            else:
                c1.store(isn=currTic+1)
            c1.et()
            if lastMin != t[4]:
                lastMin = t[4]
                print lastMin, # print minute
            else:
                print '.',   # print ticks within minute
            count-=1         # count down
        time.sleep(SLEEPINT/2.) # make sure we don't miss a minute
        # print time.strftime('%Y-%m-%d %H:%M:%S',t),lastTic, currTic

    c1.close()
    print '\nTerminated after %d ticks' % COUNT

except DatabaseError, (line, apa):
    print line
    dump.dump(apa.acb, header='Control Block')
    raise
except KeyboardInterrupt:
    # clean up
    c1.close()
    print '\nNow terminating due to KeyboardInterrupt after %d ticks.' % (COUNT-count,)
#
