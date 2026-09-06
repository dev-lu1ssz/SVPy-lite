def os_cliente_veiculo(selectdata, id_cliente=None, cpf_cliente=None, modelo=None, marca=None, data_inicio=None, data_conclusao=None, tempo_reparo=None):
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, CLIENTE.CPF_CLIENTE, VEICULO.MODELO, VEICULO.MARCA, ORDEM_SERVICO.DATA_INICIO, ORDEM_SERVICO.DATA_CONCLUSAO, ORDEM_SERVICO.TEMPO_TOTAL_REPARO, ORDEM_SERVICO.VALOR_TOTAL
            FROM ORDEM_SERVICO
            INNER JOIN CLIENTE ON CLIENTE.ID_CLIENTE = ORDEM_SERVICO.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO
        '''
        params = []
        conditions = []

        if id_cliente is not None:
            conditions.append('CLIENTE.ID_CLIENTE = ?')
            params.append(id_cliente)

        if cpf_cliente is not None:
            conditions.append('CLIENTE.CPF_CLIENTE = ?')
            params.append(cpf_cliente)

        if modelo is not None:
            conditions.append('VEICULO.MODELO = ?')
            params.append(modelo)

        if marca is not None:
            conditions.append('VEICULO.MARCA = ?')
            params.append(marca)

        if data_inicio is not None:
            conditions.append('ORDEM_SERVICO.DATA_INICIO = ?')
            params.append(data_inicio)

        if data_conclusao is not None:
            conditions.append('ORDEM_SERVICO.DATA_CONCLUSAO = ?')
            params.append(data_conclusao)

        if tempo_reparo is not None:
            conditions.append('ORDEM_SERVICO.TEMPO_TOTAL_REPARO = ?')
            params.append(tempo_reparo)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            saida,
            ['CLIENTE', 'CPF', 'MODELO DO VEÍCULO', 'MARCA DO VEÍCULO',
             'DATA INÍCIO', 'DATA CONCLUSÃO', 'TEMPO DE REPARO (DIAS)',
             'VALOR TOTAL (R$)']
        )
