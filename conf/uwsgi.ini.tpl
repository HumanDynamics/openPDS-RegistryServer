# none of this is documented in our deployment docs, but we really ought to..
[uwsgi]
socket = 127.0.0.1:{{ uwsgi_port }}
threads = 40
master = 1
env = DJANGO_SETTINGS_MODULE=settings.{{ app_env }}
module = django.core.handlers.wsgi:WSGIHandler()
chdir = {{ instance_root }}/{{ repo_name }}/registryServer
