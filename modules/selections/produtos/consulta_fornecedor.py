def consulta_fornecedor(selectdata, nome=None, cnpj=None):
        query_sql = 'SELECT * FROM FORNECEDOR '
        params = []
        conditions = []

        if nome is not None:
            conditions.append('NOME_FORNECEDOR LIKE ?')
            params.append(f'%{nome}%')

        if cnpj is not None:
            conditions.append('CNPJ = ?')
            params.append(cnpj)

        if conditions:
            query_sql += 'WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(registros, ['ID', 'NOME', 'CNPJ', 'TELEFONE', 'ID ENDEREÇO'])
