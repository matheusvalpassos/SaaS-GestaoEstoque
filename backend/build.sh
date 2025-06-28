#!/usr/bin/env bash
# Exit on error
set -o errexit

# --- ETAPA 1: BUILD DO FRONTEND ---
echo "Compilando o Tailwind CSS..."
cd ../frontend 
npm install
npm run build
cd ../backend

# --- ETAPA 2: BUILD DO BACKEND ---
echo "Instalando dependências do Python..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Aplicando migrações do banco de dados..."
python manage.py migrate