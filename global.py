#import editdistance
import sys
import os
from Bio import SeqIO
import pandas as pd
import csv
#from Bio import pairwise2
from graph import *
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt

#genomefile1 = sys.argv[1]
#genomefile2 = sys.argv[2]
inputdir = sys.argv[1]          #the main directory
metadata = inputdir+"metadata.csv"              #the metadata of the genomes to insert
genome_dir = inputdir+"/fasta/"            #the directory with all the genomes to insert

distance_matrix_file = sys.argv[2]       #the distance matrix
output_dir = sys.argv[3]            #the output directory
mode = sys.argv[4]                  #ani or editdistance

if mode != "ani" and mode != "editdistance":
    print (mode)
    print ("Wrong mode")
    sys.exit(1)


def read_sequences(fasta_file):
    sequences = []
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            sequences.append(record)
    return sequences

def get_strains(metadata):
    df = pd.read_csv(metadata, sep=',')
    strains = df.iloc[:,0].tolist()
    return strains

def get_dates(metadata):
    df = pd.read_csv(metadata, sep=',')
    dates = df.iloc[:,1].tolist()
    return dates

def get_lineages(metadata):
    df = pd.read_csv(metadata, sep=',')
    lineages = df.iloc[:,3].tolist()
    return lineages

#this function is to align target seq to query seq and extract the query 
def extraction(target, query):
    alignments = pairwise2.align.localms(target, query, 2, -1, -1, -0.1)
    alignment = alignments[0]
    aligned_target = alignment[0]
    aligned_query = alignment[1]
    
    extract = ""
    i=0
    j=len(aligned_target)-1
    while (i<=j):
        if aligned_target[i]!='-':
            extract+=aligned_query[i]
        i=i+1
        if aligned_target[j]=='-':
            j=j-1
    return extract
    
#lists of strains, dates and lineages
strains = get_strains(metadata)
sorted_dates = get_dates(metadata)
lineages = get_lineages(metadata)

#to save all the genomes to be added
def get_all_seq(strains):
    all_seq = {}
    for strain in strains:
        filename = genome_dir+strain+".fasta"
        seq = read_sequences(filename)
        seq_str = str(seq[0].seq)
        all_seq[strain] = seq_str
    return all_seq

#dictionary to keep all the sequences in a dictionary for high efficiency
all_genomes = get_all_seq(strains)    

def group_dates(dates, strains):
    groups = {}
    for pos, date in enumerate(dates):
        if date not in groups:
            groups[date] = [strains[pos]]
        else:
            groups[date].append(strains[pos])
    
    return groups

def group_lineages(lineages, strains, output_file):
    groups = {}
    for pos, lineage in enumerate(lineages):
        if lineage not in groups:
            groups[lineage] = [strains[pos]]
        else:
            groups[lineage].append(strains[pos])
    
        
    with open(output_file, 'w') as file:
        for key, value in groups.items():
            line = key+':'+str(value)
            file.write(line)
            file.write("\n")
    return groups


def xor(bool1, bool2):
    if (bool1 == True and bool2 == False) or (bool1 == False and bool2 == True):
        return True
    return False

def days_between(d1, d2):
    
    #%m/%d/%Y
    '''
    t1 = datetime.strptime(d1, "%m/%d/%Y")
    t2 = datetime.strptime(d2, "%m/%d/%Y")
    '''
    #%Y-%m/%d
    
    t1 = datetime.strptime(d1, "%Y-%m-%d")
    t2 = datetime.strptime(d2, "%Y-%m-%d")
    
    return abs((t2-t1).days)
        

#rename the header of the distance_matrix.csv file
with open(distance_matrix_file, 'r', newline='') as infile:
    reader = csv.reader(infile)
    remaining_lines = list(reader)[1:]      #exclude the first line
    
with open(distance_matrix_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(strains)
    writer.writerows(remaining_lines)
    
with open(distance_matrix_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows=[]
    for row in reader:
        rows.append(row)

distance_matrix = rows[1:]


groups = group_dates(sorted_dates, strains)            #fixed groups dictionary
database = {}           #final dictionary of genomes; key:value == genome name:parent
accepted = []           #list of taken genomes from the pending list
lineage_file = output_dir+"lineage.txt"
lineage_groups = group_lineages(lineages, strains, lineage_file)

#the matrix is a dict of dicts
matrix = {}
i=0
for strain in strains:
    temp={}
    for j in range(0,i):
        temp[strains[j]]=float(distance_matrix[i][j])
    matrix[strain]=temp
    i+=1


for date, group in groups.items():
    main_item = group[0]
    i=1
    while i<len(group):
        j=i-1
        while j>=0:
            del matrix[group[i]][group[j]]
            j-=1
        i+=1

parent_dict = {}

reversed_strain_list = strains[::-1]
queue = []
queue.append(reversed_strain_list[0])

#print (matrix)
#for each strains, find the smallest distance from the distance_matrix
while reversed_strain_list:
    strain = reversed_strain_list.pop(0)
    
    if matrix[strain]:
        #print (matrix[strain].values())
        min_distance = min(matrix[strain].values())
        #print (min_distance)
        parents = [key for key, value in matrix[strain].items() if value==min_distance]
        parent_dict[strain]=parents
        
    else:
        parent_dict[strain]=["root"]


#this is the distance list for all the parents from the node of interest
distance_list = []

for key, value in parent_dict.items():
    distance=[]
    
    for item in value:
        if mode == "ani":
            if item != 'root':
                distance.append(float(matrix[key][item]))
                
            else:
                distance.append(0)
        else:
            if item != 'root':
                distance.append(int(matrix[key][item]))
                
            else:
                distance.append(0)
    distance_list.append(distance)

#print (distance_list)
#date distance list for all the parents from the node of interest   
date_list = []
for key, value in parent_dict.items():
    date=[]
    for d, group in groups.items():
        if key in group:
            key_date=d
            break
            
    for item in value:
        if item!= 'root':
            for d, group in groups.items():
                if item in group:
                    item_date=d
                    break    
            diff = days_between(item_date, key_date)
            date.append(diff)
                
        else:
            date.append(0)
    date_list.append(date)

df = pd.DataFrame(parent_dict.items(), columns=['variant', 'parent'])


df['date_difference']=date_list

if mode == "ani":
    df['1-ANI']=distance_list
else:
    df['edit distance']=distance_list

df.to_csv(output_dir+"evolution.csv")
nodes = df['variant'].tolist()

weight = dict(zip(nodes, distance_list))
distance = dict(zip(nodes, date_list))
      


#Graph
g = Graph()
g.add_dict(nodes, parent_dict, distance)
g.get_adj_matrix(output_dir+"adj_matrix.csv")
g.draw_graph(output_dir+"graph.png", lineage_groups)
