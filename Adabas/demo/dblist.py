""" Detect accessible databases

    Usage:

        python dblist.py --dbids <dbid>

    Options:

        -d, --dbids         <dbid> is a valid dbid
                                      or a list of dbids
        -n, --noclose       leave session open (use for testing only)

        -h, --help          display this help

    Examples:

        python dblist.py -d 241
        python dblist.py -dbids (241,10007,65535)

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

from adabas.api import *
import getopt

def usage():
    print __doc__

dbids=[]
noclose=0

try:
    opts, args = getopt.getopt(sys.argv[1:],
      'hd:n',
      ['help','dbids=','noclose'])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt in ('-n', '--noclose'):
        noclose=1
    elif opt in ('-d', '--dbids'):
        if arg[0]=='(':
            print eval(arg)
            dbids+=eval(arg)
        else:
            dbids.append(int(arg))

from adabas.api import *

print '\nCheck if the following databases are active:', dbids, '\n'

opsysDict={0: 'Mainframe (IBM/Siemens/Fujitsu)', 1: 'VMS', 2:
  "Unix, Windows", 4: 'Entire System Server'}

c1=Adabas(rbl=80,fbl=64,sbl=16,vbl=64,ibl=4)
c1.cb.cid=123456

if len(dbids)==0:
    dbids.extend([8,12,49,240,241,10006,10007,65535])

for i in dbids:  # loop through list of databases
    try:
        # c1.cb.dbid=i use c1.dbid (only set once from c1.cb.dbid)
        c1.dbid=i

        c1.open(mode=None)

        # Evaluate architecture and version information given back
        # from the open call

        if opsysDict.has_key(c1.opsys):
            s = opsysDict[c1.opsys]
        else:
            s = '%d' % c1.opsys
        if c1.opsys != 4:
            print ('Database %5d is active, V%d.%d.%d.%d, arc=%d,'\
                  ' opsys=%s,\n'+26*' '+'cluster nucid %d, %s') %\
              (c1.dbid,c1.version, c1.release, c1.smlevel, c1.ptlevel,\
               c1.archit, s, c1.nucid, archit2str(c1.archit))
        else:
            print 'Entire System %d is active, V%d.%d.%d.%d, arc=%d' %\
              (c1.dbid,c1.version, c1.release, c1.smlevel, c1.ptlevel,\
               c1.archit)
        if not noclose:
            c1.close()

    except DatabaseError, (line, apa):
        #if not apa.rsp==148:
        print 'Database %5d --'%i, line
        pass
    except InterfaceError, (line):
        print 'Database %5d -- %s' % (c1.dbid,line)
        pass
