""" menu_LBLA.py - main program for the
LOB Demo Center mod_python/APACHE web application

$Date: 2008-08-22 19:52:28 +0200 (Fri, 22 Aug 2008) $
$Rev: 58 $
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


# --------------------------------------------------------------------------------
# ---   html + javascript  head  -------------------------------------------------
# --------------------------------------------------------------------------------

# The main web page consists of HTMLhead, HTML1-HTML9, HTMLtail

HTMLhead = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
  <title>Adabas 2006 LOB Demo Center</title>
  <SCRIPT LANGUAGE="JavaScript" type="text/javascript" >
<!--
function checkForm () {
  if (document.Input.DBID.value == "")  {
   alert("please enter DBID !");
   document.Input.DBID.focus();
   return false;
  }
  var chkZ = 1;
  for (i = 0; i < document.Input.DBID.value.length; ++i)
    if (document.Input.DBID.value.charAt(i) < "0" ||
        document.Input.DBID.value.charAt(i) > "9")
      chkZ = -1;
  if (chkZ == -1) {
    alert("please enter valid DBID !");
    document.Input.DBID.focus();
    return false;
  }

  if(document.Input.FNR.value == "") {
   alert("please enter FNR !");
   document.Input.FNR.focus();
   return false;
  }
  var chkZ = 1;
  for (i = 0; i < document.Input.FNR.value.length; ++i)
    if (document.Input.FNR.value.charAt(i) < "0" ||
        document.Input.FNR.value.charAt(i) > "9")
      chkZ = -1;
  if (chkZ == -1) {
    alert("please enter valid FNR !");
    document.Input.FNR.focus();
    return false;
  }
  return true;
}
function validExt () {
  ext = 0;
  urlf=document.Input.URLFILE.value.toLowerCase();
//  alert(urlf);
  if (urlf.match("gif"))  { ext = 1; return true }
  if (urlf.match("jpg"))  { ext = 1; return true }
  if (urlf.match("JPEG")) { ext = 1; return true }
  if (urlf.match("txt"))  { ext = 1; return true }
  if (urlf.match("log"))  { ext = 1; return true }
  if (urlf.match("swf"))  { ext = 1; return true }
  if (urlf.match("pdf"))  { ext = 1; return true }
//if (urlf.match("html")) { ext = 1; return true }  // do not use
  if (ext == 0) {
    alert("invalid extension - currently it's only allowed to store image-, text- or flash-files (gif, jpg, txt, log, swf, pdf) with this application !");
    alert("send email with url to adminstrator ... we can load this object via batch-interface ...");
    document.Input.URLFILE.focus();
    return false;
  }
}
function PracticeWindow() {
  window.open("try.htm","PractWindow","status,resizable,height=530,width=460")
}
function DBStatus(DBID) {
  if (checkForm() == true) {
    call="menu_LBLA.py/dispDBstatus?DBID=" + document.Input.DBID.value;
    window.open(call,"DBstatus","status,resizable,height=30,width=650").focus();
  }
}
function FDT(DBID,FNR) {
  if (checkForm() == true) {
    call="menu_LBLA.py/readfdt?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value ;
    w1=window.open(call,"readFDT","status,resizable,height=200,width=700");
    w1.close();
    w1=window.open(call,"readFDT","status,resizable,height=200,width=700,scrollbars=1").focus();
  }
}
function numRec(DBID,FNR) {
  if (checkForm() == true) {
    call="menu_LBLA.py/getNumrec?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value ;
    window.open(call,"getNumrec","status,resizable,height=30,width=700").focus();
  }
}
function refrFile(DBID,FNR) {
   if(document.Input.FNR.value == "86") {
     alert("it's not allowed to refresh File 86 !");
   }
   else {
     call="menu_LBLA.py/refrfile?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value ;
     window.open(call,"refrfile","status,resizable,height=30,width=400").focus();
//     alert("File refreshed !");
   }
}
function urlImg(URLFILE) {
  if (validExt() == true) {
    call="menu_LBLA.py/upload?URLFILE=" + document.Input.URLFILE.value;
    w2=window.open(call,"URLimg","status,resizable,height=600,width=800,scrollbars=1").focus();
  }
}
function url2Img(URLFILE2) {
  call="menu_LBLA.py/upload?URLFILE=" + document.Input.URLFILE2.value;
  w2=window.open(call,"URLimg","status,resizable,height=600,width=800,scrollbars=1").focus();
}
function insertImage1(DBID,FNR,URLFILE) {
  if (checkForm() == true) {
    if (validExt() == true) {
      call="menu_LBLA.py/adabasInsertImage?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value
                                                                   + "&URLFILE=" + document.Input.URLFILE.value;
      w3=window.open(call,"n1img","status,resizable,height=230,width=750,scrollbars=1").focus();
      w3.close();
    }
  }
}
function insertImage2(DBID,FNR,URLFILE) {
  if (checkForm() == true) {
    call="menu_LBLA.py/adabasInsertImage?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value
                                                              + "&URLFILE=" + document.Input.URLFILE2.value;
    w4=window.open(call,"insertImage2","status,resizable,height=230,width=750,scrollbars=1").focus();
    w4.close();
  }
}
function listImages(DBID,FNR) {
  if (checkForm() == true) {
    call="adalist_LBLA.py/select?DBID=" + document.Input.DBID.value + "&FNR=" + document.Input.FNR.value;
    w7=window.open(call,"loimg","status,resizable,height=800,width=700,scrollbars=1").focus();
  }
}
//-->
</SCRIPT>
</head>
"""

