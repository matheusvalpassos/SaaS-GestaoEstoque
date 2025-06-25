# backend/config/settings.py

import os
import dj_database_url  # Importar para configurar a base de dados
from decouple import config  # Importar para ler variáveis de ambiente
from pathlib import (
    Path,
)  # Importar Path (melhor prática, embora o.path.join seja usado abaixo para consistência atual)
from django.contrib.messages import (
    constants as messages,
)  # Importar para configurar as tags de mensagem


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR agora aponta para a pasta 'backend' onde está manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# Carregar SECRET_KEY da variável de ambiente (ou .env)
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-sua_chave_secreta_padrão_para_desenvolvimento",
)


# SECURITY WARNING: don't run with debug turned on in production!
# Carregar DEBUG da variável de ambiente (ou .env)
DEBUG = config("DEBUG", cast=bool, default=False)  # Em produção, defina DEBUG=False

# ALLOWED_HOSTS para produção (lidos da variável de ambiente)
# Em produção, ALLOWED_HOSTS=seu-app.onrender.com,127.0.0.1,localhost
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para servir ficheiros estáticos de forma eficiente em produção
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS aponta para a pasta de templates do seu app 'core'
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

WSGI_APPLICATION = "config.wsgi.application"

# Database
# Configuração da Base de Dados para Produção (Supabase) e Desenvolvimento
# Configuração do Banco de Dados (Supabase)
DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I10N = True  # Renomeado de USE_I8N para USE_I10N para Django 5.0+

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Configurações de Arquivos Estáticos
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "staticfiles")  # Pasta na raiz do projeto
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
PROJECT_ROOT = os.path.dirname(BASE_DIR)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),
]
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurações de Autenticação
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "homepage"
LOGIN_URL = "login"

# Configurações de Mensagens
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# Configurações de Mídia (para ficheiros enviados por utilizadores, se aplicável)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Importar o seu User model personalizado se você tiver um (do models.py)
# from django.contrib.auth import get_user_model
# AUTH_USER_MODEL = 'core.CustomUser' # Descomente se CustomUser estiver em core/models.py
