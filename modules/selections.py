import sqlite3

class Selectdata:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()
    
    def all_tables(self):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        return self.cursor.fetchall()
    
    def columns(self, nome):
        nome = str(nome).strip()
        nome = nome.replace('"', '""')
        self.cursor.execute(f'PRAGMA table_info("{nome}");')
        colunas = self.cursor.fetchall()
        nome_colunas = [coluna[1] for coluna in colunas]
        return nome_colunas
    
    def consulta_tabela(self, nome_tabela):
        nome_tabela = str(nome_tabela).strip()

        tabelas_permitidas = {
            "CLIENTE",
            "VEICULO",
            "FORNECEDOR",
            "PRODUTO",
            "FUNCIONARIO",
            "ORDEM_SERVICO",
            "PAGAMENTO",
            "FEEDBACK",
            "DEPARTAMENTO",
            "ESPECIALIDADE",
            "ESTOQUE",
            "ATENDIMENTO",
            "AGENCIAMENTO_VEICULO",
            "FOLHA_PAGAMENTO",
            "CONTA_RECEBER",
            "CONTA_PAGAR"
        }

        if nome_tabela.upper() not in tabelas_permitidas:
            raise ValueError(f"Tabela inválida: {nome_tabela}")

        query_sql = f'SELECT * FROM "{nome_tabela.upper()}";'
        self.cursor.execute(query_sql)
        colunas = [descricao[0] for descricao in self.cursor.description]
        dados = self.cursor.fetchall()
        return colunas, dados
    
    def client_info(self, id_cliente=None):
        query_sql = '''
            SELECT ID_CLIENTE, NOME_CLIENTE, CPF_CLIENTE, TELEFONE, ENDERECO
            FROM CLIENTE
        '''
        params = []

        if id_cliente is not None:
            query_sql += ' WHERE ID_CLIENTE = ?'
            params.append(id_cliente)

        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def cliente_ult_os(self, id_cliente=None, apenas_ultimo=False, faixa_dados=None):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, VEICULO.MARCA, ORDEM_SERVICO.DESC_REPARO
            FROM CLIENTE
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_CLIENTE = CLIENTE.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO 
                    '''
        adc_client = 'WHERE CLIENTE.ID_CLIENTE = ?'
        adc_ultimo = 'ORDER BY ORDEM_SERVICO.DATA_INICIO LIMIT 1'
        
        if id_cliente:
            query_sql += adc_client
            params.append(id_cliente)

        if apenas_ultimo:
            query_sql += adc_ultimo
            self.cursor.execute(query_sql, params)
            return self.cursor.fetchone()
        else:
            self.cursor.execute(query_sql, params)
            return self.cursor.fetchall()
    
    def info_pagamento(self, id_cliente=None, sitaucao=None):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, CONTA_RECEBER.VALOR_PAGAMENTO, PAGAMENTO.METODO_PAGAMENTO, CONTA_RECEBER.STATUS
            FROM CLIENTE
            INNER JOIN PAGAMENTO ON PAGAMENTO.ID_CLIENTE = CLIENTE.ID_CLIENTE
            INNER JOIN CONTA_RECEBER ON CONTA_RECEBER.ID_PAGAMENTO = PAGAMENTO.ID_PAGAMENTO
        '''
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if sitaucao is not None:
            conditions.append('CONTA_RECEBER.STATUS = ?')
            params.append(sitaucao)

        if conditions:
            query_sql += '\nWHERE ' + ' AND '.join(conditions)

        self.cursor.execute(query_sql, params)
        return self.cursor.fetchall()

    def consulta_carro(self, placa=None):
        query_sql = 'SELECT ID_VEICULO, PLACA, MODELO, MARCA, CHASSIS FROM VEICULO'
        params = []
        
        if placa is not None:
            query_sql += ' WHERE PLACA = ?'
            params.append(placa)
        
        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_produto(self, categoria=None):
        query_sql = 'SELECT ID_PRODUTO, NOME_PRODUTO, CATEGORIA, QUANTIDADE, PRECO_UNITARIO, PRECO_TOTAL FROM PRODUTO '
        params = []
        
        if categoria is not None:
            query_sql += 'WHERE CATEGORIA = ?'
            params.append(categoria)

        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_fornecedor(self, nome=None, cnpj=None):
        query_sql = 'SELECT * FROM FORNECEDOR '
        params = []
        
        if nome is not None:
            query_sql += 'WHERE NOME = ?'
            params.append(nome)
        
        if cnpj is not None:
            query_sql += 'WHERE CNPJ = ?'
            params.append(cnpj)
        
        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_funcionarios(self, id_funcionario=None, nome=None, id_departamento=None, id_especialidade=None):
        base_query = (
            'SELECT ID_FUNCIONARIO, ID_DEPARTAMENTO, ID_ESPECIALIDADE, '
            'NOME_FUNCIONARIO, DATA_ADMISSAO, DATA_DEMISSAO, ENDERECO,  '
            'FROM FUNCIONARIO'
        )
        params = []
        conditions = []

        if id_funcionario is not None:
            conditions.append('ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if nome is not None:
            conditions.append('NOME_FUNCIONARIO LIKE ?')
            params.append(f'%{nome}%')

        if id_departamento is not None:
            conditions.append('ID_DEPARTAMENTO = ?')
            params.append(id_departamento)

        if id_especialidade is not None:
            conditions.append('ID_ESPECIALIDADE = ?')
            params.append(id_especialidade)

        class FuncQuery:
            def __init__(self, cursor, base_query, conditions, params):
                self.cursor = cursor
                self.base_query = base_query
                self.base_conditions = list(conditions)
                self.base_params = list(params)

            def _build_and_exec(self, extra_condition=None, extra_params=None, single=False):
                q = self.base_query
                conds = list(self.base_conditions)
                params = list(self.base_params)

                if conds:
                    q += '\nWHERE ' + ' AND '.join(conds)

                if extra_condition:
                    if conds:
                        q += ' AND ' + extra_condition
                    else:
                        q += '\nWHERE ' + extra_condition

                if extra_params:
                    params.extend(extra_params)

                self.cursor.execute(q, tuple(params))
                return self.cursor.fetchone() if single else self.cursor.fetchall()

            def all(self):
                return self._build_and_exec()

            def ativos(self):
                return self._build_and_exec('DATA_DEMISSAO IS NULL')

            def demitidos(self):
                return self._build_and_exec('DATA_DEMISSAO IS NOT NULL')

            def by_id(self, idv):
                return self._build_and_exec('ID_FUNCIONARIO = ?', [idv], single=True)

        return FuncQuery(self.cursor, base_query, conditions, params)
    
    def metodos_pagamento(self, nome_metodo=None):
        metodos_permitidos = {
            'PIX',
            'CARTÃO DE CRÉDITO',
            'CARTÃO DE DÉBITO',
            'BOLETO',
            'CARTÃO'
        }
        params = []
        query_sql = 'SELECT * FROM PAGAMENTO'

        if nome_metodo not in metodos_permitidos and nome_metodo is not None:
            raise ValueError(f'Valor inválido: {nome_metodo}')
                
        if nome_metodo:
            query_sql += ' WHERE METODO_PAGAMENTO = ?'
            params.append(nome_metodo)

        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_estoque_min(self):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, ESTOQUE.QTDE_ESTOQUE, ESTOQUE.QTDE_MIN,
                CASE
                    WHEN QTDE_ESTOQUE = QTDE_MIN THEN 'Limite mínimo atingido'
                    WHEN QTDE_ESTOQUE < QTDE_MIN THEN 'Abaixo do limite'
                    ELSE 'Acima do limite mínimo'
                END AS STATUS
            FROM ESTOQUE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = ESTOQUE.ID_PRODUTO;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def consulta_salario_bruto(self, salario):
        query_sql = f'''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FOLHA_PAGAMENTO.SALARIO_BRUTO, FUNCIONARIO.DATA_ADMISSAO, FUNCIONARIO.DATA_DEMISSAO
            FROM FUNCIONARIO
            INNER JOIN FOLHA_PAGAMENTO ON FOLHA_PAGAMENTO.ID_FUNCIONARIO = FUNCIONARIO.ID_FUNCIONARIO WHERE FOLHA_PAGAMENTO.SALARIO_BRUTO > {salario}
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()

    def status_agenciamento(self, status):
        query_sql = f'''
            SELECT CLIENTE.NOME_CLIENTE, VEICULO.MODELO, AGENCIAMENTO_VEICULO.DATA_AGENCIAMENTO, AGENCIAMENTO_VEICULO.STATUS
            FROM AGENCIAMENTO_VEICULO
            INNER JOIN VEICULO ON AGENCIAMENTO_VEICULO.ID_VEICULO = VEICULO.ID_VEICULO
            INNER JOIN CLIENTE ON AGENCIAMENTO_VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE
            WHERE AGENCIAMENTO_VEICULO.STATUS = '{status}'
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def clientes_e_veiculos(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, VEICULO.MODELO, VEICULO.MARCA, CLIENTE.TELEFONE
            FROM CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def produtos_e_fornecedores(self):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, PRODUTO.CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, FORNECEDOR.CNPJ, PRODUTO.QUANTIDADE, PRODUTO.PRECO_UNITARIO, PRODUTO.PRECO_TOTAL
            FROM FORNECEDOR
            INNER JOIN PRODUTO ON PRODUTO.ID_FORNECEDOR = FORNECEDOR.ID_FORNECEDOR;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def funcionario_dep_esp(self):
        query = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FUNCIONARIO.DATA_ADMISSAO, DEPARTAMENTO.NOME_DEPARTAMENTO, ESPECIALIDADE.NOME_ESPECIALIDADE
            FROM FUNCIONARIO
            INNER JOIN DEPARTAMENTO ON DEPARTAMENTO.ID_DEPARTAMENTO = FUNCIONARIO.ID_DEPARTAMENTO
            INNER JOIN ESPECIALIDADE ON ESPECIALIDADE.ID_ESPECIALIDADE = FUNCIONARIO.ID_ESPECIALIDADE;
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def os_cliente_veiculo(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, VEICULO.MODELO, VEICULO.MARCA, ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.DATA_CONCLUSAO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO, ORDEM_SERVICO.VALOR_TOTAL
            FROM ORDEM_SERVICO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ORDEM_SERVICO.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def pagamento_os(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO, ORDEM_SERVICO.DESC_REPARO, PAGAMENTO.METODO_PAGAMENTO, ORDEM_SERVICO.VALOR_TOTAL
            FROM PAGAMENTO
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_OS = PAGAMENTO.ID_OS
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def pagamento_produto(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, PRODUTO.NOME_PRODUTO, PRODUTO.CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, FORNECEDOR.CNPJ, 
            PAGAMENTO.DATA_PAGAMENTO, PRODUTO.PRECO_UNITARIO, PRODUTO.QUANTIDADE, PRODUTO.PRECO_TOTAL, PAGAMENTO.STATUS_PAGAMENTO, PAGAMENTO.METODO_PAGAMENTO
            FROM PAGAMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = PAGAMENTO.ID_PRODUTO
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = PRODUTO.ID_FORNECEDOR;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def atendimento_ao_cliente(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, ATENDIMENTO.DATA_ATENDIMENTO, 
            FUNCIONARIO.NOME_FUNCIONARIO
            FROM ATENDIMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ATENDIMENTO.ID_CLIENTE
            INNER JOIN FUNCIONARIO ON FUNCIONARIO.ID_FUNCIONARIO = ATENDIMENTO.ID_FUNCIONARIO
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def produtos_estoque(self):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, PRODUTO.CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, ESTOQUE.QTDE_ESTOQUE, ESTOQUE.VALIDADE_DIAS
            FROM ESTOQUE
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = ESTOQUE.ID_FORNECEDOR
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = ESTOQUE.ID_PRODUTO;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def dados_fp(self):
        query_sql = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FUNCIONARIO.DATA_ADMISSAO, 
            FOLHA_PAGAMENTO.MES_REFERENCIA, FOLHA_PAGAMENTO.SALARIO_BRUTO, FOLHA_PAGAMENTO.DESCONTOS, 
            FOLHA_PAGAMENTO.SALARIO_LIQUIDO, FOLHA_PAGAMENTO.STATUS_PAGAMENTO,
            CASE
                WHEN FUNCIONARIO.DATA_DEMISSAO IS NULL THEN 'Ativo na empresa'
                ELSE 'Desligado'
            END AS FUN_ON_OFF
            FROM FOLHA_PAGAMENTO
            INNER JOIN FUNCIONARIO ON FUNCIONARIO.ID_FUNCIONARIO = FOLHA_PAGAMENTO.ID_FUNCIONARIO;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def cr_pagamento(self):
        query_sql = '''
            SELECT PAGAMENTO.DATA_PAGAMENTO, PAGAMENTO.VALOR_TOTAL, PAGAMENTO.PARCELAS, PAGAMENTO.REFERENCIA,
            CONTA_RECEBER.NUMERO_PARCELA, CONTA_RECEBER.VALOR_PARCELA, CONTA_RECEBER.DATA_VENCIMENTO_RECEBER,
            CONTA_RECEBER.STATUS
            FROM CONTA_RECEBER
            INNER JOIN PAGAMENTO ON PAGAMENTO.ID_PAGAMENTO = CONTA_RECEBER.ID_PAGAMENTO
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
        
    def qtde_veiculo_cliente(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE,
            COUNT(VEICULO.ID_VEICULO) AS QTDE_VEICULOS
            FROM CLIENTE
            LEFT JOIN VEICULO ON CLIENTE.ID_CLIENTE = VEICULO.ID_CLIENTE
            GROUP BY CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE
            ORDER BY QTDE_VEICULOS DESC;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def os_pcliente(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE,
            COUNT(ORDEM_SERVICO.ID_OS) AS QTDE_OS
            FROM CLIENTE
            LEFT JOIN ORDEM_SERVICO ON CLIENTE.ID_CLIENTE = ORDEM_SERVICO.ID_CLIENTE
            GROUP BY CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE
            ORDER BY QTDE_OS DESC;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def total_pagamentos_metodo(self, metodo):
        query_sql = f'''
            SELECT PAGAMENTO.METODO_PAGAMENTO,
            COUNT (*) AS TOTAL_PAGAMENTOS,
            SUM (VALOR_TOTAL) AS VALOR_TOTAL_AGRUPADO
            FROM PAGAMENTO
            WHERE METODO_PAGAMENTO = '{metodo}'
            GROUP BY METODO_PAGAMENTO
            ORDER BY VALOR_TOTAL_AGRUPADO DESC;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
        