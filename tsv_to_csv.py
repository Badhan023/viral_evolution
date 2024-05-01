import re
import sys

tsv = sys.argv[1]              #name of the tsv file
csv = sys.argv[2]               #name of the csv file

with open(tsv, 'r') as tsv_file:
    with open(csv, 'w') as csv_file:
        for line in tsv_file:
            filecontent = re.sub("\t", ",", line)
            csv_file.write(filecontent)
            
print ("Successfully converted tsv to csv!")