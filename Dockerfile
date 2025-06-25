# Usa uma imagem base Python com a versão específica (3.13) para garantir compatibilidade.
FROM python:3.13-slim-buster 

# Definir variáveis de ambiente essenciais para o Python e o Django.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings 

# Define o diretório de trabalho inicial dentro do contentor para /app
# Este será o diretório onde o seu repositório Git será clonado.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git (o contexto atual) para /app no contentor.
# Isso garante que todas as suas pastas e ficheiros de topo estão em /app.
COPY . /app

# Mover para a pasta onde o 'manage.py' e 'requirements.txt' estão.
# Se a sua estrutura agora tem 'manage.py' e 'requirements.txt' diretamente na raiz
# do repositório (e eles foram copiados para /app), então este passo NÃO é necessário.
# Mas se eles ainda estiverem dentro de uma pasta como 'backend' (após a cópia),
# então precisamos de mudar o WORKDIR para essa pasta.
# Dado o historial de problemas, vamos ASSUMIR que manage.py e requirements.txt estão na raiz de /app.

# Instalar dependências de sistema para compilação de pacotes Python
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip e setuptools para as versões mais recentes
RUN pip install --no-cache-dir --upgrade pip setuptools

# Instala as dependências do Python a partir do ficheiro requirements.txt
# Agora, o 'requirements.txt' deve estar diretamente em '/app/requirements.txt'
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages --verbose

# Executar o comando collectstatic do Django para reunir todos os ficheiros estáticos.
# O 'manage.py' deve estar diretamente em '/app/manage.py'
RUN python manage.py collectstatic --noinput

# Definir o comando que será executado quando o contentor iniciar.
# Usamos 'sh -c' para executar um comando shell complexo que garante o PYTHONPATH e
# chama o Gunicorn de forma robusta.
# A referência 'config.wsgi' é direta porque a pasta 'config' estará em /app/config.
CMD ["sh", "-c", "python -m gunicorn --bind 0.0.0.0:$PORT config.wsgi:application"]
