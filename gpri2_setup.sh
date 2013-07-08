#! /bin/bash

#Want to source this script so env propagate

#Mount volume
#set mntdir = /Volumes/dshean_bb/MtRainier_GPRI
mntdir=~/mnt/dshean/sw
topdir=$mntdir/gpri2_root

if [[ -z "$LD_LIBRARY_PATH" ]]; then
  #export LD_LIBRARY_PATH
  #export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:/usr/local/lib
  echo "LD not defined"
fi

#export PATH=${PATH}:$topdir/bin:$topdir/usr/bin
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$topdir/lib:$topdir/usr/lib
#export PATH=$topdir/bin:$topdir/usr/bin:${PATH}
#export LD_LIBRARY_PATH=$topdir/lib:$topdir/usr/lib:${LD_LIBRARY_PATH}
#export PATH=$topdir/usr/bin:${PATH}
#export LD_LIBRARY_PATH=$topdir/usr/lib:${LD_LIBRARY_PATH}
export PATH=${PATH}:$topdir/usr/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$topdir/usr/lib
