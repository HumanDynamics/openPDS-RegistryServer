#! /bin/bash

source ../bin/activate
cd conf
pip install -r requirements.txt
cd ../registryServer
./manage.py syncdb
deactivate
