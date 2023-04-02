#!/usr/bin/bash
#	python 3
sudo apt update && sudo apt upgrade -y || echo "Error Updating"
sudo apt install python3 || echo "Error Installing Python3"
#	pip
sudo apt install python3-pip || echo "Error Installing Pip"
#	Google API
pip3 install google-auth-oauthlib || echo "Error installing google-auth-oauthlib"
pip3 install google-api-python-client || echo "Error Installing google-api-python-client"
pip3 install google-auth || echo "Error installing google-auth"
#	LCD
pip3 install adafruit-charlcd || echo "Error Installing adafruit-charlcd"
#	Fingerprint
pip3 install adafruit-circuitpython-fingerprint || echo "Error Installing adafruit-circuitpython-fingerprint"
#	Keypad
pip3 install adafruit-circuitpython-matrixkeypad || echo "Error Installing adafruit-circuitpython-matrixkeypad"
echo "Installion Complete"