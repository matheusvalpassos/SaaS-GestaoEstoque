# backend/config/settings.py
import os
import dj_database_url
from pathlib import Path
from decouple import config, Csv

# Use pathlib, que é mais moderno e seguro para caminhos de arquivo.
# BASE_DIR agora aponta para a pasta 'backend'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega as variáveis de ambiente usando decouple.
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv()
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Whitenoise deve vir logo após messages
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Suas Apps
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
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],  # Sintaxe mais limpa com pathlib
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

# Configuração do Banco de Dados usando decouple para fornecer a URL
DATABASES = {
    "default": dj_database_url.config(
        # Busca a DATABASE_URL da variável de ambiente
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
# Pasta para onde o collectstatic irá copiar os arquivos para produção
STATIC_ROOT = BASE_DIR.parent / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Autenticação
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "homepage"
LOGIN_URL = "login"
