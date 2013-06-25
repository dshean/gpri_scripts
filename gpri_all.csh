#! /bin/tcsh -f

#David Shean
#dshean@gmail.com
#12/19/12

#Basic workflow to process GPRI data

#Want to set up checks for existing data to avoid unnecessary reprocessing and overwriting
#Many of these steps can be run through gnu parallel or xargs

#Needed to set up local environment for GAMMA software install
source /Volumes/dshean_bb/MtRainier_GPRI/gpri2_usr/gpri2_setup.csh

set slcdir = slc_dir

#Create table of slc
mk_tab $slcdir slc slc.par slc_tab

#Number of range and azimuth looks to "average" in the mli
set rlks = 15 
set azlks = 1
set mlidir = mli_dir_${rlks}

#Note mk_mli_all_mt is multi-threaded
#Create mli
mk_mli_all slc_tab $mlidir $rlks $azlks 0 0.7 0.35

set step = 4
set stride = 1
set start = 1

#Create interferogram table
mk_itab itab `cat slc_tab | wc -l` $step $stride $start 

#Generate interferograms
mk_int_2d slc_tab itab `ls $mlidir/*l.mli | head -1` $mlidir diff_${rlks} $rlks $azlks 3 0 0 1 -s 0.7 -e 0.35

#Filter w/ adaptive bandpass filter
mk_adf_2d slc_tab itab `ls $mlidir/*l.mli | head -1` diff_${rlks} 5 0.4 32 4 -s 0.7 -e 0.35

#Set thresholds for correlation score and relative intensity
#set c_thr = 0.2
#set i_thr = 0.35
set c_thr = 0.7
set i_thr = 0

#Set reference coordinates for unwrapping
#These were picked for Lower Nisqually, using data from the June roi survey, rlks 15
set r_ref = 153 
set a_ref = 459

#Unwrap interferograms
mk_unw_2d slc_tab itab `ls $mlidir/*l.mli | head -1` diff_${rlks} $c_thr $i_thr 1 1 1 1 $r_ref $a_ref 1 -d diff_tab_${rlks} -s 0.7 -e 0.35 -p 1.0

#Check for availability of convert first
#Convert ras to png and rotate
foreach i (mli_${rlks}/*ras diff_${rlks}/*ras)
	convert -rotate -90 $i ${i:r}.png
	rm $i
end

