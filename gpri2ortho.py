#! /usr/bin/env python

"""
David Shean
dshean@gmail.com
2/22/13

This script will processed data files collected with the GAMMA ground-based portable radar interferometer
and processed with the GAMMA software.

Outputs a georeferenced gtif orthorectified using the input DEM

To do:
Proper argument parsing with python argparse - gcp coords, multiple par, output resolution?
Existence checks for all input files
Proper datetime handling for determining interferogram interval
Copy library functions here for standalone use
Allow override of GPRI coords with those from DGPS
Allow for multiple GCPs and an improved azimuth for N
Bilinear interpolation when extracting
Offset due to near_range_slc
"""

import sys
import os
from datetime import datetime, timedelta

import numpy as np
import scipy as sp
from osgeo import gdal, osr

#From dshean's dem_tools
from pygeotools.lib import geolib
from pygeotools.lib import iolib
from pygeotools.lib import malib

#Return a np array from image file
def open_img(fn, p):
    f = open(fn, 'rb')
    #Big endian, floating point
    dtype = '>f4'
    #dtype = str(p['image_format']).lower()
    nl = int(p['range_samples'])
    ns = int(p['azimuth_lines'])
    count = nl*ns
    img = np.fromfile(f,dtype=dtype,count=count).reshape(ns, nl)
    #Note: img is rotated so that rows correspond to azimuth,
    #Option to rotate so that rows are range (more intiutive to me)
    #img = np.rot90(img)
    f.close()
    #Convert to native float32
    return img.astype(np.float32)

#Return a dictionary with values from parameter file
def parse_par(par_fn):
    p = {}
    with open(par_fn) as f:
        #Skip the first two lines
        next(f); next(f)
        for line in f:
            #This splits after the first whitespace
            (key, val) = line.strip().split(None, 1)
            #The following populates a dictionary with only the first value (strip units, etc)
            #p[key.strip(':')] = list(val.split())[0]
            #Below will preserve strings with spaces, like date and title
            #Do the parsing during type casting
            p[key.strip(':')] = val 
    return p

#Read a file containing a GCP with 'az_px, range_px, x_coord_proj, y_coord_proj'
#Skip first line with comment
def parse_gcp(fn):
    f = open(fn, 'r')
    next(f)
    line = [float(i) for i in next(f).strip('\n').replace(' ', '').split(',')]
    f.close()
    return line

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle1 = np.arccos(np.vdot(v1_u, v2_u))
    if np.isnan(angle1).all():
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle1

def signed_angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle1 = np.arctan2(v2_u[1],v2_u[0]) - np.arctan2(v1_u[1],v1_u[0])
    if np.isnan(angle1).all():
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    #Want to go from 0 to 2pi here
    if angle1 > np.pi:
        angle1 -= 2 * np.pi
    return angle1

#extract Z value for single pixel or for coordinate arrays
def extractPoint(b, x, y):
    b = malib.checkma(b)
    x = np.clip(x, 0, b.shape[1] - 1)
    y = np.clip(y, 0, b.shape[0] - 1)
    #Note: simplest way using integer indices 
    return b[np.ma.around(y).astype(int), np.ma.around(x).astype(int)]
    #Interpolate values for sub-pixel indices
    #return geolib.bilinear(x, y, b, gt)
    #The following is the ideal way to do this
    #Unfortunately, doesn't work for nan
    #http://projects.scipy.org/scipy/ticket/1155
    #return malib.nanfill(b, sp.ndimage.interpolation.map_coordinates, [y, x], cval=b.fill_value) 
    #Creates bogus values near edges
    #return sp.ndimage.interpolation.map_coordinates(b, [y, x], cval=b.fill_value) 

#Open input file 
in_fn = sys.argv[1]
in_ext = os.path.splitext(in_fn)[1].split('.')[1]

out_fn = os.path.splitext(in_fn)[0]

