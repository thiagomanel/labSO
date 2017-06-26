#!/bin/bash
DIRECTORY=output
N=1
tests[0]=1
if [ "$#" -eq 1 ]; then
	N=$1
	tests[1]=$N
	tests[2]=$( expr $N \* 2 )
fi
if [ ! -d "$DIRECTORY" ]; then
	mkdir "$DIRECTORY"
fi
cd $DIRECTORY
for k in ${tests[*]}; do
	if [ ! -d "$k" ]; then
		mkdir "$k"
	fi
done
cd ..
for j in `seq 1 15`; do
	for i in ${tests[*]}; do
		./run_p2.sh $i > "./${DIRECTORY}/${i}/${j}.txt"
	done
done