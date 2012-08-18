'''
This is the Open Mustard Seed Registry Server deployment script, build on the 
fabric python library. "Fabric is a Python library and command-line tool for
streamlining the use of SSH for application deployment or systems administration
tasks.

It provides a basic suite of operations for executing local or remote shell
commands (normally or via sudo) and uploading/downloading files, as well as
auxiliary functionality such as prompting the running user for input, or
aborting execution." - from http://docs.fabfile.org/en/1.4.3/index.html


Overview
========

Install RegistryServer
----------------------

* source virtualenvwrapper.sh and leverage its management capabilities. this
  helps us keep all virtualenvs in one space, but complicates fabric slightly
* create new virtualenv for the app to deploy. all virtualenvs are created in 
  the WORKON_HOME directory
* clone git repo in the virtualenv. requires cd to the new virtualenv
* run pip install on the requirements.txt dependency definitions. this requires
  the virtualenv be active
* copy files around, enable services, start the application and ensure it stays
  up with process monitoring - this is not happening at present.


Other Fun Stuff
---------------

...is in the works


Important Notes
===============

* you'll need ssh access through a user on any server / system you deploy to
* the user you use must be in the www-data group
* $WORKON_HOME is meaningful, the user you use should have an export for this
  in the appropriate profile/shell rc. eg, if using bash put the following in
  $HOME/.bashrc or what have you: export WORKON_HOME="/var/python"
  while this location could be customized, the change would need to be applied
  elsewhere in our deployment process

'''
from oms_fabric.webapp import Webapp

RegistryServer = Webapp()
RegistryServer.repo_url = 'https://github.com/IDCubed/OMS-RegistryServer'
RegistryServer.repo_name = 'OMS-RegistryServer'

def deploy_project(instance='registryserver',
                   branch='master'):
    '''
    direct pull from fabfile.py in resource server, not tested and needs more
    work, just exemplifying the idea.
    '''
    RegistryServer.branch = branch
    RegistryServer.deploy_project(instance, branch)
