#!/bin/bash

echo $1     ##main directory

for fasta_file in $(find "$1" -type f -name "*.fasta"); do
    echo "Processing file: $1"    
done

mkdir $1/sig
echo "signature directory created"
cd $1/sig
sourmash sketch dna -p scaled=2,k=21 ../../$1/fasta/*.fasta
sourmash compare --distance-matrix --ksize 21 --ani --containment --csv ../distance_matrix.csv *.sig
cd ..