# Usa uma imagem base Python com a versão específica para garantir consistência.
# A versão 3.9 é uma boa escolha para estabilidade.
FROM python:3.9-slim-buster

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
# CORRIGIDO: O módulo de settings está agora na raiz do WORKDIR ('config.settings')
ENV DJANGO_SETTINGS_MODULE config.settings

# Definir o diretório de trabalho inicial dentro do contentor.
# /app será o local onde o seu repositório Git será clonado.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git (o contexto atual) para /app no contentor.
# Assumimos que o manage.py, config/, core/, requirements.txt estão agora na raiz do repositório.
COPY . /app

# NOVO: Instalar dependências de sistema para compilação de pacotes Python
# 'build-essential' (para gcc, etc.) e 'libpq-dev' (para psycopg2)
# Limpeza de cache do apt para reduzir o tamanho da imagem
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python a partir do ficheiro requirements.txt
# CORRIGIDO: O requirements.txt está agora na raiz do WORKDIR ('requirements.txt')
# NOVO: Adicionado --verbose para mais detalhes no log
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages --verbose

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
# CORRIGIDO: O manage.py está agora na raiz do WORKDIR ('manage.py')
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
# O Railway injeta $PORT automaticamente.
# CORRIGIDO: O wsgi.py está agora na raiz do WORKDIR ('config.wsgi')
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
