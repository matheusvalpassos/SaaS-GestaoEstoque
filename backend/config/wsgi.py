# backend/config/wsgi.py
import os
import sys  # NOVO: Importar sys

from django.core.wsgi import get_wsgi_application

# NOVO: Adicionar o diretório raiz do projeto Django (pasta 'backend') ao sys.path
# Isso é crucial para que o Python encontre os módulos do seu projeto como 'config' ou 'core'.
# '/opt/render/project/src' é o caminho absoluto onde o Render copia o seu rootDir (backend)
sys.path.insert(0, "/opt/render/project/src")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
