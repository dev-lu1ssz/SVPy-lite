def cr_pagamento(selectdata, data_pagamento=None, referencia=None,
                     numero_parcela=None, data_vencimento=None, status=None):
        query_sql = '''
            SELECT PAGAMENTO.DATA_PAGAMENTO, PAGAMENTO.VALOR_TOTAL, PAGAMENTO.PARCELAS, PAGAMENTO.REFERENCIA,
            CONTA_RECEBER.NUMERO_PARCELA, CONTA_RECEBER.VALOR_PARCELA, CONTA_RECEBER.DATA_VENCIMENTO_RECEBER,
            CONTA_RECEBER.STATUS
            FROM CONTA_RECEBER
            INNER JOIN PAGAMENTO ON PAGAMENTO.ID_PAGAMENTO = CONTA_RECEBER.ID_PAGAMENTO
        '''
        params = []
        conditions = []

        if data_pagamento is not None:
            conditions.append('PAGAMENTO.DATA_PAGAMENTO = ?')
            params.append(data_pagamento)

        if referencia is not None:
            conditions.append('PAGAMENTO.REFERENCIA LIKE ?')
            params.append(f'%{referencia}%')

        if numero_parcela is not None:
            conditions.append('CONTA_RECEBER.NUMERO_PARCELA = ?')
            params.append(numero_parcela)

        if data_vencimento is not None:
            conditions.append('CONTA_RECEBER.DATA_VENCIMENTO_RECEBER = ?')
            params.append(data_vencimento)

        if status is not None:
            conditions.append('CONTA_RECEBER.STATUS = ?')
            params.append(status)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['DATA DO PAGAMENTO', 'VALOR TOTAL', 'PARCELAS', 'REFERÊNCIA',
             'NÚMERO DA PARCELA', 'VALOR DA PARCELA', 'VENCIMENTO', 'STATUS']
        )
