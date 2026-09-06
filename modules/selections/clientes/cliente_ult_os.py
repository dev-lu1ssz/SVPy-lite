def cliente_ult_os(selectdata, id_cliente=None, apenas_ultimo=False):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, VEICULO.MARCA, ORDEM_SERVICO.DESC_REPARO
            FROM CLIENTE
            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_CLIENTE = CLIENTE.ID_CLIENTE
            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO
                    '''
        adc_client = 'WHERE CLIENTE.ID_CLIENTE = ?'
        adc_ultimo = ' ORDER BY substr(ORDEM_SERVICO.DATA_INICIO, 7, 4) DESC, substr(ORDEM_SERVICO.DATA_INICIO, 4, 2) DESC, substr(ORDEM_SERVICO.DATA_INICIO, 1, 2) DESC LIMIT 1'

        if id_cliente is not None:
            query_sql += adc_client
            params.append(id_cliente)

        if apenas_ultimo:
            query_sql += adc_ultimo
            selectdata.cursor.execute(query_sql, params)
            registro = selectdata.cursor.fetchone()
            return selectdata._mostrar_tabela(
                [registro] if registro is not None else [],
                ['CLIENTE', 'MARCA DO VEÍCULO', 'DESCRIÇÃO DO REPARO']
            )
        else:
            selectdata.cursor.execute(query_sql, params)
            registros = selectdata.cursor.fetchall()
            return selectdata._mostrar_tabela(
                registros,
                ['CLIENTE', 'MARCA DO VEÍCULO', 'DESCRIÇÃO DO REPARO']
            )
