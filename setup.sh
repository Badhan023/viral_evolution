conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge

##installing pyani
conda install --yes pyani

##installing sourmash
conda install -c conda-forge sourmash-minimal

##installing blast
conda install blast

#install modules
conda install anaconda::pandas
conda install -c conda-forge biopython
conda install editdistance
conda install numpy
pip install networkx
pip install matplotlib
conda install -c bioconda mafft
conda install -c bioconda raxml
pip install python-Levenshtein
