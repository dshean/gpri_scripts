#Want to source this script so env propagate

#Mount volume
set mntdir = /Volumes/dshean_bb

set topdir = $mntdir/MtRainier_GPRI/gpri2_usr

if (! $?LD_LIBRARY_PATH) setenv LD_LIBRARY_PATH

setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:$topdir/lib
setenv PATH ${PATH}:$topdir/bin
