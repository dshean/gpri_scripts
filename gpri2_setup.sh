#! /bin/bash

#Want to source this script so env propagate

#Mount volume
#set mntdir = /Volumes/dshean_bb/MtRainier_GPRI
mntdir=~/mnt/dshean/sw
topdir=$mntdir/gpri2_usr

if [[ -z "$LD_LIBRARY_PATH" ]]; then
  #export LD_LIBRARY_PATH
  export LD_LIBRARY_PATH=/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:/usr/local/lib
fi

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$topdir/lib
export PATH=${PATH}:$topdir/bin
