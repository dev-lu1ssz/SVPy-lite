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
        writer_func(f'\n{color.GREEN}Mostrando o menu de comandos de finanças{color.END}\n')
        time.sleep(1)
        menu.financas()

        while True:
            print('\nSelecione uma das opções - Digite "back" para voltar ao menu de categorias')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands/financas >{color.END} '))
            lista_comandos = ['metodos', 'pagamento_os', 'back', 'menu']

            if comando.lower() not in lista_comandos:
                print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')

            if comando.lower() == 'back':
                return

            elif comando.lower() == 'menu':
                menu.financas()

            elif comando.lower() == 'metodos':
                while True:
                    print('\n' + tabulate([('pix', 'Mostra a quantidade total de pagamentos no PIX'),
                                            ('crédito', 'Mostra a quantidade total de pagamentos no cartão de crédito'),
                                            ('debito', 'Mostra a quantidade total de pagamentos no cartão de débito'),
                                            ('boleto', 'Mostra a quantidade total de pagamentos no boleto'),
                                            ('back', 'Volta para o menu de comandos')],
                                            headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                    opcao_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()
                    
                    if opcao_filtro == 'back':
                        break

                    elif opcao_filtro.lower() in ('pix', 'credito', 'crédito', 'débito', 'debito', 'boleto'):
                        writer_func(f'\nConsulta: Total de pagamentos realizados no {opcao_filtro.capitalize()}............\n\n')
                        select.total_pagamentos_metodo(opcao_filtro.upper())

            elif comando.lower() == 'pagamento_os':
                while True:
                    print('\n' + tabulate([
                        ('registro', 'Filtrar pelo número de registro do cliente'),
                        ('cpf', 'Filtrar pelo CPF do cliente'),
                        ('inicio', 'Filtrar pela data de início da ordem de serviço'),
                        ('descricao', 'Filtrar por parte da descrição do reparo'),
                        ('metodo', 'Filtrar pelo método de pagamento'),
                        ('situacao', 'Filtrar pela situação do pagamento'),
                        ('data_pagamento', 'Filtrar pela data do pagamento'),
                        ('todos', 'Mostrar todos os pagamentos de ordens de serviço'),
                        ('back', 'Volta para o menu de comandos')
                    ], headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                    opcao_filtro = str(input(
                        f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '
                    )).strip().lower()

                    if opcao_filtro == 'back':
                        break

                    filtros = {}
                    if opcao_filtro == 'registro':
                        filtros['id_cliente'] = input('Digite o registro do cliente (ID) > ').strip()
                    elif opcao_filtro == 'cpf':
                        filtros['cpf_cliente'] = input('Digite o CPF do cliente > ').strip()
                    elif opcao_filtro == 'inicio':
                        filtros['data_inicio'] = input('Digite a data de início da OS (DD-MM-AAAA) > ').strip()
                    elif opcao_filtro == 'descricao':
                        filtros['descricao'] = input('Digite parte da descrição do reparo > ').strip()
                    elif opcao_filtro == 'metodo':
                        filtros['metodo_pagamento'] = input('Digite o método de pagamento > ').strip().upper()
                    elif opcao_filtro == 'situacao':
                        filtros['status_pagamento'] = input(
                            'Digite a situação do pagamento [Pendente/Pago/Cancelado] > '
                        ).strip().capitalize()
                    elif opcao_filtro == 'data_pagamento':
                        filtros['data_pagamento'] = input('Digite a data do pagamento (DD-MM-AAAA) > ').strip()
                    elif opcao_filtro != 'todos':
                        print(f'\n{color.RED}Filtro inválido. Escolha uma opção da tabela.{color.END}')
                        continue

                    writer_func('\nConsulta: Pagamentos relacionados às ordens de serviço............\n\n')
                    select.pagamento_os(**filtros)
                    break

    finally:
        if conexao is not None:
            conexao.close()
