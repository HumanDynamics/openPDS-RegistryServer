import os
import sys
sys.path.append('/var/www/trustframework/resourceServer');
sys.path.append('/home/jeff/org.python.pydev.debug_2.4.0.2012020116/pysrc');

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

