# 🚀 Comandos Essenciais para Deploy na AWS

## 📋 Comandos Rápidos (Copy & Paste)

### 1. Configuração Inicial da Instância
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar dependências
sudo apt install git curl wget htop nano nginx -y
```

### 2. Deploy do Projeto
```bash
# Clonar repositório (substitua pela sua URL)
git clone https://github.com/SEU_USUARIO/Fase_03.git
cd Fase_03

# Configurar ambiente
cp neon.env .env

# Deploy automático
docker-compose up --build -d
```

### 3. Configurar Nginx (Opcional)
```bash
# Criar configuração
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
sudo nginx -t && sudo systemctl restart nginx
```

### 4. Configurar Firewall
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
sudo ufw --force enable
```

## 🧪 Testes

### Teste Local
```bash
# Verificar se está rodando
docker-compose ps

# Testar API
curl http://localhost:8000/docs

# Testar endpoint
curl -H "Api-Key: test_api_key_123" http://localhost:8000/general-index-ipca
```

### Teste Externo
```bash
# Do seu computador local
curl http://SEU_IP_PUBLICO:8000/docs
```

## 🔧 Comandos de Manutenção

### Gerenciar Aplicação
```bash
# Ver logs
docker-compose logs -f app

# Parar aplicação
docker-compose down

# Reiniciar aplicação
docker-compose restart

# Rebuild completo
docker-compose down
docker-compose up --build -d
```

### Monitoramento
```bash
# Status dos containers
docker-compose ps

# Uso de recursos
htop

# Logs do sistema
sudo journalctl -f
```

## 🚨 Solução de Problemas

### Container não inicia
```bash
# Ver logs detalhados
docker-compose logs app

# Verificar portas
sudo netstat -tlnp | grep :8000
```

### Erro de permissão
```bash
# Corrigir permissões
sudo chown -R ubuntu:ubuntu /home/ubuntu/Fase_03
```

### API não responde
```bash
# Verificar se container está rodando
docker ps

# Verificar logs
docker-compose logs -f

# Testar conectividade
curl -v http://localhost:8000/
```

## 📊 URLs Importantes

- **API Documentation**: `http://SEU_IP:8000/docs`
- **API via Nginx**: `http://SEU_IP/docs`
- **Neon Console**: `https://console.neon.tech`

## ⚡ Deploy Ultra Rápido (1 comando)

Se você quiser fazer tudo de uma vez, execute este comando na instância AWS:

```bash
curl -fsSL https://raw.githubusercontent.com/SEU_USUARIO/Fase_03/main/deploy-aws.sh | bash
```

**Nota**: Substitua `SEU_USUARIO` pela sua conta do GitHub e `SEU_IP` pelo IP público da sua instância AWS.
