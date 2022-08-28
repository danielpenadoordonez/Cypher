#!/bin/bash

PYTHON_VERSION=`python3 -c 'import sys; print(sys.version_info[:][1])'`

sudo cp Cypher.py /usr/lib/python3.$PYTHON_VERSION/
sudo mv cypher /usr/bin/
