# backend/config/settings.py

import os
import dj_database_url
from decouple import config
from django.contrib.messages import constants as messages

# AGORA: BASE_DIR aponta para a raiz do seu repositório Git (saas_projeto)
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Altera para a pasta atual (config)
BASE_DIR = os.path.dirname(BASE_DIR)  # Sobe um nível para 'backend'
BASE_DIR = os.path.dirname(
    BASE_DIR
)  # Sobe mais um nível para 'saas_projeto' (raiz do repositório)

# Ou, de forma mais simples e robusta se 'settings.py' está em saas_projeto/config/
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent.parent # saas_projeto/

# No seu caso, mantendo a consistência do seu código atual, e sabendo que settings.py está em backend/config:
# BASE_DIR será a raiz do projeto (saas_projeto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # config
BASE_DIR = os.path.dirname(BASE_DIR)  # backend
BASE_DIR = os.path.dirname(BASE_DIR)  # saas_projeto

# Em vez do acima, se o `settings.py` estiver em `saas_projeto/config/`:
# BASE_DIR = Path(__file__).resolve().parent.parent

# Se você moveu 'config' para a raiz 'saas_projeto', então 'settings.py' está em 'saas_projeto/config'
# E o BASE_DIR deve ser 'saas_projeto'
# Então, o correto seria:
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent # Isso aponta para a raiz do projeto (saas_projeto)


# Vamos usar a versão mais segura, presumindo que settings.py está agora em saas_projeto/config/
from pathlib import Path

BASE_DIR = (
    Path(__file__).resolve().parent.parent
)  # Aponta para saas_projeto/ (a nova raiz)


# Quick-start development settings - unsuitable for production
SECRET_KEY = config(
    "SECRET_KEY", default="sua_chave_secreta_padrão_para_desenvolvimento"
)
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",  # Seu app 'core' agora estaria diretamente em saas_projeto/core
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Agora, ROOT_URLCONF e WSGI_APPLICATION são diretamente referenciados a partir da raiz do projeto
ROOT_URLCONF = "config.urls"  # Será saas_projeto/config/urls.py
WSGI_APPLICATION = "config.wsgi.application"  # Será saas_projeto/config/wsgi.py

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS agora aponta para 'saas_projeto/core/templates'
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
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

# Database
DATABASES = {
    "default": dj_database_url.config(
        default=config(
            "DATABASE_URL", default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
        ),
        conn_max_age=600,
    )
}

# Password validation (restante inalterado)
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

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Será saas_projeto/staticfiles
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),  # Se você tiver uma pasta static_dev na raiz
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "homepage"
LOGIN_URL = "login"

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
