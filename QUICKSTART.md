# 🚀 Guia de Início Rápido - Sistema IPCA

## Início Rápido com Docker + Neon PostgreSQL (Recomendado)

### 1. Configuração Automática
```bash
# Execute o script de setup automatizado
./setup.sh
```

### 2. Configuração Manual
```bash
# 1. Copie o arquivo de configuração (já tem credenciais do Neon)
cp env.example .env

# 2. Opcional: Edite o arquivo .env se quiser usar suas próprias credenciais
nano .env

# 3. Inicie os serviços (usando Neon PostgreSQL na nuvem)
docker-compose up -d

# 4. Verifique se está funcionando
curl http://localhost:8000/docs
```

**Nota**: O projeto já está configurado com credenciais de teste do Neon PostgreSQL. Não é necessário instalar PostgreSQL localmente!

## Início Rápido Local (Sem Docker)

### 1. Instalar dependências
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar banco de dados
```bash
# Instalar PostgreSQL e criar banco
createdb ipca_db

# Configurar .env
cp env.example .env
# Editar DB_URL no .env
```

### 3. Executar aplicação
```bash
python main.py
```

## 🔗 URLs Importantes

- **API Documentation**: http://localhost:8000/docs
- **Neon Console**: https://console.neon.tech (para gerenciar o banco na nuvem)

## 🧪 Teste Rápido da API

```bash
# Teste de previsão (substitua YOUR_API_KEY)
curl -X POST "http://localhost:8000/prevision-ipca/" \
  -H "Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.5, 0.3, 0.2, 0.4, 0.6, 0.1, 0.7, 0.8]}'

# Consultar dados gerais
curl -X GET "http://localhost:8000/general-index-ipca" \
  -H "Api-Key: YOUR_API_KEY"
```

## 📋 Comandos Docker Úteis

```bash
# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Reiniciar
docker-compose restart

# Acessar container
docker-compose exec app bash

# Rebuild
docker-compose up --build
```

## ⚠️ Problemas Comuns

### Porta 8000 já em uso
```bash
# Parar outros serviços na porta 8000
sudo lsof -ti:8000 | xargs kill -9
```

### Erro de conexão com banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose logs postgres

# Reiniciar apenas o banco
docker-compose restart postgres
```

### Aplicação não responde
```bash
# Verificar logs da aplicação
docker-compose logs app

# Verificar se todas as dependências estão instaladas
docker-compose exec app pip list
```

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
Fase_03/
├── app/                    # Código da aplicação
├── main.py                # Ponto de entrada
├── requirements.txt       # Dependências Python
├── Dockerfile            # Imagem Docker
├── docker-compose.yml    # Orquestração de containers
├── setup.sh             # Script de configuração
└── README.md            # Documentação completa
```

### Adicionando Novas Features
1. Crie a feature no diretório `app/`
2. Adicione testes se necessário
3. Atualize a documentação
4. Faça commit com mensagem descritiva

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs: `docker-compose logs`
2. Consulte a documentação completa no `README.md`
3. Verifique se todas as dependências estão instaladas
4. Confirme se as variáveis de ambiente estão corretas
