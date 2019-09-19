#/bin/bash

# This script uses a minimal workload. It's only purpose is for debbuging and better understanding of your code

npages=7
clock=2


alg=random # This is where you select the algorithm you want to test
    
for nframes in 2 3 4 5 6 7
do
    python memory_simulation.py $npages $nframes $alg $clock < load/minimal > output/minimal.$alg.$nframes.out
done
