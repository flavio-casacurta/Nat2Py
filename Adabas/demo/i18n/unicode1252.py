#! /usr/bin/env python
# -*- coding: windows-1252 -*-
"""Verify that windows-1252 characters are shown properly in output

Per default the Windows Command Prompt is set to a PC codepage (e.g. 437)
In order to display the windows-1252 characters issue on the command line:
    >>GRAFTABL 1252   or >>chcp 1252

Additionally, make sure that the Command Prompt (properties) uses a font
containing these characters (e.g. other font than Raster Font)

$Date: 2008-08-22 13:32:56 +0200 (Fri, 22 Aug 2008) $
$Rev: 57 $
"""

import sys
import adabas
from adabas.dump import *

a=adabas.Abuf(300)


# the following hex codepoints were
# replaced by space (20)
# 00  0a 0c 0d 1a  1c 1f 7F 81 8D 8F 90 9D
# NUL LF FF CR SUB FS US DEL

hex256=u'''
         
  !"#$%&\'()*+,-./0123456789:;<=>?
 @ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_
 `abcdefghijklmnopqrstuvwxyz{|}~
 € ‚ƒ„…†‡ˆ‰Š‹Œ Ž  ‘’“”•–—˜™š›œ žŸ
  ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿
 ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß
 àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ
'''

a.write(hex256.encode('cp1252'))

dump(a)
sz=a.tell()
a.seek(0)

print a.read(sz).decode('cp1252')


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
