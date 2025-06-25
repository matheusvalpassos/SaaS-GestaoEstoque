# Usa uma imagem base Python com a versão específica (3.10) para garantir consistência.
# Esta versão é compatível com o Django 5.x.
FROM python:3.10-slim-buster 

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
# CORRIGIDO: O módulo de settings está agora em 'config.settings' (diretamente na raiz do projeto)
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
# CORRIGIDO: O requirements.txt está agora na raiz do WORKDIR ('requirements.txt')
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages --verbose

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
# CORRIGIDO: O manage.py está agora na raiz do WORKDIR ('manage.py')
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
# O Railway injeta $PORT automaticamente.
# CORRIGIDO: O wsgi.py está agora na raiz do WORKDIR ('config.wsgi')
# O Gunicorn e o config.wsgi estão diretamente acessíveis em /app.
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
