import pandas as pd
import sys
import os
from Bio import SeqIO
import editdistance
import numpy as np

fasta_dir = sys.argv[1]
blast_dir = sys.argv[2]
distance_matrix_file = sys.argv[3]        

#function to extract the subsequences with start and end position
def extract_seq(file, start, end):
    sequences = []
    with open(file, 'r') as handle:
        for record in SeqIO.parse(handle, "fasta"):
            sequences.append(record)
    seq_str = str(sequences[0].seq)
    seq = seq_str[start-1: end]
    return seq

def get_whole_seq(file, genes):
    seq=""
    for gene, positions in genes.items():
        for position in positions:
            extracted_gene = extract_seq(file, position[0], position[1])
            seq += extracted_gene
    return seq

def get_gene_seq(file, positions):
    seq=""
    for position in positions:
        extracted_gene = extract_seq(file, position[0], position[1])
        seq += extracted_gene
    return seq

  
    
genomes={}                      #dictionary of dictionaries (genes per genome)
genome_count=0
genome_list=[]
name_list=[]
gene_list=["gene_1", "gene_2", "gene_3", "gene_4", "gene_5", "gene_6", "gene_7", "gene_8", "gene_9", "gene_10", "gene_11"]
#loop through the blast directory to access the csv files
for filename in os.listdir(blast_dir):
    if filename.endswith('.csv'):
        genome_count+=1
        file_path = os.path.join(blast_dir, filename)
        
        name = os.path.splitext(filename)[0]
        
        
        gene_positions={                             #genes are dictionary of lists of tuples; these tuples are of start and end positions
            "gene_1":[],
            "gene_2":[],
            "gene_3":[],
            "gene_4":[],
            "gene_5":[],
            "gene_6":[],
            "gene_7":[],
            "gene_8":[],
            "gene_9":[],
            "gene_10":[],
            "gene_11":[]
        }
        gene_sequences={                             #dictionary to keep the gene sequences
            "gene_1":"",
            "gene_2":"",
            "gene_3":"",
            "gene_4":"",
            "gene_5":"",
            "gene_6":"",
            "gene_7":"",
            "gene_8":"",
            "gene_9":"",
            "gene_10":"",
            "gene_11":""
        }
        df = pd.read_csv(file_path, header=None)
        for index, row in df.iterrows():
            fullgene=row[0]
            parts = fullgene.split('_')
            
            gene = parts[-2]+'_'+parts[-1]
            
            pident=row[2]
            sstart=row[8]
            send=row[9]
            position_tuple=(sstart, send)
            gene_positions[gene].append(position_tuple)
        
        #fasta file of the genome
        fasta_file = fasta_dir+name+".fasta"
        
        #sort the positions in ascending order
        for gene, positions in gene_positions.items():
            sorted_positions = sorted(positions, key=lambda x:x[0])             #sorting the positions in ascending order
            gene_positions[gene] = sorted_positions                            #reassigning the sorted positions
            gene_sequences[gene] = get_gene_seq(fasta_file, gene_positions[gene])           #to get the gene sequence
        
        genome_list.append(get_whole_seq(fasta_file, gene_positions))           #list to just keep the sequences
        name_list.append(name)
        genomes[name] = gene_sequences
        
    
#creating the distance matrix using numpy array

distance_matrix = np.zeros((genome_count, genome_count))


#saving half time by computing upper half triangle of the matrix
i=0
j=0
for i in range(0, genome_count):
    for j in range(i+1, genome_count):
        distance_from_genes = 0
        for gene in gene_list:
            distance_from_genes += editdistance.eval(genomes[name_list[i]][gene], genomes[name_list[j]][gene])
        print (distance_from_genes)
        distance_matrix[i,j] = distance_from_genes
        distance_matrix[j,i] = distance_from_genes
        

header=""
for name in name_list:
    header += name+","

header = header[:-1]
print (header)

np.savetxt(distance_matrix_file, distance_matrix, delimiter=",", header=header, comments="", fmt="%d")



