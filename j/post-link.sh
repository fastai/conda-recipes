#!/bin/bash

cd $PREFIX/share
rm -rf $PREFIX/share/j901
unzip -qo j.zip -d j901 
rm j.zip
ln -s $PREFIX/share/j901/bin/jconsole $PREFIX/bin/

