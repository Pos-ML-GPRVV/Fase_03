-- Script de inicialização do banco de dados PostgreSQL
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Comentários sobre o banco
COMMENT ON DATABASE ipca_db IS 'Banco de dados para sistema de previsão de IPCA';

-- Configurações de timezone
SET timezone = 'America/Sao_Paulo';

-- Log de inicialização
DO $$
BEGIN
    RAISE NOTICE 'Banco de dados IPCA inicializado com sucesso!';
    RAISE NOTICE 'Timezone configurado para: %', current_setting('timezone');
END $$;
