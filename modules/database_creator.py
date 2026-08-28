import os
import sqlite3

schema_sql = '''
            CREATE TABLE IF NOT EXISTS SCHEMA_VERSION(
                VERSION INTEGER PRIMARY KEY NOT NULL
            );

            CREATE TABLE IF NOT EXISTS DEPARTAMENTO(
                ID_DEPARTAMENTO INTEGER PRIMARY KEY NOT NULL,
                NOME_DEPARTAMENTO VARCHAR(25) NOT NULL UNIQUE,
                CHECK (length(NOME_DEPARTAMENTO) BETWEEN 1 AND 25)
            );

            CREATE TABLE IF NOT EXISTS ENDERECO(
                ID_ENDERECO INTEGER PRIMARY KEY NOT NULL,
                LOGRADOURO TEXT NOT NULL,
                NUMERO TEXT,
                COMPLEMENTO TEXT,
                BAIRRO TEXT,
                CIDADE TEXT NOT NULL,
                UF TEXT NOT NULL,
                CEP TEXT NOT NULL,
                CHECK (length(LOGRADOURO) BETWEEN 1 AND 200),
                CHECK (NUMERO IS NULL OR length(NUMERO) <= 10),
                CHECK (COMPLEMENTO IS NULL OR length(COMPLEMENTO) <= 100),
                CHECK (BAIRRO IS NULL OR length(BAIRRO) <= 100),
                CHECK (length(CIDADE) BETWEEN 1 AND 100),
                CHECK (length(UF) = 2),
                CHECK (length(CEP) IN (8, 9))
            );

            CREATE TABLE IF NOT EXISTS CLIENTE(
                ID_CLIENTE INTEGER PRIMARY KEY NOT NULL,
                NOME_CLIENTE VARCHAR(30) NOT NULL,
                ID_ENDERECO INTEGER NOT NULL,
                TELEFONE TEXT NOT NULL,
                CPF_CLIENTE TEXT NOT NULL UNIQUE,
                FOREIGN KEY (ID_ENDERECO) REFERENCES ENDERECO(ID_ENDERECO),
                CHECK (length(NOME_CLIENTE) BETWEEN 1 AND 30),
                CHECK (length(TELEFONE) BETWEEN 8 AND 15),
                CHECK (length(CPF_CLIENTE) IN (11, 14))
            );

            CREATE TABLE IF NOT EXISTS FORNECEDOR(
                ID_FORNECEDOR INTEGER PRIMARY KEY NOT NULL,
                NOME_FORNECEDOR VARCHAR(30) NOT NULL,
                CNPJ VARCHAR(14) NOT NULL UNIQUE,
                TELEFONE TEXT NOT NULL,
                ID_ENDERECO INTEGER NOT NULL,
                FOREIGN KEY (ID_ENDERECO) REFERENCES ENDERECO(ID_ENDERECO),
                CHECK (length(NOME_FORNECEDOR) BETWEEN 1 AND 30),
                CHECK (length(CNPJ) = 14),
                CHECK (length(TELEFONE) BETWEEN 8 AND 15)
            );

            CREATE TABLE IF NOT EXISTS ESPECIALIDADE(
                ID_ESPECIALIDADE INTEGER PRIMARY KEY NOT NULL,
                NOME_ESPECIALIDADE VARCHAR(30) NOT NULL UNIQUE,
                CHECK (length(NOME_ESPECIALIDADE) BETWEEN 1 AND 30)
            );

            CREATE TABLE IF NOT EXISTS FUNCIONARIO(
                ID_FUNCIONARIO INTEGER PRIMARY KEY NOT NULL,
                ID_DEPARTAMENTO INTEGER NOT NULL,
                ID_ESPECIALIDADE INTEGER NOT NULL,
                NOME_FUNCIONARIO VARCHAR(30) NOT NULL,
                DATA_ADMISSAO DATE NOT NULL,
                DATA_DEMISSAO DATE NULL,
                ID_ENDERECO INTEGER NOT NULL,
                FOREIGN KEY (ID_DEPARTAMENTO) REFERENCES DEPARTAMENTO(ID_DEPARTAMENTO),
                FOREIGN KEY (ID_ESPECIALIDADE) REFERENCES ESPECIALIDADE(ID_ESPECIALIDADE),
                FOREIGN KEY (ID_ENDERECO) REFERENCES ENDERECO(ID_ENDERECO),
                CHECK (DATA_DEMISSAO IS NULL OR substr(DATA_DEMISSAO, 7, 4) || substr(DATA_DEMISSAO, 4, 2) || substr(DATA_DEMISSAO, 1, 2) >= substr(DATA_ADMISSAO, 7, 4) || substr(DATA_ADMISSAO, 4, 2) || substr(DATA_ADMISSAO, 1, 2)),
                CHECK (length(NOME_FUNCIONARIO) BETWEEN 1 AND 30),
                CHECK (DATA_ADMISSAO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'),
                CHECK (DATA_DEMISSAO IS NULL OR DATA_DEMISSAO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS VEICULO(
                ID_VEICULO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                PLACA VARCHAR(7) NOT NULL,
                MODELO VARCHAR(10) NOT NULL,
                MARCA VARCHAR(30) NOT NULL,
                CHASSIS VARCHAR(17) NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                UNIQUE (ID_VEICULO, ID_CLIENTE),
                UNIQUE (PLACA),
                UNIQUE (CHASSIS),
                CHECK (length(PLACA) = 7),
                CHECK (length(MODELO) BETWEEN 1 AND 10),
                CHECK (length(MARCA) BETWEEN 1 AND 30),
                CHECK (length(CHASSIS) = 17)
            );

            CREATE TABLE IF NOT EXISTS CATEGORIA_PRODUTO(
                ID_CATEGORIA INTEGER PRIMARY KEY NOT NULL,
                NOME_CATEGORIA VARCHAR(25) NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS PRODUTO(
                ID_PRODUTO INTEGER PRIMARY KEY NOT NULL,
                ID_FORNECEDOR INTEGER NOT NULL,
                NOME_PRODUTO VARCHAR(25) NOT NULL,
                ID_CATEGORIA INTEGER NOT NULL,
                QUANTIDADE INTEGER NOT NULL,
                PRECO_UNITARIO REAL NOT NULL,
                PRECO_TOTAL REAL GENERATED ALWAYS AS (QUANTIDADE * PRECO_UNITARIO) STORED,
                FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR),
                FOREIGN KEY (ID_CATEGORIA) REFERENCES CATEGORIA_PRODUTO(ID_CATEGORIA),
                CHECK (QUANTIDADE >= 0),
                CHECK (PRECO_UNITARIO >= 0),
                CHECK (length(NOME_PRODUTO) BETWEEN 1 AND 25)
            );

            CREATE TABLE IF NOT EXISTS ORDEM_SERVICO(
                ID_OS INTEGER PRIMARY KEY NOT NULL,
                ID_VEICULO INTEGER NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                DATA_INICIO DATE NOT NULL,
                DATA_CONCLUSAO DATE NULL,
                TEMPO_TOTAL_REPARO INTEGER,
                AGENDAMENTO DATE NULL,
                VALOR_TOTAL REAL NOT NULL,
                DESC_REPARO VARCHAR(100) NOT NULL,
                FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO),
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                FOREIGN KEY (ID_VEICULO, ID_CLIENTE) REFERENCES VEICULO(ID_VEICULO, ID_CLIENTE),
                CHECK (DATA_CONCLUSAO IS NULL OR substr(DATA_CONCLUSAO, 7, 4) || substr(DATA_CONCLUSAO, 4, 2) || substr(DATA_CONCLUSAO, 1, 2) >= substr(DATA_INICIO, 7, 4) || substr(DATA_INICIO, 4, 2) || substr(DATA_INICIO, 1, 2)),
                CHECK (TEMPO_TOTAL_REPARO IS NULL OR TEMPO_TOTAL_REPARO >= 0),
                CHECK (VALOR_TOTAL >= 0),
                CHECK (DATA_INICIO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'),
                CHECK (DATA_CONCLUSAO IS NULL OR DATA_CONCLUSAO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'),
                CHECK (AGENDAMENTO IS NULL OR AGENDAMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS PAGAMENTO(
                ID_PAGAMENTO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                METODO_PAGAMENTO VARCHAR(30) NOT NULL,
                PARCELAS INTEGER NOT NULL DEFAULT 1,
                DATA_PAGAMENTO DATE NOT NULL,
                STATUS_PAGAMENTO VARCHAR(20) NOT NULL,
                VALOR_TOTAL REAL NOT NULL,
                REFERENCIA VARCHAR(30) NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                CHECK (PARCELAS >= 1),
                CHECK (VALOR_TOTAL >= 0),
                CHECK (STATUS_PAGAMENTO IN ('Pendente', 'Pago', 'Cancelado')),
                CHECK (length(METODO_PAGAMENTO) BETWEEN 1 AND 30),
                CHECK (length(REFERENCIA) BETWEEN 1 AND 30),
                CHECK (DATA_PAGAMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS PAGAMENTO_ITEM(
                ID_PAGAMENTO_ITEM INTEGER PRIMARY KEY NOT NULL,
                ID_PAGAMENTO INTEGER NOT NULL,
                ID_OS INTEGER NULL,
                ID_PRODUTO INTEGER NULL,
                QUANTIDADE INTEGER NOT NULL DEFAULT 1,
                VALOR_ITEM REAL NOT NULL,
                FOREIGN KEY (ID_PAGAMENTO) REFERENCES PAGAMENTO(ID_PAGAMENTO),
                FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS),
                FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO),
                CHECK ((ID_OS IS NOT NULL) <> (ID_PRODUTO IS NOT NULL)),
                CHECK (QUANTIDADE > 0),
                CHECK (VALOR_ITEM >= 0)
            );

            CREATE TABLE IF NOT EXISTS FEEDBACK(
                ID_FEEDBACK INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                AVALIACAO INTEGER NOT NULL,
                DESCRICAO TEXT NULL,
                DATA_FEEDBACK DATE NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                CHECK (AVALIACAO BETWEEN 0 AND 10),
                CHECK (DATA_FEEDBACK GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS CONTA_RECEBER(
                ID_CONTA_RECEBER INTEGER PRIMARY KEY NOT NULL,
                ID_PAGAMENTO INTEGER NOT NULL,
                NUMERO_PARCELA INTEGER NOT NULL,
                VALOR_PARCELA REAL NOT NULL,
                DATA_VENCIMENTO_RECEBER DATE NOT NULL,
                DATA_RECEBIMENTO DATE NULL,
                STATUS VARCHAR(15) NOT NULL,
                UNIQUE (ID_PAGAMENTO, NUMERO_PARCELA),
                FOREIGN KEY (ID_PAGAMENTO) REFERENCES PAGAMENTO(ID_PAGAMENTO),
                CHECK (NUMERO_PARCELA >= 1),
                CHECK (VALOR_PARCELA >= 0),
                CHECK (STATUS IN ('Pendente', 'Recebido', 'Vencida')),
                CHECK (STATUS <> 'Recebido' OR DATA_RECEBIMENTO IS NOT NULL),
                CHECK (DATA_VENCIMENTO_RECEBER GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'),
                CHECK (DATA_RECEBIMENTO IS NULL OR DATA_RECEBIMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS CONTA_PAGAR(
                ID_CONTA_PAGAR INTEGER PRIMARY KEY NOT NULL,
                DESCRICAO VARCHAR(100) NOT NULL,
                VALOR REAL NOT NULL,
                DATA_VENCIMENTO DATE NOT NULL,
                STATUS VARCHAR(20) NOT NULL,
                CHECK (VALOR >= 0),
                CHECK (STATUS IN ('Pendente', 'Pago', 'Vencida', 'Cancelada')),
                CHECK (length(DESCRICAO) BETWEEN 1 AND 100),
                CHECK (DATA_VENCIMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS ATENDIMENTO(
                ID_ATENDIMENTO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                ID_FUNCIONARIO INTEGER NOT NULL,
                DATA_ATENDIMENTO DATE NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO),
                CHECK (DATA_ATENDIMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS AGENCIAMENTO_VEICULO(
                ID_AGENCIAMENTO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                ID_VEICULO INTEGER NOT NULL,
                DATA_INICIO_AGENCIAMENTO DATE NOT NULL,
                DATA_FIM_AGENCIAMENTO DATE NOT NULL,
                VALOR REAL NOT NULL,
                PRAZO_DIAS INTEGER NOT NULL,
                COMISSAO FLOAT NOT NULL,
                STATUS VARCHAR(20) NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO),
                FOREIGN KEY (ID_VEICULO, ID_CLIENTE) REFERENCES VEICULO(ID_VEICULO, ID_CLIENTE),
                CHECK (substr(DATA_FIM_AGENCIAMENTO, 7, 4) || substr(DATA_FIM_AGENCIAMENTO, 4, 2) || substr(DATA_FIM_AGENCIAMENTO, 1, 2) >= substr(DATA_INICIO_AGENCIAMENTO, 7, 4) || substr(DATA_INICIO_AGENCIAMENTO, 4, 2) || substr(DATA_INICIO_AGENCIAMENTO, 1, 2)),
                CHECK (VALOR >= 0),
                CHECK (PRAZO_DIAS >= 0),
                CHECK (COMISSAO >= 0),
                CHECK (STATUS IN ('Pendente', 'Vendido', 'Cancelado')),
                CHECK (DATA_INICIO_AGENCIAMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]'),
                CHECK (DATA_FIM_AGENCIAMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS FOLHA_PAGAMENTO(
                ID_FP INTEGER PRIMARY KEY NOT NULL,
                ID_FUNCIONARIO INTEGER NOT NULL,
                STATUS_PAGAMENTO VARCHAR(10) NOT NULL,
                MES_REFERENCIA INTEGER NOT NULL,
                DATA_PAGAMENTO DATE NOT NULL,
                SALARIO_BRUTO REAL NOT NULL,
                ADICIONAIS REAL NULL,
                DESCONTOS REAL NOT NULL,
                SALARIO_LIQUIDO REAL GENERATED ALWAYS AS ((SALARIO_BRUTO + COALESCE(ADICIONAIS, 0)) - DESCONTOS) STORED,
                FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO),
                CHECK (MES_REFERENCIA BETWEEN 1 AND 12),
                CHECK (SALARIO_BRUTO >= 0),
                CHECK (COALESCE(ADICIONAIS, 0) >= 0),
                CHECK (DESCONTOS >= 0),
                CHECK (STATUS_PAGAMENTO IN ('Realizado', 'Programado')),
                UNIQUE (ID_FUNCIONARIO, MES_REFERENCIA, DATA_PAGAMENTO),
                CHECK (DATA_PAGAMENTO GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE TABLE IF NOT EXISTS ESTOQUE(
                ID_ESTOQUE INTEGER PRIMARY KEY NOT NULL,
                ID_PRODUTO INTEGER NOT NULL,
                QTDE_ESTOQUE INTEGER NOT NULL,
                QTDE_MIN INTEGER NOT NULL,
                DATA_VALIDADE DATE NOT NULL,
                VALIDADE_DIAS INTEGER NOT NULL,
                FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO),
                CHECK (QTDE_ESTOQUE >= 0),
                CHECK (QTDE_MIN >= 0),
                CHECK (VALIDADE_DIAS >= 0),
                UNIQUE (ID_PRODUTO),
                CHECK (DATA_VALIDADE GLOB '[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]')
            );

            CREATE INDEX IF NOT EXISTS IDX_FUNCIONARIO_DEPARTAMENTO
                ON FUNCIONARIO(ID_DEPARTAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_FUNCIONARIO_ESPECIALIDADE
                ON FUNCIONARIO(ID_ESPECIALIDADE);
            CREATE INDEX IF NOT EXISTS IDX_FUNCIONARIO_ENDERECO
                ON FUNCIONARIO(ID_ENDERECO);
            CREATE INDEX IF NOT EXISTS IDX_FUNCIONARIO_DEMISSAO
                ON FUNCIONARIO(DATA_DEMISSAO);

            CREATE INDEX IF NOT EXISTS IDX_VEICULO_CLIENTE
                ON VEICULO(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_VEICULO_MODELO
                ON VEICULO(MODELO);
            CREATE INDEX IF NOT EXISTS IDX_VEICULO_MARCA
                ON VEICULO(MARCA);

            CREATE INDEX IF NOT EXISTS IDX_PRODUTO_FORNECEDOR
                ON PRODUTO(ID_FORNECEDOR);
            CREATE INDEX IF NOT EXISTS IDX_PRODUTO_CATEGORIA
                ON PRODUTO(ID_CATEGORIA);
            CREATE INDEX IF NOT EXISTS IDX_PRODUTO_NOME
                ON PRODUTO(NOME_PRODUTO);

            CREATE INDEX IF NOT EXISTS IDX_OS_CLIENTE
                ON ORDEM_SERVICO(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_OS_VEICULO
                ON ORDEM_SERVICO(ID_VEICULO);
            CREATE INDEX IF NOT EXISTS IDX_OS_DATA_INICIO
                ON ORDEM_SERVICO(DATA_INICIO);
            CREATE INDEX IF NOT EXISTS IDX_OS_DATA_CONCLUSAO
                ON ORDEM_SERVICO(DATA_CONCLUSAO);
            CREATE INDEX IF NOT EXISTS IDX_OS_TEMPO_REPARO
                ON ORDEM_SERVICO(TEMPO_TOTAL_REPARO);

            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_CLIENTE
                ON PAGAMENTO(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_DATA
                ON PAGAMENTO(DATA_PAGAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_STATUS
                ON PAGAMENTO(STATUS_PAGAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_METODO
                ON PAGAMENTO(METODO_PAGAMENTO);

            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_ITEM_PAGAMENTO
                ON PAGAMENTO_ITEM(ID_PAGAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_ITEM_OS
                ON PAGAMENTO_ITEM(ID_OS);
            CREATE INDEX IF NOT EXISTS IDX_PAGAMENTO_ITEM_PRODUTO
                ON PAGAMENTO_ITEM(ID_PRODUTO);

            CREATE INDEX IF NOT EXISTS IDX_FEEDBACK_CLIENTE
                ON FEEDBACK(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_CONTA_RECEBER_PAGAMENTO
                ON CONTA_RECEBER(ID_PAGAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_CONTA_RECEBER_VENCIMENTO
                ON CONTA_RECEBER(DATA_VENCIMENTO_RECEBER);
            CREATE INDEX IF NOT EXISTS IDX_CONTA_RECEBER_STATUS
                ON CONTA_RECEBER(STATUS);
            CREATE INDEX IF NOT EXISTS IDX_ATENDIMENTO_CLIENTE
                ON ATENDIMENTO(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_ATENDIMENTO_FUNCIONARIO
                ON ATENDIMENTO(ID_FUNCIONARIO);
            CREATE INDEX IF NOT EXISTS IDX_ATENDIMENTO_DATA
                ON ATENDIMENTO(DATA_ATENDIMENTO);
            CREATE INDEX IF NOT EXISTS IDX_AGENCIAMENTO_CLIENTE
                ON AGENCIAMENTO_VEICULO(ID_CLIENTE);
            CREATE INDEX IF NOT EXISTS IDX_AGENCIAMENTO_VEICULO
                ON AGENCIAMENTO_VEICULO(ID_VEICULO);
            CREATE INDEX IF NOT EXISTS IDX_AGENCIAMENTO_STATUS
                ON AGENCIAMENTO_VEICULO(STATUS);
            CREATE INDEX IF NOT EXISTS IDX_FOLHA_FUNCIONARIO
                ON FOLHA_PAGAMENTO(ID_FUNCIONARIO);
            CREATE INDEX IF NOT EXISTS IDX_FOLHA_STATUS
                ON FOLHA_PAGAMENTO(STATUS_PAGAMENTO);
            CREATE INDEX IF NOT EXISTS IDX_ESTOQUE_PRODUTO
                ON ESTOQUE(ID_PRODUTO);
        '''

