from tabulate import tabulate

def menu_clientes():
    lista_consulta_clientes = [('info_cliente', 'Traz todas as informações sobre os clientes cadastrados'), 
                                ('cliente_ult_os', 'Traz informações sobre os clientes e suas ordens de serviço'),
                                ('info_pagamento', 'Traz informações sobre clientes que realizaram pagamentos'),
                                ('cliente_agenciamento', 'Traz informações sobre clientes que solicitaram um agenciamento'),
                                ('atendimento', 'Traz informações sobre o atendimento ao cliente'),
                                ('qtde_veiculos', 'Traz informações sobre a quantidade de veículos que cada cliente possui'),
                                ('menu', 'Mostra novamente o menu de comandos'),
                                ('back', 'Volta para o menu principal do script')]
    
    tabela = tabulate(lista_consulta_clientes, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_veiculos():
    lista_consulta_veiculos = [('info_veiculo', 'Traz informações sobre os veículos que estão cadastrados no sistema'),
                               ('ordem_servico', 'Traz informações sobre ordens de serviços realizadas'),
                               ('menu', 'Mostra novamente o menu de comandos'),
                               ('back', 'Volta para o menu principal do script')]
    tabela = tabulate(lista_consulta_veiculos, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_funcionarios():
    lista_consulta_funcionarios = [('funcionarios', 'Mostra informações de funcionários registrados no banco de dados (ativos e desligados)'),
                                   ('func_especialidades', 'Mostra informações apenas de funcionários que possuem especialidades mecânicas'),
                                   ('folha_pagamento', 'Mostra informações referente a folha de pagamento dos funcionários')]
    tabela = tabulate(lista_consulta_funcionarios, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_produtos():
    lista_consulta_produtos = [('produtos', 'Mostra informações sobre produtos e fornecedores'),
                               ('estoque_min', 'Consulta o estoque para saber qual produto atingiu a quantidade mínima'),
                               ('compra_produto', 'Mostra informações úteis sobre produtos e a quantidade gasta na compra (R$)'),
                               ('produtos_estoque', 'Mostra quais são os produtos que tem no estoque'),
                               ('categoria', 'Mostra a quantidade de produtos separados por categorias'),
                               ('fornecedor', 'Consulta informações da lista de fornecedores no banco de dados')]
    tabela = tabulate(lista_consulta_produtos, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='center')
    return print(f'\n{tabela}\n')

def categorias():
    lista_categorias = [('clientes', 'Consultas para trazer as principais informações sobre os cliente'),
                                ('veiculos', 'Consultas para trazer as principais informações sobre os veículos dos clientes'),
                                ('funcionarios', 'Consultas para trazer as principais informações sobre os funcionários da empresa'),
                                ('produtos', 'Consultas para trazer as principais informações sobre os produtos')]
    tabela = tabulate(lista_categorias, headers=['Categoria', 'Descrição'], tablefmt='grid')
    return print(f'\n{tabela}\n')