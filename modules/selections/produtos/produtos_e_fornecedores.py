def produtos_e_fornecedores(selectdata, nome_produto=None, id_produto=None):
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

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'CNPJ', 'QUANTIDADE',
             'PREÇO UNITÁRIO (R$)', 'VALOR TOTAL (R$)']
        )
