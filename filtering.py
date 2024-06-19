import sys
import os
from Bio import SeqIO
import pandas as pd

fasta_dir = sys.argv[1]          #fasta directory
metadata = sys.argv[2]          #metadata.csv file
threshold = float(sys.argv[3])         #threshold of N's in percentage

def read_sequences(fasta_file):
    sequences = []
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            if find_N(record):
                N_count = record.count('N')
                
                return N_count
    return 0

def sequence_length(fasta):
    sequences = []
    count = 0
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            count += len(record)
    return count
    

def find_N(seq):
    return seq.count('N')

perfect=[]
for filename in os.listdir(fasta_dir):
    if filename.endswith('.fasta') or filename.endswith('.fa'):
        fasta_file = os.path.join(fasta_dir, filename)
        
        count = read_sequences(fasta_file)
        name = os.path.splitext(filename)[0]
        percentage = (count/sequence_length(fasta_file))*100
        if percentage<=threshold:
            perfect.append(filename)

print (perfect)
just_names=[]
for file in perfect:
    just_names.append(file.split(".fasta")[0])          #get the file name just without the extension


for file in os.listdir(fasta_dir):
    if file not in perfect:
        os.remove(os.path.join(fasta_dir, file))
  
print (len(os.listdir(fasta_dir)))

#edit metadata accordingly
df = pd.read_csv(metadata)

df = df[df['Accession ID'].isin(just_names)]            #filtering the metadata
df = df.reset_index(drop=True)
print (df)
df.to_csv(metadata, index=False)