#Open parameter file
#par_fn = in_fn+'.par'
par_fn = sys.argv[2]
p = parse_par(par_fn)

#There's probably a clever way to do this when populating the dictionary
#For now, force type casting into new variables here
azimuth_lines = int(p['azimuth_lines'])
range_samples = int(p['range_samples'])
range_looks = int(p['range_looks'])
#This should already have been corrected with the range_looks scaling
range_pixel_spacing = float(p['range_pixel_spacing'].split()[0])
#Check these - may need to shift to center of range_looks 
near_range_slc = float(p['near_range_slc'].split()[0])
far_range_slc = float(p['far_range_slc'].split()[0])
#Convert GPRI_az_angle_step and GPRI_az_start_angle to radians
az_angle_step = np.radians(float(p['GPRI_az_angle_step'].split()[0]))
az_start_angle = np.radians(float(p['GPRI_az_start_angle'].split()[0]))
#lon, lat, elev of GPRI
ref_coord = [float(p['GPRI_ref_east']), float(p['GPRI_ref_north']), float(p['GPRI_ref_alt'].split()[0])]

freq = float(p['radar_frequency'].split()[0])
c = 299792458.0 #m/s
wavelength = c/freq

#Need to handle date extraction
title = p['title']
date_str = p['date'].replace(' ', '')
center_time = p['center_time']

single_list = ['slc', 'mli']
multi_list = ['unw', 'diff']
#'adf', 'cc'

if in_ext in single_list:
    #Open img and create masked array
    img_ma = np.ma.masked_equal(open_img(in_fn, p), 0)
    #Mask out values - might want to make this a function of range 
    #Or potentially input mask from GAMMA software
    #thresh = 0.12
    thresh = 0
    img_ma = np.ma.masked_less(img_ma, thresh)
elif in_ext in multi_list:
    #Open img and create masked array
    img_ma = np.ma.masked_equal(open_img(in_fn, p), 0)
    #Want to open 2nd parameter file for diff or unw
    #par_fn2 = sys.argv[3]
    #p2 = parse_par(par_fn2)
    #Alternatively, could parse fn and find par in same mli_dir
    #Or, parse FN to get datetime

    #This is interval between MLIs used to produce interferogram
    #Need proper datetime extraction of interval
    #Hardcoded for now
    #dt = timedelta(seconds=3600.0)
    dt = timedelta(seconds=7200.0)
    #Conversion factors
    dt_days = dt.total_seconds()/86400.0
    dt_yr = dt.total_seconds()/(365.25 * 86400.0)
    
    #Unwrapped input values should be m?
    #Now scale values to be LOS displacements in m/day
    #img_ma = -(wavelength/(4*np.pi)) * img_ma / dt_days
    img_ma = wavelength * -img_ma / dt_days
elif in_ext == 'mat':
    import scipy.io
    mat = scipy.io.loadmat(in_fn)
    #Mean
    #key = mat.keys()[0]
    #Std
    #key = mat.keys()[1]
    #Median
    key = mat.keys()[4]
    #Search for ndv
    #Assume ndv if not found
    #ndv = 0
    #Note: Kate's files are transpose of original inputs
    #img_ma = np.ma.masked_equal(mat[key].T, ndv)
    #img_ma = np.ma.masked_equal(np.ma.fix_invalid(mat[key].T), ndv)

    #out_fn += '_'date_str+'_'+key
    out_fn = os.path.join(os.path.split(in_fn)[0], date_str+'_'+key)

    #Note, values are negative
    img_ma = -np.ma.fix_invalid(mat[key].T)

    #mask_fn = os.path.splitext(in_fn)[0]+'_mask.mat'
    #mask_mat = scipy.io.loadmat(mask_fn)
    #mask_key = key+'mask'
    #mask = mask_mat[mask_key].T
else:
    print "Unrecognized extension, continuing without filtering or scaling"

