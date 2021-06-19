# msr4ml
Reconstructing Artifact traceability in Machine Learning Repositories

## Purpose
This repository contains the code and data for the paper MSR4ML: Reconstructing Artifact Traceability in Machine Learning Repositories.
Its main objective is to retrieve missing links between ML artifacts, mainly dataset and the corresponding code where it is imported.

## How to reproduce
Right now, only the artefact identifier is functional. The remaining modules will be added later.

1) Prepare the python environnement and install the dependencies using pip: pip install -r requirements.txt
2) Download the ML project you want to analyse and run the identifier module: python identifier.run -p \[dir_path of the project\]
3) The results will be in a json file \[dir_path of the project\]-links.json
