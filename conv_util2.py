#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cd /Volumes/Transcend/JAXA土地被覆

import numpy as np
from osgeo import gdal
from osgeo import osr
import pyproj
dstProj = pyproj.Proj(proj="utm", zone="54", ellps="WGS84", units="m")
srcProj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')

lat0=0.0 ; lon0=0.0
dlat=0.0 ; dlon=0.0

xs=0.0 ; xe=0.0
ye=0.0 ; ys=0.0
dx=0.0 ; dy=0.0

# for utm zone54
wkt='PROJCS["WGS 84 / UTM zone 54N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",141],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","32654"]]'

# for lat-lon
wkt2='GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]]'

def bl2utm(ll):
  x,y=pyproj.transform(srcProj, dstProj, ll[1], ll[0])
  return [x,y]

def utm2bl(xy):
  lon,lat=pyproj.transform(dstProj, srcProj, xy[0], xy[1])
  return[lat,lon]

def read_tif(fname):
  src = gdal.Open(fname, gdal.GA_Update)
  pdem = src.GetRasterBand(1)
  gt = src.GetGeoTransform()
  image = pdem.ReadAsArray()
  proj = osr.SpatialReference()
  proj.ImportFromWkt(src.GetProjectionRef())
  return [gt,proj,image]

def write_tif(dname,data,select):
  driver = gdal.GetDriverByName('GTiff')
  #wkt_projection=proj.ExportToWkt()
  y_pixels,x_pixels=data.shape
  dataset = driver.Create(
    dname,
    x_pixels,
    y_pixels,
    1,
    gdal.GDT_Float32, )
  dataset.SetGeoTransform((
    xs,
    dx,
    0, 
    ye,
    0,
    -dy))  
  #dataset.SetProjection(wkt_projection)
  if select==1: dataset.SetProjection(wkt)
  else: dataset.SetProjection(wkt2)
  dataset.GetRasterBand(1).WriteArray(data)
  dataset.FlushCache()

def write_tifB(dname,data,select):
  driver = gdal.GetDriverByName('GTiff')
  #wkt_projection=proj.ExportToWkt()
  y_pixels,x_pixels=data.shape
  dataset = driver.Create(
    dname,
    x_pixels,
    y_pixels,
    1,
    gdal.GDT_Byte, )
  dataset.SetGeoTransform((
    xs,
    dx,
    0, 
    ye,
    0,
    -dy))  
  #dataset.SetProjection(wkt_projection)
  if select==1: dataset.SetProjection(wkt)
  else: dataset.SetProjection(wkt2)
  dataset.GetRasterBand(1).WriteArray(data)
  dataset.FlushCache()

def convert(image,imax,jmax):
  data=np.zeros(imax*jmax,dtype=np.float32).reshape(jmax,imax)
  for j in range(jmax):
    if (j % 100) == 0 : print(j)
    y=ye-j*dy
    for i in range(imax):
      x=xs+i*dx
      temp=utm2bl([x,y])
      ii=int(np.round((temp[1]-lon0)/dlon))
      jj=int(np.round((lat0-temp[0])/dlat))
      data[j,i]=image[jj,ii]
  return data

def convert2(image,imax,jmax):
  data=np.zeros(imax*jmax,dtype=np.uint8).reshape(jmax,imax)
  for j in range(jmax):
    if (j % 100) == 0 : print(j)
    y=ye-j*dy
    for i in range(imax):
      x=xs+i*dx
      temp=utm2bl([x,y])
      ii=int(np.round((temp[1]-lon0)/dlon))
      jj=int(np.round((lat0-temp[0])/dlat))
      test=image[(jj-1):(jj+2),(ii-1):(ii+2)]
      count=np.zeros(11)
      for k in range(9) :
        count[test[k/3,k%3]]=count[test[k/3,k%3]]+1
      test2=np.where(count == np.max(count))
      data[j,i]=test2[0][0]
  return data

if __name__=='__main__':
    import sys
    param=sys.argv
    if len(param) !=3:
      print('Usaage: jaxa_util.py latitude longitude')
      exit()
    #print param[1:]
    lat=float(sys.argv[1])
    lon=float(sys.argv[2])
    x,y=bl2utm([lat,lon])
    #print('{0:6.2f} {1:6.2f}'.format(x,y))
    print('x={0:6.2f},  y={1:6.2f}'.format(x,y))
    lat2,lon2=utm2bl([x,y])
    print('lat2={0:9.7f},  lon2={1:9.7f}'.format(lat2,lon2))

    

