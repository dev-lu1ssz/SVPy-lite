def pagamento_produto(selectdata, id_cliente=None, cpf_cliente=None, nome_produto=None,
                          categoria=None, fornecedor=None, data_pagamento=None,
                          metodo_pagamento=None, status_pagamento=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, FORNECEDOR.CNPJ,
            PAGAMENTO.DATA_PAGAMENTO, PRODUTO.PRECO_UNITARIO, PAGAMENTO_ITEM.QUANTIDADE, PAGAMENTO_ITEM.VALOR_ITEM, PAGAMENTO.STATUS_PAGAMENTO, PAGAMENTO.METODO_PAGAMENTO
            FROM PAGAMENTO
            INNER JOIN PAGAMENTO_ITEM ON PAGAMENTO_ITEM.ID_PAGAMENTO = PAGAMENTO.ID_PAGAMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = PAGAMENTO.ID_CLIENTE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = PAGAMENTO_ITEM.ID_PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = PRODUTO.ID_FORNECEDOR
            WHERE PAGAMENTO_ITEM.ID_PRODUTO IS NOT NULL
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if cpf_cliente is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf_cliente)

        if nome_produto is not None:
            conditions.append('PRODUTO.NOME_PRODUTO LIKE ?')
            params.append(f'%{nome_produto}%')

        if categoria is not None:
            conditions.append('CATEGORIA_PRODUTO.NOME_CATEGORIA LIKE ?')
            params.append(f'%{categoria}%')

        if fornecedor is not None:
            conditions.append('FORNECEDOR.NOME_FORNECEDOR LIKE ?')
            params.append(f'%{fornecedor}%')

        if data_pagamento is not None:
            conditions.append('PAGAMENTO.DATA_PAGAMENTO = ?')
            params.append(data_pagamento)

        if metodo_pagamento is not None:
            conditions.append('PAGAMENTO.METODO_PAGAMENTO = ?')
            params.append(metodo_pagamento)

        if status_pagamento is not None:
            conditions.append('PAGAMENTO.STATUS_PAGAMENTO = ?')
            params.append(status_pagamento)

        if conditions:
            query_sql += ' AND ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['CLIENTE', 'CPF', 'PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'CNPJ',
             'DATA DO PAGAMENTO', 'PREÇO UNITÁRIO', 'QUANTIDADE', 'VALOR TOTAL',
             'STATUS', 'MÉTODO']
        )
