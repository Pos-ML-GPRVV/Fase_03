# Sistema de Previsão de IPCA

Este projeto implementa um sistema de previsão do Índice Nacional de Preços ao Consumidor Amplo (IPCA) utilizando machine learning com regressão linear. O sistema coleta dados históricos do IPCA através da API do SIDRA (Sistema IBGE de Recuperação Automática), treina um modelo de regressão linear e fornece previsões através de uma API REST.

## 🚀 Funcionalidades

- **Coleta de Dados**: Integração com a API do SIDRA/IBGE para obter dados históricos do IPCA
- **Treinamento de Modelo**: Implementação de regressão linear usando scikit-learn
- **Previsões**: API para gerar previsões do IPCA com base em dados de entrada
- **Métricas de Erro**: Cálculo e armazenamento de métricas de avaliação do modelo (MSE, RMSE, MAPE)
- **API REST**: Endpoints para consulta de dados e geração de previsões
- **Autenticação**: Sistema de autenticação por API Key
- **Banco de Dados**: Armazenamento em PostgreSQL com SQLAlchemy ORM

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas:

```
app/
├── auth/                 # Autenticação e autorização
├── controller/           # Controladores da API (FastAPI)
├── DAO/                  # Data Access Objects
├── enums/               # Enumerações e constantes
├── model/               # Modelos de dados (SQLAlchemy)
├── repository/          # Repositórios para acesso a dados
├── services/            # Lógica de negócio
└── utils/               # Utilitários (ML, split de dados)
```

## 📊 Modelos de Dados

### IPCA
- **Categoria**: Categoria do índice (ex: Alimentação, Transporte)
- **Mês**: Período de referência
- **Tipo**: Tipo de índice (Variação mensal, Peso mensal)
- **Valor**: Valor numérico do índice

### Predictions
- **Mês**: Período da previsão
- **Valor**: Valor previsto pelo modelo

### Error Metrics
- **MSE**: Mean Squared Error
- **RMSE**: Root Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error

## 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework web para API REST
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados relacional
- **scikit-learn**: Biblioteca de machine learning
- **pandas**: Manipulação de dados
- **numpy**: Computação numérica
- **sidrapy**: Cliente Python para API do SIDRA/IBGE
- **psycopg2**: Driver PostgreSQL para Python

## 📋 Pré-requisitos

- Python 3.8+
- Neon PostgreSQL (banco na nuvem) ou PostgreSQL 12+ local
- Docker e Docker Compose (opcional)

## 🚀 Instalação e Execução

### Opção 1: Docker com Neon PostgreSQL (Recomendado)

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Fase_03
```

2. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações do Neon
```

3. Execute com Docker Compose:
```bash
docker-compose up -d
```

**Nota**: O projeto está configurado para usar Neon PostgreSQL na nuvem. As credenciais de teste já estão configuradas no `env.example`.

### Opção 2: Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Fase_03
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados PostgreSQL e as variáveis de ambiente no arquivo `.env`

5. Execute a aplicação:
```bash
python main.py
```

## 🔑 Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

### Para Neon PostgreSQL (Recomendado):
```env
# Banco de Dados Neon
DB_URL=postgresql://neondb_owner:npg_5m3pUxFNWStB@ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech:5432/neondb?sslmode=require

# Variáveis individuais do Neon
PGHOST=ep-wandering-meadow-adx8oa1k-pooler.c-2.us-east-1.aws.neon.tech
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=npg_5m3pUxFNWStB
PGSSLMODE=require
PGCHANNELBINDING=require

# API Key para autenticação
API_KEY=sua_api_key_aqui
```

### Para PostgreSQL Local:
```env
# Banco de Dados Local
DB_URL=postgresql://usuario:senha@localhost:5432/ipca_db

# API Key para autenticação
API_KEY=sua_api_key_aqui
```

## 📚 API Endpoints

### Autenticação
Todos os endpoints requerem autenticação via header `Api-Key`.

### Endpoints Disponíveis

#### `POST /prevision-ipca/`
Gera previsão do IPCA com base em dados de entrada.

**Request Body:**
```json
{
  "data": [valor1, valor2, valor3, valor4, valor5, valor6, valor7, valor8]
}
```

**Response:**
```json
{
  "prediction": 0.45
}
```

#### `GET /general-index-ipca`
Retorna o índice geral do IPCA com valores reais e predições.

#### `GET /target-ipca`
Retorna os dados de target (índice geral) ordenados por mês.

#### `GET /feature-ipca`
Retorna as features (categorias) do IPCA com seus pesos.

#### `GET /errors-metrics`
Retorna as métricas de erro do modelo (MSE, RMSE, MAPE).

#### `POST /training-model`
Retreina o modelo e atualiza as predições e métricas.

## 🔄 Fluxo de Dados

1. **Coleta**: Dados são coletados da API do SIDRA/IBGE
2. **Processamento**: Dados são processados e armazenados no PostgreSQL
3. **Treinamento**: Modelo de regressão linear é treinado com dados históricos
4. **Previsão**: Modelo treinado gera previsões para novos dados
5. **Avaliação**: Métricas de erro são calculadas e armazenadas

## 📈 Categorias do IPCA

O sistema trabalha com as seguintes categorias do IPCA:
- Alimentação e bebidas
- Artigos de residência
- Comunicação
- Despesas pessoais
- Educação
- Habitação
- Saúde e cuidados pessoais
- Transportes

## 🧪 Testando a API

### Exemplo de requisição para previsão:

```bash
curl -X POST "http://localhost:8000/prevision-ipca/" \
  -H "Api-Key: sua_api_key_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [0.5, 0.3, 0.2, 0.4, 0.6, 0.1, 0.7, 0.8]
  }'
```

### Exemplo de consulta de dados:

```bash
curl -X GET "http://localhost:8000/general-index-ipca" \
  -H "Api-Key: sua_api_key_aqui"
```

## 📝 Logs

O sistema gera logs para:
- Criação de tabelas no banco de dados
- Inserção de dados do IPCA
- Treinamento do modelo
- Geração de predições
- Erros e exceções

### Contribuição
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- ⁠Gustavo Silva Imbelloni Borde RM364281
- ⁠Patrick Gabriel Meirelles RM361488 
- Raíssa Campos dos Santos RM364024
- Vitor Crispim Romera Rodrigues RM361332