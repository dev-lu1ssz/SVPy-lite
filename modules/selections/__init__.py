import sqlite3

from modules.selections.clientes.atendimento_ao_cliente import atendimento_ao_cliente
from modules.selections.clientes.os_pcliente import os_pcliente
from modules.selections.clientes.clientes_e_veiculos import clientes_e_veiculos
from modules.selections.clientes.client_info import client_info
from modules.selections.clientes.cliente_ult_os import cliente_ult_os
from modules.selections.clientes.info_pagamento import info_pagamento
from modules.selections.clientes.nome_cliente import nome_cliente
from modules.selections.clientes.qtde_veiculo_cliente import qtde_veiculo_cliente
from modules.selections.financas.total_pagamentos_metodo import total_pagamentos_metodo
from modules.selections.financas.pagamento_os import pagamento_os
from modules.selections.financas.pagamento_produto import pagamento_produto
from modules.selections.financas.cr_pagamento import cr_pagamento
from modules.selections.financas.status_agenciamento import status_agenciamento
from modules.selections.funcionarios.funcionario_dep_esp import funcionario_dep_esp
from modules.selections.funcionarios.funcionarios import funcionarios
from modules.selections.funcionarios.consulta_salario_bruto import consulta_salario_bruto
from modules.selections.funcionarios.dados_fp import dados_fp
from modules.selections.funcionarios.consulta_funcionarios import consulta_funcionarios
from modules.selections.veiculos.consulta_carro import consulta_carro
from modules.selections.veiculos.os_cliente_veiculo import os_cliente_veiculo
from modules.selections.produtos.consulta_estoque_min import consulta_estoque_min
from modules.selections.produtos.produtos_estoque import produtos_estoque
from modules.selections.produtos.consulta_fornecedor import consulta_fornecedor
from modules.selections.produtos.consulta_produto import consulta_produto
from modules.selections.produtos.produtos_e_fornecedores import produtos_e_fornecedores
from modules.selections.produtos.total_produtos_categoria import total_produtos_categoria


