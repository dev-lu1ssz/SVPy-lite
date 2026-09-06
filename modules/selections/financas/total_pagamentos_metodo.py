def total_pagamentos_metodo(selectdata, metodo):
        query_sql = '''
            SELECT PAGAMENTO.METODO_PAGAMENTO,
            COUNT (*) AS TOTAL_PAGAMENTOS
            FROM PAGAMENTO
            WHERE METODO_PAGAMENTO = ?
            GROUP BY METODO_PAGAMENTO
            ORDER BY TOTAL_PAGAMENTOS DESC;
        '''
        selectdata.cursor.execute(query_sql, (metodo,))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['MÉTODO DE PAGAMENTO', 'TOTAL DE PAGAMENTOS']
        )
