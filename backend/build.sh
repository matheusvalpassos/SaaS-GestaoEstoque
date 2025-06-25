#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos
python manage.py collectstatic --no-input

# 3. Roda as migrações do banco de dados
python manage.py migrate