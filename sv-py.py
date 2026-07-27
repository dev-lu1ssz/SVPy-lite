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
        CREATE TABLE DEPARTAMENTO IF NOT EXISTS (
            ID DEPARTAMENTO INTEGER PRIMARY KEY NOT NULL,
            NOME_DEPARTAMENTO VARCHAR(25) NOT NULL
        );
    '''
    table_cliente = '''
        CREATE TABLE IF NOT EXISTS CLIENTE(
            ID_CLIENTE INTEGER PRIMARY KEY NOT NULL,
            NOME_CLIENTE VARCHAR(30) NOT NULL,
            ENDERECO VARCHAR(200) NOT NULL,
            TELEFONE INTEGER NOT NULL
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
    table_funcionario = ''''
        CREATE TABLE IF NOT EXISTS FUNCIONARIO(
            ID_FUNCIONARIO INTEGER PRIMARY KEY NOT NULL,
            ID_DEPARTAMENTO INTEGER NOT NULL,
            NOME_FUNCIONARIO VARCHAR(30) NOT NULL,
            SALARIO REAL NOT NULL,
            DATA_ADMISSAO DATE NOT NULL,
            DATA_DEMISSAO DATE,
            MOTIVO_DEMISSAO VARCHAR(70),
            ESPECIALIDADE VARCHAR(50) NOT NULL,
            COMISSAO_PROC FLOAT NOT NULL,
            ENDERECO VARCHAR(200) NOT NULL,
            FOREIGN KEY (ID_DEPARTAMENTO) REFERENCES DEPARTAMENTO(ID_DEPARTAMENTO)
        );
    '''
    table_veiculo = ''''
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
    table_produto = ''''
        CREATE TABLE IF NOT EXISTS PRODUTO(
            ID_PRODUTO INTEGER PRIMARY KEY NOT NULL,
            ID_FORNECEDOR INTEGER NOT NULL,
            NOME_PRODUTO VARCHAR(25) NOT NULL,
            DESCRICAO TEXT NOT NULL,
            CATEGORIA VARCHAR(25) NOT NULL,
            QUANTIDADE INTEGER NOT NULL,
            PRECO REAL NOT NULL,
            VALIDADE DATE NULL,
            FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR)
        );
    '''
    table_ordem_servico = '''
        CREATE TABLE IF NOT EXISTS ORDEM_SERVICO(
            ID_OS INTEGER PRIMARY KEY NOT NULL,
            ID_VEICULO INTEGER NOT NULL,
            ID_CLIENTE INTEGER NOT NULL,
            DATA_INICIO DATE NOT NULL,
            DATA_CONCLUSAO DATE NULL,
            DATA_PREVISTA DATE NULL,
            AGENDAMENTO DATE NULL,
            VALOR_TOTAL REAL NOT NULL,
            REPARO VARCHAR(100) NOT NULL,
            FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO),
            FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
        );
    '''
    
except sqlite3.DatabaseError as err:
    print('Erro no banco de dado:', err)

finally:    
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()