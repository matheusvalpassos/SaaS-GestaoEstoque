# backend/config/settings.py

import os
import dj_database_url
from decouple import config
from django.contrib.messages import constants as messages

# Define o BASE_DIR como o caminho absoluto para a pasta 'backend'.
# Isso é importante para que todos os outros caminhos (templates, static, media) sejam relativos a ela.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Configurações de segurança e depuração.
# A SECRET_KEY deve ser lida de uma variável de ambiente por segurança.
SECRET_KEY = config(
    "SECRET_KEY", default="sua-chave-secreta-padrao-para-desenvolvimento-local"
)

# DEBUG deve ser False em produção. Ele é lido de uma variável de ambiente.
DEBUG = config("DEBUG", cast=bool, default=False)

# ALLOWED_HOSTS define quais domínios podem servir a sua aplicação.
# No Railway, será o domínio que eles atribuírem. Use split(',') para lidar com múltiplos hosts.
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")


# Definição das aplicações Django.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # O seu app principal
    "widget_tweaks",  # Se estiver a usar esta biblioteca
]

# Middlewares (camadas de processamento de requisições).
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para servir ficheiros estáticos de forma eficiente em produção.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Configurações de URL e WSGI.
ROOT_URLCONF = "config.urls"  # O módulo principal de URLs.

# Configurações de Templates.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS: Onde o Django vai procurar por templates fora dos diretórios de apps.
        # Aponta para a pasta 'templates' dentro do seu app 'core'.
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,  # Permite que o Django procure templates dentro das pastas 'templates' de cada app.
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = (
    "config.wsgi.application"  # O módulo WSGI que o Gunicorn vai executar.
)

# Configuração da Base de Dados.
# Usa dj_database_url para ler a cadeia de conexão da variável de ambiente DATABASE_URL.
# default: Se DATABASE_URL não estiver definida (ex: em desenvolvimento local), usa SQLite.
# conn_max_age: Reutiliza conexões de base de dados, bom para performance.
DATABASES = {
    "default": dj_database_url.config(
        default=config(
            "DATABASE_URL", default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
        ),
        conn_max_age=600,  # 10 minutos
    )
}

# Validação de Password.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Configurações de Internacionalização e Fuso Horário.
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I10N = True  # Renomeado de USE_I8N para USE_I10N para Django 5.0+
USE_TZ = True

# Configurações de Ficheiros Estáticos (CSS, JS, Imagens para o navegador).
STATIC_URL = "/static/"

# STATIC_ROOT: Onde 'collectstatic' vai reunir TODOS os ficheiros estáticos para deploy.
# Ele aponta para uma pasta 'staticfiles' na raiz do projeto principal (saas_projeto).
# Isso é importante porque o Dockerfile copia a pasta 'backend' para /app/backend.
# Então, a raiz do seu projeto Git é /app, e os estáticos precisam estar em /app/staticfiles.
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Vai para a pasta 'saas_projeto'
STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")

# STATICFILES_DIRS: Onde o Django vai PROCURAR por ficheiros estáticos em desenvolvimento,
# além dos diretórios 'static' dentro de cada app.
# Aponta para a sua pasta 'static_dev' dentro de 'backend'.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),
]

# Habilita o armazenamento compactado de ficheiros estáticos pelo WhiteNoise em produção (quando DEBUG é False).
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configurações de Chave Primária Padrão.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurações de Autenticação.
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "homepage"
LOGIN_URL = "login"

# Configurações de Mensagens Django.
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# Configurações de Mídia (para ficheiros enviados por utilizadores).
# Em produção, você precisará de um serviço de armazenamento de objetos (ex: Supabase Storage, AWS S3).
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
