# backend/config/wsgi.py
import os

# REMOVER: A importação de sys já não é necessária se a linha sys.path.insert foi removida
# import sys

from django.core.wsgi import get_wsgi_application

# REMOVER: Esta linha deve ser removida
# sys.path.insert(0, '/opt/render/project/src')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
