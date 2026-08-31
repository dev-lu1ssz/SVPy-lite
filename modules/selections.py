import sqlite3
from tabulate import tabulate
from modules.colors import Colors
colors = Colors()
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
            "ENDERECO",
            "CATEGORIA_PRODUTO",
            "VEICULO",
            "FORNECEDOR",
            "PRODUTO",
            "FUNCIONARIO",
            "ORDEM_SERVICO",
            "PAGAMENTO",
            "PAGAMENTO_ITEM",
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
    
    def nome_cliente(self, id_cliente): # Mostra o nome do cliente usando o ID como filtro
        query_sql = '''
            SELECT NOME_CLIENTE FROM CLIENTE WHERE ID_CLIENTE = ?
        '''
        self.cursor.execute(query_sql, (id_cliente,))
        return self.cursor.fetchone()
    
    def funcionarios(self, id_funcionario): # Mostra o nome do funcionário usando o ID como filtro
        query_sql = '''
            SELECT NOME_FUNCIONARIO FROM FUNCIONARIO WHERE ID_FUNCIONARIO = ?
        '''
        self.cursor.execute(query_sql, (id_funcionario,))
        return self.cursor.fetchone()
    
    def client_info(self, id_cliente=None):
        query_sql = '''
                 SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, CLIENTE.TELEFONE,
                     ENDERECO.LOGRADOURO, ENDERECO.NUMERO, ENDERECO.CIDADE, ENDERECO.UF, ENDERECO.CEP
                 FROM CLIENTE
                 INNER JOIN ENDERECO ON ENDERECO.ID_ENDERECO = CLIENTE.ID_ENDERECO
        '''
        params = []

        if id_cliente is not None:
            query_sql += ' WHERE ID_CLIENTE = ?'
            params.append(id_cliente)

        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        if saida:
            return print(tabulate(saida, headers=['ID', 'NOME', 'CPF', 'TELEFONE', 'LOGRADOURO', 'NÚMERO', 'CIDADE', 'UF', 'CEP'], tablefmt='grid', stralign='left'))
        else:
            return print(f'{colors.RED}Erro! Dados não foram encontrados{colors.END}')
    
    def cliente_ult_os(self, id_cliente=None, apenas_ultimo=False):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, VEICULO.MARCA, ORDEM_SERVICO.DESC_REPARO
            FROM CLIENTE
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_CLIENTE = CLIENTE.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO 
                    '''
        adc_client = 'WHERE CLIENTE.ID_CLIENTE = ?'
        adc_ultimo = ' ORDER BY substr(ORDEM_SERVICO.DATA_INICIO, 7, 4) DESC, substr(ORDEM_SERVICO.DATA_INICIO, 4, 2) DESC, substr(ORDEM_SERVICO.DATA_INICIO, 1, 2) DESC LIMIT 1'
        
        if id_cliente is not None:
            query_sql += adc_client
            params.append(id_cliente)

        if apenas_ultimo:
            query_sql += adc_ultimo
            self.cursor.execute(query_sql, params)
            registro = self.cursor.fetchone()
            if registro is None:
                return print(f'{colors.RED}Erro! Dados não foram encontrados{colors.END}')
            return print(tabulate([registro], headers=['CLIENTE', 'MARCA DO VEÍCULO', 'DESCRIÇÃO DO REPARO'], tablefmt='grid', stralign='left'))
        else:
            self.cursor.execute(query_sql, params)
            registros = self.cursor.fetchall()
            if not registros:
                return print(f'{colors.RED}Erro! Dados não foram encontrados{colors.END}')
            return print(tabulate(registros, headers=['CLIENTE', 'MARCA DO VEÍCULO', 'DESCRIÇÃO DO REPARO'], tablefmt='grid', stralign='left'))
    
    def info_pagamento(self, id_cliente=None, sitaucao=None):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, PAGAMENTO.VALOR_TOTAL, 
            PAGAMENTO.METODO_PAGAMENTO, PAGAMENTO.STATUS_PAGAMENTO
            FROM CLIENTE
            INNER JOIN PAGAMENTO ON PAGAMENTO.ID_CLIENTE = CLIENTE.ID_CLIENTE 
            
            '''
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if sitaucao is not None:
            conditions.append('PAGAMENTO.STATUS_PAGAMENTO = ?')
            params.append(sitaucao)

        if conditions:
            query_sql += '\nWHERE ' + ' AND '.join(conditions)

        self.cursor.execute(query_sql, params)
        return print(tabulate(self.cursor.fetchall(), headers=['CLIENTE', 'CPF', 'VALOR (R$)', 'MÉTODO DE PAGAMENTO', 'STATUS'], tablefmt='grid', stralign='left'))

    def consulta_carro(self, placa=None, modelo=None, marca=None):
        query_sql = 'SELECT ID_VEICULO, PLACA, MODELO, MARCA, CHASSIS FROM VEICULO'
        params = []
        conditions = []
        
        if placa is not None:
            conditions.append('PLACA = ?')
            params.append(placa)
        
        if modelo is not None:
            conditions.append('MODELO = ?')
            params.append(modelo)
        
        if marca is not None:
            conditions.append('MARCA = ?')
            params.append(marca)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            return print(tabulate(saida, headers=['ID', 'PLACA', 'MODELO', 'MARCA', 'CHASSIS'], tablefmt='grid', stralign='left') + '\n')
        else:
            return print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')
    
    def consulta_produto(self, categoria=None):
        query_sql = 'SELECT PRODUTO.ID_PRODUTO, PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, PRODUTO.QUANTIDADE, PRODUTO.PRECO_UNITARIO, PRODUTO.PRECO_TOTAL FROM PRODUTO INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA '
        params = []
        
        if categoria is not None:
            query_sql += 'WHERE CATEGORIA_PRODUTO.NOME_CATEGORIA = ?'
            params.append(categoria)

        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_fornecedor(self, nome=None, cnpj=None):
        query_sql = 'SELECT * FROM FORNECEDOR '
        params = []
        conditions = []
        
        if nome is not None:
            conditions.append('NOME_FORNECEDOR = ?')
            params.append(nome)
        
        if cnpj is not None:
            conditions.append('CNPJ = ?')
            params.append(cnpj)

        if conditions:
            query_sql += 'WHERE ' + ' AND '.join(conditions)
        
        self.cursor.execute(query_sql, tuple(params))
        return self.cursor.fetchall()
    
    def consulta_funcionarios(self, id_funcionario=None, nome=None, id_departamento=None, id_especialidade=None):
        base_query = (
            'SELECT FUNCIONARIO.ID_FUNCIONARIO, FUNCIONARIO.NOME_FUNCIONARIO, DEPARTAMENTO.NOME_DEPARTAMENTO, ESPECIALIDADE.NOME_ESPECIALIDADE, '
            'DATA_ADMISSAO, DATA_DEMISSAO, ENDERECO.LOGRADOURO, ENDERECO.NUMERO, ENDERECO.CIDADE, ENDERECO.UF, ENDERECO.CEP  '
            'FROM FUNCIONARIO '
            'INNER JOIN DEPARTAMENTO ON FUNCIONARIO.ID_DEPARTAMENTO = DEPARTAMENTO.ID_DEPARTAMENTO '
            'INNER JOIN ESPECIALIDADE ON FUNCIONARIO.ID_ESPECIALIDADE = ESPECIALIDADE.ID_ESPECIALIDADE '
            'INNER JOIN ENDERECO ON FUNCIONARIO.ID_ENDERECO = ENDERECO.ID_ENDERECO'
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

            headers = ['ID', 'NOME', 'DEPARTAMENTO', 'ESPECIALIDADE', 'DATA ADMISSÃO', 'DATA DEMISSÃO', 'LOGRADOURO', 'NÚMERO', 'CIDADE', 'UF', 'CEP']

            def all(self):
                return print(tabulate(self._build_and_exec(), headers=self.headers, tablefmt='grid', stralign='left'))

            def ativos(self):
                return print(tabulate(self._build_and_exec('DATA_DEMISSAO IS NULL'), headers=self.headers, tablefmt='grid', stralign='left'))

            def demitidos(self):
                return print(tabulate(self._build_and_exec('DATA_DEMISSAO IS NOT NULL'), headers=self.headers, tablefmt='grid', stralign='left'))

            def by_id(self, idv):
                registro = self._build_and_exec('FUNCIONARIO.ID_FUNCIONARIO = ?', [idv], single=True)
                return print(tabulate([registro] if registro else [], headers=self.headers, tablefmt='grid', stralign='left'))

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
    
    def consulta_estoque_min(self, nome_produto=None, abaixo=False, acima=False, no_limite=False):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, ESTOQUE.QTDE_ESTOQUE, ESTOQUE.QTDE_MIN,
                CASE
                    WHEN QTDE_ESTOQUE = QTDE_MIN THEN 'Limite mínimo atingido'
                    WHEN QTDE_ESTOQUE < QTDE_MIN THEN 'Abaixo do limite'
                    ELSE 'Acima do limite mínimo'
                END AS STATUS
            FROM ESTOQUE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = ESTOQUE.ID_PRODUTO 
        '''
        params = []
        conditions = []
        filtros_status = []
        
        if nome_produto is not None:
            conditions.append('PRODUTO.NOME_PRODUTO = ?')
            params.append(nome_produto)
        
        if abaixo:
            filtros_status.append('ESTOQUE.QTDE_ESTOQUE < ESTOQUE.QTDE_MIN')

        if acima:
            filtros_status.append('ESTOQUE.QTDE_ESTOQUE > ESTOQUE.QTDE_MIN')

        if no_limite:
            filtros_status.append('ESTOQUE.QTDE_ESTOQUE = ESTOQUE.QTDE_MIN')

        if filtros_status:
            conditions.append(f'({" OR ".join(filtros_status)})')

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)
        
        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            return print(tabulate(saida, headers=['PRODUTO', 'QTDE EM ESTOQUE', 'QTDE ESTOQUE MIN.', 'STATUS'], tablefmt='grid', stralign='left'))
        else:
            return print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')
    
    def consulta_salario_bruto(self, salario):
        query_sql = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FOLHA_PAGAMENTO.SALARIO_BRUTO, FUNCIONARIO.DATA_ADMISSAO, FUNCIONARIO.DATA_DEMISSAO
            FROM FUNCIONARIO
            INNER JOIN FOLHA_PAGAMENTO ON FOLHA_PAGAMENTO.ID_FUNCIONARIO = FUNCIONARIO.ID_FUNCIONARIO WHERE FOLHA_PAGAMENTO.SALARIO_BRUTO > ?
        '''

        self.cursor.execute(query_sql, (salario,))
        return self.cursor.fetchall()

    def status_agenciamento(self, status=None, id_cliente=None):
        query_sql = f'''
            SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, VEICULO.MODELO, AGENCIAMENTO_VEICULO.DATA_INICIO_AGENCIAMENTO, AGENCIAMENTO_VEICULO.STATUS
            FROM AGENCIAMENTO_VEICULO
            INNER JOIN VEICULO ON AGENCIAMENTO_VEICULO.ID_VEICULO = VEICULO.ID_VEICULO
            INNER JOIN CLIENTE ON AGENCIAMENTO_VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE
        '''
        params = []
        conditions = []
        if status is not None:
            conditions.append('AGENCIAMENTO_VEICULO.STATUS = ?')
            params.append(status)
            
        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)
        
        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        if saida:
            return print(tabulate(saida, headers=['ID', 'CLIENTE', 'MODELO DO VEÍCULO', 'DATA DE AGEN.', 'STATUS AGEN.'], tablefmt='grid', stralign='left'))
        else:
            return print(f'{colors.RED}Erro! Dados não foram encontrados{colors.END}')
    
    def clientes_e_veiculos(self, id_cliente=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, CLIENTE.TELEFONE, VEICULO.MODELO, VEICULO.MARCA
            FROM CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE 
        '''
        params = []
        conditions = []
        
        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)
        
        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            return print(tabulate(saida, headers=['CLIENTE', 'CPF', 'TELEFONE', 'MODELO DO VEICULO', 'MARCA DO VEICULO'], tablefmt='grid', stralign='left'))
        else:
            print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')

    def produtos_e_fornecedores(self, nome_produto=None, id_produto=None):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, FORNECEDOR.CNPJ, PRODUTO.QUANTIDADE, PRODUTO.PRECO_UNITARIO, PRODUTO.PRECO_TOTAL
            FROM FORNECEDOR
            INNER JOIN PRODUTO ON PRODUTO.ID_FORNECEDOR = FORNECEDOR.ID_FORNECEDOR
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
        '''
        params = []
        conditions = []
        
        if nome_produto is not None:
            conditions.append('PRODUTO.NOME_PRODUTO = ?')
            params.append(nome_produto)

        if id_produto is not None:
            conditions.append('PRODUTO.ID_PRODUTO = ?')
            params.append(id_produto)

        if conditions:
            query_sql += 'WHERE ' + ' AND '.join(conditions)
    
        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            print(tabulate(saida, headers=['PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'CNPJ', 'QUANTIDADE', 'PREÇO UNITÁRIO (R$)', 'VALOR TOTAL (R$)'], tablefmt='grid', stralign='left') + '\n')
        else:
            print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')  
    
    def funcionario_dep_esp(self):
        query = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FUNCIONARIO.DATA_ADMISSAO, DEPARTAMENTO.NOME_DEPARTAMENTO, ESPECIALIDADE.NOME_ESPECIALIDADE
            FROM FUNCIONARIO
            INNER JOIN DEPARTAMENTO ON DEPARTAMENTO.ID_DEPARTAMENTO = FUNCIONARIO.ID_DEPARTAMENTO
            INNER JOIN ESPECIALIDADE ON ESPECIALIDADE.ID_ESPECIALIDADE = FUNCIONARIO.ID_ESPECIALIDADE;
        '''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def os_cliente_veiculo(self, id_cliente=None, cpf_cliente=None, modelo=None, marca=None, data_inicio=None, data_conclusao=None, tempo_reparo=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, VEICULO.MODELO, VEICULO.MARCA, ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.DATA_CONCLUSAO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO, ORDEM_SERVICO.VALOR_TOTAL
            FROM ORDEM_SERVICO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ORDEM_SERVICO.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO
        '''
        params = []
        conditions = []
        
        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if cpf_cliente is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf_cliente)

        if modelo is not None:
            conditions.append('VEICULO.MODELO = ?')
            params.append(modelo)

        if marca is not None:
            conditions.append('VEICULO.MARCA = ?')
            params.append(marca)

        if data_inicio is not None:
            conditions.append('ORDEM_SERVICO.DATA_INICIO = ?')
            params.append(data_inicio)

        if data_conclusao is not None:
            conditions.append('ORDEM_SERVICO.DATA_CONCLUSAO = ?')
            params.append(data_conclusao)

        if tempo_reparo is not None:
            conditions.append('ORDEM_SERVICO.TEMPO_TOTAL_REPARO = ?')
            params.append(tempo_reparo)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            tabela = tabulate(saida, headers=['CLIENTE', 'CPF', 'MODELO DO VEÍCULO', 'MARCA DO VEÍCULO', 'DATA INÍCIO', 'DATA CONCLUSÃO', 'TEMPO DE REPARO (DIAS)', 'VALOR TOTAL (R$)'],
                            tablefmt='grid', stralign='left')
            return print(f'{tabela}\n')
        else:
            return print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')

    def pagamento_os(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO, ORDEM_SERVICO.DESC_REPARO, PAGAMENTO.METODO_PAGAMENTO, ORDEM_SERVICO.VALOR_TOTAL
            FROM PAGAMENTO
            INNER JOIN PAGAMENTO_ITEM ON PAGAMENTO_ITEM.ID_PAGAMENTO = PAGAMENTO.ID_PAGAMENTO
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_OS = PAGAMENTO_ITEM.ID_OS
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE
            WHERE PAGAMENTO_ITEM.ID_OS IS NOT NULL;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def pagamento_produto(self):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, FORNECEDOR.CNPJ,
            PAGAMENTO.DATA_PAGAMENTO, PRODUTO.PRECO_UNITARIO, PAGAMENTO_ITEM.QUANTIDADE, PAGAMENTO_ITEM.VALOR_ITEM, PAGAMENTO.STATUS_PAGAMENTO, PAGAMENTO.METODO_PAGAMENTO
            FROM PAGAMENTO
            INNER JOIN PAGAMENTO_ITEM ON PAGAMENTO_ITEM.ID_PAGAMENTO = PAGAMENTO.ID_PAGAMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = PAGAMENTO_ITEM.ID_PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = PRODUTO.ID_FORNECEDOR
            WHERE PAGAMENTO_ITEM.ID_PRODUTO IS NOT NULL;
        '''
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()
    
    def atendimento_ao_cliente(self, id_funcionario=None, id_cliente=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, ATENDIMENTO.DATA_ATENDIMENTO, 
            FUNCIONARIO.NOME_FUNCIONARIO
            FROM ATENDIMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ATENDIMENTO.ID_CLIENTE
            INNER JOIN FUNCIONARIO ON FUNCIONARIO.ID_FUNCIONARIO = ATENDIMENTO.ID_FUNCIONARIO
        '''
        params = []
        conditions = []
        
        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)
        
        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)
        
        self.cursor.execute(query_sql, tuple(params))
        saida = self.cursor.fetchall()
        
        if saida:
            return print(tabulate(saida, headers=['CLIENTE', 'CPF', 'DATA DE ATENDIMENTO', 'FUNCIONÁRIO'], tablefmt='grid', stralign='left'))
        else:
            return print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')
    
    def produtos_estoque(self):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, ESTOQUE.QTDE_ESTOQUE, ESTOQUE.VALIDADE_DIAS
            FROM ESTOQUE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = ESTOQUE.ID_PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = PRODUTO.ID_FORNECEDOR;
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
            ORDER BY QTDE_VEICULOS DESC
        '''
        
        self.cursor.execute(query_sql)
        saida = self.cursor.fetchall()
        
        if saida:
            return print(tabulate(saida, headers=['CLIENTE', 'CPF', 'QTDE VEICULOS'], tablefmt='grid', stralign='left'))
        else:
            print(f'{colors.LIGHT_RED}Erro! Dados não foram encontrados{colors.END}')

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
        query_sql = '''
            SELECT PAGAMENTO.METODO_PAGAMENTO,
            COUNT (*) AS TOTAL_PAGAMENTOS,
            SUM (VALOR_TOTAL) AS VALOR_TOTAL_AGRUPADO
            FROM PAGAMENTO
            WHERE METODO_PAGAMENTO = ?
            GROUP BY METODO_PAGAMENTO
            ORDER BY VALOR_TOTAL_AGRUPADO DESC;
        '''
        self.cursor.execute(query_sql, (metodo,))
        return self.cursor.fetchall()
    
    def total_produtos_categoria(self, categoria):
        query_sql = f'''
            SELECT CATEGORIA_PRODUTO.NOME_CATEGORIA,
            COUNT (*) AS TOTAL_PRODUTOS,
            SUM (PRODUTO.PRECO_UNITARIO) AS PRECO_TOTAL
            FROM PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            WHERE CATEGORIA_PRODUTO.NOME_CATEGORIA = ?
            GROUP BY CATEGORIA_PRODUTO.NOME_CATEGORIA;
        '''
        self.cursor.execute(query_sql, (categoria,))
        return self.cursor.fetchall()
