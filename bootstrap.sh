#!/bin/sh

# this must be set for the webapp deployment to complete correctly
# update the /var/python path to something else you desire, if you wish to
# customize this setting.
export WORKON_HOME=/var/www/trustframework

# gcc and the python header files are needed for dependencies with components we
# must compile, like pycrypto and psycopg2
sudo aptitude install gcc python-dev

# by using setuptools/easy_install, we can obtain the most recent stable release
# of pip
sudo aptitude install python-setuptools
sudo easy_install pip

# now use pip to install fabric
sudo pip install fabric

# use fabric to continue the install
# first, by preparing the server 
sudo fab -H localhost prep_server

# and then to deploy the project
sudo fab -H localhost deploy_project

# XXX - don't actually trust this, I have to confirm the $1 bits in sh scripting
# if you wish to have this script deploy multiple projects, use the following
# command instead of the one above, 
# fab -H localhost deploy_project:$1

# XXX - uncomment once we've switched off apache/wsgi for nginx/uwsgi
#fab -H localhost start_webapp
