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
import os
from functools import wraps
from fabric.api import run, cd, env
from fabric.context_managers import prefix


def init(instance, workon_home, branch='master'):
    '''
    initialize our environment and path definitions. this is required for any
    method looking to work within an active virtualenv or with the contents of
    the repo in the virtualenv

    update the workon_home parameter if you would like to override where django
    applications are hosted (set by caller)
    '''
    env.WORKON_HOME = workon_home
    env.INSTANCE_NAME = instance
    env.INSTANCE_ROOT = os.path.join(env.WORKON_HOME, env.INSTANCE_NAME)
    env.source_virtualenvwrapper = ('export WORKON_HOME=%(WORKON_HOME)s && source /usr/local/bin/virtualenvwrapper.sh' % env)

    # update this URL if the app's git repo lives somewhere else
    env.REPO_URL = 'https://github.com/IDCubed/OMS-RegistryServer'
    # name of the repo for cloning / cd, changing this requires updates to paths
    # elsewhere in our deployment, so be wary
    env.REPO_NAME = 'OMS-RegistryServer'
    # switch to this branch with a git checkout, customize via the command line
    # to override, if necessary
    env.REPO_BRANCH = branch


def source_virtualenvwrapper(func):
    '''
    decorator. use it to ensure the virtualenvwrapper tools are active/available
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        with prefix(env.source_virtualenvwrapper):
            return func(*args, **kwargs)
    return inner


def workon():
    '''
    context manager. use it for perform actions with virtualenv activated. this
    expects init() to have been run::

        with workon():
            # virtualenv is active here
    '''
    return prefix('source %(INSTANCE_ROOT)s/bin/activate' % env)


def inside_virtualenv(func):
    ''' 
    decorator. use it for perform actions with virtualenv activated. this
    expects init() to have been run::

        @inside_virtualenv
        def my_command():
            # virtualenv is active here
            # fab user is located in: /{WORKON_HOME}/{INSTANCE_NAME}/
    '''
    @wraps(func)
    def inner(*args, **kwargs):
        with workon():
            with cd(env.INSTANCE_ROOT):
                #import pdb; pdb.set_trace()
                run('pwd')
                return func(*args, **kwargs)
    return inner


def install_virtualenv():
    '''
    use pip to install virtualenv and virtualenvwrapper.sh
    '''
    run("sudo pip install --upgrade virtualenv")
    run("sudo pip install --upgrade virtualenvwrapper")


def create_workon_home():
    '''
    '''
    # this should only do this if the directory does not already exist..
    if not os.path.exists(env.WORKON_HOME):
        run('mkdir -m 770 %(WORKON_HOME)s' % env)
    run('%(source_virtualenvwrapper)s' % env)


def prep_server(instance='registryServer', workon_home='/var/www/trustframework'):
    '''
    prepare a new server with dependencies / configs as needed
    use aptitude to install what we can, use pip for uwsgi
    '''
    init(instance, workon_home)
    install_virtualenv()
    create_workon_home()   


@source_virtualenvwrapper
def create_virtualenv():
    '''
    creates initial virtualenv home for the app to be deployed
    '''
    run('mkvirtualenv --no-site-packages %(INSTANCE_NAME)s' % env)


@inside_virtualenv
def clone_repo():
    '''
    clone the django project's git repo to WORKON_HOME/<instance>/
    '''
    if not os.path.exists(os.path.join(env.INSTANCE_ROOT, env.REPO_NAME)):
        run('pwd; git clone %(REPO_URL)s %(REPO_NAME)s' % env)


@inside_virtualenv
def checkout_branch():
    '''
    splunk on into the repo and git checkout <branch>. this expects init() to
    have been run by our caller
    '''
    with cd(env.REPO_NAME):
        run('git checkout ' + env.REPO_BRANCH)


@inside_virtualenv
def install_dependencies():
    '''
    use pip to install dependencies defined in our requirements definition
    '''
    with cd(env.REPO_NAME):
        run('pip install -r conf/requirements.txt')


def reset_permissions():
    '''
    ensure permissions in WORKON_HOME & our apps deployed are www-data:www-data
    and rw for User/Group, and nil for other
    '''
    run('chown -R www-data:www-data %(WORKON_HOME)s' % env)
    run('chmod -R o-rwx %(WORKON_HOME)s' % env)
    run('chmod -R g+rw  %(WORKON_HOME)s' % env)
    

def deploy_project(instance='registryServer',
                   branch='master',
                   workon_home='/var/www/trustframework'):
    '''
    deploy the registry project
    '''
    init(instance, workon_home, branch)

    create_virtualenv()
    clone_repo()
    checkout_branch()
    install_dependencies()
    reset_permissions()
