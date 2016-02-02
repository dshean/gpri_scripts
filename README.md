gpri_scripts
============

Scripts for processing and analyzing data from the GAMMA portable radar interferometer

These were used for processing GPRI data collected for the Nisqually and Emmons Glaciers on Mount Rainier in 2012 (see http://www.the-cryosphere.net/9/2219/2015/tc-9-2219-2015.html)

Upon review, the most useful scripts are likely:
-gpri_all.sh - processing workflow from raw SLC images to unwrapped interferograms
-gpri2orgho.py - utility to orthorectify data originally in radar coordinates (az, range) given a single control point and projected DEM

These were written about the time I finally kicked my csh habit - looks like both bash/tcsh scripts are available.

Python scripts depend on numpy, scipy, gdal/osr and libraries in demtools:
https://github.com/dshean/demtools
