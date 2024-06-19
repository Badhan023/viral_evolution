##creating a new conda environment
conda create --name evolution --yes python=3.7
conda activate evolution

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
conda install matplotlib
