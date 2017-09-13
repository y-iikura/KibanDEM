#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cd /Volumes/Transcend/KibanDEM
# extract_bl.py bl_template.txt 

import sys
import cv2
import numpy as np
from scipy import interpolate
import conv_util as ut
import kdem_util as kd

kd.fname1='FG-GML-'
kd.fname2='-dem10b-20161001.xml'

param=sys.argv
if len(param)!=2:
    print 'Usage: extract_bl.py file_name'

fname=param[1]
f=open(fname)
lines=f.readlines()
f.close()

for line in lines:
  if line.find('s_lon')!=-1: s_lon=float(line.split()[1])
  if line.find('s_lat')!=-1: s_lat=float(line.split()[1])
  if line.find('e_lon')!=-1: e_lon=float(line.split()[1])
  if line.find('e_lat')!=-1: e_lat=float(line.split()[1])
  if line.find('dlat')!=-1: dlat=float(line.split()[1])
  if line.find('dlon')!=-1: dlon=float(line.split()[1])
  print line,

#s_lat= 40.3
#e_lat= 40.9
#dlat= 0.001
#s_lon= 140.2
#e_lon= 140.8
#dlon= 0.001

nlon=int((e_lon-s_lon)/dlon)
nlat=int((e_lat-s_lat)/dlat)
print nlon,nlat
code,col,row=kd.dcode([s_lat,s_lon],[e_lat,e_lon])
#kd.xcode(code[0],code[1],col,row)
old=kd.composite(code[0],code[1],col,row)
jmax,imax=old.shape
print old.dtype,old.shape

codex=kd.mcode(e_lat,s_lon)
elatx,slonx=kd.rcode(codex[0],codex[1])
dlatx=2.0/3/8/750.0
dlonx=1.0/8/1125.0


#oldx=cv2.resize(old,(600,600))
#cv2.imshow('old',oldx/np.max(old))
#cv2.waitKey(0)

x=np.arange(float(jmax))
y=np.arange(float(imax))
ex_func=interpolate.RegularGridInterpolator((x,y),old,method='nearest')

xx=((s_lon+np.arange(nlon)*dlon)-float(slonx))/dlonx
yy=(float(elatx)-(e_lat-np.arange(nlat)*dlat))/dlatx
xxx,yyy=np.meshgrid(xx,yy)
new=ex_func((yyy,xxx))
#newx=cv2.resize(new,(600,600))
#cv2.imshow('new',newx/np.max(new))
#cv2.waitKey(0)

ut.xs=s_lon
ut.dx=dlon
ut.ye=e_lat
ut.dy=dlat
ut.write_tif('new_bl.tif',new.astype(np.float32),2)

newx=255.0*new/np.max(new)
newx[np.where(newx < 0.0)]=0.0
ut.write_tifB('new_blB.tif',newx.astype(np.uint8),2)

#cv2.destroyAllWindows()

exit()
