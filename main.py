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
                writer(f'{color.NEGATIVE}\nEscolha uma categoria para as consultas:{color.END}\n\n')
                print(tabulate([('clientes', 'Consultas para trazer as principais informações sobre os cliente'),
                                ('veiculos', 'Consultas para trazer as principais informações sobre os veículos dos clientes'),
                                ('funcionarios', 'Consultas para trazer as principais informações sobre os funcionários da empresa'),
                                ('produtos', 'Consultas para trazer as principais informações sobre os produtos')],
                                headers=['Categoria', 'Descrição'], tablefmt='grid'))
                
                categoria = str(input(f'\n{color.NEGATIVE}SVPy-lite >{color.END} '))
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
                                    writer(f'{color.LIGHT_GREEN}\nConsulta: Todas as informações do(a) cliente "{nome_cliente}" ..........{color.END}\n\n')
                                    select.client_info(eval(registro))
                                    break
                            else:
                                writer(f'\n{color.LIGHT_GREEN}Consultando banco de dados............{color.END}\n\n')
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
                                        writer('\nConsultando o banco de dados............\n\n')
                                        select.cliente_ult_os(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro.lower() == 'ultimo':
                                        writer('\nConsultando o banco de dados............\n\n')
                                        select.cliente_ult_os(apenas_ultimo=True)
                                        break
                                    
                                    elif opcao_filtro.lower() == 'combinado':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        writer('\nConsultando o banco de dados............\n\n')
                                        select.cliente_ult_os(id_cliente=eval(registro), apenas_ultimo=True)
                                        break

                            elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                                writer('\nConsulta o banco de dados............\n\n')
                                select.cliente_ult_os()
                        
                        elif comando.lower() == 'info_pagamento':
                            quest_filtro = str(input(f'{color.NEGATIVE}Deseja realizar uma consulta com filtro ? [S/N]:{color.END} '))
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                    while True:
                                        print('\n' + tabulate([('id', 'Filtrar usuário pelo número de registro'), 
                                                        ('situação', 'Filtra pela situação do pagamento (Pendente, Pago)')], 
                                                        headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                        
                                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                        
                                        if opcao_filtro.lower() == 'id':
                                            registro = input('Digite o número de registro do cliente (ID) > ')
                                            writer('\nConsultando o banco de dados............\n\n')
                                            select.info_pagamento(id_cliente=eval(registro))
                                            break
                                        
                                        elif opcao_filtro.lower() in ('situação', 'situacao'):
                                            situacao = str(input('Deseja filtrar qual situação ? [Pendente/Pago]: '))
                                            if situacao.lower() in ('pendente', 'pago'):
                                                writer('\nConsultando o banco de dados............\n\n')
                                                select.info_pagamento(sitaucao=situacao)
                                                break
                                            else:
                                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Pago){color.END}')
                            
                            elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                                writer('\nConsultando o banco de dados............\n\n')
                                select.info_pagamento()
                        
                        elif comando.lower() == 'cliente_agenciamento':
                            quest_filtro = str(input(f'{color.NEGATIVE}Deseja realizar uma consulta com filtro ? [S/N]:{color.END} '))
                            if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                                while True:
                                    print('\n' + tabulate([('id', 'Filtrar pelo número de registro do cliente'),
                                                            ('status', 'Filtrar pelo status do agenciamento (Pendente/Vendido)')],
                                                            headers=['Filtro', 'Descrição'], tablefmt='grid'))
                                    opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                                    if opcao_filtro.lower() == 'id':
                                        registro = input('Digite o número de registro do cliente (ID) > ')
                                        writer('\nConsultando o banco de dados............\n\n')
                                        select.status_agenciamento(id_cliente=eval(registro))
                                        break
                                    
                                    elif opcao_filtro.lower() == 'status':
                                        status = str(input('Deseja filtrar qual situação ? [Pendente/Vendido]: '))
                                        if status.lower() in ('pendente', 'pago'):
                                            writer('\nConsultando o banco de dados............\n\n')
                                            select.status_agenciamento(status=status)
                                            break
                                        else:
                                            print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Vendido){color.END}')
                                    
                            elif quest_filtro.lower() in ('não', 'nao', 'nn', 'n', 'no'):
                                writer('\nConsultando o banco de dados............\n\n')
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
                                        writer('\nConsultando o banco de dados............\n\n')
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
                                writer(f'{color.LIGHT_GREEN}\nConsultando banco de dados............\n\n{color.END}')
                                select.atendimento_ao_cliente()

                        elif comando.lower() == 'qtde_veiculos':
                            writer(f'{color.LIGHT_GREEN}\nConsultando o banco de dados..........{color.END}\n\n')
                            select.qtde_veiculo_cliente()
                elif categoria.lower() == 'veiculos':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos de veículos{color.END}')
                    time.sleep(1)
                    menu.menu_veiculos()
                    
                elif categoria.lower() == 'funcionarios':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos de funcionários{color.END}')
                    time.sleep(1)
                    menu.menu_funcionarios()
                    
                elif categoria.lower() == 'produtos':
                    writer(f'\n{color.GREEN}Mostrando o menu de comandos dos produtos{color.END}')
                    time.sleep(1)
                    menu.menu_produtos()

            elif opcao == 2:
                print(f'\n{color.LIGHT_GREEN}Saindo do sistema SV-Py Lite...{color.END}\n')
                conexao.close()
                exit()

        except ValueError:
            print(f'{color.RED}O valor digitado é inválido!{color.END}')

except KeyboardInterrupt:
    exit()