<h3>Cloning the repository and creating a conda environment</h3>

```
conda create --name evolution --yes python=3.8
conda activate evolution
```

<h3>Installing necessary tools and modules</h3>

Run the following command, or install the tools and modules in the setup.sh file separately in the conda environment.
```
bash setup.sh
```

<h3>Preparing the input</h3>

The input directory, **\<country\>** has to be inside the **viral_evolution** directory. **\<country\>** directory should contain a **fasta** directory holding all the fasta files of the data set, and a metadata file, **metadata.csv**, which has the following columns.
1. Accession ID
2. Collection date (in the 'mm/dd/yyyy' format)
3. Location
4. Lineage

Bhutan data set is given as a sample to see how the input directory needs to be.

<h3>Running the code</h3>

Type the following command to run the code.

```
bash evolution.sh <country> <threshold>
```
Here, **\<threshold\>** is a value between **0 and 1 (inclusive)**, which determines what percentage of N's are allowed to be in the genome sequences. Those genomes that have higher percentage of N's than the \<threshold\> are filtered out from both the fasta directory and the metadata file.

<h3>An example</h3>

The Bhutan data set is provided as a sample data set to run. The following command will run the code on the Bhutan data set.

```
bash evolution.sh Bhutan 0
```

Here, we use 0 as threshold to filter out all the genomes that have N's.

<h3>Output</h3>

This code will create the following three distance matrices in the \<country\> directory.
1. distance_matrix.csv (from sourmash)
2. anidistance_matrix.csv (from pyani)
3. editdistance_matrix.csv (from edit distance)
   
An output directory, **\<country\>_output**, will be created in the viral_evolution directory. This directory will contain the following folders.
1. sourmash
2. pyani
3. editdistance

Each of these folders will contain the following files.
1. adj_matrix.csv (the adjacency matrix of the output graph)
2. evolution.csv (the evolution history)
3. graph.png (the output graph)
4. lineage.txt (grouping the variants according to their PANGO lineages)
5. network.csv (the adjacency matrix of the disease transmission network)
