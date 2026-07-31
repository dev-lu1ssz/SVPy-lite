import sqlite3

def main():
    conexao = None
    cursor = None
    
    try:
        conexao = sqlite3.connect('C:\\Users\\luis.oliveira\\Documents\\Luissz\\python_sqlite\\speed_veiculos_sqlite\\database\\SV-Py_lite_2.db')
        cursor = conexao.cursor()

        class Indata:
            def __init__(self):
                pass
            
            def pessoa(self, nome_cliente, endereco_cliente, telefone, cpf_cliente):
                self.nome_client = nome_cliente
                self.endereco_cliente = endereco_cliente
                self.telefone = telefone
                self.cpf_cliente = cpf_cliente
            
            def funcionario(self, nome_funcionario, salario, data_admissao, data_demissao):
                self.nome_funcionario = nome_funcionario
                self.salario = salario
                self.data_admissao = data_admissao
                self.data_demissao = data_demissao

    except sqlite3.DatabaseError as err:
        print('Erro: ' + err.args)
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

if __name__ == '__main__':
    main()