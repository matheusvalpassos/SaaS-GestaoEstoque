# C:\Users\MARKETING\Desktop\saas_projeto\backend\config\urls.py

from django.contrib import admin
from django.urls import path, include

# Importar configurações do Django e a função 'static' para servir arquivos estáticos
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # Esta linha de autenticação do Django está OK, pode mantê-la:
    path("accounts/", include("django.contrib.auth.urls")),
    # Esta é a linha necessária para incluir as URLs do seu app 'core':
    path("", include("core.urls")),
]

# **APENAS PARA AMBIENTE DE DESENVOLVIMENTO (DEBUG = True)**
# Esta configuração permite que o Django sirva arquivos estáticos diretamente.
# Em produção, um servidor web (como Nginx ou Apache) deve ser configurado
# para servir os arquivos estáticos diretamente do STATIC_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
