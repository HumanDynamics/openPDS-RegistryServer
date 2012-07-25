Registry Server INSTALL
=======================

NOTES
-----

*this is a work in progress and will see updates and improvement - please feel free to submit your feedback to make this a better experience for you*

*some level of console experience and comfort is expected, though we have done our best to take out the pain in deploying this application :)*

in the future, this web app will be remotely deployable - eg, developers and system admins will have the tools to deploy this application to a remote server, from a local copy of the git repo. for now the installation scripts only support being run locally.


requirements / expectations
---------------------------

* upload a copy of the git repository to the server
* a user with access to root priviledges via sudo 
* a ubuntu 12.04 LTS server
* openssh, apache, mongodb, and mysql setup and running


steps to install the registry server
------------------------------------

* from the git repo, run ``./bootstrap.sh`` with no arguments. you may need to run ``chmod +x bootstrap.sh`` first, to flag the script as executable. this script will install dependencies and setup the environment for deployment, then call a special python script that will install more dependencies and actually deploy the django project
* edit the django project settings.py file to include your database connection info (the database, user, password, and server host). XXX - this doc ought to be updated to include a reference to the section we are expecting the user to update

