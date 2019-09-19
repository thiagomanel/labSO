#/bin/bash

# This script exercises the real workload
npages=1500000
clock=200

for trace in trace.1 trace.2
do
    for alg in fifo lru nru aging second-chance
    do
        for nframes in 4 8 16 32
        do
	    mkdir output/$trace
	    python memory_simulation.py $npages $nframes $alg $clock < load/$trace.in > output/$trace/$trace.$alg.$nframes.out
	done
    done
done
