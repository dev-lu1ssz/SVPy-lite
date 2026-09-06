def atendimento_ao_cliente(selectdata, id_funcionario=None, id_cliente=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, ATENDIMENTO.DATA_ATENDIMENTO,
            FUNCIONARIO.NOME_FUNCIONARIO
            FROM ATENDIMENTO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ATENDIMENTO.ID_CLIENTE
            INNER JOIN FUNCIONARIO ON FUNCIONARIO.ID_FUNCIONARIO = ATENDIMENTO.ID_FUNCIONARIO
        '''
        params = []
        conditions = []

        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['CLIENTE', 'CPF', 'DATA DE ATENDIMENTO', 'FUNCIONÁRIO']
        )
