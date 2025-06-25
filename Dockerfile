# Usa uma imagem base Python com a versão específica para garantir consistência.
FROM python:3.9-slim-buster

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings # AGORA: config.settings (pois config está na raiz do WORKDIR)

# Definir o diretório de trabalho dentro do contentor para /app
# Este será o diretório onde o seu repositório Git será clonado.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git para o contentor
COPY . /app

# NOVO: Instalar dependências de sistema para compilação de pacotes Python
# 'build-essential' (para gcc, etc.) e 'libpq-dev' (para psycopg2)
# Limpeza de cache do apt para reduzir o tamanho da imagem
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar as dependências do Python a partir do ficheiro requirements.txt
# AGORA: requirements.txt está diretamente em /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
# AGORA: manage.py está diretamente em /app/manage.py
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
# O Railway injeta $PORT automaticamente.
# AGORA: wsgi.py está diretamente em /app/config/wsgi.py, então a referência é 'config.wsgi'
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
