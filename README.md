# gpri_scripts
Scripts for processing and analyzing data from the GAMMA portable radar interferometer

## Command-line utilities
Upon review, the most useful scripts are likely:
- `gpri_all.sh` - processing workflow from raw SLC images to unwrapped interferograms
- `gpri2ortho.py` - utility to orthorectify data in radar coordinates (az, range) to map coordinates (x,y in UTM, for example) given a single control point and an existing DEM

## Notes
These scripts were used for processing GPRI data collected for the Nisqually and Emmons Glaciers on Mount Rainier in 2012 (see http://www.the-cryosphere.net/9/2219/2015/tc-9-2219-2015.html)

Most of this was written about the time I finally kicked my csh habit - looks like both bash/tcsh scripts are available.

## Core requirements
- GAMMA processing software
- [GDAL/OGR](http://www.gdal.org/)
- [NumPy](http://www.numpy.org/)
- [SciPy](https://www.scipy.org/)
- [pygeotools](https://github.com/dshean/pygeotools)
