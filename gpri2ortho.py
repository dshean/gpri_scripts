#! /usr/bin/env python

"""
David Shean
dshean@gmail.com
2/22/13

This script will processed data files collected with the GAMMA ground-based portable radar interferometer
and processed with the GAMMA software.

Outputs a georeferenced gtif orthorectified using the input DEM

To do:
Proper argument parsing - gcp coords, multiple par, output resolution?
Existence checks for files
Proper datetime handling
Copy library functions here for standalone use
Allow override of GPRI coords with those from DGPS
Allow for multiple GCPs and an improved azimuth for N
Bilinear interpolation when extracting
Offset due to near_range_slc
"""

import sys, os
from datetime import datetime, timedelta

import numpy, scipy
import gdal, osr

#From dshean's dem_tools
import malib, geolib

#Return a numpy array from image file
def open_img(fn, p):
    f = open(fn, 'rb')
    #Big endian, floating point
    dtype = '>f4'
    #dtype = str(p['image_format']).lower()
    nl = int(p['range_samples'])
    ns = int(p['azimuth_lines'])
    count = nl*ns
    img = numpy.fromfile(f,dtype=dtype,count=count).reshape(ns, nl)
    #Note: img is rotated so that rows correspond to azimuth,
    #Option to rotate so that rows are range (more intiutive to me)
    #img = numpy.rot90(img)
    f.close()
    #Convert to native float32
    return img.astype(numpy.float32)

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

def unit_vector(vector):
    return vector / numpy.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle1 = numpy.arccos(numpy.vdot(v1_u, v2_u))
    if numpy.isnan(angle1).all():
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return numpy.pi
    return angle1

def signed_angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle1 = numpy.arctan2(v2_u[1],v2_u[0]) - numpy.arctan2(v1_u[1],v1_u[0])
    if numpy.isnan(angle1).all():
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return numpy.pi
    #Want to go from 0 to 2pi here
    if angle1 < 0:
        angle1 += 2 * numpy.pi
    return angle1

#extract Z value for single pixel or for coordinate arrays
def extractPoint(b, x, y):
    b = malib.checkma(b)
    x = numpy.clip(x, 0, b.shape[1] - 1)
    y = numpy.clip(y, 0, b.shape[0] - 1)
    #Note: simplest way using integer indices 
    return b[numpy.ma.around(y).astype(int), numpy.ma.around(x).astype(int)]
    #Interpolate values for sub-pixel indices
    #return geolib.bilinear(x, y, b, gt)
    #The following is the ideal way to do this
    #Unfortunately, doesn't work for nan
    #http://projects.scipy.org/scipy/ticket/1155
    #return malib.nanfill(b, scipy.ndimage.interpolation.map_coordinates, [y, x], cval=b.fill_value) 
    #Creates bogus values near edges
    #return scipy.ndimage.interpolation.map_coordinates(b, [y, x], cval=b.fill_value) 

#Open img image (or image to project)
in_fn = sys.argv[1]
in_ext = os.path.splitext(in_fn)[1].split('.')[1]

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
az_angle_step = numpy.radians(float(p['GPRI_az_angle_step'].split()[0]))
az_start_angle = numpy.radians(float(p['GPRI_az_start_angle'].split()[0]))
#lon, lat, elev of GPRI
ref_coord = [float(p['GPRI_ref_east']), float(p['GPRI_ref_north']), float(p['GPRI_ref_alt'].split()[0])]

freq = float(p['radar_frequency'].split()[0])
c = 299792458.0 #m/s
wavelength = c/freq

#Need to handle date extraction
title = p['title']
date_str = p['date']
center_time = p['center_time']
#Open img and create masked array
img_ma = numpy.ma.masked_equal(open_img(in_fn, p), 0)

single_list = ['slc', 'mli']
multi_list = ['unw', 'diff', 'adf', 'cc']

