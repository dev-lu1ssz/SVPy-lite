def dados_fp(selectdata, id_funcionario=None, nome_funcionario=None,
                 mes_referencia=None, status_pagamento=None, situacao=None):
        query_sql = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FUNCIONARIO.DATA_ADMISSAO,
            FOLHA_PAGAMENTO.MES_REFERENCIA, FOLHA_PAGAMENTO.SALARIO_BRUTO, FOLHA_PAGAMENTO.DESCONTOS,
            FOLHA_PAGAMENTO.SALARIO_LIQUIDO, FOLHA_PAGAMENTO.STATUS_PAGAMENTO,
            CASE
                WHEN FUNCIONARIO.DATA_DEMISSAO IS NULL THEN 'Ativo na empresa'
                ELSE 'Desligado'
            END AS FUN_ON_OFF
            FROM FOLHA_PAGAMENTO
            INNER JOIN FUNCIONARIO ON FUNCIONARIO.ID_FUNCIONARIO = FOLHA_PAGAMENTO.ID_FUNCIONARIO
        '''
        params = []
        conditions = []

        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if nome_funcionario is not None:
            conditions.append('FUNCIONARIO.NOME_FUNCIONARIO LIKE ?')
            params.append(f'%{nome_funcionario}%')

        if mes_referencia is not None:
            conditions.append('FOLHA_PAGAMENTO.MES_REFERENCIA = ?')
            params.append(mes_referencia)

        if status_pagamento is not None:
            conditions.append('FOLHA_PAGAMENTO.STATUS_PAGAMENTO = ?')
            params.append(status_pagamento)

        if situacao is not None:
            conditions.append(
                "CASE WHEN FUNCIONARIO.DATA_DEMISSAO IS NULL THEN 'Ativo na empresa' ELSE 'Desligado' END = ?"
            )
            params.append(situacao)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['FUNCIONÁRIO', 'DATA ADMISSÃO', 'MÊS', 'SALÁRIO BRUTO', 'DESCONTOS',
             'SALÁRIO LÍQUIDO', 'STATUS', 'SITUAÇÃO']
        )
