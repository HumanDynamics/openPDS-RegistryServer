Project Mustard Seed - Registry Server
======================================

We need some good docs in here detailing:

* what is the Registry Server
 
    The Registry Server is a trustframework registry (includes users, roles etc..) and is also an OAuth 2.0 registry.

* how do you get started / installing in virtual environment and running locally

    >apt-get install python pip
    
    >apt-get install python-virtualenv

    >virtualenv registryvirtenv
    
    >cd registryvirtenv
    
    >source bin/activate
    
    >git clone git@github.com:IDCubed/OMS-RegistryServer.git -b master

    >cd OMS-RegistryServer
    
    >pip install -r conf/requirements.txt

    >cd registryServer
    
    >python manage.py runserver 0.0.0.0:8000 (for access to local VM)
    
* links to important pages / wiki / etc
