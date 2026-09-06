def info_pagamento(selectdata, id_cliente=None, cpf=None, metodo_pagamento=None, sitaucao=None):
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

        if cpf is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf)

        if metodo_pagamento is not None:
            conditions.append('PAGAMENTO.METODO_PAGAMENTO = ?')
            params.append(metodo_pagamento)

        if sitaucao is not None:
            conditions.append('PAGAMENTO.STATUS_PAGAMENTO = ?')
            params.append(sitaucao)

        if conditions:
            query_sql += '\nWHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['CLIENTE', 'CPF', 'VALOR (R$)', 'MÉTODO DE PAGAMENTO', 'STATUS']
        )
