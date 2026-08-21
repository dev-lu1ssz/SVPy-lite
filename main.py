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

if not DB_PATH:
    print('Base de dados não encontrada. Criando base de dados SV-Py')
    database_creator.main()
    
    if not DB_PATH:
        print('Ocorreu algum erro ao tentar criar a base de dados no diretório "database"')
        exit()

try:
    opcao = 0
    color = Colors()
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute('PRAGMA foreign_keys = on')
    select = Selectdata(conexao)

    while opcao != 3:
        try:
            print('\nSeja bem vindo ao seu Sistema de Gerenciamento de Banco de Dados da Speed-Veiculos montado com SQLite!\n')
            print('Escolha uma das opções abaixo:')
            print('''
                [1] - Ver o menu de comandos para consultas no BD
                [2] - Adicionar dados a uma tabela
                [3] - Sair
            ''')

            opcao = int(input(f'{color.NEGATIVE}SVPy-lite >{color.END} '))

            if opcao not in (1, 2, 3):
                print('Opção inválida! Digite uma opção entre 1 e 3.')
            elif opcao == 1:
                print('\nMostrando o menu de comandos de clientes')
                menu.menu_clientes()
                
                while True:
                    print('\nSelecione uma das opções - Digite "back" para voltar ao menu principal')
                    comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
                    lista_comandos = ['info_cliente', 'cliente_ult_os', 'info_pagamento', 'cliente_agenciamento', 'atendimento', 'qtde_veiculos', 'back', 'menu', 'back']
                    
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
                                writer('\nConsultando banco de dados............\n\n')
                                select.client_info(eval(registro))
                                break
                        else:
                            writer('\nConsultando banco de dados............\n\n')
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

        
        except ValueError:
            print(f'{color.RED}O valor digitado é inválido!{color.END}')

except KeyboardInterrupt:
    exit()