#Parse GCPs
gcp_fn = os.path.splitext(in_fn)[0]+'.gcp' 
gcp = parse_gcp(gcp_fn) 

#Load DEM
#Should be in projected, cartesian coords
dem_fn = sys.argv[3]

#Extract DEM to ma
dem_ds = iolib.fn_getds(dem_fn)
dem_srs = geolib.get_ds_srs(dem_ds)
dem_gt = dem_ds.GetGeoTransform()
dem = iolib.ds_getma(dem_ds)

#Compute azimuth pixel size in meters (function of range)
az_pixel_spacing = az_angle_step * np.arange(near_range_slc, far_range_slc, range_pixel_spacing)

#Downsample DEM to match radar GSD, or 2x radar GSD?
#min(range, az)

#Want to allow for input more precise DGPS coordinates for GPRI origin
#Trimble GeoXH shp output has XY, need to process raw data for XYZ
#46.78364631
#-121.7502352
#ref_coord = [-121.7502352, 46.78364631, ref_coord[2]]
#Need to correct boresight for "principal point" of radar relative to GPS point at top of tower - this will depend on antenna used for interferogram

#Convert GPRI origin to projected coords
#GPRI origin coordinates in header are WGS84
ref_srs = geolib.wgs_srs
#Create coordinate transformation object
ct = osr.CoordinateTransformation(ref_srs, dem_srs)

#Projected coordinates of GPRI origin
#x, y, z
ref_coord_proj = np.array(ct.TransformPoint(*ref_coord))
#GCP vector in (x,y) mapped coord (ignore z)
#Setting ref_coord to (0,0)
gcp_v = np.array(gcp[2:4] - ref_coord_proj[0:2])

#Define North vector in (x,y) mapped coord
#Setting ref_coord to (0,0)
N_v = np.array([ref_coord_proj[0], ref_coord_proj[1] + far_range_slc] - ref_coord_proj[0:2]) 

#Compute angle between north and reference azimuth (radians)
#ang_N_minus_gcp = angle_between(gcp_v, N_v)
#This uses perp dot product for signed angle
ang_N_minus_gcp = signed_angle(gcp_v, N_v)

#This is the N azimuth sample number
#NOTE: may be outside range of (0, azimuth_lines) 
az_N = gcp[0] - ang_N_minus_gcp / az_angle_step 

#This is azimuth column number of 0 deg survey origin
az_0 = int(np.rint(-az_start_angle / az_angle_step))

#az_angle_list = ang_N_minus_gcp + az_angle_step * np.arange(azimuth_lines)
az_angle_list = az_angle_step * (np.arange(azimuth_lines) - az_N)

#Compute the heading angle for each az column relative to N (for printing)
az_angle_list_deg = np.rad2deg(az_angle_list) 
az_angle_list_deg[az_angle_list_deg < 0] += 360

#This is for generalization of the (r, az) to (x, y) coords
range_list = np.empty_like(az_angle_list)
range_list = far_range_slc

#Compute dimensions of output grid in world coordinates
#Polar to cartesian coords, with theta=0 along meridian
#x = r*sin(theta)
#y = r*cos(theta)
#Coordinates for maximum range at all azimuths
x = ref_coord_proj[0] + range_list * np.sin(az_angle_list)
y = ref_coord_proj[1] + range_list * np.cos(az_angle_list)

print
print "Origin: (%0.3f, %0.3f)" % (ref_coord_proj[0], ref_coord_proj[1])
print "Min azimuth: %0.1f (%0.3f, %0.3f)" % (az_angle_list_deg[0], x[0], y[0])
print "Zero azimuth: %0.1f (%0.3f, %0.3f)" % (az_angle_list_deg[az_0], x[az_0], y[az_0])
print "Max azimuth: %0.1f (%0.3f, %0.3f)" % (az_angle_list_deg[-1], x[-1], y[-1])
print

