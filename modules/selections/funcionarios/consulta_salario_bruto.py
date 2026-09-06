def consulta_salario_bruto(selectdata, salario, id_funcionario=None, nome_funcionario=None,
                               data_admissao=None, data_demissao=None):
        query_sql = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FOLHA_PAGAMENTO.SALARIO_BRUTO, FUNCIONARIO.DATA_ADMISSAO, FUNCIONARIO.DATA_DEMISSAO
            FROM FUNCIONARIO
            INNER JOIN FOLHA_PAGAMENTO ON FOLHA_PAGAMENTO.ID_FUNCIONARIO = FUNCIONARIO.ID_FUNCIONARIO
        '''
        params = [salario]
        conditions = ['FOLHA_PAGAMENTO.SALARIO_BRUTO > ?']

        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if nome_funcionario is not None:
            conditions.append('FUNCIONARIO.NOME_FUNCIONARIO LIKE ?')
            params.append(f'%{nome_funcionario}%')

        if data_admissao is not None:
            conditions.append('FUNCIONARIO.DATA_ADMISSAO = ?')
            params.append(data_admissao)

        if data_demissao is not None:
            conditions.append('FUNCIONARIO.DATA_DEMISSAO = ?')
            params.append(data_demissao)

        query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['FUNCIONÁRIO', 'SALÁRIO BRUTO', 'DATA ADMISSÃO', 'DATA DEMISSÃO']
        )
