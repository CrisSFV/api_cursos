# Configuración de Gunicorn para Flask
# Ubicación: /opt/flask_app/gunicorn_config.py

import multiprocessing
import os

# Configuración de workers
workers = multiprocessing.cpu_count() * 2 + 1  # Fórmula recomendada
worker_class = 'sync'  # Tipo de worker
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 60  # Timeout en segundos
keepalive = 5

# Binding
bind = '0.0.0.0:8000'
backlog = 2048

# Logging
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Proceso
daemon = False
pidfile = '/var/run/gunicorn.pid'
umask = 0
user = 'ec2-user'
group = 'ec2-user'
tmp_upload_dir = None

# SSL (opcional)
# keyfile = '/etc/nginx/ssl/nginx-selfsigned.key'
# certfile = '/etc/nginx/ssl/nginx-selfsigned.crt'

# Server Mechanics
preload_app = True  # Mejorar rendimiento cargando la app una sola vez
forwarded_allow_ips = '*'  # Para proxies

# Hooks
def on_starting(server):
    print("Gunicorn server is starting...")

def when_ready(server):
    print("Gunicorn server is ready. Spawning workers")

def on_exit(server):
    print("Gunicorn server is exiting")
