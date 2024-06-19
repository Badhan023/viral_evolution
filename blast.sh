#!/bin/bash

echo $1
echo $2
echo $3

#give directory without the /
query_dir="$1"          #queries are the reference genes
subject_dir="$2"        #subjects are the genomes, so fasta directory
output_dir="$3"

mkdir "$output_dir"

for subject_file in "$subject_dir"/*.fasta; do
    if [ -f "$subject_file" ]; then
        subject_filename=$(basename -- "$subject_file")     #extracting the basename of the subject file
        subject_filename_no_ext="${subject_filename%.*}"
        echo "baalsaal"
        for query_file in "$query_dir"/*.fasta; do
            if [ -f "$query_file" ]; then
                blastn -query "$query_file" -subject "$subject_file" -outfmt "10 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore" >> "$output_dir"/"${subject_filename_no_ext}.csv"
                echo "BLAST search completed for $query_file"
            fi
        done
    fi
done