def criar_banco(db_path):
    conexao = None
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conexao = sqlite3.connect(db_path)
        conexao.execute('PRAGMA foreign_keys = on')
        conexao.executescript(schema_sql)
        conexao.commit()
        conexao.close()

    except sqlite3.DatabaseError:
        if conexao:
            conexao.rollback()
        raise

def recriar_banco(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)

    criar_banco(db_path)


# Tempo total vai retornar a quantidade em dias
# A transação pode estar ligada a OS, a produto, ou aos dois, mas pelo menos um deles deve existir.
# Referencia - String que mostra exatamente o que ele comprou; para produto, informa o nome do produto; para OS, usa "Reparo".
# PARCELAS indica a quantidade total de parcelas do pagamento.
# O cliente pode fazer avaliações de 0 a 10 estrelas, ele também poderá preencher o motivo da avaliação
# Cada linha representa uma parcela específica do pagamento.
# VALOR_PARCELA guarda o valor individual da parcela, sem duplicar o valor total do pagamento.
# STATUS - Pendente/Recebido/Vencida
# STATUS - Pendente/Pago
# STATUS PAGAMENTO - Realizado/Programado
# MES_REFERENCIA - 1 a 12
# ADICIONAIS - Horas extras (nem todos os funcionarios)
# DESCONTOS - Beneficios (INSS, FGTS, Vale-Transporte, Vale-Refeição, Vale-Alimentação)
# SALARIO_LIQUIDO - Coluna calculada e armazenada