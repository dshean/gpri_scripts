#! /usr/bin/env python

"""
David Shean
dshean@gmail.com
2/22/13

This script will processed data collected with the GAMMA ground-based portable radar interferometer.
Outputs a georeferenced gtif orthorectified using the input DEM

To do:
Unwrapped displacement grids
Override GPRI coords with those from DGPS
Allow for multiple GCPs and an improved azimuth for N
Better interpolation when extracting
Offset due to near_range_slc
"""

import sys, os
import numpy
import gdal, osr
import malib, geolib
import extractZ_csv

def open_mli(fn, p):
    f = open(fn, 'rb')
    #Big endian, floating point
    dtype = '>f4'
    #dtype = str(p['image_format']).lower()
    nl = int(p['range_samples'])
    ns = int(p['azimuth_lines'])
    count = nl*ns
    #Note: mli is rotated so that rows correspond to azimuth,
    #Option to rotate so that rows are range (more intiutive to me)
    #mli = numpy.rot90(numpy.fromfile(f,dtype=dtype,count=count).reshape(ns, nl))
    mli = numpy.fromfile(f,dtype=dtype,count=count).reshape(ns, nl)
    f.close()
    #Convert to float32
    return mli.astype(numpy.float32)

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

#Open mli image (or image to project)
mli_fn = sys.argv[1]

#Open parameter file
par_fn = mli_fn+'.par'

#Populate a dictionary with parameter file
p = {}
with open(par_fn) as f:
    next(f)
    next(f)
    for line in f:
        (key, val) = line.strip().split(None, 1)
        p[key.strip(':')] = list(val.split())[0]

#mli = Image.Open(mli_fn)
mli = open_mli(mli_fn, p)

#Mask out values - might want to make this a function of range 
#Or potentially input mask from GAMMA software
thresh = 0.12
mli_ma = numpy.ma.masked_less(mli, thresh)

#Load DEM
#projected, cartesian coords
dem_fn = sys.argv[2]

#Add existence checks for all files

#Extract DEM to ma
dem_ds = gdal.Open(dem_fn, gdal.GA_ReadOnly)
dem_srs = geolib.get_srs(dem_ds)
dem_gt = dem_ds.GetGeoTransform()
dem = malib.gdal_getma(dem_ds)

#There's probably a clever way to do this when populating the dictionary
#For now, force type casting into new variables here
azimuth_lines = int(p['azimuth_lines'])
range_samples = int(p['range_samples'])
range_looks = int(p['range_looks'])
#This should already have been corrected with the range_looks scaling
range_pixel_spacing = float(p['range_pixel_spacing'])
#Check these - may need to shift to center of range_looks 
near_range_slc = float(p['near_range_slc'])
far_range_slc = float(p['far_range_slc'])
#Convert GPRI_az_angle_step and GPRI_az_start_angle to radians
az_angle_step = numpy.radians(float(p['GPRI_az_angle_step']))
az_start_angle = numpy.radians(float(p['GPRI_az_start_angle']))
#lon, lat, elev of GPRI
ref_coord = [float(p['GPRI_ref_east']), float(p['GPRI_ref_north']), float(p['GPRI_ref_alt'])]

#This is output GSD
#mli range_pixel_spacing needs to be multiplied by range_looks
#range_pixel_spacing_mli = range_pixel_spacing * range_looks
range_pixel_spacing_mli = range_pixel_spacing 

#Compute azimuth pixel size in meters (function of range)
az_pixel_spacing = az_angle_step * numpy.arange(near_range_slc, far_range_slc, range_pixel_spacing_mli)

#az_angle_list = az_start_angle + az_angle_step * numpy.arange(azimuth_lines)

#Downsample DEM to match radar GSD, or 2x radar GSD?
#min(range, az)

#Input more precise DGPS coordinates

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
#Radar coords (az, r), (row, col)
gcp_rc = [302, 665]
#World coords (x, y)
#Might want to add z here, need to update angle methods
gcp_wc_latlon = [-121.76924, 46.84570]
gcp_wc_proj = [593837.962, 5188753.337]

#GCP vector in (x,y) mapped coord (ignore z)
#gcp_v = numpy.array([ref_coord_proj[0:2], gcp_wc_proj])
#Setting ref_coord to (0,0)
gcp_v = numpy.array(gcp_wc_proj - ref_coord_proj[0:2])

