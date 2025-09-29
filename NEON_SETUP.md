# 🚀 Configuração com Neon PostgreSQL

Este projeto está configurado para usar **Neon PostgreSQL** na nuvem, eliminando a necessidade de instalar PostgreSQL localmente.

## 🔧 Configuração Rápida

### 1. Usar Credenciais de Teste (Mais Fácil)
```bash
# Copie o arquivo de configuração do Neon
cp neon.env .env

# Inicie a aplicação
docker-compose up -d
```

### 2. Usar Suas Próprias Credenciais
```bash
# Copie o template
cp env.example .env

# Edite com suas credenciais do Neon
nano .env
```

## 📋 Credenciais de Teste Incluídas

As seguintes credenciais de teste já estão configuradas:

```env
DB_URL=postgresql://neondb_owner:npg_5m3pUxFNWStB@ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech:5432/neondb?sslmode=require

PGHOST=ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=npg_5m3pUxFNWStB
PGSSLMODE=require
PGCHANNELBINDING=require
```

## 🎯 Vantagens do Neon

- ✅ **Sem instalação local**: Não precisa instalar PostgreSQL
- ✅ **Sempre disponível**: Banco na nuvem 24/7
- ✅ **SSL automático**: Conexão segura por padrão
- ✅ **Backup automático**: Dados seguros na nuvem
- ✅ **Escalável**: Cresce com suas necessidades

## 🔗 Acessos Importantes

- **API da aplicação**: http://localhost:8000/docs
- **Console Neon**: https://console.neon.tech
- **Documentação Neon**: https://neon.tech/docs

## 🧪 Teste de Conexão

```bash
# Teste se a aplicação está funcionando
curl http://localhost:8000/docs

# Teste de previsão (substitua pela sua API_KEY)
curl -X POST "http://localhost:8000/prevision-ipca/" \
  -H "Api-Key: test_api_key_123" \
  -H "Content-Type: application/json" \
  -d '{"data": [0.5, 0.3, 0.2, 0.4, 0.6, 0.1, 0.7, 0.8]}'
```

## 🔧 Comandos Docker

```bash
# Iniciar aplicação
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar aplicação
docker-compose down

# Rebuild da aplicação
docker-compose up --build -d
```

## ⚠️ Notas Importantes

1. **API Key**: A API_KEY padrão é `test_api_key_123`. Para produção, altere no arquivo `.env`
2. **Credenciais de Teste**: As credenciais incluídas são para teste. Para produção, use suas próprias credenciais do Neon
3. **SSL**: O Neon requer SSL, que já está configurado
4. **Limites**: O plano gratuito do Neon tem limites de uso

## 🆘 Solução de Problemas

### Erro de Conexão
```bash
# Verificar se as variáveis estão corretas
docker-compose logs app

# Verificar conectividade
docker-compose exec app ping ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech
```

### Aplicação não inicia
```bash
# Verificar logs detalhados
docker-compose logs -f

# Rebuild completo
docker-compose down
docker-compose up --build -d
```

### Problemas de SSL
- Verifique se `PGSSLMODE=require` está no `.env`
- Confirme se a URL inclui `?sslmode=require`

## 📚 Próximos Passos

1. **Teste a API**: Acesse http://localhost:8000/docs
2. **Configure sua API Key**: Edite o arquivo `.env`
3. **Monitore o banco**: Use o console do Neon
4. **Deploy em produção**: Configure suas próprias credenciais

## 🔗 Links Úteis

- [Neon Console](https://console.neon.tech)
- [Documentação Neon](https://neon.tech/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
