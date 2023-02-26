#!/bin/bash

conda install -y -c conda-forge mamba
mamba env create -f environment.yml
echo "conda activate dactyl-keyboard" >> ~/.bashrc
