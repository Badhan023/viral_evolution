#!/bin/bash

echo $1

dir="$1"        #main directory
threshold="$2"         #threshold for filtering
gene_dir="ref_genes"      

metadata="/metadata.csv"
outputdir="_output"
fastadir="/fasta"
blastdir="/blasts"
sourmash="/sourmash"
pyani="/pyani"
editdistance="/editdistance"

mkdir "$dir$outputdir"
mkdir "$dir$outputdir$sourmash"
mkdir "$dir$outputdir$pyani"
mkdir "$dir$outputdir$editdistance"

python3 filtering.py "$dir$fastadir" "$dir$metadata" "$threshold"          #threshold zero

##sourmash
sourmash_script="sourmash.sh"
chmod +x "$sourmash_script"
./sourmash.sh $dir

##pyani
pyani_script="pyani.sh"
chmod +x "$pyani_script"
./pyani.sh $dir

##mafft
mafft "$dir"/all_seq.fasta > "$dir"/aligned.fasta

##truncate
python3 truncate.py "$dir"/aligned.fasta "$dir"/truncated.fasta

##editdistance
python3 editdistance.py "$dir"/truncated.fasta "$dir"/edit.csv


##sourmash
python3 global.py "$dir"/ "$dir"/distance_matrix.csv "$dir$outputdir"/sourmash/ ani

##pyani
python3 global.py "$dir"/ "$dir"/anidistance_matrix.csv "$dir$outputdir"/pyani/ ani

##editdistance
python3 global.py "$dir"/ "$dir"/edit.csv "$dir$outputdir"/editdistance/ editdistance
