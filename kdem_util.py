#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cd /Volumes/Transcend/KibanDEM
import os
import numpy as np

def mcode(lat,lon):
  b0=int(1.5*lat)
  b1=int(8*(1.5*lat-b0))
  l0=int(lon-100.0)
  l1=int(8*(lon-100.0-l0))
  return [100*b0+l0,10*b1+l1]

def rcode(code1,code2):
  b0=code1 /100
  b1=code2 / 10
  l0=code1 % 100
  l1=code2 % 10
  lat = b0 * 2.0 /3.0 + (b1+1) * 2.0/3.0/8.0
  lon = 100.0 + l0 + l1 / 8.0
  return [lat,lon]

def rcode2(xysrt,xyend):
  csrt=mcode(xysrt[0],xysrt[1])
  cend=mcode(xyend[0],xyend[1])
  code1=(cend[0]/100)*100+(csrt[0] % 100)
  code2=(cend[1]/10)*10+(csrt[1] % 10)
  return rcode(code1,code2)

def dcode(xysrt,xyend):
  csrt=mcode(xysrt[0],xysrt[1])
  cend=mcode(xyend[0],xyend[1])
  d1=8*(cend[0] % 100)+(cend[1] % 10)-8*(csrt[0] % 100)-(csrt[1] % 10)
  d2=8*cend[0]/100+cend[1]/10-8*csrt[0]/100-csrt[1]/10
  return [csrt,d1+1,d2+1]

def xdem(fin):
  #dem=np.zeros((750,1125))
  tall='a' ; type='a'
  elev=0.0
  flag=0
  if os.path.exists(fin)==False:
    print 'No file found'
    return 0
  f=open(fin)
  lines=f.readlines()
  f.close()
  data=[]
  flag=0
  for line in lines:
    if flag==1:
      temp=line.split(',')
      if len(temp)==2: data.append(float(temp[1]))   
    if line.find('<gml:tupleList>')!=-1: flag=1
  datax=np.array(data).reshape((750,1125))
  return np.flipud(datax.astype(np.float32))

def xcode(code1,code2,ncol,nrow):
  imax=ncol*1125
  jmax=nrow*750
  #image=np.zeros((jmax,imax))
  fname1='FG-GML-'
  fname2='-dem10b-20090201.xml'
  x2=code1 % 100
  x3=code2 % 10
  y2=code1 / 100
  y3=code2 /10
  for i in range(ncol):
    ix2=x2 ; ix3=x3+i
    #if(ix3 ge 8) then ix2=ix2+1
    ix2=ix2+ix3/8
    ix3=ix3 % 8
    for j in range(nrow):
      iy2=y2 ; iy3=y3+j
      #if(iy3 ge 8) then iy2=iy2+1
      iy2=iy2+iy3/8
      iy3=iy3 % 8
      code1x='{:02d}'.format(100*iy2+ix2)
      code2x='{:02d}'.format(10*iy3+ix3)
      fin=code1x+'/'+fname1+code1x+'-'+code2x+fname2
      print fin
      #temp=xdem(fin)
      #image[(i*1125):((i+1)*1125),(j*750):((j+1)*750)]=temp
 
def composite(code1,code2,ncol,nrow):
  imax=ncol*1125
  jmax=nrow*750
  image=np.zeros((jmax,imax))
  fname1='FG-GML-'
  fname2='-dem10b-20090201.xml'
  x2=code1 % 100
  x3=code2 % 10
  y2=code1 / 100
  y3=code2 /10
  for i in range(ncol):
    ix2=x2 ; ix3=x3+i
    #if(ix3 ge 8) then ix2=ix2+1
    ix2=ix2+ix3/8
    ix3=ix3 % 8
    for j in range(nrow):
      iy2=y2 ; iy3=y3+j
      #if(iy3 ge 8) then iy2=iy2+1
      iy2=iy2+iy3/8
      iy3=iy3 % 8
      code1x='{:02d}'.format(100*iy2+ix2)
      code2x='{:02d}'.format(10*iy3+ix3)
      fin=code1x+'/'+fname1+code1x+'-'+code2x+fname2
      print fin
      temp=xdem(fin)
      image[(j*750):((j+1)*750),(i*1125):((i+1)*1125)]=temp
  return np.flipud(image)
 