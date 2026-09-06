def consulta_carro(selectdata, placa=None, modelo=None, marca=None):
        query_sql = 'SELECT ID_VEICULO, PLACA, MODELO, MARCA, CHASSIS FROM VEICULO'
        params = []
        conditions = []

        if placa is not None:
            conditions.append('PLACA = ?')
            params.append(placa)

        if modelo is not None:
            conditions.append('MODELO = ?')
            params.append(modelo)

        if marca is not None:
            conditions.append('MARCA = ?')
            params.append(marca)

        if conditions:
            query_sql += ' WHERE ' + ' AND '.join(conditions)

        selectdata.cursor.execute(query_sql, tuple(params))
        saida = selectdata.cursor.fetchall()
        return selectdata._mostrar_tabela(saida, ['ID', 'PLACA', 'MODELO', 'MARCA', 'CHASSIS'])
