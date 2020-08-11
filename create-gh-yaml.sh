#!/bin/bash

python create-gh-yaml.py
conda build gh
conda convert ~/anaconda3/conda-bld/linux-64/gh*.tar.bz2 -p linux-32 -p osx-64 -o build
anaconda -t $TOKEN upload build/*/*.tar.bz2

