#!/usr/bin/env bash
# Exit on error
set -o errexit

# --- ETAPA 1: BUILD DO FRONTEND ---
echo "Compilando o Tailwind CSS..."
cd ../frontend 
npm install
npm rebuild
npm run build
cd ../backend

# --- ETAPA 2: BUILD DO BACKEND ---
echo "Instalando dependências do Python..."
pip install -r requirements.txt

# Define o arquivo de settings para produção ANTES de rodar qualquer comando manage.py
# 'config' é o nome da pasta que contém seu settings.py
export DJANGO_SETTINGS_MODULE=config.settings

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Aplicando migrações do banco de dados..."
python manage.py migrate
echo "Iniciando o servidor de desenvolvimento..."
python manage.py runserver
