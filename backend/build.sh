#!/usr/bin/env bash
# Exit on error
set -o errexit

# --- ETAPA 1: BUILD DO FRONTEND ---
echo "Compilando o Tailwind CSS..."
# Navega até a pasta do frontend
cd ../frontend 
# Instala as dependências do Node.js (Tailwind)
npm install
# NOVO: Força a recompilação de pacotes
npm rebuild
# Roda o script de build para gerar o arquivo output.css
npm run build
# Volta para a pasta do backend para continuar
cd ../backend

# --- ETAPA 2: BUILD DO BACKEND ---
echo "Instalando dependências do Python..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
# O Django coleta TODOS os arquivos estáticos, incluindo o output.css
python manage.py collectstatic --no-input

echo "Aplicando migrações do banco de dados..."
python manage.py migrate
echo "Iniciando o servidor de desenvolvimento..."