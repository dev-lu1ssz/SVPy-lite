import modules.database_creator as database_creator
import modules.insertions as insertions
from modules.selections import Selectdata
import modules.menu as menu
import os
from tabulate import tabulate
import sqlite3
import time
from modules.colors import Colors

def writer(a):
    for i in a:
        print(i, flush=True, end='')
        time.sleep(0.02)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'SV-Py_lite_updated.db')
color = Colors()

if not DB_PATH:
    print(f'{color.RED}Base de dados não encontrada. Criando base de dados SV-Py{color.END}')
    database_creator.main()
    
    if not DB_PATH:
        print(f'{color.RED}Ocorreu algum erro ao tentar criar a base de dados no diretório "database"{color.END}')
        exit()

try:
    opcao = 0
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute('PRAGMA foreign_keys = on')
    select = Selectdata(conexao)

    while opcao != 2:
        try:
            print(f'\n{color.LIGHT_GREEN}Seja bem vindo ao seu Sistema de Gerenciamento de Banco de Dados da Speed-Veiculos montado com SQLite!{color.END}\n')
            print('Escolha uma das opções abaixo:')
            print('''
                [1] - Ver o menu de comandos de consultas
                [2] - Sair
            ''')

            opcao = int(input(f'{color.NEGATIVE}SVPy-lite >{color.END} '))

            if opcao not in (1, 2):
                print(f'{color.LIGHT_RED}\nOpção inválida! Digite uma opção entre 1 e 2.{color.END}')
            
            elif opcao == 1:
                writer(f'{color.NEGATIVE}\nEscolha uma categoria para as consultas:{color.END}\n')
                menu.categorias()
                
                categoria = str(input(f'{color.NEGATIVE}SVPy-lite >{color.END} '))
                categorias_disponiveis = ['clientes', 'veiculos', 'funcionarios', 'produtos']
                
                if categoria.lower() not in categorias_disponiveis:
                    print(f'\n{color.LIGHT_RED}Escolha uma categoria que esteja disponível na lista{color.END}\n')
                
                elif categoria.lower() == 'clientes':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos de clientes{color.END}\n')
                    time.sleep(1)
                    menu.menu_clientes()
                    
                    while True:
                        print('\nSelecione uma das opções - Digite "back" para voltar ao menu principal')
                        comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
                        lista_comandos = ['info_cliente', 'cliente_ult_os', 'info_pagamento', 'cliente_agenciamento', 'atendimento', 'qtde_veiculos', 'back', 'menu']
                        
                        if comando.lower() not in lista_comandos:
                            print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')
                        
                        if comando.lower() == 'back':
                            break
                        
                        elif comando.lower() == 'menu':
                            menu.menu_clientes()
                        
                        elif comando.lower() == 'info_cliente':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                                while True:
                                    registro = input('\nDigite o número de registro do cliente (ID) > ')
                                    nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                    writer(f'{color.LIGHT_GREEN}\nConsulta: Cadastro do(a) cliente "{nome_cliente}" ..........{color.END}\n\n')
                                    select.client_info(eval(registro))
                                    break
                            else:
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de todos os clientes............{color.END}\n\n')
                                select.client_info()
                        
                        elif comando.lower() == 'cliente_ult_os':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                while True:
                                    print('\n' + tabulate([('id', 'Filtrar usuário pelo número de registro'), 
                                                    ('ultimo', 'Trazer apenas a última OS registrada'), 
                                                    ('combinado', 'Combina os dois filtros de consulta')], 
                                                headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                    
                                    opcao_filtro = str(input('\nEsolha o filtro que deseja utilizar > '))

                                    if opcao_filtro.lower() == 'id':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                        writer(f'\nConsulta: Todas OS solicitadas pelo(a) cliente "{nome_cliente}"............\n\n')
                                        select.cliente_ult_os(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro.lower() == 'ultimo':
                                        writer('\nConsulta: Última OS registrada no sistema............\n\n')
                                        select.cliente_ult_os(apenas_ultimo=True)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'combinado':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                        writer(f'\nConsulta: Última OS solicitada pelo(a) cliente "{nome_cliente}"............\n\n')
                                        select.cliente_ult_os(id_cliente=eval(registro), apenas_ultimo=True)
                                        break

                            elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                                writer('\nConsulta o banco de dados............\n\n')
                                select.cliente_ult_os()
                        
                        elif comando.lower() == 'info_pagamento':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                    while True:
                                        print('\n' + tabulate([('id', 'Filtrar usuário pelo número de registro'), 
                                                        ('situação', 'Filtra pela situação do pagamento (Pendente, Pago)')], 
                                                        headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                        
                                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                        
                                        if opcao_filtro.lower() == 'id':
                                            registro = input('Digite o número de registro do cliente (ID) > ')
                                            nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                            writer(f'\nConsulta: Todos os pagamentos realizados pelo cliente "{nome_cliente}"............\n\n')
                                            select.info_pagamento(id_cliente=eval(registro))
                                            break
                                        
                                        elif opcao_filtro.lower() in ('situação', 'situacao'):
                                            situacao = str(input('Deseja filtrar qual situação ? [Pendente/Pago]: '))
                                            if situacao.lower() in ('pendente', 'pago'):
                                                writer(f'\nConsulta: Todos os pagamentos com a situação "{situacao}"............\n\n')
                                                select.info_pagamento(sitaucao=situacao)
                                                break
                                            else:
                                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Pago){color.END}')
                            
                            elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                                writer('\nConsultando o banco de dados............\n\n')
                                select.info_pagamento()
                        
                        elif comando.lower() == 'cliente_agenciamento':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                while True:
                                    print('\n' + tabulate([('id', 'Filtrar pelo número de registro do cliente'),
                                                            ('status', 'Filtrar pelo status do agenciamento (Pendente/Vendido)')],
                                                            headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                    opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    if opcao_filtro.lower() == 'id':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                        writer(f'\nConsulta: Todo agenciamento solicitado pelo(a) cliente "{nome_cliente}"............\n\n')
                                        select.status_agenciamento(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro.lower() == 'status':
                                        status = str(input('Deseja filtrar qual situação ? [Pendente/Vendido]: '))
                                        if status.lower() in ('pendente', 'pago'):
                                            writer(f'\nConsulta: Todos os agenciamento que possuem o status "{status}"............\n\n')
                                            select.status_agenciamento(status=status)
                                            break
                                        else:
                                            print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Vendido){color.END}')
                                    
                            elif quest_filtro.lower() in ('não', 'nao', 'nn', 'n', 'no'):
                                writer('\nConsulta: Todos os agenciamentos que foram solicitados............\n\n')
                                select.status_agenciamento()

                        elif comando.lower() == 'atendimento':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                                while True:
                                    print('\n' + tabulate([('id_cliente', 'Filtrar pelo número de registro do cliente'),
                                                            ('id_funcionario', 'Filtrar pelo número de registro do funcionário')], 
                                                        headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                    opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    
                                    if opcao_filtro == 'id_cliente':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                        writer(f'\nConsulta: Todos os atendimentos realizados para o cliente "{nome_cliente}"............\n\n')
                                        select.atendimento_ao_cliente(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro == 'id_funcionario':
                                        registro = input('Digite o número de registro do funcionário (ID) > ')
                                        nome_funcionario, = select.funcionarios(eval(registro[0].strip()))
                                        writer(f'{color.LIGHT_GREEN}\nConsulta: Todos atendimentos realizados pelo funcionário "{nome_funcionario}" ..........{color.END}\n\n')
                                        select.atendimento_ao_cliente(id_funcionario=eval(registro))
                                        break
                                    
                                    else:
                                        print(f'{color.LIGHT_RED}Opção de filtro inválida, escolha um dos filtros disponíveis{color.END}')
                            elif quest_filtro.lower() in ('não', 'nao', 'n', 'no'):
                                writer(f'{color.LIGHT_GREEN}\nConsulta: Todos os atendimentos realizados............\n\n{color.END}')
                                select.atendimento_ao_cliente()

                        elif comando.lower() == 'qtde_veiculos':
                            writer(f'{color.LIGHT_GREEN}\nConsultando o banco de dados..........{color.END}\n\n')
                            select.qtde_veiculo_cliente()

                elif categoria.lower() == 'veiculos':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos de veículos{color.END}')
                    time.sleep(1)
                    menu.menu_veiculos()
                    
                    while True:
                        print('Selecione uma das opções - Digite "back" para voltar ao menu principal')
                        comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
                        lista_comandos = ['info_veiculo', 'ordem_servico', 'back', 'menu']
                        if comando.lower() not in lista_comandos:
                            print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')
                        
                        if comando.lower() == 'back':
                            break
                        
                        elif comando.lower() == 'menu':
                            menu.menu_veiculos()
                            
                        elif comando.lower() == 'info_veiculo':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                                while True:
                                    print(f'\n{tabulate([("placa", "Utiliza a placa do veículo como filtro"),
                                            ("marca", "Retorna todos os veículos de uma marca específica"),
                                            ("modelo", "Retorna todos os veículos de um modelo específico")], headers=["Filtro", "Descrição"], tablefmt="grid")}\n')
                                    
                                    opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    lista_filtros_veiculos = ['placa', 'marca', 'modelo']
                                    
                                    if opcao_filtro not in lista_filtros_veiculos:
                                        print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')
                                    
                                    if opcao_filtro.lower() == 'placa':
                                        placa = input('\nDigite a placa do veículo > ').upper()
                                        writer(f'{color.LIGHT_GREEN}\nConsulta: Veiculo com a placa "{placa}"..........{color.END}\n\n')
                                        select.consulta_carro(placa=placa)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'marca':
                                        marca = str(input('\nDigite a marca do veículo > ')).capitalize()
                                        writer(f'\nConsulta: Todos os veículos da marca "{marca}"..........{color.END}\n\n')
                                        select.consulta_carro(marca=marca)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'modelo':
                                        modelo = str(input('\nDigite o modelo do veículo > ')).capitalize()
                                        writer(f'\nConsulta: Todos os veículos do modelo "{modelo}"..........{color.END}\n\n')
                                        select.consulta_carro(modelo=modelo)
                                        break
                                
                            elif quest_filtro.lower() in ('nao', 'nn', 'n', 'no'):
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os veículos registrados no sistema..........{color.END}\n\n')
                                select.consulta_carro()
                            
                        elif comando.lower() == 'ordem_servico':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                                while True:
                                    print('\n' + tabulate([('id_cliente', 'Filtrar OS solicitadas por clientes usando o número de registro'),
                                                            ('cpf', 'Filtrar OS solicitadas por clientes usando o CPF'),
                                                            ('modelo', 'Filtrar pelo modelo do veículo'),
                                                            ('marca', 'Filtrar pela marca do veículo'),
                                                            ('inicio', 'Filtrar pela data de início da OS'),
                                                            ('conclusao', 'Filtrar pela data de conclusão da OS'),
                                                            ('tempo_reparo', 'Filtrar pelo tempo total de reparo')], tablefmt='grid', stralign='left'))
                                    opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    lista_filtros_os = ['cpf', 'id_cliente', 'modelo', 'marca', 'inicio', 'conclusao', 'tempo_reparo']
                                    
                                    if opcao_filtro not in lista_filtros_os:
                                        print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')
                                    
                                    if opcao_filtro.lower() == 'id_cliente':
                                        registro = input('\nDigite o registro do cliente (ID) > ')
                                        nome_cliente, = select.nome_cliente(id_cliente=eval(registro))
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas pelo(a) cliente "{nome_cliente}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro.lower() == 'cpf':
                                        registro = input('\nDigite o CPF do cliente (Somente números) > ')
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas pelo(a) cliente dono do CPF "{registro}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(cpf_cliente=registro)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'modelo':
                                        registro = input('\nDigite o modelo do veículo > ').capitalize()
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas para veículos do modelo "{registro}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(modelo=registro)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'marca':
                                        registro = input('\nDigite a marca do veículo > ').capitalize()
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas para veículos da marca "{registro}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(marca=registro)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'inicio':
                                        registro = input('\nDigite a data de início da OS > ')
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas na data "{registro}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(data_inicio=registro)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'conclusao':
                                        registro = input('\nDigite a data de conclusão da OS > ').capitalize()
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS que foram finalizadas na data "{registro}"..........{color.END}\n\n')
                                        select.os_cliente_veiculo(data_conclusao=registro)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'tempo_reparo':
                                        registro = input('\nDigite o tempo total de reparo do veículo (dias) > ').capitalize()
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todas OS que duraram por {registro} dias..........{color.END}\n\n')
                                        select.os_cliente_veiculo(tempo_reparo=registro)
                                        break
                        
                            elif quest_filtro.lower() in ('nao', 'nn', 'n', 'no'):
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os veículos registrados no sistema..........{color.END}\n\n')
                                select.os_cliente_veiculo()

                elif categoria.lower() == 'funcionarios':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos de funcionários{color.END}')
                    time.sleep(1)
                    menu.menu_funcionarios()
                    
                    while True:
                        print('Selecione uma das opções - Digite "back" para voltar ao menu principal')
                        comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
                        
                        if comando.lower() == 'back':
                            break
                            
                        elif comando.lower() == 'menu':
                            menu.menu_funcionarios()
                        
                        lista_comandos_funcionarios = ['info_funcionarios', 'func_especialidades', 'folha_pagamento', 'menu', 'back']
                        if comando.lower() not in lista_comandos_funcionarios:
                            print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')
                            
                        if comando.lower() == 'info_funcionarios':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                op_func = select.consulta_funcionarios()
                                while True:
                                    print('\n' + tabulate([('funcionarios_ativos', 'Mostra os funcionarios ainda ativos na empresa'),
                                                            ('funcionarios_desligados', 'Mostra os funcionários que foram demitidos da empresa'),
                                                            ('id_funcionario', 'Procurar por um funcionário específico usando o número de registro (ID)')],
                                                            headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                                    
                                    quest_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END}: '))
                                    lista_filtro = ['funcionarios_ativos', 'funcionarios_desligados', 'id_funcionario', 'todos']
                                    
                                    if quest_filtro not in lista_filtro:
                                        print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')
                                    
                                    if quest_filtro == 'funcionarios_ativos':
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários ainda ativos na empresa..........{color.END}\n\n')
                                        op_func.ativos()
                                        break
                                    
                                    elif quest_filtro == 'funcionarios_desligados':
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários que foram desligados da empresa..........{color.END}\n\n')
                                        op_func.demitidos()
                                        break
                                        
                                    elif quest_filtro == 'id_funcionario':
                                        id_funcionario = input('\nDigite o número de registro do funcionário (ID) > ')
                                        nome_funcioario, = select.funcionarios(id_funcionario=eval(id_funcionario))
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Informações sobre o funcionário "{nome_funcioario}"..........{color.END}\n\n')
                                        op_func.by_id(id_funcionario)
                                        break
                                    
                            elif quest_filtro.lower() in ('nao', 'não', 'n', 'nn'):
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários registrados no sistema..........{color.END}\n\n')
                                funcionarios = select.consulta_funcionarios()
                                print(funcionarios.all())
                                
                elif categoria.lower() == 'produtos':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos dos produtos{color.END}')
                    time.sleep(1)
                    menu.menu_produtos()
                    
                    while True:
                        print('Selecione uma das opções - Digite "back" para voltar ao menu principal')
                        comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
                        
                        if comando.lower() == 'back':
                            break
                        
                        elif comando.lower() == 'menu':
                            menu.menu_produtos()
                            
                        listas_comandos_produtos = ['info_produtos', 'estoque_min', 'compra_produto', 'produtos_estoque', 'categoria', 'fornecedor']
                        if comando.lower() not in listas_comandos_produtos:
                            print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')
                        
                        if comando.lower() == 'info_produtos':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                print('\n' + tabulate([('nome', 'Filtrar utilizando o nome do produto'),
                                                        ('registro', 'Filtrar utilizando o número de registro (ID) do produto')],
                                                        headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='center') + '\n')
                                
                                while True:
                                    opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    lista_opcao_filtro = ['nome', 'registro']
                                    
                                    if opcao_filtro not in lista_opcao_filtro:
                                        print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')
                                    
                                    if opcao_filtro.lower() == 'nome':
                                        nome = str(input('\nDigite o nome do produto > ')).capitalize()
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto "{nome}" no banco de dados..........{color.END}\n\n')
                                        select.produtos_e_fornecedores(nome_produto=nome)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'registro':
                                        registro = input('\nDigite o número de registro do produto (ID) > ')
                                        writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto N° {registro}..........{color.END}\n\n')
                                        select.produtos_e_fornecedores(id_produto=registro)
                                        break
                            
                            elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros de produtos..........{color.END}\n\n')
                                select.produtos_e_fornecedores()
                        
                        if comando.lower() == 'estoque_min':
                            quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                            
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                     print('\n' + tabulate([('nome', 'Filtrar utilizando o nome do produto')],
                                                            headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='center') + '\n')
                                     while True:
                                        opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                        lista_opcao_filtro = ['nome']

                                        if opcao_filtro not in lista_opcao_filtro:
                                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')

                                        if opcao_filtro.lower() == 'nome':
                                            nome = str(input('\nDigite o nome do produto > ')).capitalize()
                                            writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto "{nome}" no banco de dados..........{color.END}\n\n')
                                            select.consulta_estoque_min(nome_produto=nome)
                                            break
                            if quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                                writer(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros de produtos e sua quantidade em estoque..........{color.END}\n\n')
                                select.consulta_estoque_min()
                                select.consulta_estoque_min(abaixo=True)

            elif opcao == 2:
                print(f'\n{color.LIGHT_GREEN}Saindo do sistema SV-Py Lite...{color.END}\n')
                conexao.close()
                exit()

        except ValueError:
            print(f'{color.RED}O valor digitado é inválido!{color.END}')

except KeyboardInterrupt:
    exit()