if in_ext in single_list:
    #Mask out values - might want to make this a function of range 
    #Or potentially input mask from GAMMA software
    #thresh = 0.12
    thresh = 0
    img_ma = numpy.ma.masked_less(img_ma, thresh)
elif in_ext in multi_list:
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
    #img_ma = -(wavelength/(4*numpy.pi)) * img_ma / dt_days
    img_ma = wavelength * -img_ma / dt_days
else:
    print "Unrecognized extension, continuing without filtering or scaling"

#Load DEM
#Should be in projected, cartesian coords
dem_fn = sys.argv[3]

#Extract DEM to ma
dem_ds = gdal.Open(dem_fn, gdal.GA_ReadOnly)
dem_srs = geolib.get_srs(dem_ds)
dem_gt = dem_ds.GetGeoTransform()
dem = malib.gdal_getma(dem_ds)

#Compute azimuth pixel size in meters (function of range)
az_pixel_spacing = az_angle_step * numpy.arange(near_range_slc, far_range_slc, range_pixel_spacing)

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
ref_coord_proj = numpy.array(ct.TransformPoint(*ref_coord))

#GCP reference 
#Paradise Pullout (roi)
#Radar coords (az, r), (row, col)
gcp_rc = [302, 665]
#World coords (x, y)
#Might want to add z here, would need to update angle methods
gcp_wc_latlon = [-121.76924, 46.84570]
gcp_wc_proj = [593837.962, 5188753.337]

#Sunrise
#gcp_rc = [202, 2119]
#gcp_wc_latlon = [-121.73161,46.87221]
#gcp_wc_proj = [596659.249,5191743.850]

#GCP vector in (x,y) mapped coord (ignore z)
#gcp_v = numpy.array([ref_coord_proj[0:2], gcp_wc_proj])
#Setting ref_coord to (0,0)
gcp_v = numpy.array(gcp_wc_proj - ref_coord_proj[0:2])

#Define North vector in (x,y) mapped coord
#N_v = numpy.array([ref_coord_proj[0:2], [ref_coord_proj[0], ref_coord_proj[1] + far_range_slc]]) 
#Setting ref_coord to (0,0)
N_v = numpy.array([ref_coord_proj[0], ref_coord_proj[1] + far_range_slc] - ref_coord_proj[0:2]) 

#Compute angle between north and reference azimuth (radians)
#ang_N_minus_gcp = angle_between(gcp_v, N_v)
#This uses perp dot product for signed angle
ang_N_minus_gcp = signed_angle(gcp_v, N_v)

#This is the N azimuth sample number
#NOTE: may be outside range of (0, azimuth_lines) for south facing surveys
az_N = gcp_rc[0] - ang_N_minus_gcp / az_angle_step 

#az_angle_list = ang_N_minus_gcp + az_angle_step * numpy.arange(azimuth_lines)
az_angle_list = az_angle_step * (numpy.arange(azimuth_lines) - az_N)

range_list = numpy.empty_like(az_angle_list)
range_list = far_range_slc

#Compute dimensions of output grid in world coordinates
#Polar to cartesian coords, with theta=0 along meridian
#x = r*sin(theta)
#y = r*cos(theta)
#Coordinates for maximum range at all azimuths
x = ref_coord_proj[0] + range_list * numpy.sin(az_angle_list)
y = ref_coord_proj[1] + range_list * numpy.cos(az_angle_list)

ul_x = numpy.append(x, [ref_coord_proj[0]]).min()
ul_y = numpy.append(y, [ref_coord_proj[1]]).max()
lr_x = numpy.append(x, [ref_coord_proj[0]]).max()
lr_y = numpy.append(y, [ref_coord_proj[1]]).min()

"""
Lazy approach in early tests
ul_x = ref_coord_proj[0] - far_range_slc * numpy.sin(az_angle_step*(az_N - 0))
ul_y = ref_coord_proj[1] + far_range_slc
lr_x = ref_coord_proj[0] + far_range_slc * numpy.sin(az_angle_step*(azimuth_lines - az_N))
lr_y = ref_coord_proj[1] 
"""

