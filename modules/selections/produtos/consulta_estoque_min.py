def consulta_estoque_min(selectdata, nome_produto=None, abaixo=False, acima=False, no_limite=False):
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

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['PRODUTO', 'QTDE EM ESTOQUE', 'QTDE ESTOQUE MIN.', 'STATUS']
        )
