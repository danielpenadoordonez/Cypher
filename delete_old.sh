#!/bin/bash

PYTHON_VERSION=`python3 -c 'import sys; print(sys.version_info[:][1])'`
sudo rm /usr/lib/python3.$PYTHON_VERSION/Cypher.py
sudo rm /usr/bin/Cypher
