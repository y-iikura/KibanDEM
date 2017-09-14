#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cd /Volumes/Transcend/KibanDEM
# extract_utm.py utm_template.txt 

import sys
import cv2
import numpy as np
from scipy import interpolate
import conv_util2 as ut
import kdem_util as kd

kd.fname1='FG-GML-'
kd.fname2='-dem10b-20161001.xml'

param=sys.argv
if len(param)!=2:
    print 'Usage: extract_utm.py file_name'

fname=param[1]
f=open(fname)
lines=f.readlines()
f.close()

for line in lines:
  if line.find('xs')!=-1: ut.xs=float(line.split()[1])
  if line.find('xe')!=-1: ut.xe=float(line.split()[1])
  if line.find('ys')!=-1: ut.ys=float(line.split()[1])
  if line.find('ye')!=-1: ut.ye=float(line.split()[1])
  if line.find('dx')!=-1: ut.dx=float(line.split()[1])
  if line.find('dy')!=-1: ut.dy=float(line.split()[1])
  print line,

#ut.xs= 406200.0
#ut.xe= 442200.0
#ut.dx= 30.0
#ut.ys= 4460750.0
#ut.ye= 4496750.0
#ut.dy= 30.0

ul=ut.utm2bl([ut.xs,ut.ye])
ur=ut.utm2bl([ut.xe,ut.ye])
ll=ut.utm2bl([ut.xs,ut.ys])
lr=ut.utm2bl([ut.xe,ut.ys])

s_lat=np.min([ul[0],ur[0],ll[0],lr[0]])
e_lat=np.max([ul[0],ur[0],ll[0],lr[0]])
s_lon=np.min([ul[1],ur[1],ll[1],lr[1]])
e_lon=np.max([ul[1],ur[1],ll[1],lr[1]])

code,col,row=kd.dcode([s_lat,s_lon],[e_lat,e_lon])
#kd.xcode(code[0],code[1],col,row)
old=kd.composite(code[0],code[1],col,row)
jmax,imax=old.shape
print old.dtype,old.shape

codex=kd.mcode(e_lat,s_lon)
ut.lat0,ut.lon0=kd.rcode(codex[0],codex[1])

#oldx=cv2.resize(old,(600,600))
#cv2.imshow('old',oldx/np.max(oldx))
#cv2.waitKey(0)

ut.dlat=2.0/3/8/750.0
ut.dlon=1.0/8/1125.0
imax=int((ut.xe-ut.xs)/ut.dx)
jmax=int((ut.ye-ut.ys)/ut.dy)
new=ut.convert(old,imax,jmax)
newx=cv2.resize(new,(600,600))
#cv2.imshow('new',newx/np.max(newx))
#cv2.waitKey(0)

ut.write_tif('new_utm.tif',new,1)

newx=255.0*new/np.max(new)
newx[np.where(newx < 0.0)]=0.0
ut.write_tifB('new_utmB.tif',newx.astype(np.uint8),1)

#cv2.destroyAllWindows()

exit()
