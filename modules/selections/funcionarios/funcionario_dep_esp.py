def funcionario_dep_esp(selectdata, id_funcionario=None, nome_funcionario=None,
                             nome_departamento=None, nome_especialidade=None,
                             data_admissao=None, data_demissao=None):
        query = '''
            SELECT FUNCIONARIO.NOME_FUNCIONARIO, FUNCIONARIO.DATA_ADMISSAO, DEPARTAMENTO.NOME_DEPARTAMENTO, ESPECIALIDADE.NOME_ESPECIALIDADE
            FROM FUNCIONARIO
            INNER JOIN DEPARTAMENTO ON DEPARTAMENTO.ID_DEPARTAMENTO = FUNCIONARIO.ID_DEPARTAMENTO
            INNER JOIN ESPECIALIDADE ON ESPECIALIDADE.ID_ESPECIALIDADE = FUNCIONARIO.ID_ESPECIALIDADE
        '''
        params = []
        conditions = []

        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if nome_funcionario is not None:
            conditions.append('FUNCIONARIO.NOME_FUNCIONARIO LIKE ?')
            params.append(f'%{nome_funcionario}%')

        if nome_departamento is not None:
            conditions.append('DEPARTAMENTO.NOME_DEPARTAMENTO LIKE ?')
            params.append(f'%{nome_departamento}%')

        if nome_especialidade is not None:
            conditions.append('ESPECIALIDADE.NOME_ESPECIALIDADE LIKE ?')
            params.append(f'%{nome_especialidade}%')

        if data_admissao is not None:
            conditions.append('FUNCIONARIO.DATA_ADMISSAO = ?')
            params.append(data_admissao)

        if data_demissao is not None:
            conditions.append('FUNCIONARIO.DATA_DEMISSAO = ?')
            params.append(data_demissao)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query, tuple(params))
        registros = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(
            registros,
            ['FUNCIONÁRIO', 'DATA ADMISSÃO', 'DEPARTAMENTO', 'ESPECIALIDADE']
        )
