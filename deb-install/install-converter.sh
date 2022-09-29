#!/bin/bash

cd ./deb-pip

sudo dpkg -i ca-certificates_20200601~deb10u2_all.deb
sudo dpkg -i python-pip-whl_18.1-5_all.deb
sudo dpkg -i python3-distutils_3.6.5-3_all.deb
sudo dpkg -i python3-pip_18.1-5_all.deb
sudo dpkg -i converter-2.2.deb
