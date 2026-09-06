def funcionarios(selectdata, id_funcionario): # Mostra o nome do funcionário usando o ID como filtro
        query_sql = '''
            SELECT NOME_FUNCIONARIO FROM FUNCIONARIO WHERE ID_FUNCIONARIO = ?
        '''
        selectdata.cursor.execute(query_sql, (id_funcionario,))
        return selectdata.cursor.fetchone()
