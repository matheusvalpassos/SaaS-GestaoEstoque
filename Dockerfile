# Usa uma imagem base Python com a versão específica (3.13) para garantir compatibilidade.
# Esta versão é compatível com Django 5.x e audioop-lts.
# CORRIGIDO: Usando a tag '3.13-slim' que é mais comum e existente.
FROM python:3.13-slim 

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings 

# Definir o diretório de trabalho inicial dentro do contentor para /app
# /app será o local onde o seu repositório Git será clonado.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git (o contexto atual) para /app no contentor.
# Assumimos que manage.py, config/, core/, requirements.txt estão agora na raiz do repositório.
COPY . /app

# Instalar dependências de sistema para compilação de pacotes Python
# 'build-essential' (para gcc, etc.) e 'libpq-dev' (para psycopg2)
# Limpeza de cache do apt para reduzir o tamanho da imagem
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip e setuptools para as versões mais recentes
RUN pip install --no-cache-dir --upgrade pip setuptools

# Instala as dependências do Python a partir do ficheiro requirements.txt
# A flag --break-system-packages é mais comum para Python 3.10+
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages --verbose

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
# O Railway injeta $PORT automaticamente.
# NOVO: Define PYTHONPATH para incluir o diretório de site-packages e a raiz do projeto.
# Isso garante que o Python pode encontrar tanto o 'gunicorn' quanto o 'config.wsgi'.
CMD ["sh", "-c", "export PYTHONPATH=/usr/local/lib/python3.13/site-packages:/app:$PYTHONPATH && /usr/local/bin/python -m gunicorn --bind 0.0.0.0:$PORT config.wsgi:application"]