HTML1="""
<!--------------------------------------------------------------------------------
  ---   html body / form  --------------------------------------------------------
  --------------------------------------------------------------------------------
-->
<body>
<font face=arial,sans-serif color=#000000>
 <table width=100%><tr>
 <td>   <center> <a href="http://www.softwareag.com/" target="_blank"> <img src="Images/natureofbusiness.jpg" width="750" height="110" > </a> </td>
 </tr></table>
<p style="text-align: center">
<br>
<!-- <h1> ADAv8 LOB Demo </h1>  comment -->
<fieldset>
<legend>&nbsp <b>ADABAS 2006 LOB Demo </b> &nbsp </legend>
<form name="Input" action="menu_LBLA.py" target="_blank" method="POST" enctype="multipart/form-data" onsubmit="return checkForm()" ><br>

<fieldset>
<legend>&nbsp Databases &nbsp </legend>
  <ul> <li> <b> <LABEL for="DBID">DBID &nbsp  </LABEL> </b>
  <SELECT NAME="DBID">
"""

HTML2="""
       <OPTION selected value="%s">%s </OPTION>
"""

HTML3="""
     <OPTGROUP label="%s">
"""

HTML4="""
       <OPTION value="%d">%s</OPTION>
"""

HTML4s="""
       <OPTION value="%s">%s</OPTION>
"""

HTML5="""
     </OPTGROUP>
"""
HTML6="""
  </SELECT> &nbsp&nbsp
  <INPUT TYPE="button"  VALUE="Show Database Version  " NAME="dispDBstat" ONCLICK="DBStatus()">
  </ul>
</fieldset><br>

<fieldset>
<legend>&nbsp Table Information &nbsp </legend>
  <ul> <li> <strong> <LABEL for="FNR">Table Number &nbsp </LABEL> </strong>
  <SELECT NAME="FNR">
"""

HTML7="""
     <OPTION VALUE="%d">%d
"""

