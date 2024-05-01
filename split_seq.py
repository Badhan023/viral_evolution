import os
import sys

def split(filename):
    file = open(filename, 'r')
    f = open("initial.fasta", "w")
    while True:
        line = file.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        if line[0]=='>':
            print ("begining of a sequence")
            print (line)
            words = line.split('|')
            index= words[1]
            f = open(dirname+index+".fasta", "w")
            f.write(line)
    
        else:
            f.write(line)
  
    file.close()
    os.remove('initial.fasta')
    
print (sys.argv[1])
filename = sys.argv[1]

dirname = 'Iran/fasta/'
 
# giving file extension
ext = ('.fasta')

split(filename)

    
