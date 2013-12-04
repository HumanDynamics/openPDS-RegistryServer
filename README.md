openPDS - Registry Server
======================================

* What is the Registry Server?
 
    The Registry Server is a trustframework registry (includes users, roles etc..) and is also an OAuth 2.0 registry.

* To get started, you'll need python pip and virtualenv installed on your machine (this probably will require root access)

    >apt-get install python-pip
    
    >apt-get install python-virtualenv

    >virtualenv registryEnv
    
    >cd registryEnv
    
    >source bin/activate
    
    >git clone git@github.com:HumanDynamics/openPDS-RegistryServer.git -b master

    >cd openPDS-RegistryServer
    
    >pip install -r conf/requirements.txt

    >cd registryServer
    
    >python manage.py syncdb
    
    >python manage.py runserver 0.0.0.0:8000 (for access to local VM)
    
* The above steps will get you started with a registry server on port 8000 of your machine's loopback interface (for local access only). 