HTML8="""
  </SELECT> &nbsp&nbsp
  <INPUT TYPE="button"  VALUE="Show FDT" NAME="readFDT" ONCLICK="FDT()" >
  <INPUT TYPE="button"  VALUE="Number of Records" NAME="getNumrec" ONCLICK="numRec()">
  <INPUT TYPE="button"  VALUE="List Image Records" NAME="listADArecords" ONCLICK="listImages()">
  <INPUT TYPE="button"  VALUE="Refresh File" NAME="refreshFile" ONCLICK="refrFile()">
 </ul>
</fieldset><br>

<fieldset>
<legend>&nbsp Load Large Objects &nbsp </legend>
 <ul> <li> <strong> <LABEL for="URLFILE">URLFILE1 &nbsp </LABEL> </strong> <input type=text name=URLFILE value=http://www.softwareag.com/demo/adabas/images/main_r1_c1.jpg size=70 maxlength=180>
  &nbsp&nbsp
  <INPUT TYPE="button"  VALUE="Show URL Image" NAME="dispURLimg" ONCLICK="urlImg()">
  <INPUT TYPE="button"  VALUE="Store URL Image" NAME="saveURLimg" ONCLICK="insertImage1()" >
 </ul>

 <ul> <li> <strong> <LABEL for="URLFILE2">URLFILE2 &nbsp </LABEL> </strong>
  <SELECT NAME="URLFILE2">
     <OPTION selected value="none">None</OPTION>
"""

HTML9="""
  </SELECT>
   &nbsp&nbsp
  <INPUT TYPE="button"  VALUE="Show URL2 Image" NAME="dispURL2img" ONCLICK="url2Img()">
  <INPUT TYPE="button"  VALUE="Store URL2 Image" NAME="saveURLimg" ONCLICK="insertImage2()">
 </ul>
</fieldset>
"""

HTMLtail="""
  <br><br>
  <hr>
  <br>
  <TABLE cellpadding=0 cellspacing=0 border=0 width=100%>
  <TR valign="top"><TD colspan="2">
  <a href="images/ADAv8_LOBdemo.jpg" target="_blank"> ADABAS v8 LOB-Demo - Architecture <br> </a>
  <a href="fdt/mf_lodlob88_jcl.txt" target="_blank"> ADABAS v8 LOB-Demo - ADALOD example JCL <br> </a>
  <br> external link:
  <br>
  <a href="http://www.adobe.com/de/products/flash/about/" target="_blank"> Flash Player plugin - check availability <br> </a>
  </TD>
  <TD></TD>
  <TD nowrap align=left>
  <a href="http://www.softwareag.com/adabas/" target="_blank"> <img src="Images/adabas2006.jpg" width="230" height="70"> </a>
  </TD></TR>
  </TABLE>

</form>
</body></html>
"""

# --------------------------------------------------------------------------------
# ---   python  scripts  ---------------------------------------------------------
# --------------------------------------------------------------------------------
import cStringIO # *much* faster than StringIO
from datetime import datetime
import Image
import os, os.path
from struct import *
from string import find, rfind
import sys
from time import sleep,time
import urllib, urllib2
from urlparse import urlparse

import adabas
from adabas import adaerror
from adabas.dump import dump as adadump
from adabas.api import *
import settings # LOB demo center settings

logfile=False # for debug purposes: log specific command
adatcpDB = []

