"""readfdt.py
   prints the Adabas field definitions (FDT) for database DBID and file FNR
   Modify DBID and FNR for your environment

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

from adabas.api import *      # access Adabas objects

DBID=12  # <--
FNR=27   # <--

a = Adabas(rbl=64)
a.dbid=DBID
a.dumpcb=1

# open user session
a.open()

readFDT(DBID,FNR,printfdt=True) # Read and print FDT

# close user session
a.close()
