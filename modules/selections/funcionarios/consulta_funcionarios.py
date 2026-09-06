def consulta_funcionarios(selectdata, id_funcionario=None, nome_funcionario=None, cidade=None, uf=None, cep=None, logradouro=None, data_admissao=None, data_demissao=None, nome_departamento=None, nome_especialidade=None):
        base_query = (
            'SELECT FUNCIONARIO.ID_FUNCIONARIO, FUNCIONARIO.NOME_FUNCIONARIO, DEPARTAMENTO.NOME_DEPARTAMENTO, ESPECIALIDADE.NOME_ESPECIALIDADE, '
            'FUNCIONARIO.DATA_ADMISSAO, FUNCIONARIO.DATA_DEMISSAO, ENDERECO.LOGRADOURO, ENDERECO.NUMERO, ENDERECO.CIDADE, ENDERECO.UF, ENDERECO.CEP '
            'FROM FUNCIONARIO '
            'INNER JOIN DEPARTAMENTO ON FUNCIONARIO.ID_DEPARTAMENTO = DEPARTAMENTO.ID_DEPARTAMENTO '
            'INNER JOIN ESPECIALIDADE ON FUNCIONARIO.ID_ESPECIALIDADE = ESPECIALIDADE.ID_ESPECIALIDADE '
            'INNER JOIN ENDERECO ON FUNCIONARIO.ID_ENDERECO = ENDERECO.ID_ENDERECO'
        )
        params = []
        conditions = []

        if id_funcionario is not None:
            conditions.append('FUNCIONARIO.ID_FUNCIONARIO = ?')
            params.append(id_funcionario)

        if nome_funcionario is not None:
            conditions.append('FUNCIONARIO.NOME_FUNCIONARIO LIKE ?')
            params.append(f'%{nome_funcionario}%')

        if cidade is not None:
            conditions.append('ENDERECO.CIDADE LIKE ?')
            params.append(f'%{cidade}%')

        if uf is not None:
            conditions.append('ENDERECO.UF = ?')
            params.append(uf.upper())

        if cep is not None:
            conditions.append('ENDERECO.CEP = ?')
            params.append(cep)

        if logradouro is not None:
            conditions.append('ENDERECO.LOGRADOURO LIKE ?')
            params.append(f'%{logradouro}%')

        if data_admissao is not None:
            conditions.append('FUNCIONARIO.DATA_ADMISSAO = ?')
            params.append(data_admissao)

        if data_demissao is not None:
            conditions.append('FUNCIONARIO.DATA_DEMISSAO = ?')
            params.append(data_demissao)

        if nome_departamento is not None:
            conditions.append('DEPARTAMENTO.NOME_DEPARTAMENTO LIKE ?')
            params.append(f'%{nome_departamento}%')

        if nome_especialidade is not None:
            conditions.append('ESPECIALIDADE.NOME_ESPECIALIDADE LIKE ?')
            params.append(f'%{nome_especialidade}%')

        class FuncQuery:
            def __init__(self, cursor, base_query, conditions, params, mostrar_tabela):
                self.cursor = cursor
                self.base_query = base_query
                self.base_conditions = list(conditions)
                self.base_params = list(params)
                self._mostrar_tabela = mostrar_tabela

            def _build_and_exec(self, extra_condition=None, extra_params=None, single=False):
                q = self.base_query
                conds = list(self.base_conditions)
                params = list(self.base_params)

                if conds:
                    q += '\nWHERE ' + ' AND '.join(conds)

                if extra_condition:
                    if conds:
                        q += ' AND ' + extra_condition
                    else:
                        q += '\nWHERE ' + extra_condition

                if extra_params:
                    params.extend(extra_params)

                self.cursor.execute(q, tuple(params))
                return self.cursor.fetchone() if single else self.cursor.fetchall()

            headers = ['ID', 'NOME', 'DEPARTAMENTO', 'ESPECIALIDADE', 'DATA ADMISSÃO', 'DATA DEMISSÃO', 'LOGRADOURO', 'NÚMERO', 'CIDADE', 'UF', 'CEP']

            def all(self):
                registros = self._build_and_exec()
                return self._mostrar_tabela(registros, self.headers)

            def ativos(self):
                registros = self._build_and_exec('DATA_DEMISSAO IS NULL')
                return self._mostrar_tabela(registros, self.headers)

            def demitidos(self):
                registros = self._build_and_exec('DATA_DEMISSAO IS NOT NULL')
                return self._mostrar_tabela(registros, self.headers)

            def by_id(self, idv):
                registro = self._build_and_exec('FUNCIONARIO.ID_FUNCIONARIO = ?', [idv], single=True)
                return self._mostrar_tabela(
                    [registro] if registro is not None else [],
                    self.headers
                )

        return FuncQuery(selectdata.cursor, base_query, conditions, params, selectdata._mostrar_tabela)