def index(req):
    """ create LOB Demo Center main page

    The html of the main page is dynamically created using configuration
    in settings.py. The code could be improved using a proper templating
    system
    """
    req.content_type="text/html"

    if len(settings.DATABASES)==0:
        req.write("Configuration Error: no DATABASES defined in settings")
    else:
        req.write(HTMLhead)
        req.write(HTML1)

        ingroup=dbid1=0; desc1=''
        for dbid, _, desc1 in settings.DATABASES:
            if dbid>0:      # find first entry with dbid>0
                dbid1=dbid
                break
        if dbid1==0:
            req.write("Configuration Error: no DATABASE found in settings")
            return
        else:
            req.write(HTML2 % (dbid1, desc1))   # Option selected
        #files=[]
        for dbid, adatcp, desc in settings.DATABASES:
            if dbid == 0:
                if ingroup:
                    req.write(HTML5)
                req.write(HTML3 % (desc,))
                ingroup=1
            else:
                req.write(HTML4 % (dbid,desc))
                # if fnr>0 and (fnr not in files):
                #    files.append(fnr)
            if adatcp==True:
              adatcpDB.append(dbid)
        if ingroup:
            req.write(HTML5)
        req.write(HTML6)
        for fnr in settings.FILES:
            req.write(HTML7 % (fnr,fnr))
        req.write(HTML8)
        gflag=0; desc=''; url=''
        for gflag, desc, url in settings.IMAGES:
          if gflag == 1:
            if ingroup:
              req.write(HTML5)
              ingroup=0
            req.write(HTML3 % (desc,))
            ingroup=1
          else:
            req.write(HTML4s % (url,desc))
        if ingroup:
          req.write(HTML5)
        req.write(HTML9)
        req.write(HTMLtail)
    return

def upload(req, URLFILE):
    """Read image from URL"""

    up = urlparse(URLFILE)

    # up = tuple of (scheme, netloc, path, ...)
    # from path split off ext w/o leading .
    #                    path
    #                          '.gif'
    #                             'gif'
    ext=os.path.splitext(up[2])[1][1:]

    if ext=='mpg':
        req.content_type="video/mpeg"
    if ext=='swf':
        req.content_type="application/x-shockwave-flash"
    lst= [ 'jpg' , 'jpeg' , 'gif' , 'JPG' , 'JPEG' , 'GIF' ]
    if ext in lst:
        req.content_type="image/gif"
    if URLFILE=='none':
        req.write('please select URL first ...')
        return
    proxies=settings.proxies
    for nopx in settings.noproxy: # discard proxy if intranet domain
        if up[1].endswith(nopx):
            proxies={}
        break
    proxy_handler = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        urlf=opener.open(URLFILE)
    except IOError, e:
        if hasattr(e,'reason'):             # URLEerror
            req.write('<p>Could not reach the server:  %s'%URLFILE)
            req.write('<p>Reason:%s'%str(e.reason))
        elif hasattr(e,'code'):             # HTTPError
            req.write('<p>The server could not fulfil the request: %s'%URLFILE)
            req.write('<p>Error Code:%s'%str(e.code))
        return
    strarr=urlf.read()
    req.write(strarr)
    return


