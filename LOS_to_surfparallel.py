#! /usr/bin/env python

#Utility to take GPRI LOS displacements (mapped) and produce absolute surface velocity vectors

#Consult Konrad et al (1999)

#Open DEM
#Smooth and downsample to ~5-10 ice thicknesses
#Ian suggested tangential plane fitting to each pixel - how large?
#Compute gdaldem slope and aspect
#Forulate numpy slope vector at each pixel - need to convert aspect into x,y from 0,0
#Extract GPRI ref_coord (wgs84), transform to DEM coord
#Use DEM GT to create xyz ndarray for each pixel in DEM (meshgrid)
#Compute GPRI LOS vector
#Dot the two
#Output resultant x and y velocity component grids

#This provides surface parallel velocities
#Simple relation to get column-average velocity ~0.8*Us
#But need to account for basal sliding, which will be significant for Nisqually
#If we know ice thickness, we have ice flux
#With ice thickness and surface slopes, can also calculate deformation velocity component
from glaclib import *
T = 273
C = 2*A(T)*(rho_i*g)**n/(n+2)
u = C*slope**n*h**(n+1)

#If we know flux on a grid, can compute divergence - derivative of x and y component
#Do we have any idea about SMB?  Need to know accumulation and ablation spatial distribution.
#With all of that, can use continuity to isolate vertical velocity change - dh/dt

#See Konrad et al, (1999), Rignot et al (2002) - talk to Bernard

