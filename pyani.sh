#!/bin/bash

echo $1         #input directory


cd $1
mkdir pyani
cd ..
average_nucleotide_identity.py --force --method ANIb --indir $1/fasta/ --outdir $1/pyani/ --workers 4
python3 anidistance.py $1/pyani/ANIb_percentage_identity.tab $1/
echo "ANI distance matrix created!"