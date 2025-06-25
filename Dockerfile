# Usa uma imagem base Python com a versão específica (3.10) para garantir consistência.
# Esta versão é compatível com o Django 5.x.
FROM python:3.10-slim-buster 

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings 

# Definir o diretório de trabalho inicial dentro do contentor para /app
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git para o contentor
COPY . /app

# NOVO: Instalar dependências de sistema para compilação de pacotes Python
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# NOVO: Atualizar pip e setuptools para as versões mais recentes
RUN pip install --no-cache-dir --upgrade pip setuptools

# Instala as dependências do Python a partir do ficheiro requirements.txt
# A flag --break-system-packages é mais comum para Python 3.10+
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages --verbose

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
