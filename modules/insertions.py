import sqlite3
import datetime


class InData:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()

    @staticmethod
    def _data_mais_meses(data_base, meses):
        data = datetime.datetime.strptime(data_base, '%d-%m-%Y').date()
        ano = data.year + ((data.month - 1 + meses) // 12)
        mes = (data.month - 1 + meses) % 12 + 1
        dia = min(data.day, 28)
        return datetime.date(ano, mes, dia).strftime('%d-%m-%Y')

    @staticmethod
    def _valor_parcela_total(valor_total, parcelas):
        valor_total = float(valor_total)
        parcelas = int(parcelas)
        valor_base = round(valor_total / parcelas, 2)
        return valor_base

    def cliente(self, nome_cliente, id_endereco, telefone, cpf_cliente):
        self.cursor.execute(
            '''
                INSERT INTO CLIENTE(NOME_CLIENTE, ID_ENDERECO, TELEFONE, CPF_CLIENTE) VALUES
                (?, ?, ?, ?)
            ''',
            (nome_cliente, id_endereco, telefone, cpf_cliente),
        )
        self.conexao.commit()

    def funcionario(self, id_departamento, id_especialidade, nome_funcionario, data_admissao, data_demissao, id_endereco):
        self.cursor.execute(
            '''
                INSERT INTO FUNCIONARIO(ID_DEPARTAMENTO, ID_ESPECIALIDADE, NOME_FUNCIONARIO, DATA_ADMISSAO, DATA_DEMISSAO, ID_ENDERECO) VALUES
                (?, ?, ?, ?, ?, ?)
            ''',
            (id_departamento, id_especialidade, nome_funcionario, data_admissao, data_demissao, id_endereco),
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

    def fornecedor(self, nome_fornecedor, cnpj, telefone, id_endereco):
        self.cursor.execute(
            '''
                INSERT INTO FORNECEDOR(NOME_FORNECEDOR, CNPJ, TELEFONE, ID_ENDERECO) VALUES
                (?, ?, ?, ?)
            ''',
            (nome_fornecedor, cnpj, telefone, id_endereco),
        )
        self.conexao.commit()

    def endereco(self, logradouro, numero, complemento, bairro, cidade, uf, cep):
        self.cursor.execute(
            '''
                INSERT INTO ENDERECO(LOGRADOURO, NUMERO, COMPLEMENTO, BAIRRO, CIDADE, UF, CEP)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (logradouro, numero, complemento, bairro, cidade, uf, cep),
        )
        self.conexao.commit()
        return self.cursor.lastrowid
    def ordem_servico(self, id_veiculo, id_cliente, data_inicio, data_conclusao, tempo_total, agendamento, valor_total, desc_reparo):
        self.cursor.execute(
            '''
                INSERT INTO ORDEM_SERVICO(ID_VEICULO, ID_CLIENTE, DATA_INICIO, DATA_CONCLUSAO, TEMPO_TOTAL_REPARO, AGENDAMENTO, VALOR_TOTAL, DESC_REPARO) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_veiculo, id_cliente, data_inicio, data_conclusao, tempo_total, agendamento, valor_total, desc_reparo),
        )
        self.conexao.commit()

    def pagamento(self, id_cliente, id_os, id_produto, metodo_pagamento, parcelas, data_pagamento, status_pagamento, valor_total, referencia):
        self.cursor.execute(
            '''
                INSERT INTO PAGAMENTO(ID_CLIENTE, METODO_PAGAMENTO, PARCELAS, DATA_PAGAMENTO, STATUS_PAGAMENTO, VALOR_TOTAL, REFERENCIA) VALUES
                (?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_cliente, metodo_pagamento, parcelas, data_pagamento, status_pagamento, valor_total, referencia),
        )
        id_pagamento = self.cursor.lastrowid

        self.cursor.execute(
            '''
                INSERT INTO PAGAMENTO_ITEM(ID_PAGAMENTO, ID_OS, ID_PRODUTO, VALOR_ITEM)
                VALUES (?, ?, ?, ?)
            ''',
            (id_pagamento, id_os, id_produto, valor_total),
        )

        valor_base = self._valor_parcela_total(valor_total, parcelas)
        total_ja_distribuido = 0.0

        for parcela in range(1, int(parcelas) + 1):
            if parcela == int(parcelas):
                valor_parcela = round(float(valor_total) - total_ja_distribuido, 2)
            else:
                valor_parcela = valor_base
                total_ja_distribuido = round(total_ja_distribuido + valor_parcela, 2)

            data_vencimento = self._data_mais_meses(data_pagamento, parcela - 1)
            self.cursor.execute(
                '''
                    INSERT INTO CONTA_RECEBER(ID_PAGAMENTO, NUMERO_PARCELA, VALOR_PARCELA, DATA_VENCIMENTO_RECEBER, DATA_RECEBIMENTO, STATUS)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (id_pagamento, parcela, valor_parcela, data_vencimento, None, 'Pendente'),
            )

        self.conexao.commit()
        return id_pagamento

    def produto(self, id_fornecedor, nome_produto, id_categoria, quantidade, preco_unitario):
        self.cursor.execute(
            '''
                INSERT INTO PRODUTO(ID_FORNECEDOR, NOME_PRODUTO, ID_CATEGORIA, QUANTIDADE, PRECO_UNITARIO) VALUES
                (?, ?, ?, ?, ?)
            ''',
            (id_fornecedor, nome_produto, id_categoria, quantidade, preco_unitario),
        )
        self.conexao.commit()

    def estoque(self, id_produto, qtde_estoque, qtde_min, data_validade, validade_dias):
        self.cursor.execute(
            '''
                INSERT INTO ESTOQUE(ID_PRODUTO, QTDE_ESTOQUE, QTDE_MIN, DATA_VALIDADE, VALIDADE_DIAS) VALUES
                (?, ?, ?, ?, ?)
            ''',
            (id_produto, qtde_estoque, qtde_min, data_validade, validade_dias),
        )
        self.conexao.commit()
        return self.cursor.lastrowid

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

    def conta_receber(self, pagamento_id, numero_parcela, data_vencimento_receber, valor_parcela, status='Pendente', data_recebimento=None):
        self.cursor.execute(
            '''
                INSERT INTO CONTA_RECEBER(ID_PAGAMENTO, NUMERO_PARCELA, VALOR_PARCELA, DATA_VENCIMENTO_RECEBER, DATA_RECEBIMENTO, STATUS) VALUES
                (?, ?, ?, ?, ?, ?)
            ''',
            (pagamento_id, numero_parcela, valor_parcela, data_vencimento_receber, data_recebimento, status),
        )
        self.conexao.commit()
        return self.cursor.lastrowid

    def atendimento(self, id_cliente, id_funcionario, data_atendimento):
        self.cursor.execute(
            '''
                INSERT INTO ATENDIMENTO(ID_CLIENTE, ID_FUNCIONARIO, DATA_ATENDIMENTO) VALUES
                (?, ?, ?)
            ''',
            (id_cliente, id_funcionario, data_atendimento),
        )
        self.conexao.commit()

    def agenciamento_veiculo(self, id_cliente, id_veiculo, data_inicio_agenciamento, data_fim_agenciamento, valor, prazo_dias, comissao, status):
        self.cursor.execute(
            '''
                INSERT INTO AGENCIAMENTO_VEICULO(ID_CLIENTE, ID_VEICULO, DATA_INICIO_AGENCIAMENTO, DATA_FIM_AGENCIAMENTO, VALOR, PRAZO_DIAS, COMISSAO, STATUS) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_cliente, id_veiculo, data_inicio_agenciamento, data_fim_agenciamento, valor, prazo_dias, comissao, status),
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