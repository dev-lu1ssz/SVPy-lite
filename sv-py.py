import sqlite3
from faker import Faker

conexao = None
cursor = None
fake = Faker('pt_BR')

try:
    conexao = sqlite3.connect('SV-Py_lite.db')
    conexao.execute('PRAGMA foreign_keys = on')
    cursor = conexao.cursor()
    
    table_departamento = '''
        CREATE TABLE IF NOT EXISTS DEPARTAMENTO(
            ID DEPARTAMENTO INTEGER PRIMARY KEY NOT NULL,
            NOME_DEPARTAMENTO VARCHAR(25) NOT NULL
        );
    '''
    table_cliente = '''
        CREATE TABLE IF NOT EXISTS CLIENTE(
            ID_CLIENTE INTEGER PRIMARY KEY NOT NULL,
            NOME_CLIENTE VARCHAR(30) NOT NULL,
            ENDERECO VARCHAR(200) NOT NULL,
            TELEFONE BIGINT NOT NULL,
            CPF_CLIENTE BIGINT UNIQUE
        );
    '''
    table_fornecedor = '''
        CREATE TABLE IF NOT EXISTS FORNECEDOR(
            ID_FORNECEDOR INTEGER PRIMARY KEY NOT NULL,
            NOME_FORNECEDOR VARCHAR(30) NOT NULL,
            CNPJ VARCHAR(14) NOT NULL,
            TELEFONE BIGINT NOT NULL,
            ENDERECO VARCHAR(200) NOT NULL
        );
    '''
    table_funcionario = '''
        CREATE TABLE IF NOT EXISTS FUNCIONARIO(
            ID_FUNCIONARIO INTEGER PRIMARY KEY NOT NULL,
            ID_DEPARTAMENTO INTEGER NOT NULL,
            ID_ESPECIALIDADE INTEGER NOT NULL,
            NOME_FUNCIONARIO VARCHAR(30) NOT NULL,
            SALARIO REAL NOT NULL,
            DATA_ADMISSAO DATE NOT NULL,
            DATA_DEMISSAO DATE NULL,
            ENDERECO VARCHAR(200) NOT NULL,
            FOREIGN KEY (ID_DEPARTAMENTO) REFERENCES DEPARTAMENTO(ID_DEPARTAMENTO),
            FOREIGN KET (ID_ESPECIALIDADE) REFERENCES ESPECIALIDADE(ID_ESPECIALIDADE)
        );
    '''
    table_veiculo = '''
        CREATE TABLE IF NOT EXISTS VEICULO(
            ID_VEICULO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            PLACA VARCHAR(7) NOT NULL,
            MODELO VARCHAR(10) NOT NULL,
            MARCA VARCHAR(30) NOT NULL,
            CHASSIS VARCHAR(17) NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
        );
    '''
    table_produto = '''
        CREATE TABLE IF NOT EXISTS PRODUTO(
            ID_PRODUTO INTEGER PRIMARY KEY NOT NULL,
            ID_FORNECEDOR INTEGER NOT NULL,
            NOME_PRODUTO VARCHAR(25) NOT NULL,
            CATEGORIA VARCHAR(25) NOT NULL,
            QUANTIDADE INTEGER NOT NULL,
            PRECO REAL NOT NULL,
            VALIDADE DATE NULL,
            FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR)
        );
    ''' # COLUNA 'VALIDADE' SERÁ UM CAMPO CALCULADO
    table_ordem_servico = '''
        CREATE TABLE IF NOT EXISTS ORDEM_SERVICO(
            ID_OS INTEGER PRIMARY KEY NOT NULL,
            ID_VEICULO INTEGER NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            DATA_INICIO DATE NOT NULL,
            DATA_CONCLUSAO DATE NULL,
            AGENDAMENTO DATE NULL,
            VALOR_TOTAL REAL NOT NULL,
            DESC_REPARO VARCHAR(100) NOT NULL,
            FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO),
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
        );
    '''
    table_pagamento = '''
        CREATE TABLE IF NOT EXISTS PAGAMENTO(
            ID_PAGAMENTO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NULL,
            ID_OS INTEGER NULL,
            ID_PRODUTO INTEGER NULL,
            METODO_PAGAMENTO VARCHAR(30),
            PARCELAS INTEGER NULL,
            DATA_PAGAMENTO DATE NOT NULL,
            VALOR_PAGAMENTO REAL NOT NULL,
            STATUS_PAGAMENTO VARCHAR(20) NOT NULL,
            REFERÊNCIA VARCHAR(30) NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS),
            FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO)
        );
    '''
    table_feedback = '''
        CREATE TABLE IF NOT EXISTS FEEDBACK(
            ID_FEEDBACK INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            AVALIACAO INTEGER NOT NULL,
            DESCRICAO TEXT NULL,
            DATA_FEEDBACK DATE NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
        );
    ''' # O cliente pode fazer avaliações de 0 a 10 estrelas, ele também poderá preencher o motivo da avaliação
    table_origem_da_receita = '''
        CREATE TABLE IF NOT EXISTS ORIGEM_RECEITA(
            ORIGEM_ID INTEGER PRIMARY KEY NOT NULL,
            NOME VARCHAR(20),
            CATEGORIA VARCHAR(20)
        );
    ''' #  CATEGORIA - Produto, Reparo, Agenciamento
    table_conta_receber = '''
        CREATE TABLE IF NOT EXISTS CONTA_RECEBER(
            ID_CONTA_RECEBER INTEGER PRIMARY KEY NOT NULL,
            VALOR_RECEBER REAL NOT NULL,
            DATA_VENCIMENTO_RECEBER DATE NOT NULL,
            STATUS VARCHAR(15) NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_VENDA) REFERENCES VENDAS(ID_VENDA)
        );
    '''
    table_conta_pagar = '''
        CREATE TABLE IF NOT EXISTS CONTA_PAGAR(
            ID_CONTA_PAGAR INTEGER PRIMARY KEY NOT NULL,
            ID_FORNECEDOR INTEGER NOT NULL,
            ID_PRODUTO INTEGER NOT NULL,
            VALOR_PAGAR REAL NOT NULL,
            DATA_EMISSAO_PAGAR DATE NOT NULL,
            DATA_VENCIMENTO_PAGAR DATE NOT NULL,
            STATUS_PAGAR VARCHAR(20) NOT NULL,
            FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR),
            FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO)
        );
    '''
    table_movimento_estoque = '''
        CREATE TABLE IF NOT EXISTS MOVIMENTO_ESTOQUE(
            ID_MOVIMENTO INTEGER PRIMARY KEY NOT NULL,
            ID_PRODUTO INTEGER NOT NULL,
            ID_OS INTEGER NOT NULL,
            ID_FORNECEDOR INTEGER NOT NULL,
            QUANTIDADE INTEGER NOT NULL,
            TIPO_MOVIMENTO VARCHAR(10) NOT NULL,
            DATA_MOVIMENTO DATE NOT NULL,
            FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO),
            FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS),
            FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR)
        );    
    '''
    table_atendimento_= '''
        CREATE TABLE IF NOT EXISTS ATENDIMENTO(
            ID_ATENDIMENTO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            ID_FUNCIONARIO INTEGER NOT NULL,
            DATA_ATENDIMENTO DATE NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO)
        );
    '''
    table_os_tecnico = '''
        CREATE TABLE IF NOT EXISTS OS_TECNICO(
            ID_OS_TECNICO INTEGER PRIMARY KEY NOT NULL,
            ID_OS INTEGER NOT NULL,
            ID_FUNCIONARIO INTEGER NOT NULL,
            DATA_ATRIBUICAO DATE NOT NULL,
            FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS),
            FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO)
        );
    '''
    table_garantia_os = '''
        CREATE TABLE IF NOT EXISTS GARANTIA_OS(
            ID_GARANTIA INTEGER PRIMARY KEY NOT NULL,
            ID_OS INTEGER NOT NULL,
            DATA_GARANTIA DATE NOT NULL,
            PERIODO_MESES INTEGER NOT NULL,
            STATUS_GARANTIA VARCHAR(20) NOT NULL,
            FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS)
        );
    '''
    table_reclamacao = '''
        CREATE TABLE IF NOT EXISTS RECLAMACAO(
            ID_RECLAMACAO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            ID_GARANTIA INTEGER NOT NULL,
            DATA_RECLAMACAO DATE NOT NULL,
            DESCRICAO TEXT NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_GARANTIA) REFERENCES GARANTIA_OS(ID_GARANTIA)
        );
    '''
    table_contrato = '''
        CREATE TABLE IF NOT EXISTS CONTRATO(
            ID_CONTRATO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            ID_FUNCIONARIO INTEGER NOT NULL,
            TIPO_CONTATO VARCHAR(20) NOT NULL,
            DATA_INICIO DATE NOT NULL,
            DATA_FIM DATE NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO)
        );    
    '''
    table_agenciamento_veiculo = '''
        CREATE TABLE IF NOT EXISTS AGENCIAMENTO_VEICULO(
            ID_AGENCIAMENTO INTEGER PRIMARY KEY NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            ID_VEICULO INTEGER NOT NULL,
            DATA_AGENCIAMENTO DATE NOT NULL,
            VALOR_AGENCIAMENTO REAL NOT NULL,
            PRAZO_DIAS INTEGER NOT NULL,
            COMISSAO_PROC FLOAT NOT NULL,
            STATUS_AGENCIAMENTO VARCHAR(20) NOT NULL,
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
            FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO)
        );
    '''
    
    all_tables = table_departamento + table_cliente + table_fornecedor + table_funcionario + table_veiculo + table_produto + table_ordem_servico + table_vendas + table_pagamento + table_feedback + table_financiamento + table_seguro_garantia + table_conta_receber + table_conta_pagar + table_movimento_estoque + table_atendimento_ + table_os_tecnico + table_garantia_os + table_reclamacao + table_contrato + table_agenciamento_veiculo
    cursor.executescript(all_tables)
    
    conexao.commit()
    print('Todas as tabelas foram criadas com sucesso!')

except sqlite3.DatabaseError as err:
    print('Erro no banco de dado:', err)

finally:    
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()