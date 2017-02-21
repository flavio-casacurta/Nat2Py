"""stck1.py - Demo of stck module

   stck.py does IBM/390 and other timestamp conversions

$Date: 2008-09-01 14:51:03 +0200 (Mon, 01 Sep 2008) $
$Rev: 81 $
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

from adabas.stck import *

print
print 'sstck(0xb1962f93L):', sstck(0xb1962f93L)

# four byte stck
stck1999=0xb1962f93L # 1.1.1999
stck1997=0xaee3efa4L # 1.1.1997

# 8 byte stck
stdk1999=0xb1962f9305180000L # 1.1.1999
stdk1997=0xaee3efa402f40000L # 1.1.1997

s1=0xBEF5EC8129A08A45L
s2=0xBEFAFAAD99907388L

s,m = cstckd(s1)
print
print 'cstckd:', time.localtime(s), m, type(m)
print

STCKSEC=1.048576
a=stdk1997>>12
b=a/1000000 # seconds
c=a%1000000 # micro sec
d=b-sec1970+0.0 # seconds since the epoch 1970

print 'time.gmtime(): ', time.gmtime(d)
print 'seconds since epoch 1970:', d

secs = cstck(stck1999)
print '\ncstck:', time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(secs))
print '\nsstck:', sstck(stck1999)

print '\nsstckd:'
print sstckd(stdk1999)
print sstckd(s1)
print sstckd(s2)
