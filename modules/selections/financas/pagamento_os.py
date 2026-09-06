def pagamento_os(selectdata, id_cliente=None, cpf_cliente=None, data_inicio=None,
                     descricao=None, metodo_pagamento=None, status_pagamento=None,
                     data_pagamento=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE,
                   ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO,
                   ORDEM_SERVICO.DESC_REPARO, PAGAMENTO.DATA_PAGAMENTO,
                   PAGAMENTO.METODO_PAGAMENTO, PAGAMENTO.STATUS_PAGAMENTO,
                   ORDEM_SERVICO.VALOR_TOTAL
            FROM PAGAMENTO
            INNER JOIN PAGAMENTO_ITEM ON PAGAMENTO_ITEM.ID_PAGAMENTO = PAGAMENTO.ID_PAGAMENTO
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_OS = PAGAMENTO_ITEM.ID_OS
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE
            WHERE PAGAMENTO_ITEM.ID_OS IS NOT NULL
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if cpf_cliente is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf_cliente)

        if data_inicio is not None:
            conditions.append('ORDEM_SERVICO.DATA_INICIO = ?')
            params.append(data_inicio)

        if descricao is not None:
            conditions.append('ORDEM_SERVICO.DESC_REPARO LIKE ?')
            params.append(f'%{descricao}%')

        if metodo_pagamento is not None:
            conditions.append('PAGAMENTO.METODO_PAGAMENTO = ?')
            params.append(metodo_pagamento)

        if status_pagamento is not None:
            conditions.append('PAGAMENTO.STATUS_PAGAMENTO = ?')
            params.append(status_pagamento)

        if data_pagamento is not None:
            conditions.append('PAGAMENTO.DATA_PAGAMENTO = ?')
            params.append(data_pagamento)

        if conditions:
            query_sql += ' AND ' + ' AND '.join(conditions)

        query_sql += ' ORDER BY ORDEM_SERVICO.DATA_INICIO DESC'
        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['CLIENTE', 'CPF', 'DATA DA OS', 'TEMPO DE REPARO (DIAS)',
             'DESCRIÇÃO', 'DATA DO PAGAMENTO', 'MÉTODO', 'STATUS',
             'VALOR DA OS (R$)']
        )
