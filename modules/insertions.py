import sqlite3


class InData:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()

    def cliente(self, nome_cliente, endereco_cliente, telefone, cpf_cliente):
        self.cursor.execute(
            '''
                INSERT INTO CLIENTE(NOME_CLIENTE, ENDERECO, TELEFONE, CPF_CLIENTE) VALUES
                (?, ?, ?, ?)
            ''',
            (nome_cliente, endereco_cliente, telefone, cpf_cliente),
        )
        self.conexao.commit()

    def funcionario(self, id_departamento, id_especialidade, nome_funcionario, salario, data_admissao, data_demissao, endereco):
        self.cursor.execute(
            '''
                INSERT INTO FUNCIONARIO(ID_DEPARTAMENTO, ID_ESPECIALIDADE, NOME_FUNCIONARIO, SALARIO, DATA_ADMISSAO, DATA_DEMISSAO, ENDERECO) VALUES
                (?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_departamento, id_especialidade, nome_funcionario, salario, data_admissao, data_demissao, endereco),
        )
        self.conexao.commit()

    def departamento(self, nome_departamento):
        self.cursor.execute(
            '''
                INSERT INTO DEPARTAMENTO(NOME_DEPARTAMENTO) VALUES
                (?)
            ''',
            (nome_departamento,),
        )
        self.conexao.commit()

    def especialidade(self, id_especialidade, nome_especialidade):
        self.cursor.execute(
            '''
                INSERT INTO ESPECIALIDADE(ID_ESPECIALIDADE, NOME_ESPECIALIDADE) VALUES
                (?, ?)
            ''',
            (id_especialidade, nome_especialidade),
        )
        self.conexao.commit()

    def feedback(self, id_cliente, avaliacao, descricao, data_feedback):
        self.cursor.execute(
            '''
                INSERT INTO FEEDBACK(ID_CLIENTE, AVALIACAO, DESCRICAO, DATA_FEEDBACK) VALUES
                (?, ?, ?, ?)
            ''',
            (id_cliente, avaliacao, descricao, data_feedback),
        )
        self.conexao.commit()

    def fornecedor(self, nome_fornecedor, cnpj, telefone, endereco_fornecedor):
        self.cursor.execute(
            '''
                INSERT INTO FORNECEDOR(NOME_FORNECEDOR, CNPJ, TELEFONE, ENDERECO) VALUES
                (?, ?, ?, ?)
            ''',
            (nome_fornecedor, cnpj, telefone, endereco_fornecedor),
        )
        self.conexao.commit()

    def ordem_servico(self, id_veiculo, id_cliente, data_inicio, data_conclusao, tempo_total, agendamento, valor_total, desc_reparo):
        self.cursor.execute(
            '''
                INSERT INTO ORDEM_SERVICO(ID_VEICULO, ID_CLIENTE, DATA_INICIO, DATA_CONCLUSAO, TEMPO_TOTAL_REPARO, AGENDAMENTO, VALOR_TOTAL, DESC_REPARO) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_veiculo, id_cliente, data_inicio, data_conclusao, tempo_total, agendamento, valor_total, desc_reparo),
        )
        self.conexao.commit()

    def pagamento(self, id_cliente, id_os, id_produto, metodo_pagamento, parcelas, data_pagamento, valor_pagamento, status_pagamento, referencia):
        self.cursor.execute(
            '''
                INSERT INTO PAGAMENTO(ID_CLIENTE, ID_OS, ID_PRODUTO, METODO_PAGAMENTO, PARCELAS, DATA_PAGAMENTO, VALOR_PAGAMENTO, STATUS_PAGAMENTO, REFERENCIA) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_cliente, id_os, id_produto, metodo_pagamento, parcelas, data_pagamento, valor_pagamento, status_pagamento, referencia),
        )
        self.conexao.commit()

    def produto(self, id_fornecedor, nome_produto, categoria, quantidade, preco_unitario, validade):
        self.cursor.execute(
            '''
                INSERT INTO PRODUTO(ID_FORNECEDOR, NOME_PRODUTO, CATEGORIA, QUANTIDADE, PRECO_UNITARIO, VALIDADE) VALUES
                (?, ?, ?, ?, ?, ?)
            ''',
            (id_fornecedor, nome_produto, categoria, quantidade, preco_unitario, validade),
        )
        self.conexao.commit()

    def veiculo(self, id_cliente, placa, modelo, marca, chassis):
        self.cursor.execute(
            '''
                INSERT INTO VEICULO(ID_CLIENTE, PLACA, MODELO, MARCA, CHASSIS) VALUES
                (?, ?, ?, ?, ?)
            ''',
            (id_cliente, placa, modelo, marca, chassis),
        )
        self.conexao.commit()

    def conta_pagar(self, descricao, valor, data_vencimento, status):
        self.cursor.execute(
            '''
                INSERT INTO CONTA_PAGAR(DESCRICAO, VALOR, DATA_VENCIMENTO, STATUS) VALUES
                (?, ?, ?, ?)
            ''',
            (descricao, valor, data_vencimento, status),
        )
        self.conexao.commit()

    def conta_receber(self, pagamento_id, data_vencimento_receber, status):
        self.cursor.execute(
            '''
                INSERT INTO CONTA_RECEBER(ID_PAGAMENTO, DATA_VENCIMENTO_RECEBER, STATUS) VALUES
                (?, ?, ?)
            ''',
            (pagamento_id, data_vencimento_receber, status),
        )
        self.conexao.commit()

    def atendimento(self, id_cliente, id_funcionario, data_atendimento):
        self.cursor.execute(
            '''
                INSERT INTO ATENDIMENTO(ID_CLIENTE, ID_FUNCIONARIO, DATA_ATENDIMENTO) VALUES
                (?, ?, ?)
            ''',
            (id_cliente, id_funcionario, data_atendimento),
        )
        self.conexao.commit()

    def agenciamento_veiculo(self, id_cliente, id_veiculo, data_agenciamento, valor, prazo_dias, comissao, status):
        self.cursor.execute(
            '''
                INSERT INTO AGENCIAMENTO_VEICULO(ID_CLIENTE, ID_VEICULO, DATA_AGENCIAMENTO, VALOR, PRAZO_DIAS, COMISSAO, STATUS) VALUES
                (?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_cliente, id_veiculo, data_agenciamento, valor, prazo_dias, comissao, status),
        )
        self.conexao.commit()
        
    def folha_pagamento(self, id_funcionario, status_pagamento, mes_referencia, data_pagamento, salario_bruto, adicionais, descontos):
        self.cursor.execute(
            '''
                INSERT INTO FOLHA_PAGAMENTO(ID_FUNCIONARIO, STATUS_PAGAMENTO, MES_REFERENCIA, DATA_PAGAMENTO, SALARIO_BRUTO, ADICIONAIS, DESCONTOS) VALUES
                (?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_funcionario, status_pagamento, mes_referencia, data_pagamento, salario_bruto, adicionais, descontos)
        )
        self.conexao.commit()