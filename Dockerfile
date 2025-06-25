# Usa uma imagem base Python com a versão específica para garantir consistência.
FROM python:3.9-slim-buster

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE backend.config.settings

# Define o diretório de trabalho inicial dentro do contentor.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git (o contexto atual) para /app no contentor.
COPY . /app

# Muda o diretório de trabalho para a pasta 'backend'.
WORKDIR /app/backend

# Instalar dependências de sistema para compilação de pacotes Python
# 'build-essential' (para gcc, etc.) e 'libpq-dev' (para psycopg2)
# Limpeza de cache do apt para reduzir o tamanho da imagem
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# NOVO: Garante que o ficheiro requirements.txt está no formato UNIX (LF)
# E tente instalar as dependências Python listadas.
# Também adiciona --break-system-packages para Python 3.10+ (embora estejamos em 3.9)
# Isso é uma precaução para algumas instalações em sistemas baseados em Debian
RUN sed -i 's/\r$//' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt --break-system-packages

# Executa o comando 'collectstatic' do Django para reunir todos os ficheiros estáticos.
RUN python manage.py collectstatic --noinput

# Define o comando que será executado quando o contentor iniciar.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
