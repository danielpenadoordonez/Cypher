#!/bin/bash

echo "Uninstalling previous cypher version............."
PYTHON_VERSION=`python3 -c 'import sys; print(sys.version_info[:][1])'`
sudo rm /usr/lib64/python3.$PYTHON_VERSION/Cypher.py
sudo rm /usr/bin/cypher
sleep 1
echo "cypher uninstalled!!"