def l1ADAimg(req,DBID,FNR,ISN,TYPE,logfile=logfile):
    """Read LOB from record=isn FB=L1.
       This call is coming from the user clicking the URLs in the hyperlinks
       that are with the ISN or the thumbnail image in the LOB listing
       generated by the adalist_LBLA.py module.

       Several multi-media content types are supported (see below)
       An ACBX call is used with one record buffer of MAXIMAGESIZE.
       The LOB is prefixed with the 4 byte variable length element.
    """

    contyp="text/plain"
    req.content_type="text/plain"   # start with text

    print 'in l1ADAimg:', DBID, FNR, ISN, TYPE

    if TYPE=='asf':
        contyp="video/x-ms-wmv"
    elif TYPE=='wmv':
        contyp="video/x-ms-wmv"
    elif TYPE=='swf':
        contyp="application/x-shockwave-flash"
    elif TYPE.lower() == 'gif':
        contyp="image/gif"
    elif TYPE in ('jpg' , 'jpeg', 'JPG','JPEG'):
        contyp="image/jpeg"
    elif TYPE=='pdf':
        contyp="application/pdf"
    elif TYPE=='rtf':
        contyp="application/rtf"
    elif TYPE=='ppt':
        contyp="application/vnd.ms-powerpoint"
    elif TYPE=='mp3':
        contyp="audio/x-mpeg"
    elif TYPE=='mpg':
        contyp="video/mpeg"

    if int(DBID) in adatcpDB:
      c1=Adabasx(rbl=settings.MAXADATCP,fbl=64)
    else:
      c1=Adabasx(rbl=settings.MAXIMAGESIZE,fbl=64)
    c1.cb.dbid=int(DBID)
    c1.cb.fnr=int(FNR)
    c1.cb.isn=int(ISN)

    c1.dumpcb=c1.dumprb=c1.dumpfb=0 # no loggging

    FB='L1.'
    c1.fb.value=FB
    c1.cb.cid=FNR

    #  c1.rb.value='ACC=.'
    #  c1.open(mode=None,etid=ISN)

    resp=-1
    systemp=None
    while resp in [-1,153]:  # try it again
        try:
            resp=0

            if logfile and not systemp: # write Adabas buffers to log file
                c1.dumpcb=c1.dumpfb=c1.dumprb=1
                systemp=sys.stdout
                sys.stdout = open(settings.TEMPPATH + "out.txt","w")


            # c1.cb.cid='rdim'
            c1.rabd.send=0

            c1.get(int(ISN))

            l1, = unpack('=I',c1.rb[0:4])

            if systemp:
                print 'l1 =', l1
                c1.dumpcb=c1.dumpfb=c1.dumprb=0
                sys.stdout=systemp
                req.sendfile(settings.TEMPPATH + "out.txt")
                systemp=None

            req.content_type=contyp
            req.write(c1.rb[4:l1])

            c1.close()
        except DataEnd:
            req.write('\n record not exists ...\n')
            return
        except DatabaseError, (line, c1):
            if (c1.cb.rsp == 153):
                sleep(0.1)
                resp=c1.cb.rsp
            else:
                req.write(line)
                return
        except InterfaceError, (line):
            req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
            return
        finally:
            if systemp:
                c1.dumpcb=c1.dumpfb=c1.dumprb=0    #
                sys.stdout=systemp                 #
                req.sendfile(settings.TEMPPATH + "out.txt")
                systemp=None
    return


def l2ADAimg(req,DBID,FNR,ISN,logfile=logfile):
    """Read Thumbnail from record=isn field=L2
       this call is coming in from the image URL that the browser finds
       when it interprets the HTML of LOB listing generated by the
       adalist_LBLA.py module
    """

    c1=Adabas(rbl=5500,fbl=128)
    c1.cb.dbid=int(DBID)
    c1.cb.fnr=int(FNR)
    c1.cb.isn=int(ISN)
    fb='L2.'
    c1.fb.value=fb
    c1.cb.cid=FNR
    c1.rb.value='ACC=.'
    c1.open(mode=None,etid=ISN)

    resp=-1
    counter=0
    systemp=None
    while resp in [-1,153]:  # try it again
        try:
            if logfile and not systemp: # write Adabas buffers to log file
                c1.dumpcb=c1.dumpfb=c1.dumprb=1    #
                systemp=sys.stdout                 #
                sys.stdout = open(settings.TEMPPATH + "out.txt","w")

            resp=0

            c1.get(int(ISN))

            l1, = unpack('=H',c1.rb[0:2])

            if systemp:
                c1.dumpcb=c1.dumpfb=c1.dumprb=0    #
                sys.stdout=systemp                 #
                req.sendfile(settings.TEMPPATH + "out.txt")
                systemp=None

            req.content_type="image/gif"
            req.write(c1.rb[2:l1])

            c1.close()
        except DatabaseError, (line, c1):
            if (c1.cb.rsp == 153):
                sleep(0.2)
                resp=c1.cb.rsp
            else:
                req.write(line)
                return
        except InterfaceError, (line):
            # ignore -1
            counter=counter + 1
            if counter == 5:
                req.write(counter)
                req.write('\n')
                req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
        finally:
            if systemp:
                c1.dumpcb=c1.dumpfb=c1.dumprb=0    #
                sys.stdout=systemp                 #
                req.sendfile(settings.TEMPPATH + "out.txt")
                systemp=None

    return


