#!/bin/bash

CONDA_PREFIX="${CONDA_PREFIX:-/opt/conda}"
python create-gh-yaml.py
conda build gh
conda convert $CONDA_PREFIX/conda-bld/linux-64/gh*.tar.bz2 -p linux-32 -p osx-64 -o build
anaconda -t $TOKEN upload --skip $CONDA_PREFIX/conda-bld/linux-64/gh*.tar.bz2
anaconda -t $TOKEN upload --skip build/*/*.tar.bz2

