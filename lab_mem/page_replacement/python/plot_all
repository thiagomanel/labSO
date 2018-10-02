#!/bin/bash

#simulation output format
#fault_counter num_pages num_frames alg clock

#plot input format
#nfaults,nframes,alg
#15000,6,opt

# Note that this script expects that we have related file in the output directory. For example, we cannot mix
# output generated from different input files in output directory.

for d in `find output/* -type d`
do
    echo $f
    allsamples="output/`basename $d`.mem.plot"
    echo "nfaults,nframes,alg" > $allsamples
    cat $d/*out | cut -d" " -f1,3,4 | sed 's/ /\,/g' >> $allsamples
    Rscript plot.r $allsamples
done
