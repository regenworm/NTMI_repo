#!/bin/bash

for h in -1 0 1 2 3 4 5
do
	for v in -1 1 2 3 4 5
	do
		python b-step2.py -h $h -v $v -input data/train20.txt -output "temp/train20.txt.h"$h"v"$v
		echo "h:$h, v:$v"
		java -ea -Xmx1G -cp bin/ nlp.assignments.parsing.SimpleParser -train "temp/train20.txt.h"$h"v"$v -test data/validation20.txt | tail -n1
	done
done
