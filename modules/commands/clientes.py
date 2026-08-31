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
from modules.commands.funcionarios import obter_nome_funcionario

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
            print('\nSelecione uma das opções - Digite "back" para voltar ao menu de categorias')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands/clientes >{color.END} '))
            lista_comandos = ['clientes', 'ultimo_os', 'pagamentos', 'agenciamentos', 'atendimentos', 'veiculos', 'back', 'menu']

            if comando.lower() not in lista_comandos:
                print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')

            if comando.lower() == 'back':
                return

            elif comando.lower() == 'menu':
                menu.menu_clientes()

            elif comando.lower() == 'clientes':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro', 'Filtrar pelo número de registro do cliente'),
                                               ('cpf', 'Filtrar pelo CPF do cliente'),
                                               ('logradouro', 'Filtrar pelo logradouro do cliente'),
                                               ('cidade', 'Filtrar pela cidade do cliente'),
                                               ('uf', 'Filtrar pela UF do endereço'),
                                               ('cep', 'Filtrar pelo CEP do cliente'),
                                               ('combinado', 'Combina dois ou mais filtros ao mesmo tempo'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()

                        if opcao_filtro == 'back':
                            break

                        if opcao_filtro == 'registro':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'{color.LIGHT_GREEN}\nConsulta: Cadastro do(a) cliente "{nome_cliente}" ..........{color.END}\n\n')
                            select.client_info(id_cliente=int(registro))
                            break

                        elif opcao_filtro == 'cpf':
                            cpf = input('Digite o CPF do cliente > ').strip()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro do cliente com CPF "{cpf}"............{color.END}\n\n')
                            select.client_info(cpf=cpf)
                            break

                        elif opcao_filtro == 'logradouro':
                            logradouro = input('Digite o logradouro do cliente > ').strip()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes com o logradouro "{logradouro}"............{color.END}\n\n')
                            select.client_info(logradouro=logradouro)
                            break

                        elif opcao_filtro == 'numero':
                            numero = input('Digite o número do endereço > ').strip()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes com o número "{numero}"............{color.END}\n\n')
                            select.client_info(numero=numero)
                            break

                        elif opcao_filtro == 'cidade':
                            cidade = input('Digite a cidade do cliente > ').strip()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes da cidade "{cidade}"............{color.END}\n\n')
                            select.client_info(cidade=cidade)
                            break

                        elif opcao_filtro == 'uf':
                            uf = input('Digite a UF do endereço (EX: SP) > ').strip().upper()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes da UF "{uf}"............{color.END}\n\n')
                            select.client_info(uf=uf)
                            break

                        elif opcao_filtro == 'cep':
                            cep = input('Digite o CEP do cliente > ').strip()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes com o CEP "{cep}"............{color.END}\n\n')
                            select.client_info(cep=cep)
                            break

                        elif opcao_filtro == 'combinado':
                            filtros = {}
                            registro = input('Digite o ID do cliente (opcional) > ').strip()
                            if registro:
                                filtros['id_cliente'] = int(registro)

                            cpf = input('Digite o CPF do cliente (opcional) > ').strip()
                            if cpf:
                                filtros['cpf'] = cpf

                            logradouro = input('Digite o logradouro (opcional) > ').strip()
                            if logradouro:
                                filtros['logradouro'] = logradouro

                            cidade = input('Digite a cidade (opcional) > ').strip()
                            if cidade:
                                filtros['cidade'] = cidade

                            uf = input('Digite a UF (opcional) > ').strip().upper()
                            if uf:
                                filtros['uf'] = uf

                            cep = input('Digite o CEP (opcional) > ').strip()
                            if cep:
                                filtros['cep'] = cep

                            if not filtros:
                                print(f'{color.RED}Nenhum filtro foi informado. Retornando ao menu.{color.END}')
                                continue

                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de clientes com os filtros informados............{color.END}\n\n')
                            select.client_info(**filtros)
                            break

                        else:
                            print(f'{color.LIGHT_RED}Opção de filtro inválida, escolha um dos filtros disponíveis{color.END}')
                else:
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Cadastro de todos os clientes............{color.END}\n\n')
                    select.client_info()

            elif comando.lower() == 'ultimo_os':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro', 'Filtrar usuário pelo número de registro'),
                                               ('ultimo', 'Trazer apenas a última OS registrada'),
                                               ('combinado', 'Combina os dois filtros de consulta'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        opcao_filtro = str(input('\nEscolha o filtro que deseja utilizar > ')).strip().lower()

                        if opcao_filtro == 'back':
                            break

                        if opcao_filtro == 'registro':
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

            elif comando.lower() == 'pagamentos':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro', 'Filtrar pelo número de registro do cliente'),
                                               ('cpf', 'Filtrar pelo CPF do cliente'),
                                               ('metodo', 'Filtrar pelo método de pagamento'),
                                               ('situacao', 'Filtra pela situação do pagamento (Pendente, Pago)'),
                                               ('combinado', 'Combina registro, CPF, método e situação'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()

                        if opcao_filtro == 'back':
                            break

                        if opcao_filtro == 'registro':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todos os pagamentos realizados pelo cliente "{nome_cliente}"............\n\n')
                            select.info_pagamento(id_cliente=int(registro))
                            break

                        elif opcao_filtro == 'cpf':
                            cpf = input('Digite o CPF do cliente > ').strip()
                            writer_func(f'\nConsulta: Todos os pagamentos do cliente com CPF "{cpf}"............\n\n')
                            select.info_pagamento(cpf=cpf)
                            break

                        elif opcao_filtro == 'metodo':
                            metodo = str(input('Digite o método de pagamento > ')).strip().title()
                            writer_func(f'\nConsulta: Todos os pagamentos realizados com o método "{metodo}"............\n\n')
                            select.info_pagamento(metodo_pagamento=metodo)
                            break

                        elif opcao_filtro.lower() in ('situacao', 'situação'):
                            situacao = str(input('Deseja filtrar qual situação ? [Pendente/Pago]: ')).strip().capitalize()
                            if situacao.lower() in ('pendente', 'pago'):
                                writer_func(f'\nConsulta: Todos os pagamentos com a situação "{situacao}"............\n\n')
                                select.info_pagamento(sitaucao=situacao)
                                break
                            else:
                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Pago){color.END}')

                        elif opcao_filtro.lower() == 'combinado':
                            registro = input('Digite o número de registro do cliente (ID) > ').strip()
                            cpf = input('Digite o CPF do cliente (opcional) > ').strip() or None
                            metodo = input('Digite o método de pagamento (opcional) > ').strip() or None
                            situacao = input('Digite a situação do pagamento [Pendente/Pago/Cancelado] (opcional) > ').strip().capitalize() or None
                            if situacao and situacao not in ('Pendente', 'Pago', 'Cancelado'):
                                print(f'{color.RED}Situação inválida.{color.END}')
                                continue
                            select.info_pagamento(
                                id_cliente=int(registro) if registro else None,
                                cpf=cpf,
                                metodo_pagamento=metodo.title() if metodo else None,
                                sitaucao=situacao,
                            )
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n'):
                    writer_func('\nConsultando o banco de dados............\n\n')
                    select.info_pagamento()

            elif comando.lower() == 'agenciamentos':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro', 'Filtrar pelo número de registro do cliente'),
                                               ('nome', 'Filtrar pelo nome do cliente'),
                                               ('status', 'Filtrar pelo status do agenciamento (Pendente/Vendido)'),
                                               ('modelo', 'Filtrar pelo modelo do veículo'),
                                               ('combinado', 'Combina registro, nome, status e modelo'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()
                        if opcao_filtro == 'back':
                            break
                        if opcao_filtro == 'registro':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todo agenciamento solicitado pelo(a) cliente "{nome_cliente}"............\n\n')
                            select.status_agenciamento(id_cliente=int(registro))
                            break

                        elif opcao_filtro == 'nome':
                            nome = input('Digite o nome do cliente > ').strip()
                            writer_func(f'\nConsulta: Todos os agenciamentos do cliente "{nome}"............\n\n')
                            select.status_agenciamento(nome_cliente=nome)
                            break

                        elif opcao_filtro.lower() == 'status':
                            status = str(input('Deseja filtrar qual situação ? [Pendente/Vendido]: ')).strip().capitalize()
                            if status.lower() in ('pendente', 'vendido', 'cancelado'):
                                writer_func(f'\nConsulta: Todos os agenciamento que possuem o status "{status}"............\n\n')
                                select.status_agenciamento(status=status)
                                break
                            else:
                                print(f'{color.RED}O valor digitado é inválido! Por favor digite apenas um dos valores (Pendente/Vendido){color.END}')

                        elif opcao_filtro == 'modelo':
                            modelo = input('Digite o modelo do veículo > ').strip().capitalize()
                            writer_func(f'\nConsulta: Todos os agenciamentos para veículos do modelo "{modelo}"............\n\n')
                            select.status_agenciamento(modelo_veiculo=modelo)
                            break

                        elif opcao_filtro.lower() == 'combinado':
                            registro = input('Digite o número de registro do cliente (ID) (opcional) > ').strip()
                            nome = input('Digite o nome do cliente (opcional) > ').strip() or None
                            status = input('Digite o status [Pendente/Vendido/Cancelado] (opcional) > ').strip().capitalize() or None
                            modelo = input('Digite o modelo do veículo (opcional) > ').strip().capitalize() or None
                            if status and status not in ('Pendente', 'Vendido', 'Cancelado'):
                                print(f'{color.RED}Status inválido.{color.END}')
                                continue
                            select.status_agenciamento(
                                status=status,
                                id_cliente=int(registro) if registro else None,
                                nome_cliente=nome,
                                modelo_veiculo=modelo,
                            )
                            break

                elif quest_filtro.lower() in ('não', 'nao', 'nn', 'n', 'no'):
                    writer_func('\nConsulta: Todos os agenciamentos que foram solicitados............\n\n')
                    select.status_agenciamento()

            elif comando.lower() == 'atendimentos':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro_cliente', 'Filtrar pelo número de registro do cliente'),
                                               ('registro_funcionario', 'Filtrar pelo número de registro do funcionário'),
                                               ('combinado', 'Combina cliente e funcionário'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()

                        if opcao_filtro == 'back':
                            break

                        if opcao_filtro == 'registro_cliente':
                            registro = input('Digite o número de registro do cliente (ID) > ')
                            nome_cliente = obter_nome_cliente(select, registro, color)
                            if nome_cliente is None:
                                continue
                            writer_func(f'\nConsulta: Todos os atendimentos realizados para o cliente "{nome_cliente}"............\n\n')
                            select.atendimento_ao_cliente(id_cliente=int(registro))
                            break

                        elif opcao_filtro == 'registro_funcionario':
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

            elif comando.lower() == 'veiculos':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('registro', 'Filtrar pelo número de registro do cliente'),
                                               ('nome', 'Filtrar pelo nome do cliente'),
                                               ('cpf', 'Filtrar pelo CPF do cliente'),
                                               ('quantidade', 'Filtrar pela quantidade de veículos do cliente'),
                                               ('combinado', 'Combina registro, nome, CPF e quantidade'),
                                               ('back', 'Volta para o menu de comandos')],
                                              headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()
                        if opcao_filtro == 'back':
                            break
                        if opcao_filtro == 'registro':
                            registro = input('Digite o número de registro do cliente (ID) > ').strip()
                            writer_func(f'\nConsulta: Quantidade de veículos do cliente com registro "{registro}"............\n\n')
                            select.qtde_veiculo_cliente(id_cliente=int(registro))
                            break
                        elif opcao_filtro == 'nome':
                            nome = input('Digite o nome do cliente > ').strip()
                            writer_func(f'\nConsulta: Quantidade de veículos do cliente "{nome}"............\n\n')
                            select.qtde_veiculo_cliente(nome_cliente=nome)
                            break
                        elif opcao_filtro == 'cpf':
                            cpf = input('Digite o CPF do cliente > ').strip()
                            writer_func(f'\nConsulta: Quantidade de veículos do cliente com CPF "{cpf}"............\n\n')
                            select.qtde_veiculo_cliente(cpf_cliente=cpf)
                            break
                        elif opcao_filtro == 'quantidade':
                            quantidade = input('Digite a quantidade de veículos > ').strip()
                            writer_func(f'\nConsulta: Clientes com "{quantidade}" veículos............\n\n')
                            select.qtde_veiculo_cliente(qtde_veiculos=int(quantidade))
                            break
                        elif opcao_filtro == 'combinado':
                            registro = input('Digite o registro do cliente (opcional) > ').strip()
                            nome = input('Digite o nome do cliente (opcional) > ').strip() or None
                            cpf = input('Digite o CPF do cliente (opcional) > ').strip() or None
                            quantidade = input('Digite a quantidade de veículos (opcional) > ').strip()
                            select.qtde_veiculo_cliente(
                                id_cliente=int(registro) if registro else None,
                                nome_cliente=nome,
                                cpf_cliente=cpf,
                                qtde_veiculos=int(quantidade) if quantidade else None,
                            )
                            break
                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                    writer_func(f'{color.LIGHT_GREEN}\nConsulta: Todos os clientes e suas quantidades de veículos............\n\n{color.END}')
                    select.qtde_veiculo_cliente()
    finally:
        if conexao is not None:
            conexao.close()