bbox = [ul_x, ul_y, lr_x, lr_y]
out_xsize_m = lr_x - ul_x
out_ysize_m = ul_y - lr_y

#Output grid resolution
res = numpy.mean([az_pixel_spacing.mean(), range_pixel_spacing])

#Initialize output grid
out_nl = int(round(out_ysize_m/res))
out_ns = int(round(out_xsize_m/res))
out = numpy.zeros((out_nl, out_ns))

#Want to double check center vs corner of UL pixel
out_gt = [ul_x, res, 0.0, ul_y, 0.0, -res]

#Compute pixel coordinates for GPRI origin in output grid
ref_coord_px = geolib.mapToPixel(ref_coord_proj[0], ref_coord_proj[1], out_gt)

#Create arrays of x and y map coordinates for each output grid cell
out_y_px, out_x_px = numpy.indices(out.shape)
out_x_map, out_y_map = geolib.pixelToMap(out_x_px, out_y_px, out_gt)

#Extract DEM elevations for output map coordinates
dem_x_px, dem_y_px = geolib.mapToPixel(out_x_map, out_y_map, dem_gt)
z = extractPoint(dem, dem_x_px, dem_y_px) 

#Want to clean these up and define functions

#Compute range (meters) for each x,y,z in output grid
r = numpy.sqrt((out_x_map-ref_coord_proj[0])**2 + (out_y_map-ref_coord_proj[1])**2 + (z-ref_coord_proj[2])**2) 
#az_px = az_N + numpy.arctan2((out_x_map-ref_coord_proj[0]), (out_y_map-ref_coord_proj[1])) / az_angle_step

#Angles should be 0 to 2*pi relative to N
out_az_angle_list = numpy.arctan2((out_x_map-ref_coord_proj[0]), (out_y_map-ref_coord_proj[1]))
if numpy.any(out_az_angle_list < 0):
    out_az_angle_list += 2 * numpy.pi
    #out_az_angle_list %= 2 * numpy.pi
az_px = az_N + out_az_angle_list / az_angle_step

#Should be possible to do this in output map pixels, but the above works
#r = numpy.sqrt(out_x_px**2 + out_y_px**2 + ((z - ref_coord_proj[2]) / range_pixel_spacing)**2) # / range_pixel_spacing
#az = az_N - numpy.arctan2(out_x_px, out_y_px) / az_angle_step

#Want to preserve only valid ranges
r_ma = numpy.ma.masked_outside(r, near_range_slc, far_range_slc) 
#Convert range values to pixels for extraction from img
r_px_ma = r_ma / range_pixel_spacing
#Want to preserve only valid azimuths
az_px_ma = numpy.ma.masked_outside(az_px, 0, azimuth_lines)

#Extract img values from input grid in (r, az) coord
out = extractPoint(img_ma, r_px_ma, az_px_ma)

#Mask out all invalid areas
common_mask = numpy.ma.mask_or(r_px_ma.mask, az_px_ma.mask) 
out_ma = numpy.ma.masked_array(out, mask=common_mask)

#Trim to valid area
#Need to update geotransform as well
#Might be best to preserve the same dimensions, as different images will have different valid regions, preserving allows for direct comparison
#out_ma_trim = malib.masktrim(out_ma)

#Write out gtif 
gtif_drv = gdal.GetDriverByName("GTiff")

out_fn = in_fn+'_ortho.tif'
out_srs = dem_srs.ExportToWkt()
out_dt = gdal.GDT_Float32
out_ndv = 0.0

out_ds = gtif_drv.Create(out_fn, out_ns, out_nl, 1, out_dt) 
out_ds.SetGeoTransform(out_gt)
out_ds.SetProjection(out_srs)
out_ds.GetRasterBand(1).WriteArray(out_ma.filled(out_ndv))
out_ds.GetRasterBand(1).SetNoDataValue(out_ndv)

out_ds = None
