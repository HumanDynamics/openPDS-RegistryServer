Human Dynamics openPDS-RegistryServer
======================================

MIT Trustframework deployment instructions are now up at https://github.com/JDSchmitzMedia/trustframework-deploy

    >apt-get install python-pip
    
    >apt-get install python-virtualenv
    
    >apt-get install mongodb mongodb-server
    
    >apt-get install git
    
    >apt-get install build-essential
    
    >apt-get install python-dev
    
    >service mongodb start
    
    >virtualenv pdsrsvirtenv

    >cd pdsrsvirtenv
    
    >git clone git@github.com:HumanDynamics/openPDS-RegistryServer.git

    >source bin/activate
    
    >cd openPDS-RegistryServer/conf
    
    >pip install -r requirements.txt
    
    >cd ../
    
    >cd registryServer
    
    >python manage.py runserver 0.0.0.0:8001 (for access to local VM)
