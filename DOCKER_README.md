# 🐳 Executando o Projeto com Docker

Este guia mostra como executar o sistema completo de previsão de IPCA usando Docker, incluindo a API FastAPI e o Dashboard Streamlit.

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Arquivo `.env` configurado

## 🚀 Execução Rápida

### Opção 1: Script Automatizado (Recomendado)

```bash
./start-docker.sh
```

### Opção 2: Comandos Manuais

```bash
# 1. Parar containers existentes
docker-compose down

# 2. Construir e iniciar serviços
docker-compose up --build -d

# 3. Verificar status
docker-compose ps
```

## 🔧 Configuração

### Arquivo .env

Certifique-se de que o arquivo `.env` está configurado com:

```env
# Banco de Dados Neon
DB_URL=postgresql://neondb_owner:npg_5m3pUxFNWStB@ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech:5432/neondb?sslmode=require

# API Key
API_KEY=senha123

# URLs para comunicação entre containers
API_URL=http://app:8000
API_URL_EXTERNAL=http://localhost:8000
```

## 🌐 Acessos

Após a inicialização, você pode acessar:

- **API FastAPI**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs
- **Dashboard Streamlit**: http://localhost:8501

## 📊 Serviços

### 1. API FastAPI (app)
- **Porta**: 8000
- **Container**: ipca_app
- **Função**: API REST para previsões de IPCA
- **Health Check**: http://localhost:8000/health

### 2. Dashboard Streamlit (dashboard)
- **Porta**: 8501
- **Container**: ipca_dashboard
- **Função**: Interface web para visualização e análise
- **Dependência**: Aguarda a API estar saudável

## 🔍 Comandos Úteis

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f app
docker-compose logs -f dashboard

# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reconstruir apenas um serviço
docker-compose up --build -d app
docker-compose up --build -d dashboard

# Entrar no container da API
docker-compose exec app bash

# Entrar no container do dashboard
docker-compose exec dashboard bash
```

## 🐛 Troubleshooting

### Problema: Dashboard não consegue conectar com a API

**Solução**: Verifique se a API está saudável:
```bash
docker-compose ps
curl http://localhost:8000/health
```

### Problema: Erro de SSL na coleta de dados

**Solução**: A API está configurada para pular a coleta automática de dados na inicialização. Use o endpoint `/training-model` para treinar o modelo quando necessário.

### Problema: Porta já em uso

**Solução**: Pare outros serviços que possam estar usando as portas 8000 ou 8501:
```bash
# Encontrar processos usando as portas
lsof -i :8000
lsof -i :8501

# Parar processos específicos
kill -9 <PID>
```

## 📈 Monitoramento

### Health Checks

Ambos os serviços possuem health checks configurados:

- **API**: Verifica endpoint `/health`
- **Dashboard**: Verifica se o Streamlit está respondendo

### Logs

Os logs são salvos no diretório `./logs` e também podem ser visualizados via Docker:

```bash
# Logs em tempo real
docker-compose logs -f

# Logs históricos
docker-compose logs --tail=100
```

## 🔄 Atualizações

Para aplicar mudanças no código:

```bash
# Reconstruir e reiniciar
docker-compose down
docker-compose up --build -d
```

## 🛡️ Segurança

- Containers executam com usuário não-root
- Variáveis sensíveis são passadas via environment
- Rede isolada para comunicação entre serviços
- Health checks para monitoramento automático
