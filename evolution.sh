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

##blasts
blast_script="blast.sh"
chmod +x "$blast_script"
./blast.sh $gene_dir $dir$fastadir $dir$blastdir

##editdistance
python3 identity_from_blast.py "$dir"/


##sourmash
python3 global.py "$dir"/ "$dir"/distance_matrix.csv "$dir$outputdir"/sourmash/ ani

##pyani
python3 global.py "$dir"/ "$dir"/anidistance_matrix.csv "$dir$outputdir"/pyani/ ani

##editdistance
python3 global.py "$dir"/ "$dir"/editdistance_matrix.csv "$dir$outputdir"/editdistance/ editdistance

##create matrix for disease transmission network
python3 transmission.py "$dir$outputdir"/sourmash/
python3 transmission.py "$dir$outputdir"/pyani/
python3 transmission.py "$dir$outputdir"/editdistance/