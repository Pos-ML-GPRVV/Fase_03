# 🚀 Guia de Deploy na AWS

Este guia mostra como fazer o deploy do projeto IPCA em uma instância AWS EC2.

## 📋 Pré-requisitos da Instância AWS

### Instância Recomendada:
- **Tipo**: t3.medium ou superior
- **Sistema Operacional**: Ubuntu 20.04 LTS ou 22.04 LTS
- **Armazenamento**: 20GB mínimo
- **Portas abertas**: 22 (SSH), 80 (HTTP), 443 (HTTPS), 8000 (API)

## 🔧 Configuração da Instância

### 1. Conectar via SSH
```bash
ssh -i sua-chave.pem ubuntu@seu-ip-publico
```

### 2. Atualizar o sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Instalar Docker e Docker Compose
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version
```

### 4. Instalar Git
```bash
sudo apt install git -y
```

## 📦 Deploy do Projeto

### 1. Clonar o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd Fase_03
```

### 2. Configurar variáveis de ambiente
```bash
# Copiar arquivo de configuração
cp neon.env .env

# Editar se necessário (opcional)
nano .env
```

### 3. Executar o projeto
```bash
# Build e start dos containers
docker-compose up --build -d

# Verificar se está rodando
docker-compose ps
```

### 4. Verificar logs
```bash
# Ver logs da aplicação
docker-compose logs -f app

# Ver logs em tempo real
docker-compose logs -f
```

## 🌐 Configuração de Acesso Externo

### 1. Configurar Nginx (Recomendado)
```bash
# Instalar Nginx
sudo apt install nginx -y

# Criar configuração
sudo nano /etc/nginx/sites-available/ipca-api
```

**Conteúdo do arquivo `/etc/nginx/sites-available/ipca-api`:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com ou SEU_IP_PUBLICO;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar o site
sudo ln -s /etc/nginx/sites-available/ipca-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. Configurar Firewall
```bash
# Permitir portas necessárias
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
sudo ufw enable
```

## 🧪 Testar a Aplicação

### 1. Teste local na instância
```bash
# Testar API
curl http://localhost:8000/docs

# Testar endpoint específico
curl -X GET "http://localhost:8000/general-index-ipca" \
  -H "Api-Key: test_api_key_123"
```

### 2. Teste externo
```bash
# Do seu computador local
curl http://SEU_IP_PUBLICO:8000/docs

# Ou se configurou Nginx
curl http://SEU_IP_PUBLICO/docs
```

## 📊 Monitoramento

### 1. Verificar status dos containers
```bash
docker-compose ps
docker-compose logs app
```

### 2. Verificar uso de recursos
```bash
# Uso de CPU e memória
htop

# Uso de disco
df -h

# Logs do sistema
sudo journalctl -f
```

### 3. Reiniciar aplicação se necessário
```bash
# Parar
docker-compose down

# Iniciar
docker-compose up -d

# Rebuild completo
docker-compose down
docker-compose up --build -d
```

## 🔧 Comandos Úteis

### Gerenciamento de Containers
```bash
# Ver containers rodando
docker ps

# Ver todos os containers
docker ps -a

# Parar todos os containers
docker-compose down

# Ver logs em tempo real
docker-compose logs -f app

# Acessar container
docker-compose exec app bash
```

### Backup e Restore
```bash
# Backup do banco (se necessário)
docker-compose exec postgres pg_dump -U neondb_owner neondb > backup.sql

# Restore do banco
docker-compose exec -T postgres psql -U neondb_owner neondb < backup.sql
```

## 🚨 Solução de Problemas

### 1. Container não inicia
```bash
# Ver logs detalhados
docker-compose logs app

# Verificar se as portas estão livres
sudo netstat -tlnp | grep :8000
```

### 2. Erro de conexão com banco
```bash
# Verificar variáveis de ambiente
docker-compose exec app env | grep DB_URL

# Testar conexão
docker-compose exec app python -c "from app.database import engine; print(engine.url)"
```

### 3. Erro de permissão
```bash
# Dar permissões corretas
sudo chown -R ubuntu:ubuntu /home/ubuntu/Fase_03
chmod +x setup.sh
```

## 🔒 Segurança

### 1. Alterar API Key padrão
```bash
# Editar arquivo .env
nano .env

# Alterar a linha:
API_KEY=sua_api_key_super_segura_aqui
```

### 2. Configurar HTTPS (Opcional)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com
```

## 📈 Escalabilidade

### 1. Usar Docker Swarm (Para múltiplas instâncias)
```bash
# Inicializar swarm
docker swarm init

# Deploy com stack
docker stack deploy -c docker-compose.yml ipca-stack
```

### 2. Usar Load Balancer AWS
- Configure um Application Load Balancer
- Adicione sua instância como target
- Configure health checks para a porta 8000

## 📝 Checklist de Deploy

- [ ] Instância AWS configurada
- [ ] Docker e Docker Compose instalados
- [ ] Projeto clonado
- [ ] Arquivo .env configurado
- [ ] Containers rodando (`docker-compose ps`)
- [ ] API respondendo (`curl http://localhost:8000/docs`)
- [ ] Firewall configurado
- [ ] Nginx configurado (opcional)
- [ ] Teste externo funcionando
- [ ] API Key alterada para produção

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs -f`
2. Verifique se as portas estão abertas
3. Confirme se as variáveis de ambiente estão corretas
4. Teste a conectividade com o banco Neon

## 📞 URLs Importantes

- **API Documentation**: http://SEU_IP:8000/docs
- **Neon Console**: https://console.neon.tech
- **Docker Hub**: https://hub.docker.com
