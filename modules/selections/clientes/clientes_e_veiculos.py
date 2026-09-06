def clientes_e_veiculos(selectdata, id_cliente=None, nome_cliente=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, CLIENTE.TELEFONE, VEICULO.MODELO, VEICULO.MARCA
            FROM CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if nome_cliente is not None:
            conditions.append('CLIENTE.NOME_CLIENTE LIKE ?')
            params.append(f'%{nome_cliente}%')

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['CLIENTE', 'CPF', 'TELEFONE', 'MODELO DO VEICULO', 'MARCA DO VEICULO']
        )
