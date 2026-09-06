def nome_cliente(selectdata, id_cliente): # Mostra o nome do cliente usando o ID como filtro
        query_sql = '''
            SELECT NOME_CLIENTE FROM CLIENTE WHERE ID_CLIENTE = ?
        '''
        selectdata.cursor.execute(query_sql, (id_cliente,))
        return selectdata.cursor.fetchone()
