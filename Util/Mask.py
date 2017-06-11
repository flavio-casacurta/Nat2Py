# -*- coding: utf-8 -*-
import re
from operator import truth
from gluon.validators import *
from datetime import date, time

mask_yyyymmdd = lambda data : not (IS_DATE()('{}{}{}{}-{}{}-{}{}'.format(*'{:08}'.format(int(data))))[1])
mask_ddmmyyyy = lambda data : not (IS_DATE()('{}-{}-{}'.format(data[4:],data[2:4],data[0:2]))[1])
mask_dddotmmdotyyyy = lambda data : ((not IS_DATE()('{}-{}-{}'.format(data[6:],data[3:5],data[0:2]))[1]) and
                                     truth(re.match(r'(\d{2}\.){2}\d{4}', data)))
mask_ddbmmbyyyy = lambda data : ((not IS_DATE()('{}-{}-{}'.format(data[6:],data[3:5],data[0:2]))[1]) and
                                  truth(re.match(r'(\d{2}\/){2}\d{4}', data)))

mask_dd = lambda dd : 0 < dd < 32
mask_mm = lambda mm : 0 < mm < 13
mask_hhmmss = lambda time : not (IS_TIME()('{}{}:{}{}:{}{}'.format(*'{:06}'.format(int(time))))[1])
mask_hh2pmm2pss = lambda time : not (IS_TIME()(time)[1])
mask_full_num = lambda num, l: truth(re.match(r'\d{}{},{}{}'.format('{', l, l,'}'), num))
mask_date = lambda data, mask='%d-%m-%Y': date.fromordinal(int(data[2:])-364).strftime(mask)
mask_bytes = lambda bytes : '{:<08}'.format(bytes.encode('hex').upper())