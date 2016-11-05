# coding: utf-8
import malib
import geolib
from osgeo import gdal

def dist(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

pos1 = [595396.48277,5181880.22677]
pos2 = [596168.611,5182875.521]

ds = gdal.Open('rainierlidar_wgs84_shpclip.tif')
dem = malib.ds_getma(ds)
x, y = geolib.get_xy_grids(ds)

d = dist(pos1, pos2)
grid = np.array([x, y])
b = dist(pos1, grid)
c = dist(pos2, grid)
conv = np.rad2deg(np.arccos((b**2 + c**2 - d**2)/(2*b*c)))
conv_m = np.ma.array(conv, mask=dem.mask)
malib.iv(conv_m)
malib.print_stats(conv_m)
