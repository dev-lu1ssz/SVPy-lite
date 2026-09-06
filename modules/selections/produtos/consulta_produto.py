def consulta_produto(selectdata, categoria=None, nome_produto=None, preco_unitario=None, id_produto=None):
        query_sql = '''SELECT PRODUTO.ID_PRODUTO, PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, PRODUTO.QUANTIDADE,
        PRODUTO.PRECO_UNITARIO, PRODUTO.PRECO_TOTAL
        FROM PRODUTO
        INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA'''
        params = []
        conditions = []

        if categoria is not None:
            conditions.append('CATEGORIA_PRODUTO.NOME_CATEGORIA = ?')
            params.append(categoria)

        if nome_produto is not None:
            conditions.append('PRODUTO.NOME_PRODUTO LIKE ?')
            params.append(f'%{nome_produto}%')

        if preco_unitario is not None:
            conditions.append('PRODUTO.PRECO_UNITARIO = ?')
            params.append(preco_unitario)

        if id_produto is not None:
            conditions.append('PRODUTO.ID_PRODUTO = ?')
            params.append(id_produto)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['ID', 'PRODUTO', 'CATEGORIA', 'QTDE', 'PREÇO UNITÁRIO', 'PREÇO TOTAL']
        )
