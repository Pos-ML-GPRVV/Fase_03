#!/bin/bash

# Script de Deploy Automatizado para AWS
# Execute este script em uma instância Ubuntu AWS

set -e

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

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para instalar Docker
install_docker() {
    print_message "Instalando Docker..."
    
    if command_exists docker; then
        print_message "Docker já está instalado ✓"
    else
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        print_message "Docker instalado com sucesso ✓"
    fi
}

# Função para instalar Docker Compose
install_docker_compose() {
    print_message "Instalando Docker Compose..."
    
    if command_exists docker-compose; then
        print_message "Docker Compose já está instalado ✓"
    else
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        print_message "Docker Compose instalado com sucesso ✓"
    fi
}

# Função para instalar dependências do sistema
install_system_deps() {
    print_message "Instalando dependências do sistema..."
    
    sudo apt update
    sudo apt install -y git curl wget htop nano
    
    print_message "Dependências instaladas ✓"
}

# Função para configurar firewall
configure_firewall() {
    print_message "Configurando firewall..."
    
    sudo ufw allow 22
    sudo ufw allow 80
    sudo ufw allow 443
    sudo ufw allow 8000
    sudo ufw --force enable
    
    print_message "Firewall configurado ✓"
}

# Função para configurar Nginx
configure_nginx() {
    print_message "Configurando Nginx..."
    
    if command_exists nginx; then
        print_message "Nginx já está instalado ✓"
    else
        sudo apt install -y nginx
    fi
    
    # Criar configuração do Nginx
    sudo tee /etc/nginx/sites-available/ipca-api > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Ativar site
    sudo ln -sf /etc/nginx/sites-available/ipca-api /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo nginx -t
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    
    print_message "Nginx configurado ✓"
}

# Função para clonar e configurar projeto
setup_project() {
    print_message "Configurando projeto..."
    
    # Verificar se já existe
    if [ -d "Fase_03" ]; then
        print_warning "Diretório Fase_03 já existe. Atualizando..."
        cd Fase_03
        git pull
    else
        print_message "Clonando repositório..."
        # Substitua pela URL do seu repositório
        read -p "Digite a URL do seu repositório Git: " REPO_URL
        git clone $REPO_URL
        cd Fase_03
    fi
    
    # Configurar arquivo .env
    if [ ! -f .env ]; then
        cp neon.env .env
        print_message "Arquivo .env criado ✓"
    else
        print_message "Arquivo .env já existe ✓"
    fi
    
    print_message "Projeto configurado ✓"
}

# Função para buildar e executar containers
deploy_application() {
    print_message "Fazendo deploy da aplicação..."
    
    # Build e start
    docker-compose down 2>/dev/null || true
    docker-compose up --build -d
    
    # Aguardar aplicação inicializar
    print_message "Aguardando aplicação inicializar..."
    sleep 30
    
    # Verificar se está rodando
    if docker-compose ps | grep -q "Up"; then
        print_message "Aplicação deployada com sucesso ✓"
    else
        print_error "Erro no deploy da aplicação"
        docker-compose logs app
        exit 1
    fi
}

# Função para testar aplicação
test_application() {
    print_message "Testando aplicação..."
    
    # Teste local
    if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
        print_message "API respondendo localmente ✓"
    else
        print_error "API não está respondendo localmente"
        return 1
    fi
    
    # Teste de endpoint
    if curl -f -H "Api-Key: test_api_key_123" http://localhost:8000/general-index-ipca > /dev/null 2>&1; then
        print_message "Endpoints funcionando ✓"
    else
        print_warning "Endpoints podem ter problemas"
    fi
}

# Função para mostrar informações finais
show_final_info() {
    print_header "DEPLOY CONCLUÍDO"
    
    # Obter IP público
    PUBLIC_IP=$(curl -s http://checkip.amazonaws.com/ || echo "N/A")
    
    echo -e "${GREEN}🎉 Deploy realizado com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}📋 URLs de acesso:${NC}"
    echo "  • API Documentation: http://$PUBLIC_IP:8000/docs"
    echo "  • API via Nginx: http://$PUBLIC_IP/docs"
    echo "  • Endpoint de teste: http://$PUBLIC_IP:8000/general-index-ipca"
    echo ""
    echo -e "${BLUE}🔧 Comandos úteis:${NC}"
    echo "  • Ver logs: docker-compose logs -f"
    echo "  • Parar: docker-compose down"
    echo "  • Reiniciar: docker-compose restart"
    echo "  • Status: docker-compose ps"
    echo ""
    echo -e "${BLUE}🧪 Teste rápido:${NC}"
    echo "  curl -H \"Api-Key: test_api_key_123\" http://$PUBLIC_IP:8000/general-index-ipca"
    echo ""
    echo -e "${YELLOW}⚠️  Lembre-se de alterar a API_KEY no arquivo .env para produção!${NC}"
}

# Função principal
main() {
    print_header "DEPLOY AUTOMATIZADO - PROJETO IPCA"
    
    # Verificar se é root
    if [ "$EUID" -eq 0 ]; then
        print_error "Não execute como root. Use um usuário com sudo."
        exit 1
    fi
    
    # Instalar dependências
    install_system_deps
    install_docker
    install_docker_compose
    configure_firewall
    configure_nginx
    
    # Configurar projeto
    setup_project
    
    # Deploy
    deploy_application
    
    # Testar
    test_application
    
    # Mostrar informações
    show_final_info
}

# Executar função principal
main "$@"
