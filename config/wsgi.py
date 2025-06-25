# backend/config/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django.
# Isso é essencial para que o Django saiba onde encontrar as suas configurações.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Obtém a aplicação WSGI do Django.
# Esta 'application' é o que o Gunicorn irá executar.
application = get_wsgi_application()
