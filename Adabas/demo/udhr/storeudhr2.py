"""Store UDHR data into database using ACB and data broken into MU fields
   Adjust settings:
     FNR DBID
     ZF

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


#FNR=47;DBID=12             # UDHR  DB12
FNR=47;DBID=8               #

# Copora downloaded from Natural Language Toolkit site
ZF='C:/z/install/nltk/nltk-corpora-0.8.zip'
UPREFIX='corpora/udhr/'


from zipfile import *
import adabas
import adabas.dump
from adabas.api import *
from adabas.datamap import *

#
# define Adabas resources
#

c1=Adabas(fbl=64,rbl=4032) # allocat set of adabas buffers

#c1.dumpcb=c1.dumpfb=c1.dumprb=c1.dumpbefore=1 # print Adabas buffers

#FB='AA,32,A,WW1-25,160.'
FB='AA,32,A,WW1-32,125.'

udh=Datamap('udhr_record',
    String('country', 32),
    String('declaration', 4000),  # stored in WW1-32 * 125 bytes
    buffer=c1.rb)

def storeone(country, text):
    "store one record with the country and the text related to the country"

    wwl=len(text)
    udh.country=country

    i=0
    j=[]
    for k in range(32):
        if i < wwl:
            if i < wwl-125:
                m=text.rfind(' ',i,i+125)-i # position of next ' '
                if m==-1:   # last word has no space
                    m=min(wwl-i,125)
            else:
                m=wwl-i

            j.append(text[i:i+m]+(125-m)*' ') # fill as much text as possible
                                                # but don't split a word
                                                # fill rest of occ with spaces
            i+=m

        else:
            j.append(125*' ')

    udh.declaration=''.join(j)

    # dump.dump(c1.rb)

    try:
        c1.store()              # issue N1
        print '%s stored, ISN %d, size %d' % (country, c1.cb.isn, wwl)
        c1.et()                 # end of transaction
    except DatabaseError, (line, apa):
        print line
        dump.dump(apa.rb, header='Record Buffer')
        dump.dump(apa.acb, header='Control Block')
        print "Skipping country", country
        x=raw_input("Press enter to continue")
        pass


try:
    # print Adabas call buffers before and after
    c1.cb.dbid=DBID         # for ACBX; c1.dbid=DBID for ACB
    c1.cb.fnr=FNR           # set control block fields
    #c1.dumpcb=1
    c1.open(wcharset='UTF-8') # issue OP

    c1.cb.cid='udhr'
    c1.cb.isn=0
    c1.fb.value=FB          # put data into format buffer


    #
    # open corpora file and extract udhr file names
    #
    z=ZipFile(ZF)
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

    for k, v in zd.iteritems():
        print k,v
        if 'UTF8' in v:
            utext=z.read(UPREFIX+k+'-UTF8')
            storeone(k,utext.decode('utf8','replace').encode('utf8'))  # get rid of invalid chars
        elif 'UFT8' in v:
            utext=z.read(UPREFIX+k+'-UFT8')
            storeone(k,utext.decode('utf8','replace').encode('utf8'))
        elif 'Latin1' in v:
            utext=z.read(UPREFIX+k+'-Latin1')
            storeone(k, utext.decode('latin1','replace').encode('utf8'))
        elif 'Latin2' in v:
            utext=z.read(UPREFIX+k+'-Latin2')
            storeone(k, utext.decode('latin2','replace').encode('utf8'))
        elif 'Arabic' in v:
            utext=z.read(UPREFIX+k+'-Arabic')
            storeone(k+'-cp1256', utext.decode('cp1256','replace').encode('utf8'))
        else:
            print 'unhandled:', k, v

    z.close()               # zipfile close
    c1.close()              # database close

except DatabaseError, (line, apa):
    print line
    dump.dump(apa.acb, header='Control Block')
    dump.dump(apa.rb, header='Recor Buffer')
    c1.close()
    raise
#
