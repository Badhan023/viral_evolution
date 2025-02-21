from Bio import AlignIO
from Bio import SeqIO
from Levenshtein import distance  # Install using: pip install python-Levenshtein
import numpy as np
import sys

msa_file = sys.argv[1]  # Replace with your MSA file
output_matrix = sys.argv[2]     #matrix csv format

def get_header(fasta_file):
    """
    Extracts the second item from each FASTA header using Biopython.

    Parameters:
        fasta_file (str): Path to the FASTA file.

    Returns:
        list: A list of second items from each header.
    """
    second_items = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        parts = record.id.split("|")  # Split by '|'
        second_items.append(parts[1] if len(parts) > 1 else "N/A")  # Handle missing parts
    return second_items

def compute_pairwise_edit_distances(msa_file, file_format="fasta"):
    """
    Computes the pairwise edit distance (Levenshtein distance) from a multiple sequence alignment.
    
    Parameters:
        msa_file (str): Path to the MSA file.
        file_format (str): Format of the MSA file (e.g., 'fasta', 'clustal', 'phylip').
        
    Returns:
        np.array: Pairwise edit distance matrix.
    """
    # Read the multiple sequence alignment
    alignment = AlignIO.read(msa_file, file_format)
    num_sequences = len(alignment)
    
    # Initialize distance matrix
    distance_matrix = np.zeros((num_sequences, num_sequences))

    # Compute pairwise edit distances
    for i in range(num_sequences):
        for j in range(i+1, num_sequences):
            seq1 = str(alignment[i].seq)
            seq2 = str(alignment[j].seq)
            edit_dist = distance(seq1, seq2)  # Compute Levenshtein distance
            distance_matrix[i, j] = edit_dist
            distance_matrix[j, i] = edit_dist  # Symmetric matrix
    
    return distance_matrix

# Example usage

distance_matrix = compute_pairwise_edit_distances(msa_file)
name_list = get_header(msa_file)
header=""
for name in name_list:
    header += name+","
header = header[:-1]

#print(distance_matrix)
np.savetxt(output_matrix, distance_matrix, delimiter=",", header=header, comments="", fmt="%d")