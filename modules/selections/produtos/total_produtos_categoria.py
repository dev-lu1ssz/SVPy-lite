def total_produtos_categoria(selectdata, categoria=None):
        query_sql = '''
            SELECT CATEGORIA_PRODUTO.NOME_CATEGORIA,
            COUNT (*) AS TOTAL_PRODUTOS,
            SUM (PRODUTO.PRECO_UNITARIO) AS PRECO_TOTAL
            FROM PRODUTO
            INNER JOIN CATEGORIA_PRODUTO ON CATEGORIA_PRODUTO.ID_CATEGORIA = PRODUTO.ID_CATEGORIA
            GROUP BY CATEGORIA_PRODUTO.NOME_CATEGORIA;
        '''
        params = []
        if categoria is not None:
            query_sql = query_sql.replace(
                'GROUP BY CATEGORIA_PRODUTO.NOME_CATEGORIA;',
                'WHERE CATEGORIA_PRODUTO.NOME_CATEGORIA = ?\n'
                'GROUP BY CATEGORIA_PRODUTO.NOME_CATEGORIA;'
            )
            params.append(categoria)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(registros, ['CATEGORIA', 'TOTAL DE PRODUTOS', 'PREÇO TOTAL'])