def adabasInsertImage(req,DBID,FNR,URLFILE,logfile=logfile):
    """ Store image into file """
    req.content_type="text/plain"
    if URLFILE=='none':
        req.write('please select URL first ...')
        return
    up = urlparse(URLFILE)
    i1=rfind(up[2],'.')
    i2=rfind(up[2],'/')
    pathname=up[2][0:i2+1]     # path up last /
    a1=up[2][i2+1:i1]          # filename w/o ext
    a1=a1[0:24]                # due to problems with rsp. 55 ADAv61
    a2=up[2][i1+1:len(up[2])]  # extension
    req.write("test - store image in ADABAS file !\n\n")
    req.write('name= %s ; type = %s ; ' %(a1,a2))
    dt1=datetime.now() # stopwatch start

    proxies=settings.proxies
    for nopx in settings.noproxy: # discard proxy if intranet domain
        if up[1].endswith(nopx):
            proxies={}
        break
    proxy_handler = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    try:
        urlf=opener.open(URLFILE)
    except IOError, e:
        if hasattr(e,'reason'):             # URLEerror
            req.write('<p>Could not reach the server:  %s'%URLFILE)
            req.write('<p>Reason:%s'%str(e.reason))
        elif hasattr(e,'code'):             # HTTPError
            req.write('<p>The server could not fulfil the request: %s'%URLFILE)
            req.write('<p>Error Code:%s'%str(e.code))
        return

    istr = cStringIO.StringIO(urlf.read()) # StringIO object holding the image
    strarr=istr.read()
    dt2=datetime.now() # stopwatch read-from-web time
    len1=len(strarr)
    hx1=hex(len1 + 4)
    req.write('length: %s   \n' % (len1))
    req.write('\n')

    hx1=pack('=L',len1 + 4)
    a3=str(len1)                    # plain image length as string
    dum1=0

    if (int(DBID) in adatcpDB) and (len1 > settings.MAXADATCP):
       req.write("Image size (%d bytes) > maximum allowed image size (%d bytes) - ADATCP "\
                 % (len1, settings.MAXADATCP))
       return

    if (len1 > settings.MAXIMAGESIZE) :
      req.write("Image size (%d bytes) > maximum allowed image size (%d bytes) "\
                 % (len1, settings.MAXIMAGESIZE))
      return
    else:
        #req.write("\nlength > 5000 bytes  --> use adabasx now !")
        ind1=dum1
        ind2=ind1+len(a1)
        ind3=ind2+len(a2)
        ind4=ind3+len(a3)
        ind5=ind4+len(URLFILE)
        ind6=ind5+4+len(strarr)

        x0=Adabasx()
        x0.cb.dbid=int(DBID)
        x0.cb.fnr=int(FNR)

        if (len1 > settings.MAXADATCP):
            x1=Adabasx(rbl=settings.MAXIMAGESIZE,fbl=96)
        else:
            x1=Adabasx(rbl=settings.MAXADATCP,fbl=96)

        x1.cb.dbid=int(DBID)
        x1.cb.fnr=int(FNR)
        x1.cb.cid=1

        # set fields in record buffer:
        #
        #   01,A1,025,A,DE,NU       ;filename w/o extension
        #   01,A2,004,A,DE,NU       ;extension
        #   01,A3,008,A             ;loblength as string
        #   01,L1,0,A,LB,NV,NB,NU   ;lob
        #   01,L2,0,A,LA,NV         ;thumbnail
        #   01,X1,180,A,NU          ;url of origin
        #
        x1.rb[ind1:ind2]=a1
        x1.rb[ind2:ind3]=a2
        x1.rb[ind3:ind4]=a3
        x1.rb[ind4:ind5]=URLFILE
        x1.rb[ind5:ind5+4]=hx1
        x1.rb[ind5+4:ind6]=strarr   # image byte string

        if a2 in [ 'jpg', 'jpeg' , 'gif' , 'JPG' , 'JPEG' , 'GIF' ] :
            # create thumbnail in L2
            FB='A1,%d,A,A2,%d,A,A3,%d,A,X1,%d,A,L1,L2.' % (len(a1),len(a2),len(a3),len(URLFILE) )

            # create thumbnail from image
            im = Image.open( cStringIO.StringIO(opener.open(URLFILE).read()) )
            im=im.convert("RGB")
            im.thumbnail((70,50))
            imgname= settings.TEMPPATH + 'small_'+ a1 + '.gif'
            im.save(imgname)

            # read thumb from disk into byte string strarr2
            opener2 = urllib.FancyURLopener({})
            urlf2 = opener2.open(imgname)
            istr2 = cStringIO.StringIO(urlf2.read()) # constructs a StringIO holding the image
            strarr2=istr2.read()
            len2=len(strarr2)
            hx2=pack('=H',len2 + 2)
            ind7=ind6+2+len2
            x1.rb[ind6:ind6+2]=hx2
            x1.rb[ind6+2:ind7]=strarr2  # write thumbnail to record
        else:
            FB='A1,%d,A,A2,%d,A,A3,%d,A,X1,%d,A,L1.' % (len(a1),len(a2),len(a3),len(URLFILE) )

        x1.fb.value=FB
        if (len1 > settings.MAXADATCP):
          x1.rabd.send=settings.MAXIMAGESIZE
        else:
          x1.rabd.send=settings.MAXADATCP

        try:
            if logfile: # write Adabas buffers to log file
                x1.dumpcb=x1.dumpfb=x1.dumprb=1    #
                systemp=sys.stdout                 #
                sys.stdout = open(settings.TEMPPATH + "out.txt","w")

            isnret=x1.store()

            if logfile:
                x1.dumpcb=x1.dumpfb=x1.dumprb=0    #
                sys.stdout=systemp                 #
                req.sendfile(settings.TEMPPATH + "out.txt")

            req.write ('\nstore rsp= %s  isn= %s ' % (x1.cb.rsp,isnret) )
            x0.et()
            x0.close()
            req.write('et rsp= %s \n' % (x1.cb.rsp) )
        except DatabaseError, (line, x1):
            req.write(line)
            req.write('\n cmd= %s   /  rsp= %s   /  subcode= %s \n' % (x1.cb.cmd,x1.cb.rsp,x1.cb.ad2) )

            f=cStringIO.StringIO()
            adadump(x1.acbx,header='Adabas Control Block',fd=f)
            f.seek(0)
            req.write(f.read())
            x0.bt()
            x0.close()
            req.write('bt rsp= %s \n' % (x1.cb.rsp) )

            if logfile:
                x1.dumpcb=x1.dumpfb=x1.dumprb=0    #
                sys.stdout=systemp                 #
                req.sendfile(settings.TEMPPATH + "out.txt")

        except InterfaceError, (line):
            req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )

    dt3=datetime.now() # stopwatch finished storing LOB
    req.write('\n\nTime to read from URL:   '+str(dt2-dt1)[0:-3])
    req.write('\nTime to store in Adabas: '+str(dt3-dt2)[0:-3])
    req.write('\n\n please close this window !')
    return


