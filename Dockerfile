# Dockerfile

# Etapa 1: Imagem Base
FROM python:3.11-slim

# Etapa 2: Variáveis de Ambiente do Contêiner
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Etapa 3: Instalação de Dependências do Sistema
RUN apt-get update && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Etapa 4: Configuração do Ambiente de Trabalho
WORKDIR /app

# Etapa 5: Build do Frontend (Tailwind CSS)
COPY frontend/package*.json frontend/
RUN cd frontend && npm install
COPY frontend/ frontend/
RUN cd frontend && npm run build

# Etapa 6: Instalação do Backend (Python/Django)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# Etapa 7: Coleta de Arquivos Estáticos do Django
# Fornecemos valores temporários para as variáveis de ambiente
# apenas para que o `collectstatic` possa ser executado durante o build.
RUN SECRET_KEY="dummy" DJANGO_ALLOWED_HOSTS="localhost" DATABASE_URL="sqlite:///dummy.db" python manage.py collectstatic --no-input

# Etapa 8: Exposição da Porta
EXPOSE 8000

# Etapa 9: Comando de Inicialização
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "config.wsgi"]