#Define North vector in (x,y) mapped coord
#N_v = numpy.array([ref_coord_proj[0:2], [ref_coord_proj[0], ref_coord_proj[1] + far_range_slc]]) 
#Setting ref_coord to (0,0)
N_v = numpy.array([ref_coord_proj[0], ref_coord_proj[1] + far_range_slc] - ref_coord_proj[0:2]) 

#Compute angle between north and reference azimuth (radians)
az_N_minus_ref = angle_between(gcp_v, N_v)

#This is the N azimuth sample number
az_N = gcp_rc[0] + az_N_minus_ref / az_angle_step 

#Compute dimensions of output grid in world coordinates
#Polar to cartesian coords, with theta=0 along meridian
#x = r*sin(theta)
#y = r*cos(theta)
#Note az_start = 0 (sample number)
ul_x = ref_coord_proj[0] - far_range_slc * numpy.sin(az_angle_step*(az_N - 0))
#ul_y = ref_coord_proj[1] + far_range_slc * numpy.sin(az_angle_step*(az_N - 0))
ul_y = ref_coord_proj[1] + far_range_slc
lr_x = ref_coord_proj[0] + far_range_slc * numpy.sin(az_angle_step*(azimuth_lines - az_N))
#lr_y = ref_coord_proj[1] - far_range_slc * numpy.sin(az_angle_step*(azimuth_lines - az_N))
lr_y = ref_coord_proj[1] 

bbox = [ul_x, ul_y, lr_x, lr_y]

out_xsize_m = lr_x - ul_x
out_ysize_m = ul_y - lr_y

#Output grid resolution
res = numpy.mean([az_pixel_spacing.mean(), range_pixel_spacing_mli])

#Initialize output grid
out_nl = int(round(out_ysize_m/res))
out_ns = int(round(out_xsize_m/res))
out = numpy.zeros((out_nl, out_ns))

#Want to double check center vs corner of UL pixel
out_gt = [ul_x, res, 0.0, ul_y, 0.0, -res]

ref_coord_px = geolib.mapToPixel(ref_coord_proj[0], ref_coord_proj[1], out_gt)

#Create arrays of x and y map coordinates for each x and y grid cell
out_y_px, out_x_px = numpy.indices(out.shape)
#out_y_px -= ref_coord_px[0]
#out_x_px -= ref_coord_px[1]
out_x_map, out_y_map = geolib.pixelToMap(out_x_px, out_y_px, out_gt)
dem_x_px, dem_y_px = geolib.mapToPixel(out_x_map, out_y_map, dem_gt)
z = extractZ_csv.extractPoint(dem, dem_x_px, dem_y_px) 

#Need to account for first range offset: near_range_slc

#Compute range (meters) for each x,y,z in output grid
r = numpy.sqrt((out_x_map-ref_coord_proj[0])**2 + (out_y_map-ref_coord_proj[1])**2 + (z-ref_coord_proj[2])**2) 

az_px = az_N + numpy.arctan2((out_x_map-ref_coord_proj[0]), (out_y_map-ref_coord_proj[1])) / az_angle_step

#r = numpy.sqrt(out_x_px**2 + out_y_px**2 + ((z - ref_coord_proj[2]) / range_pixel_spacing_mli)**2) # / range_pixel_spacing_mli
#az = az_N - numpy.arctan2(out_x_px, out_y_px) / az_angle_step

#Convert range values to pixels for extraction from mli
r_ma = numpy.ma.masked_outside(r, near_range_slc, far_range_slc) 
r_px_ma = r_ma / range_pixel_spacing_mli
az_px_ma = numpy.ma.masked_outside(az_px, 0, azimuth_lines)

#Extract MLI values from input grid in (r, az) coord
out = extractZ_csv.extractPoint(mli_ma, r_px_ma, az_px_ma)

#Mask out all invalid areas
common_mask = numpy.ma.mask_or(r_px_ma.mask, az_px_ma.mask) 
out_ma = numpy.ma.masked_array(out, mask=common_mask)

#Write out gtif 
gtif_drv = gdal.GetDriverByName("GTiff")

out_fn = mli_fn+'_ortho.tif'
out_srs = dem_srs.ExportToWkt()
out_dt = gdal.GDT_Float32
out_ndv = 0.0

out_ds = gtif_drv.Create(out_fn, out_ns, out_nl, 1, out_dt) 
out_ds.SetGeoTransform(out_gt)
out_ds.SetProjection(out_srs)
out_ds.GetRasterBand(1).WriteArray(out_ma.filled(out_ndv))
out_ds.GetRasterBand(1).SetNoDataValue(out_ndv)

out_ds = None
