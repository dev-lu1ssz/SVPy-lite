from tabulate import tabulate

def menu_clientes():
    lista_consulta_clientes = [('clientes', 'Traz todas as informações sobre os clientes cadastrados'), 
                                ('ultimo_os', 'Traz informações sobre os clientes e suas ordens de serviço'),
                                ('pagamentos', 'Traz informações sobre clientes que realizaram pagamentos'),
                                ('agenciamentos', 'Traz informações sobre clientes que solicitaram um agenciamento'),
                                ('atendimentos', 'Traz informações sobre o atendimento ao cliente'),
                                ('veiculos', 'Traz informações sobre a quantidade de veículos que cada cliente possui'),
                                ('menu', 'Mostra novamente o menu de comandos'),
                                ('back', 'Volta para o menu de categorias')]
    
    tabela = tabulate(lista_consulta_clientes, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_veiculos():
    lista_consulta_veiculos = [('veiculos', 'Traz informações sobre os veículos que estão cadastrados no sistema'),
                               ('ordem_servico', 'Traz informações sobre ordens de serviços realizadas'),
                               ('menu', 'Mostra novamente o menu de comandos'),
                               ('back', 'Volta para o menu de categorias')]
    tabela = tabulate(lista_consulta_veiculos, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_funcionarios():
    lista_consulta_funcionarios = [('funcionarios', 'Mostra informações de funcionários registrados no banco de dados (ativos e desligados)'),
                                   ('especialidades', 'Mostra informações apenas de funcionários que possuem especialidades mecânicas'),
                                   ('pagamentos', 'Mostra informações referente a folha de pagamento dos funcionários')]
    tabela = tabulate(lista_consulta_funcionarios, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def menu_produtos():
    lista_consulta_produtos = [('produtos', 'Mostra informações sobre produtos e fornecedores'),
                                ('minimo', 'Consulta o estoque para saber qual produto atingiu a quantidade mínima'),
                                ('compras', 'Mostra informações úteis sobre produtos e a quantidade gasta na compra (R$)'),
                                ('estoque', 'Mostra quais são os produtos que tem no estoque'),
                                ('categoria', 'Mostra a quantidade de produtos separados por categorias')]
    
    tabela = tabulate(lista_consulta_produtos, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

def categorias():
    lista_categorias = [('clientes', 'Consultas para trazer as principais informações sobre os cliente'),
                                ('veiculos', 'Consultas para trazer as principais informações sobre os veículos dos clientes'),
                                ('funcionarios', 'Consultas para trazer as principais informações sobre os funcionários da empresa'),
                                ('produtos', 'Consultas para trazer as principais informações sobre os produtos')]
    tabela = tabulate(lista_categorias, headers=['Categoria', 'Descrição'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')