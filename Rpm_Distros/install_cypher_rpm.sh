#!/bin/bash

#Check that Python3 is installed
which python3 > /dev/null

if [ $?	-ne 0 ] ; then
	echo "Python3 is required for cypher to run, and it is not installed!!"
	read "Install Python3 (y/n)? " ANSWER
        
	if [ $ANSWER == "Y" ] -o [ $ANSWER == "y" ] ; then
		sudo apt update
		sudo apt install python3
	else
		exit
	fi
fi

#Check if cypher is already installed
which cypher > /dev/null

if [ $? -eq 0 ] ; then
	#echo "Uninstalling previous version of cypher....................."
	sudo ./delete_old.sh
	sleep 2
fi

#Get the current Python Version and make the installation
PYTHON_VERSION=`python3 -c 'import sys; print(sys.version_info[:][1])'`
echo "...............Installing cypher..............."
sleep 2
sudo cp ../Cypher.py /usr/lib64/python3.$PYTHON_VERSION/
sudo mv cypher /usr/bin/
echo "cypher has been installed!!"
sleep 1