#Compute bounding box in mapped coordinates
ul_x = np.append(x, [ref_coord_proj[0]]).min()
ul_y = np.append(y, [ref_coord_proj[1]]).max()
lr_x = np.append(x, [ref_coord_proj[0]]).max()
lr_y = np.append(y, [ref_coord_proj[1]]).min()

bbox = [ul_x, ul_y, lr_x, lr_y]
out_xsize_m = lr_x - ul_x
out_ysize_m = ul_y - lr_y

#Output grid resolution
#Might want to take min of these two?  Or just use range res?
res = np.mean([az_pixel_spacing.mean(), range_pixel_spacing])

#Initialize output grid
out_nl = int(round(out_ysize_m/res))
out_ns = int(round(out_xsize_m/res))
out = np.zeros((out_nl, out_ns))

#Want to double check whether we're using center vs corner of UL pixel - add 0.5 px offsets
out_gt = [ul_x, res, 0.0, ul_y, 0.0, -res]

#Compute pixel coordinates for GPRI origin in output grid
ref_coord_px = geolib.mapToPixel(ref_coord_proj[0], ref_coord_proj[1], out_gt)

#Create arrays of x and y map coordinates for each output grid cell
out_y_px, out_x_px = np.indices(out.shape)
out_x_map, out_y_map = geolib.pixelToMap(out_x_px, out_y_px, out_gt)

#Extract DEM elevations for output map coordinates
dem_x_px, dem_y_px = geolib.mapToPixel(out_x_map, out_y_map, dem_gt)
z = extractPoint(dem, dem_x_px, dem_y_px) 

#Want to clean these up and define functions

#Compute range (meters) for each x,y,z in output grid
r = np.sqrt((out_x_map-ref_coord_proj[0])**2 + (out_y_map-ref_coord_proj[1])**2 + (z-ref_coord_proj[2])**2) 
#az_px = az_N + np.arctan2((out_x_map-ref_coord_proj[0]), (out_y_map-ref_coord_proj[1])) / az_angle_step

#Angles should be 0 to 2*pi relative to N
out_az_angle_list = np.arctan2((out_x_map-ref_coord_proj[0]), (out_y_map-ref_coord_proj[1]))
#if np.any(out_az_angle_list < 0):
#    out_az_angle_list += 2 * np.pi
az_px = az_N + out_az_angle_list / az_angle_step

#Want to preserve only valid ranges
r_ma = np.ma.masked_outside(r, near_range_slc, far_range_slc) 
#Convert range values to pixels for extraction from img
#r_px_ma = r_ma / range_pixel_spacing
r_px_ma = (r_ma - near_range_slc) / range_pixel_spacing
#Want to preserve only valid azimuths
az_px_ma = np.ma.masked_outside(az_px, 0, azimuth_lines)

#Extract img values from input grid in (r, az) coord
out = extractPoint(img_ma, r_px_ma, az_px_ma)

#Mask out all invalid areas
common_mask = np.ma.mask_or(r_px_ma.mask, az_px_ma.mask) 
out_ma = np.ma.masked_array(out, mask=common_mask)

#Trim to valid area
#Note: need to update geotransform as well - need an alternative masktrim that accepts/returns gt
#On second thought, might be best to preserve the same dimensions, as different images will have different valid regions, preserving allows for direct comparison
#out_ma_trim = malib.masktrim(out_ma)

#Write out gtif 
gtif_drv = gdal.GetDriverByName("GTiff")

out_fn = out_fn+'_ortho.tif'
out_srs = dem_srs.ExportToWkt()
out_dt = gdal.GDT_Float32
out_ndv = 0.0

out_ds = gtif_drv.Create(out_fn, out_ns, out_nl, 1, out_dt) 
out_ds.SetGeoTransform(out_gt)
out_ds.SetProjection(out_srs)
out_ds.GetRasterBand(1).WriteArray(out_ma.filled(out_ndv))
out_ds.GetRasterBand(1).SetNoDataValue(out_ndv)

out_ds = None
