# backend/config/wsgi.py
import os
import sys  # NOVO: Importar sys para manipulação de caminho

from django.core.wsgi import get_wsgi_application

# Adicionar o diretório raiz do projeto Django (pasta 'backend') ao sys.path
# '/opt/render/project/src' é o caminho absoluto onde o Render copia o seu rootDir (backend)
# Isso garante que Python pode encontrar 'config' e 'core'
sys.path.insert(0, "/opt/render/project/src")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
