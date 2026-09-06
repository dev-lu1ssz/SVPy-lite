def client_info(selectdata, id_cliente=None, cpf=None, logradouro=None, numero=None,
                    cidade=None, uf=None, cep=None):
        query_sql = '''
                 SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, CLIENTE.TELEFONE,
                     ENDERECO.LOGRADOURO, ENDERECO.NUMERO, ENDERECO.CIDADE, ENDERECO.UF, ENDERECO.CEP
                 FROM CLIENTE
                 INNER JOIN ENDERECO ON ENDERECO.ID_ENDERECO = CLIENTE.ID_ENDERECO
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if cpf is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf)

        if logradouro is not None:
            conditions.append('ENDERECO.LOGRADOURO LIKE ?')
            params.append(f'%{logradouro}%')

        if numero is not None:
            conditions.append('ENDERECO.NUMERO = ?')
            params.append(numero)

        if cidade is not None:
            conditions.append('ENDERECO.CIDADE LIKE ?')
            params.append(f'%{cidade}%')

        if uf is not None:
            conditions.append('ENDERECO.UF = ?')
            params.append(uf.upper())

        if cep is not None:
            conditions.append('ENDERECO.CEP = ?')
            params.append(cep)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['ID', 'NOME', 'CPF', 'TELEFONE', 'LOGRADOURO', 'NÚMERO', 'CIDADE', 'UF', 'CEP']
        )
