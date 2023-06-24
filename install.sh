#!/usr/bin/bash

set -e

if [ "$(id -u)" != "0" ]; then
echo "Current User : $USER"
echo "Please Run the Script as root user or with SUDO Priviledges" 1>&2
exit 1
fi

sudo apt update || (echo "Error Updating" && exit 1)
sudo apt-get install python3 || (echo "Error Install Python3" && exit 1)
sudo apt install python3-pip || (echo "Error Install pip" && exit 1)

#	Google API
python3 -m pip3 install google-auth-oauthlib || (echo "Error installing google-auth-oauthlib" && exit 1)
python3 -m pip3 install google-api-python-client || (echo "Error Installing google-api-python-client" && exit 1)
python3 -m pip3 install google-auth || (echo "Error installing google-auth" && exit 1)

#	LCD
pip3 install adafruit-charlcd || (echo "Error Installing adafruit-charlcd" && exit 1)

#	Fingerprint
pip3 install adafruit-circuitpython-fingerprint || (echo "Error Installing adafruit-circuitpython-fingerprint" && exit 1)

#	Keypad
pip3 install adafruit-circuitpython-matrixkeypad || (echo "Error Installing adafruit-circuitpython-matrixkeypad" && exit 1)

echo "Dependency Install/Setup Successfull" && exit 0