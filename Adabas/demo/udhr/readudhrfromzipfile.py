""" Explore ntlk corpora file for UDHR resources

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

from zipfile import *

zf='C:/z/install/nltk/nltk-corpora-0.8.zip'

UPREFIX='corpora/udhr/'

z=ZipFile(zf)

#zn=[]
#for x in z.namelist():
#    if x.startswith('corpora/udhr/'):
#        # print x
#        zn.append(x)
#print zn
zn=[x for x in z.namelist() if x.startswith('corpora/udhr/')]

zn.sort()
zd={}
for n in zn:
    fn=n.replace(UPREFIX,'')
    nn = fn.rsplit('-',1)       # Bosnian_Bosanski-UTF8  to script/code page
    f1=nn[0]
    if len(nn)==2:
        f2=nn[1]
    else:           # no '-' found
        f2=''

    if f1 in zd:
        zd[f1].append(f2)
    else:
        zd[f1]=[f2]
zn=[]

for k, v in zd.iteritems():
    if 'UTF8' in v:
        zn.append(k+'-UTF8')
    elif 'UFT8' in v:
        zn.append(k+'-UFT8')
    elif 'Latin1' in v:
        zn.append(k+'-Latin1')
    elif 'Latin2' in v:
        zn.append(k+'-Latin2')
    else:
        print 'unhandled:', k, v
        if 'Arabic' in v:
            # read from zip file and convert
            # using the 3 different arabic code pages known in Python
            utext=z.read(UPREFIX+k+'-Arabic')
            fo=open('file/'+k+'-Arabic_IBM864','w')
            fo.write(utext.decode('IBM864','replace').encode('utf8'))
            fo.close()
            fo=open('file/'+k+'-Arabic_cp1256','w')
            fo.write(utext.decode('cp1256','replace').encode('utf8'))
            fo.close()
            fo=open('file/'+k+'-Arabic_iso8859_6','w')
            fo.write(utext.decode('iso8859_6','replace').encode('utf8'))
            fo.close()

import sys;sys.exit()

zn.sort()
for n in zn:
    print n


z.close()
