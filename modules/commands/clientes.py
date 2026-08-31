import os
import sqlite3
import sys
import time

from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import modules.menu as menu
from modules.colors import Colors
from modules.selections import Selectdata


DB_PATH = os.path.join(BASE_DIR, 'database', 'SV-Py_lite_updated.db')


def writer(a):
    for i in a:
        print(i, flush=True, end='')
        time.sleep(0.02)


def conectar_banco():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute('PRAGMA foreign_keys = on')
    return conexao


def obter_nome_cliente(select, registro, color):
    resultado = select.nome_cliente(id_cliente=int(registro))
    if resultado is None:
        print(f'{color.RED}Erro! Nenhum cliente encontrado com o ID {registro}. Tente outro valor.{color.END}')
        return None
    nome_cliente, = resultado
    return nome_cliente


def executar(select=None, color=None, writer_func=None):
    color = color or Colors()
    writer_func = writer_func or writer
    conexao = None

    if select is None:
        conexao = conectar_banco()
        select = Selectdata(conexao)

    try:
        writer_func(f'\n{color.GREEN}Mostrando o menu de comandos de clientes{color.END}\n')
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
                        nome_cliente = obter_nome_cliente(select, registro, color)
                        if nome_cliente is None:
                            continue
                        writer_func(f'{color.LIGHT_GREEN}\nConsulta: Cadastro do(a) cliente "{nome_cliente}" ..........{color.END}\n\n')
                        select.client_info(int(registro))
                        break
                else:
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de todos os clientes............{color.END}\n\n')
                    select.client_info()

            elif comando.lower() == 'cliente_ult_os':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('id', 'Filtrar usuário pelo número de registro'),
                                               ('ultimo', 'Trazer apenas a última OS registrada'),
                                               ('combinado', 'Combina os dois filtros de consulta')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        opcao_filtro = str(input('\nEscolha o filtro que deseja utilizar > '))

                        if opcao_filtro.lower() == 'id':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todas OS solicitadas pelo(a) cliente "{nome_cliente}"............\n\n')
                            select.cliente_ult_os(id_cliente=int(registro))
                            break

                        elif opcao_filtro.lower() == 'ultimo':
                            writer_func('\nConsulta: Última OS registrada no sistema............\n\n')
                            select.cliente_ult_os(apenas_ultimo=True)
                            break

                        elif opcao_filtro.lower() == 'combinado':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Última OS solicitada pelo(a) cliente "{nome_cliente}"............\n\n')
                            select.cliente_ult_os(id_cliente=int(registro), apenas_ultimo=True)
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                    writer_func('\nConsulta o banco de dados............\n\n')
                    select.cliente_ult_os()

            elif comando.lower() == 'info_pagamento':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('id', 'Filtrar usuário pelo número de registro'),
                                               ('situação', 'Filtra pela situação do pagamento (Pendente, Pago)'),
                                               ('combinado', 'Combina ID do cliente e situação')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))

                        if opcao_filtro.lower() == 'id':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todos os pagamentos realizados pelo cliente "{nome_cliente}"............\n\n')
                            select.info_pagamento(id_cliente=int(registro))
                            break

                        elif opcao_filtro.lower() in ('situação', 'situacao'):
                            situacao = str(input('Deseja filtrar qual situação ? [Pendente/Pago]: ')).strip().capitalize()
                            if situacao.lower() in ('pendente', 'pago'):
                                writer_func(f'\nConsulta: Todos os pagamentos com a situação "{situacao}"............\n\n')
                                select.info_pagamento(sitaucao=situacao)
                                break
                            else:
                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Pago){color.END}')

                        elif opcao_filtro.lower() == 'combinado':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            situacao = input('Digite a situação do pagamento [Pendente/Pago/Cancelado] > ').strip().capitalize()
                            if situacao in ('Pendente', 'Pago', 'Cancelado'):
                                select.info_pagamento(id_cliente=int(registro), sitaucao=situacao)
                                break
                            print(f'{color.RED}Situação inválida.{color.END}')

                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                    writer_func('\nConsultando o banco de dados............\n\n')
                    select.info_pagamento()

            elif comando.lower() == 'cliente_agenciamento':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('id', 'Filtrar pelo número de registro do cliente'),
                                               ('status', 'Filtrar pelo status do agenciamento (Pendente/Vendido)'),
                                               ('combinado', 'Combina ID do cliente e status')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                        if opcao_filtro.lower() == 'id':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todo agenciamento solicitado pelo(a) cliente "{nome_cliente}"............\n\n')
                            select.status_agenciamento(id_cliente=int(registro))
                            break

                        elif opcao_filtro.lower() == 'status':
                            status = str(input('Deseja filtrar qual situação ? [Pendente/Vendido]: ')).strip().capitalize()
                            if status.lower() in ('pendente', 'vendido', 'cancelado'):
                                writer_func(f'\nConsulta: Todos os agenciamento que possuem o status "{status}"............\n\n')
                                select.status_agenciamento(status=status)
                                break
                            else:
                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Vendido){color.END}')

                        elif opcao_filtro.lower() == 'combinado':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            status = input('Digite o status [Pendente/Vendido/Cancelado] > ').strip().capitalize()
                            if status in ('Pendente', 'Vendido', 'Cancelado'):
                                select.status_agenciamento(status=status, id_cliente=int(registro))
                                break
                            print(f'{color.RED}Status inválido.{color.END}')

                elif quest_filtro.lower() in ('não', 'nao', 'nn', 'n', 'no'):
                    writer_func('\nConsulta: Todos os agenciamentos que foram solicitados............\n\n')
                    select.status_agenciamento()

            elif comando.lower() == 'atendimento':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('id_cliente', 'Filtrar pelo número de registro do cliente'),
                                               ('id_funcionario', 'Filtrar pelo número de registro do funcionário'),
                                               ('combinado', 'Combina cliente e funcionário')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))

                        if opcao_filtro == 'id_cliente':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todos os atendimentos realizados para o cliente "{nome_cliente}"............\n\n')
                            select.atendimento_ao_cliente(id_cliente=int(registro))
                            break

                        elif opcao_filtro == 'id_funcionario':
                            registro = input('Digite o número de registro do funcionário (ID) > ')
                            nome_funcionario = obter_nome_funcionario(select, registro, color)
                            if nome_funcionario is None:
                                continue
                            writer_func(f'{color.LIGHT_GREEN}\nConsulta: Todos atendimentos realizados pelo funcionário "{nome_funcionario}" ..........{color.END}\n\n')
                            select.atendimento_ao_cliente(id_funcionario=int(registro))
                            break

                        elif opcao_filtro == 'combinado':
                            id_cliente = int(input('Digite o ID do cliente > '))
                            id_funcionario = int(input('Digite o ID do funcionário > '))
                            select.atendimento_ao_cliente(id_cliente=id_cliente, id_funcionario=id_funcionario)
                            break

                        else:
                            print(f'{color.LIGHT_RED}Opção de filtro inválida, escolha um dos filtros disponíveis{color.END}')
                elif quest_filtro.lower() in ('não', 'nao', 'n', 'no'):
                    writer_func(f'{color.LIGHT_GREEN}\nConsulta: Todos os atendimentos realizados............\n\n{color.END}')
                    select.atendimento_ao_cliente()

            elif comando.lower() == 'qtde_veiculos':
                writer_func(f'{color.LIGHT_GREEN}\nConsultando o banco de dados..........{color.END}\n\n')
                select.qtde_veiculo_cliente()
    finally:
        if conexao is not None:
            conexao.close()