class Selectdata:
    def __init__(self, conexao: sqlite3.Connection):
        self.conexao = conexao
        self.cursor = conexao.cursor()

    def _mostrar_tabela(self, registros, headers, mensagem_erro='Erro! Dados não foram encontrados'):
        from tabulate import tabulate
        from modules.colors import Colors

        colors = Colors()
        if registros:
            print(tabulate(registros, headers=headers, tablefmt='grid', stralign='left'))
            return registros
        print(f'{colors.RED}{mensagem_erro}{colors.END}')
        return []

    def atendimento_ao_cliente(self, id_funcionario=None, id_cliente=None):
        return atendimento_ao_cliente(self, id_funcionario, id_cliente)

    def os_pcliente(self, nome_cliente=None, cpf_cliente=None, id_cliente=None, qtde_os=None):
        return os_pcliente(self, nome_cliente, cpf_cliente, id_cliente, qtde_os)

    def clientes_e_veiculos(self, id_cliente=None, nome_cliente=None):
        return clientes_e_veiculos(self, id_cliente, nome_cliente)

    def client_info(self, id_cliente=None, cpf=None, logradouro=None, numero=None, cidade=None, uf=None, cep=None):
        return client_info(self, id_cliente, cpf, logradouro, numero, cidade, uf, cep)

    def cliente_ult_os(self, id_cliente=None, apenas_ultimo=False):
        return cliente_ult_os(self, id_cliente, apenas_ultimo)

    def info_pagamento(self, id_cliente=None, cpf=None, metodo_pagamento=None, sitaucao=None):
        return info_pagamento(self, id_cliente, cpf, metodo_pagamento, sitaucao)

    def nome_cliente(self, id_cliente):
        return nome_cliente(self, id_cliente)

    def qtde_veiculo_cliente(self, nome_cliente=None, cpf_cliente=None, id_cliente=None, qtde_veiculos=None):
        return qtde_veiculo_cliente(self, nome_cliente, cpf_cliente, id_cliente, qtde_veiculos)

    def total_pagamentos_metodo(self, metodo):
        return total_pagamentos_metodo(self, metodo)

    def pagamento_os(self, id_cliente=None, cpf_cliente=None, data_inicio=None, descricao=None, metodo_pagamento=None, status_pagamento=None, data_pagamento=None):
        return pagamento_os(self, id_cliente, cpf_cliente, data_inicio, descricao, metodo_pagamento, status_pagamento, data_pagamento)

    def pagamento_produto(self, id_cliente=None, cpf_cliente=None, nome_produto=None, categoria=None, fornecedor=None, data_pagamento=None, metodo_pagamento=None, status_pagamento=None):
        return pagamento_produto(self, id_cliente, cpf_cliente, nome_produto, categoria, fornecedor, data_pagamento, metodo_pagamento, status_pagamento)

    def cr_pagamento(self, data_pagamento=None, referencia=None, numero_parcela=None, data_vencimento=None, status=None):
        return cr_pagamento(self, data_pagamento, referencia, numero_parcela, data_vencimento, status)

    def status_agenciamento(self, status=None, id_cliente=None, nome_cliente=None, modelo_veiculo=None):
        return status_agenciamento(self, status, id_cliente, nome_cliente, modelo_veiculo)

    def funcionario_dep_esp(self, id_funcionario=None, nome_funcionario=None, nome_departamento=None, nome_especialidade=None, data_admissao=None, data_demissao=None):
        return funcionario_dep_esp(self, id_funcionario, nome_funcionario, nome_departamento, nome_especialidade, data_admissao, data_demissao)

    def funcionarios(self, id_funcionario):
        return funcionarios(self, id_funcionario)

    def consulta_salario_bruto(self, salario, id_funcionario=None, nome_funcionario=None, data_admissao=None, data_demissao=None):
        return consulta_salario_bruto(self, salario, id_funcionario, nome_funcionario, data_admissao, data_demissao)

    def dados_fp(self, id_funcionario=None, nome_funcionario=None, mes_referencia=None, status_pagamento=None, situacao=None):
        return dados_fp(self, id_funcionario, nome_funcionario, mes_referencia, status_pagamento, situacao)

    def consulta_funcionarios(self, id_funcionario=None, nome_funcionario=None, cidade=None, uf=None, cep=None, logradouro=None, data_admissao=None, data_demissao=None, nome_departamento=None, nome_especialidade=None):
        return consulta_funcionarios(self, id_funcionario, nome_funcionario, cidade, uf, cep, logradouro, data_admissao, data_demissao, nome_departamento, nome_especialidade)

    def consulta_carro(self, placa=None, modelo=None, marca=None):
        return consulta_carro(self, placa, modelo, marca)

    def os_cliente_veiculo(self, id_cliente=None, cpf_cliente=None, modelo=None, marca=None, data_inicio=None, data_conclusao=None, tempo_reparo=None):
        return os_cliente_veiculo(self, id_cliente, cpf_cliente, modelo, marca, data_inicio, data_conclusao, tempo_reparo)

    def consulta_estoque_min(self, nome_produto=None, abaixo=False, acima=False, no_limite=False):
        return consulta_estoque_min(self, nome_produto, abaixo, acima, no_limite)

    def produtos_estoque(self, nome_produto=None, categoria=None, fornecedor=None):
        return produtos_estoque(self, nome_produto, categoria, fornecedor)

    def consulta_fornecedor(self, nome=None, cnpj=None):
        return consulta_fornecedor(self, nome, cnpj)

    def consulta_produto(self, categoria=None, nome_produto=None, preco_unitario=None, id_produto=None):
        return consulta_produto(self, categoria, nome_produto, preco_unitario, id_produto)

    def produtos_e_fornecedores(self, nome_produto=None, id_produto=None):
        return produtos_e_fornecedores(self, nome_produto, id_produto)

    def total_produtos_categoria(self, categoria=None):
        return total_produtos_categoria(self, categoria)
