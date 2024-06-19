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
