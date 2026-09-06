def produtos_estoque(selectdata, nome_produto=None, categoria=None, fornecedor=None):
        query_sql = '''
            SELECT PRODUTO.NOME_PRODUTO, CATEGORIA_PRODUTO.NOME_CATEGORIA, FORNECEDOR.NOME_FORNECEDOR, ESTOQUE.QTDE_ESTOQUE, ESTOQUE.VALIDADE_DIAS
            FROM ESTOQUE
            INNER JOIN PRODUTO ON PRODUTO.ID_PRODUTO = ESTOQUE.ID_PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            INNER JOIN FORNECEDOR ON FORNECEDOR.ID_FORNECEDOR = PRODUTO.ID_FORNECEDOR
        '''
        params = []
        conditions = []

        if nome_produto is not None:
            conditions.append('PRODUTO.NOME_PRODUTO LIKE ?')
            params.append(f'%{nome_produto}%')

        if categoria is not None:
            conditions.append('CATEGORIA_PRODUTO.NOME_CATEGORIA LIKE ?')
            params.append(f'%{categoria}%')

        if fornecedor is not None:
            conditions.append('FORNECEDOR.NOME_FORNECEDOR LIKE ?')
            params.append(f'%{fornecedor}%')

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'QTDE EM ESTOQUE', 'VALIDADE (DIAS)']
        )
