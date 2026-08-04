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
            
            def cliente(self, nome_cliente, endereco_cliente, telefone, cpf_cliente):
                self.nome_client = nome_cliente
                self.endereco_cliente = endereco_cliente
                self.telefone = telefone
                self.cpf_cliente = cpf_cliente
            
            def funcionario(self, nome_funcionario, salario, data_admissao, data_demissao):
                self.nome_funcionario = nome_funcionario
                self.salario = salario
                self.data_admissao = data_admissao
                self.data_demissao = data_demissao
                
            def departamento(self, nome_departamento):
                self.nome_departamento = nome_departamento
            
            def especialidade(self, nome_especialidade):
                self.nome_especialidade = nome_especialidade
                
            def feedback(self, id_cliente, avaliacao, descricao):
                self.id_cliente = id_cliente
                self.avaliacao = avaliacao
                self.descricao = descricao
            
            def fornecedor(self, nome_fornecedor, cnpj, telefone, endereco_fornecedor):
                self.nome_fornecedor = nome_fornecedor
                self.cnpj = cnpj
                self.telefone = telefone
                self.endereco = endereco_fornecedor

            def ordem_servico(self, data_inicio, data_conclusao, agendamento, valor_total, desc_reparo):
                self.data_inicio = data_inicio
                self.data_conclusao = data_conclusao
                self.agendamento = agendamento
                self.valor_total = valor_total
                self.desc_reparo = desc_reparo
                
            def pagamento(self, metodo_pagamento, parcelas, data_pagamento, valor_pagamento, status_pagamento, referencia):
                self.metodo_pagamento = metodo_pagamento
                self.parcelas = parcelas
                self.data_pagamento = data_pagamento
                self.valor_pagamento = valor_pagamento
                self.status_pagamento = status_pagamento
                self.referencia = referencia
            
            def produto(self, nome_produto, categoria, quantidade, preco, validade):
                self.nome_produto = nome_produto
                self.categoria = categoria
                self.quantidade = quantidade
                self.preco = preco
                self.validade = validade
            
            def veiculo(self, placa, modelo, marca, chassis):
                self.placa = placa
                self.modelo = modelo
                self.marca = marca
                self.chassis = chassis

    except sqlite3.DatabaseError as err:
        print('Erro: ' + err.args)
    
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

if __name__ == '__main__':
    main()