#!/bin/bash

# Script para executar o ambiente Docker completo do IPCA
# Inclui API FastAPI e Dashboard Streamlit

echo "🚀 Iniciando ambiente Docker do IPCA..."
echo "📊 API FastAPI: http://localhost:8000"
echo "📈 Dashboard Streamlit: http://localhost:8501"
echo ""

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copiando env.example para .env..."
    cp env.example .env
    echo "⚠️  Por favor, edite o arquivo .env com suas configurações antes de continuar."
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar os serviços
echo "🔨 Construindo e iniciando serviços..."
docker-compose up --build -d

# Aguardar os serviços ficarem prontos
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Verificar status dos serviços
echo "📋 Status dos serviços:"
docker-compose ps

echo ""
echo "✅ Ambiente Docker iniciado com sucesso!"
echo ""
echo "🔗 Acesse:"
echo "   • API FastAPI: http://localhost:8000"
echo "   • Documentação da API: http://localhost:8000/docs"
echo "   • Dashboard Streamlit: http://localhost:8501"
echo ""
echo "📝 Para parar os serviços: docker-compose down"
echo "📊 Para ver logs: docker-compose logs -f"
