#!/bin/bash

python create-gh-yaml.py
conda build gh --output-folder build
conda convert build/linux-64/gh*.tar.bz2 -p linux-32 -p osx-64 -o build
anaconda -t $TOKEN upload --skip build/*/*.tar.bz2

