import sqlite3

class Selectdata:
    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = conexao.cursor()
        
    def cliente_ult_os(self, id_cliente=None, apenas_ultimo=False):
        params = []
        query_sql = '''
            SELECT CLIENTE.NOME_CLIENTE, VEICULO.MARCA, ORDEM_SERVICO.DESC_REPARO
                            FROM CLIENTE
                            INNER JOIN ORDEM_SERVICO ON ORDEM_SERVICO.ID_CLIENTE = CLIENTE.ID_CLIENTE
                            INNER JOIN VEICULO ON VEICULO.ID_VEICULO = ORDEM_SERVICO.ID_VEICULO 
                    '''
        adc_client = 'WHERE CLIENTE.ID_CLIENTE = ?'
        adc_ultimo = 'ORDER BY ORDEM_SERVICO.DATA_INICIO LIMIT 1'
        
        if id_cliente:
            query_sql += adc_client
            params.append(id_cliente)

        if apenas_ultimo:
            query_sql += adc_ultimo
            self.cursor.execute(query_sql, params)
            return self.cursor.fetchone()
        else:
            self.cursor.execute(query_sql, params)
            return self.cursor.fetchall()