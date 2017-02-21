# -*- coding: cp1252 -*-
"""Show the Mapping features of the datamap module

1. Define datamap with field of each format
2. Assign values
3. Dump buffers
4. Pretty print buffers

When running this script in command line the value cha1 may not
come out as the copyright symbol unless the the Windows codepage 1252
is set
    GRAFTABL 1252  (on the command line)

and non-raster font is being used

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


from adabas import Abuf
from adabas.datamap import *
from adabas.dump import *

p = Datamap( 'test_all_formats',
        String( 'str8', 8),
        Unicode('uni4', 4),   # unicode 4 chars = 8 bytes
        Utf8(   'utf8', 8),
        Bytes(  'byt4', 4),
        Char(   'cha1'),
        Int1(   'int1'),
        Uint1(  'uin1'),
        Int2(   'int2'),
        Uint2(  'uin2'),
        Int4(   'int4'),
        Uint4(  'uin4', opt=T_STCK),    # Uint4 STCK display as time
        Int8(   'int8'),
        Uint8(  'uin8', opt=T_STCK),    # Uint8 STCK display as timestamp
        Float(  'flo4'),
        Double( 'dou8'),
        )

sz=p.getsize()  # return size of datamap

print
print '--- Datamap=%s, size=%d ---\n' % (p.dmname, sz)

p.buffer = Abuf(sz)

# set field values

p.str8='ABCDefgh'          # string

p.uni4=u'ßöäü'             # unicode
p.utf8=u'äßö'              # utf8

p.byt4='\xC1\xC4\xC1\x4B'  # Bytes are displayed in HEX

p.cha1='©'                 # copyright character

p.int1=-128
p.uin1=255

p.int2=-32768
p.uin2=65535

p.int4=-0x80000000L
p.uin4= 0xaee3efa4L # 1.1.1997

p.int8=-0x8000000000000000L
p.uin8= 0xb1962f9305180000L # 1.1.1999

p.flo4 = 2.0
p.dou8 = 0.5

print '--- Dumping datamap structure ---'
dump(p.buffer)

print '---Printing datamap structure ---\n'
p.dprint()  # print datamap

try:
    print '--- Assigning to undefined field xx ---'
    p.xx=123
except DatamapError, (line, dmap):
    print '\t',line
