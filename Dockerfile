# Usa uma imagem base Python com a versão específica para garantir consistência.
# A versão 3.9 é uma boa escolha para estabilidade.
FROM python:3.9-slim-buster

# Define variáveis de ambiente essenciais para o Python e o Django.
# PYTHONUNBUFFERED: Garante que os logs do Python são exibidos em tempo real.
# DJANGO_SETTINGS_MODULE: Informa ao Django onde encontrar o ficheiro de configurações.
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE backend.config.settings

# Define o diretório de trabalho inicial dentro do contentor.
# /app será o local onde o seu repositório Git será clonado.
WORKDIR /app

# Copia todo o conteúdo do seu repositório Git (o contexto atual) para /app no contentor.
# Isso inclui as pastas 'backend', 'frontend', etc.
COPY . /app

# Muda o diretório de trabalho para a pasta 'backend'.
# Isso é crucial para que os comandos seguintes (pip install, manage.py)
# sejam executados no contexto correto onde 'manage.py' e 'requirements.txt' residem.
WORKDIR /app/backend

# Instala as dependências Python listadas no 'requirements.txt'.
# --no-cache-dir: Evita o cache de pacotes, reduzindo o tamanho final da imagem.
RUN pip install --no-cache-dir -r requirements.txt

# Executa o comando 'collectstatic' do Django para reunir todos os ficheiros estáticos.
# --noinput: Evita perguntas interativas durante a coleta de estáticos.
RUN python manage.py collectstatic --noinput

# Define o comando que será executado quando o contentor iniciar.
# 'gunicorn': O servidor WSGI para aplicações Django.
# '--bind 0.0.0.0:$PORT': Diz ao Gunicorn para ouvir em todas as interfaces
#                           na porta que o Railway injeta como variável de ambiente ($PORT).
# 'config.wsgi:application': O caminho para o seu ficheiro WSGI a partir da pasta 'backend' (WORKDIR).
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
