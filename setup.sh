#!/bin/bash

# Script de configuração e inicialização do projeto IPCA
# Este script automatiza o processo de setup do ambiente

set -e

echo "🚀 Iniciando configuração do projeto IPCA..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    print_message "Docker e Docker Compose encontrados ✓"
}

# Criar arquivo .env se não existir
create_env_file() {
    if [ ! -f .env ]; then
        print_message "Criando arquivo .env a partir do neon.env (Neon PostgreSQL)..."
        cp neon.env .env
        print_message "Arquivo .env criado com credenciais do Neon PostgreSQL ✓"
        print_warning "IMPORTANTE: Para produção, altere a API_KEY no arquivo .env!"
    else
        print_message "Arquivo .env já existe ✓"
    fi
}

# Criar diretório de logs
create_logs_dir() {
    if [ ! -d logs ]; then
        print_message "Criando diretório de logs..."
        mkdir -p logs
    fi
    print_message "Diretório de logs ✓"
}

# Construir e iniciar containers
start_containers() {
    print_header "INICIANDO CONTAINERS"
    
    print_message "Construindo imagem da aplicação..."
    docker-compose build
    
    print_message "Iniciando containers..."
    docker-compose up -d
    
    print_message "Aguardando serviços ficarem prontos..."
    sleep 10
}

# Verificar status dos serviços
check_services() {
    print_header "VERIFICANDO SERVIÇOS"
    
    # Verificar aplicação (Neon PostgreSQL é externo)
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        print_message "Aplicação está rodando ✓"
    else
        print_warning "Aplicação ainda não está respondendo. Aguarde alguns segundos..."
        sleep 5
        if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
            print_message "Aplicação está rodando ✓"
        else
            print_error "Aplicação não está respondendo. Verifique os logs: docker-compose logs app"
            return 1
        fi
    fi
}

# Mostrar informações úteis
show_info() {
    print_header "INFORMAÇÕES IMPORTANTES"
    
    echo -e "${GREEN}🎉 Setup concluído com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}📋 URLs importantes:${NC}"
    echo "  • API Documentation: http://localhost:8000/docs"
    echo "  • Neon Console: https://console.neon.tech"
    echo ""
    echo -e "${BLUE}🔑 Credenciais do Neon PostgreSQL:${NC}"
    echo "  • Host: ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech"
    echo "  • Database: neondb"
    echo "  • User: neondb_owner"
    echo "  • Password: npg_5m3pUxFNWStB"
    echo "  • SSL: Requerido"
    echo ""
    echo -e "${BLUE}📝 Comandos úteis:${NC}"
    echo "  • Ver logs: docker-compose logs -f"
    echo "  • Parar serviços: docker-compose down"
    echo "  • Reiniciar: docker-compose restart"
    echo "  • Acessar container: docker-compose exec app bash"
    echo ""
    echo -e "${YELLOW}⚠️  Lembre-se de alterar a API_KEY no arquivo .env para produção!${NC}"
}

# Função principal
main() {
    print_header "CONFIGURAÇÃO DO PROJETO IPCA"
    
    check_docker
    create_env_file
    create_logs_dir
    start_containers
    check_services
    show_info
}

# Executar função principal
main "$@"
