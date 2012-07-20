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

* source virtualenvwrapper.sh and leverage its management capabilities
* create new virtualenv for the app to deploy
* clone git repo in the virtualenv
* run pip install on the requirements.txt dependency definitions
* copy files around, enable services, start the application and ensure it stays
  up with process monitoring.


Other Fun Stuff
---------------

...is in the works


Important Notes
===============

* you'll need ssh access through a user on any server / system you deploy to
* $WORKON_HOME is meaningful, the user you use should have an export for this
  in the appropriate profile/shell rc. eg, if using bash put the following in
  $HOME/.bashrc or what have you: export WORKON_HOME="/var/python"
  while this location could be customized, the change would need to be applied
  elsewhere in our deployment process

'''
import os
from functools import wraps
from fabric.api import local, run, cd, env
from fabric.context_managers import prefix


def init(instance='registryServer', workon_home='/var/python'):
    '''
    initialize our environment and path definitions. this is required for any
    method looking to work within an active virtualenv or with the contents of
    the repo in the virtualenv

    update the workon_home parameter if you would like to override where django
    applications are hosted
    '''
    env.WORKON_HOME = workon_home
    env.INSTANCE_NAME = instance
    env.INSTANCE_ROOT = os.path.join(env.WORKON_HOME, env.INSTANCE_NAME)
    env.source_virtualenvwrapper = 'source /usr/local/bin/virtualenvwrapper.sh'

    # update this URL if the app's git repo lives somewhere else
    env.REPO_URL = 'https://github.com/IDCubed/OMS-RegistryServer'


def source_virtualenvwrapper(func):
    '''
    decorator. use it to ensure the virtualenvwrapper tools are active/available
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        with prefix(env.source_virtualenvwrapper):
            return func(*args, **kwargs)
    return inner


def install_virtualenv():
    '''
    use pip to install virtualenv and virtualenvwrapper.sh
    '''
    local("sudo pip install --upgrade virtualenv")
    local("sudo pip install --upgrade virtualenvwrapper")


def prep_server():
    '''
    prepare a new server with dependencies / configs as needed
    use aptitude to install what we can, use pip for uwsgi
    '''
    install_virtualenv()
    local('sudo mkdir /var/python')


@source_virtualenvwrapper
def create_virtualenv():
    '''
    creates initial virtualenv home for the app to be deployed
    '''
    run('mkvirtualenv --no-site-packages %(INSTANCE_NAME)s' % env)


def clone_repo():
    '''
    clone the django project's git repo to WORKON_HOME/<instance>/
    '''
    with cd(env.INSTANCE_ROOT):
        local('git clone %(REPO_URL)s' % env)


def install_dependencies():
    '''
    use pip to install dependencies defined in our requirements definition
    '''
    init()
    with cd(env.INSTANCE_ROOT):
        local('pip install -r conf/requirements.txt')


def deploy_project(instance, workon_home):
    '''
    deploy the registry project
    '''
    init()

    create_virtualenv()
    clone_repo()
    install_dependencies()


