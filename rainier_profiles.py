#! /usr/bin/env python

import os
import sys
import numpy 
import matplotlib.pyplot as plt
import scipy.signal
import cookb_signalsmooth as sm
import scipy.ndimage
import malib

def smooth(x, window_len=11):
    return scipy.signal.medfilt(x, window_len)

def smooth2(x, window_len=11, window='hanning'):
    return sm.smooth(x, window_len, window='hanning')

csv_fn = sys.argv[1]

#Exporting from Profile tool includes nan
#genfromtxt cleans these up
a = numpy.genfromtxt(csv_fn, delimiter=',', missing_values=0, usemask=True, names=True)
names = numpy.array(a.dtype.names).reshape(6,2)

#Note: last column is LiDAR

win = 9 
i = 1 
plt.figure(figsize=(6,10))
title = os.path.splitext(csv_fn)[0]
plt.subplot(311)
plt.title(title)
plt.ylim(-0.1, 1.5)

for x,y in names[:-1]:
    y_ma = numpy.ma.masked_equal(a[y], 0)
    #This dilates the mask to throw out interpolated values near nodata
    #Works very well when combined with malib.nanfill for the smoothing (which uses ndimage and can't handle ma)
    y_ma.mask = scipy.ndimage.binary_dilation(y_ma.mask, iterations=i)
    y_smooth = malib.nanfill(y_ma, smooth2, win)
    plt.plot(a[x], y_smooth, label=y)

#plt.xlabel('Distance from summit (m)')
plt.ylabel('LOS Velocity (m/day)')
plt.legend(prop={'size':8})
#plt.savefig(title+'_LOS_v.pdf')

#Plot elevation
win = 1
x,y = names[-1]
x_ma = a[x]
y_ma = numpy.ma.masked_equal(a[y], 0)
y_elev_smooth = malib.nanfill(y_ma, smooth2, win)
plt.subplot(312)
plt.plot(x_ma, y_ma)
#plt.xlabel('Distance from summit (m)')
plt.ylabel('2008 LiDAR Elevation (m NAD80)')

#Deal with slopes
#Define ice thickness
h = 100.
#Compute spacing
dx = numpy.ma.diff(a[x])
#Compute average spacing
avg_dx = dx.mean()
#Define smoothing window 2*h
win = 2*h/avg_dx
y_ma = numpy.ma.masked_equal(a[y], 0)
y_slope_smooth = numpy.ma.diff(malib.nanfill(y_ma, smooth2, win))

plt.subplot(313)
plt.plot(x_ma[:-1]+0.5*dx, y_slope_smooth)
plt.ylim(-1.5, 0)
plt.xlabel('Distance from summit (m)')
plt.ylabel('Slope (deg, %0.0f m window)' % win) 
plt.savefig(title+'.pdf', bbox_inches='tight')
plt.show()
