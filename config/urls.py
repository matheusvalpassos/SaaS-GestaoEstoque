# backend/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # Inclui todas as URLs do seu aplicativo 'core'.
    # O seu app 'core' é a raiz da sua aplicação para o usuário.
    path("", include("core.urls")),
]

# APENAS PARA AMBIENTE DE DESENVOLVIMENTO (DEBUG = True)
# Estas configurações permitem que o Django sirva ficheiros estáticos e de mídia
# diretamente do servidor de desenvolvimento.
# Em produção, um servidor web (como Nginx/Render/Railway) é responsável
# por servir estes ficheiros diretamente do STATIC_ROOT/MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
