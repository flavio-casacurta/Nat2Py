"""settings.py - LOB Demo Center settings file

Defines databases and other resources for the operation of the
LOB Demo Center (LDC) application.

Note: The paramters in the settings module must adhere to the normal Python syntax
      otherwise errors will be reported from the interpreter

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

# MAXIMAGESIZE defines maximum image size
# Make sure that the Adabas nuclei and NetWork use adequate parameters
# for LU and NAB
MAXIMAGESIZE=5100000

# MAXADATCP maximum size for ADATCP
# ADATCP is currenlty limited to 999,999 bytes
MAXADATCP=999999

# HTTP Proxy
# Define the proxies to reach the outer world from within the firewall
proxies={
    'http': 'http://httpprox.example.com:8080/',
    }

noproxy=('localhost','.exa','.example.de')


# List of databases that can be selected in the LDC main menu
#   each entry is a list of
#     DBID, file-number, adatcpTrueFalse, display text
#
#   adatcpTrueFalse: may have the values 0, 1 or False, True for
#     databases with ADATCP. If True or 1: will use MAXADATCP as max.
#     record buffer size
#   an entry with DBID==0 may be used for grouping following entries
#
DATABASES=(
    (    8,  False, '00008 - v81 - z/OS 1.7 on EXAF - WCP61'),
    (    0,       0, 'Demo Environment'),
    (    2,   False, '00002 - v61 - win32            - local'),
    (  104,   False, '00104 - v81 - z/OS 1.7 on EXAA - WCP61 '),
    (    0,       0, 'Development environment - ... not available all the time ...'),
    (   12,   False, '00012 - v61 - pc01 win32     - local '),
#   (   61,   False, '00061 - v61 - sunsol9/64 on SUN3 - local'),
    (  220,   False, '00220 - v81 - z/OS 1.7 on EXAF - WCP61'),
    (22081,   False, '22081 - v81 - z/OS 1.7 on EXAF - WCP61 '),
    (51081,    True, '51081 - v81 - z/OS 1.7 on EXAF - ADATCP'),
    )

# List of file numbers that can be selected in the LDC main menu
FILES=( 88, 86)

# List of images/urls that can be selected in the LDC main menu
#   each entry is a list of
#     group-flag, description, url
#
IMGLOCL="c|/ADA/WEB/LobDemoCenter/images" # path to images for this application, omitting starting '/'
#       "FS/fs1234/sun3/prog/exa/adapy/adabas/demo/LobDemoCenter/images"
IMAGES=(
    (1, '< 10000 bytes',''),
      (0, 'local - adabas.gif (2781 b)','file:///%s/adabas.gif'%IMGLOCL),
      (0, 'http://www.apache.org/images/asf_logo_wide.gif (5866 b)','http://www.apache.org/images/asf_logo_wide.gif'),
    (1, '< 100000 bytes',''),
      (0, 'local - adabas2006.jpg (13506 b)','file:///%s/adabas2006.jpg'%IMGLOCL),
      (0, 'local - natureofbusiness.jpg (21501 b)','file:///%s/natureofbusiness.jpg'%IMGLOCL),
    (1, '< 1,0 MB',''),
      (0, 'http://antwrp.gsfc.nasa.gov/...earthlights02_dmsp_big.jpg (207685 b)','http://antwrp.gsfc.nasa.gov/apod/image/0610/earthlights02_dmsp_big.jpg'),
      (0, 'local - softwareag-hq-in-summer.jpg (206903 b)','file:///%s/softwareag-hq-in-summer.jpg'%IMGLOCL),
      (0, 'local - softwareag-hq-in-winter.jpg (444101 b)','file:///%s/softwareag-hq-in-winter.jpg'%IMGLOCL),
    (1, '< 2,0 MB',''),
      (0, 'http://antwrp.gsfc.nasa.gov/.../robinson_sts114_big.jpg (1270197 b)','http://antwrp.gsfc.nasa.gov/apod/image/0605/robinson_sts114_big.jpg'),
      (0, 'http://upload.wikimedia.org/.../Acinonyx_jubatus_walking_edit.jpg  (1526510 b)','http://upload.wikimedia.org/wikipedia/commons/4/42/Acinonyx_jubatus_walking_edit.jpg'),
    (1, '< 4,0 MB',''),
      (0, 'http://antwrp.gsfc.nasa.gov/.../skylab_nasa_big.jpg (2289866 b)','http://antwrp.gsfc.nasa.gov/apod/image/0604/skylab_nasa_big.jpg'),
    )

# Path to store temporary files like thumbnails and readFDT output
#   default on WIN-environment is your 'Apache2' folder
TEMPPATH=''
# TEMPPATH='/FS/fs1234//sun3/prog/exa/apache2/tmp/'

