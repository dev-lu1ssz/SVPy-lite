import os
import sqlite3

def main():
    conexao = None
    cursor = None

    try:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'SV-Py_lite_updated.db')
        db_path = os.path.abspath(db_path)

        if os.path.exists(db_path):
            os.remove(db_path)

        conexao = sqlite3.connect(db_path)
        conexao.execute('PRAGMA foreign_keys = on')
        cursor = conexao.cursor()

        schema_sql = '''
            CREATE TABLE IF NOT EXISTS DEPARTAMENTO(
                ID_DEPARTAMENTO INTEGER PRIMARY KEY NOT NULL,
                NOME_DEPARTAMENTO VARCHAR(25) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS CLIENTE(
                ID_CLIENTE INTEGER PRIMARY KEY NOT NULL,
                NOME_CLIENTE VARCHAR(30) NOT NULL,
                ENDERECO VARCHAR(200) NOT NULL,
                TELEFONE TEXT NOT NULL,
                CPF_CLIENTE TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS FORNECEDOR(
                ID_FORNECEDOR INTEGER PRIMARY KEY NOT NULL,
                NOME_FORNECEDOR VARCHAR(30) NOT NULL,
                CNPJ VARCHAR(14) NOT NULL,
                TELEFONE TEXT NOT NULL,
                ENDERECO VARCHAR(200) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ESPECIALIDADE(
                ID_ESPECIALIDADE INTEGER PRIMARY KEY NOT NULL,
                NOME_ESPECIALIDADE VARCHAR(30) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS FUNCIONARIO(
                ID_FUNCIONARIO INTEGER PRIMARY KEY NOT NULL,
                ID_DEPARTAMENTO INTEGER NOT NULL,
                ID_ESPECIALIDADE INTEGER NOT NULL,
                NOME_FUNCIONARIO VARCHAR(30) NOT NULL,
                DATA_ADMISSAO DATE NOT NULL,
                DATA_DEMISSAO DATE NULL,
                ENDERECO VARCHAR(200) NOT NULL,
                FOREIGN KEY (ID_DEPARTAMENTO) REFERENCES DEPARTAMENTO(ID_DEPARTAMENTO),
                FOREIGN KEY (ID_ESPECIALIDADE) REFERENCES ESPECIALIDADE(ID_ESPECIALIDADE)
            );

            CREATE TABLE IF NOT EXISTS VEICULO(
                ID_VEICULO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                PLACA VARCHAR(7) NOT NULL,
                MODELO VARCHAR(10) NOT NULL,
                MARCA VARCHAR(30) NOT NULL,
                CHASSIS VARCHAR(17) NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
            );

            CREATE TABLE IF NOT EXISTS PRODUTO(
                ID_PRODUTO INTEGER PRIMARY KEY NOT NULL,
                ID_FORNECEDOR INTEGER NOT NULL,
                NOME_PRODUTO VARCHAR(25) NOT NULL,
                CATEGORIA VARCHAR(25) NOT NULL,
                QUANTIDADE INTEGER NOT NULL,
                PRECO_UNITARIO REAL NOT NULL,
                PRECO_TOTAL REAL GENERATED ALWAYS AS (QUANTIDADE * PRECO_UNITARIO) STORED,
                FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR)
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
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
            );

            CREATE TABLE IF NOT EXISTS PAGAMENTO(
                ID_PAGAMENTO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NULL,
                ID_OS INTEGER NULL,
                ID_PRODUTO INTEGER NULL,
                METODO_PAGAMENTO VARCHAR(30) NOT NULL,
                PARCELAS INTEGER NOT NULL DEFAULT 1,
                DATA_PAGAMENTO DATE NOT NULL,
                STATUS_PAGAMENTO VARCHAR(20) NOT NULL,
                VALOR_TOTAL REAL NOT NULL,
                REFERENCIA VARCHAR(30) NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                FOREIGN KEY (ID_OS) REFERENCES ORDEM_SERVICO(ID_OS),
                FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO),
                CHECK (
                    ID_OS IS NOT NULL OR ID_PRODUTO IS NOT NULL
                ),
                CHECK (PARCELAS >= 1)
            );

            CREATE TABLE IF NOT EXISTS FEEDBACK(
                ID_FEEDBACK INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                AVALIACAO INTEGER NOT NULL,
                DESCRICAO TEXT NULL,
                DATA_FEEDBACK DATE NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
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
                CHECK (STATUS IN ('Pendente', 'Recebido', 'Vencida'))
            );

            CREATE TABLE IF NOT EXISTS CONTA_PAGAR(
                ID_CONTA_PAGAR INTEGER PRIMARY KEY NOT NULL,
                DESCRICAO VARCHAR(100) NOT NULL,
                VALOR REAL NOT NULL,
                DATA_VENCIMENTO DATE NOT NULL,
                STATUS VARCHAR(20) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ATENDIMENTO(
                ID_ATENDIMENTO INTEGER PRIMARY KEY NOT NULL,
                ID_CLIENTE INTEGER NOT NULL,
                ID_FUNCIONARIO INTEGER NOT NULL,
                DATA_ATENDIMENTO DATE NOT NULL,
                FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
                FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO)
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
                FOREIGN KEY (ID_VEICULO) REFERENCES VEICULO(ID_VEICULO)
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
                FOREIGN KEY (ID_FUNCIONARIO) REFERENCES FUNCIONARIO(ID_FUNCIONARIO)
            );

            CREATE TABLE IF NOT EXISTS ESTOQUE(
                ID_ESTOQUE INTEGER PRIMARY KEY NOT NULL,
                ID_FORNECEDOR INTEGER NOT NULL,
                ID_PRODUTO INTEGER NOT NULL,
                QTDE_ESTOQUE INTEGER NOT NULL,
                QTDE_MIN INTEGER NOT NULL,
                DATA_VALIDADE DATE NOT NULL,
                VALIDADE_DIAS INTEGER NOT NULL,
                FOREIGN KEY (ID_FORNECEDOR) REFERENCES FORNECEDOR(ID_FORNECEDOR),
                FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO(ID_PRODUTO)
            );
        '''

        cursor.executescript(schema_sql)
        
        conexao.commit()

    except sqlite3.DatabaseError as err:
        print('Erro no banco de dado:', err.args)

    finally:    
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

if __name__ == '__main__':
    main()

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