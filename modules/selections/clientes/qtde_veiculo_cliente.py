def qtde_veiculo_cliente(selectdata, nome_cliente=None, cpf_cliente=None, id_cliente=None, qtde_veiculos=None):
        query_sql = '''
            SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE,
            COUNT(VEICULO.ID_VEICULO) AS QTDE_VEICULOS
            FROM CLIENTE
            LEFT JOIN VEICULO ON CLIENTE.ID_CLIENTE = VEICULO.ID_CLIENTE
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if nome_cliente is not None:
            conditions.append('CLIENTE.NOME_CLIENTE LIKE ?')
            params.append(f'%{nome_cliente}%')

        if cpf_cliente is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf_cliente)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        query_sql += ' GROUP BY CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE'

        if qtde_veiculos is not None:
            query_sql += ' HAVING COUNT(VEICULO.ID_VEICULO) = ?'
            params.append(qtde_veiculos)

        query_sql += ' ORDER BY QTDE_VEICULOS DESC'

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['REGISTRO', 'CLIENTE', 'CPF', 'QTDE VEICULOS']
        )
