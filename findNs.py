import sys
import os
from Bio import SeqIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fasta_dir = sys.argv[1]
blast_dir = sys.argv[2]
output_dir = sys.argv[3]            #csv with comparison

def read_sequences(fasta_file):
    sequences = []
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            if find_N(record):
                N_count = record.count('N')
                
                return N_count
    return 0

def find_N(seq):
    return seq.count('N')

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
genome_list={}
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
        
        genome_list[name]=get_whole_seq(fasta_file, gene_positions)           #list to just keep the sequences
        name_list.append(name)
        genomes[name] = gene_sequences

original_genome_Ns = {}             #list for the count of N's in the original genomes
coding_region_Ns = {}               #list for the count of N's in the coding regions
perfect=[]


for filename in os.listdir(fasta_dir):
    if filename.endswith('.fasta') or filename.endswith('.fa'):
        fasta_file = os.path.join(fasta_dir, filename)
        
        count = read_sequences(fasta_file)
        name = os.path.splitext(filename)[0]
        original_genome_Ns[name] = count
        percentage = (count/29903)*100
        if percentage<=1:
            perfect.append(filename)

for name, genome in genome_list.items():
    count = find_N(genome)
    coding_region_Ns[name]=count

original_list=[]
coding_list=[]

for name, genome in original_genome_Ns.items():
    coding_list.append(coding_region_Ns[name])
    original_list.append(original_genome_Ns[name])

df = pd.DataFrame(original_genome_Ns.items(), columns=['genome', 'Ns in orginal genomes'])   

df['Ns in the coding region']=coding_list



df.to_csv(output_dir+"comparison_Ns.csv")

bar_width = 0.3
x = np.arange(len(name_list))

plt.bar(x - bar_width/2, original_list, width=bar_width, label='original_genome')

plt.bar(x + bar_width/2, coding_list, width=bar_width, label='coding_region')

plt.xlabel('Genomes')
plt.ylabel('Count of Ns')
plt.title('Count of Ns in the original genomes and the coding regions')
plt.xticks(x, name_list, rotation='vertical')
plt.legend()

plt.show()
plt.savefig(output_dir+'comparison_barchart.png')
