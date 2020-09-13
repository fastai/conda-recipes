#!/bin/bash

#python create-j-yaml.py
#conda build j --output-folder build
conda convert build/linux-64/j*.tar.bz2 -p osx-64 -o build
anaconda -t $TOKEN upload --skip build/*/*.tar.bz2

