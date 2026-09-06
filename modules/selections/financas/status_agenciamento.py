def status_agenciamento(selectdata, status=None, id_cliente=None, nome_cliente=None, modelo_veiculo=None):
        query_sql = f'''
            SELECT CLIENTE.ID_CLIENTE, CLIENTE.NOME_CLIENTE, VEICULO.MODELO, AGENCIAMENTO_VEICULO.DATA_INICIO_AGENCIAMENTO, AGENCIAMENTO_VEICULO.STATUS
            FROM AGENCIAMENTO_VEICULO
            INNER JOIN VEICULO ON AGENCIAMENTO_VEICULO.ID_VEICULO = VEICULO.ID_VEICULO
            INNER JOIN CLIENTE ON AGENCIAMENTO_VEICULO.ID_CLIENTE = CLIENTE.ID_CLIENTE
        '''
        params = []
        conditions = []
        if status is not None:
            conditions.append('AGENCIAMENTO_VEICULO.STATUS = ?')
            params.append(status)

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if nome_cliente is not None:
            conditions.append('CLIENTE.NOME_CLIENTE LIKE ?')
            params.append(f'%{nome_cliente}%')

        if modelo_veiculo is not None:
            conditions.append('VEICULO.MODELO LIKE ?')
            params.append(f'%{modelo_veiculo}%')

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['ID', 'CLIENTE', 'MODELO DO VEÍCULO', 'DATA DE AGEN.', 'STATUS AGEN.']
        )
