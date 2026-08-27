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


def executar(select=None, color=None, writer_func=None):
    color = color or Colors()
    writer_func = writer_func or writer
    conexao = None

    if select is None:
        conexao = conectar_banco()
        select = Selectdata(conexao)

    try:
        writer_func(f'\n{color.GREEN}Mostrando o menu de comandos de funcionários{color.END}')
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
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários ainda ativos na empresa..........{color.END}\n\n')
                            op_func.ativos()
                            break

                        elif quest_filtro == 'funcionarios_desligados':
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários que foram desligados da empresa..........{color.END}\n\n')
                            op_func.demitidos()
                            break

                        elif quest_filtro == 'id_funcionario':
                            id_funcionario = input('\nDigite o número de registro do funcionário (ID) > ')
                            nome_funcioario, = select.funcionarios(id_funcionario=eval(id_funcionario))
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Informações sobre o funcionário "{nome_funcioario}"..........{color.END}\n\n')
                            op_func.by_id(id_funcionario)
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'n', 'nn'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários registrados no sistema..........{color.END}\n\n')
                    funcionarios = select.consulta_funcionarios()
                    funcionarios.all()
    finally:
        if conexao is not None:
            conexao.close()