def getNumrec(req,DBID,FNR):
    """Display number of records loaded"""
    c1=Adabas(rbl=48,fbl=64,sbl=24,vbl=64,ibl=4)
    c1.cb.dbid=int(DBID)
    c1.cb.fnr=int(FNR)
    c1.cb.cid='nrec'
    if c1.cb.fnr==40:
        c1.fb.value='AA.'
        c1.sb.value='AA,GT.'
    else:
        c1.fb.value='A2.'
        c1.sb.value='A2,GT.'
    c1.vb.value=''
    #c1.vb.write('\u0020',0)
    try:
        c1.find(saveisn=1)
        req.write("\n\nDBID: " + DBID + "  FNR: " + FNR + \
            "    number of records: " + str(c1.cb.isq) + " \n\n")
    except DatabaseError, (line, apa):
        req.write ('Database %5d  --  %s '  % (apa.dbid, line) )
        pass
    except InterfaceError, (line):
        req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
    c1.close()
    return


def readfdt(req,DBID,FNR):
    """ Display Field Definition Table of selected Adabas file"""
    sys.stdout = open(settings.TEMPPATH + "out.txt","w")

    try:
        readFDT(int(DBID),int(FNR),printfdt=1)
        req.write("DBID: " + DBID + "  FNR: " + FNR + "\n\n")
        req.sendfile(settings.TEMPPATH + "out.txt")
    except DatabaseError, (line, apa):
        req.write ('Database %5d  --  %s '  % (apa.dbid, line) )
        pass
    except InterfaceError, (line):
        req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
    return


