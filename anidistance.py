import pandas as pd
import sys
import os

tab_file = sys.argv[1]
out_dir = sys.argv[2]            #where the anidistance.csv file will be saved

df = pd.read_csv(tab_file, sep='\t')

# Delete the first column
df = df.drop(df.columns[0], axis=1)


for index, row in df.iterrows():
    for column in df.columns:
        cell_value = row[column]
        row[column] = 1-cell_value

df.to_csv(out_dir+'anidistance_matrix.csv', sep=',', index=False)

