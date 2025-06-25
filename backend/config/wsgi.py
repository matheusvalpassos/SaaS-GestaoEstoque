# backend/config/wsgi.py
import os

# import sys # REMOVER: Não precisamos mais de importar sys aqui para o sys.path.insert

from django.core.wsgi import get_wsgi_application

# REMOVER: Esta linha deve ser removida
# sys.path.insert(0, '/opt/render/project/src')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