def refrfile(req,DBID,FNR):
    """ Refresh file """
    c1=Adabas(rbl=48,fbl=64,sbl=24,vbl=64,ibl=4)
    c1.cb.dbid=int(DBID)
    c1.cb.fnr=int(FNR)
    c1.cb.cid='S1E1'
    c1.fb.value='A1,A2,7,A3.'
    c1.sb.value='A2,1,GT.'
    c1.vb.value='a'
    try:
        c1.find(saveisn=1)
        nrrec=c1.cb.isq
        if nrrec==0:
            req.write('\n\n\n ... no records found ...\n')
            return
        if c1.cb.isq > 0:
            req.write("\n\nDBID: " + DBID + "  FNR: " + FNR + \
                "    number of records: " + str(c1.cb.isq) + " \n\n")
            i=0
            while 1:
                c1.getnext()
                c1.delete(c1.cb.isn)
                c1.et()
                c1.cb.cid='S1E1'
                i=i+1

    except DataEnd:
        # c1.et()
        req.write ('\n End of get next ... file refreshed ... \n')
    except DatabaseError, (line, apa):
        req.write ('Database %5d  --  %s '  % (apa.dbid, line) )
        c1.bt()
    except InterfaceError, (line):
        req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
        c1.bt()
    c1.close()
    return

def dispDBstatus(req, DBID):
    """ Display database status """
    opsysDict={0: 'Mainframe (IBM/Siemens/Fujitsu)', 1: 'VMS',
               2: "Unix, Windows", 4: 'Entire System Server'}
    c1=Adabas(rbl=16,fbl=64,sbl=16,vbl=64,ibl=4)
    c1.cb.cid='    '
    try:
        c1.cb.dbid=int(DBID)
        c1.open(mode=None)
        if opsysDict.has_key(c1.opsys):
            s = opsysDict[c1.opsys]
        else:
            s = '%d' % c1.opsys
        if c1.opsys != 4:
            req.write ("\n\nDatabase %5d is active, V%d.%d.%d.%d, arc=%d, opsys=%s " %
              (c1.dbid,c1.version, c1.release, c1.smlevel, c1.ptlevel, c1.archit, s) )
        else:
            req.write ('Entire System %d is active, V%d.%d.%d.%d, arc=%d, phys=%d, remote=%d' %
                       (c1.dbid,c1.version, c1.release, c1.smlevel, c1.ptlevel, c1.archit, c1.ctphys, c1.remote) )
        c1.close()
    except DatabaseError, (line, apa):
        req.write ('Database %5d  --  %s '  % (apa.dbid, line) )
        c1.dumpcb=0;c1.dumprb=0
    except InterfaceError, (line):
        req.write ('Database %s  --   not active !!   --  (  %s  )' % (DBID,line) )
    return

# --------------------------------------------------------------------------------
# ---   python  scripts  end -----------------------------------------------------
# --------------------------------------------------------------------------------
