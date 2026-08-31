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


def obter_nome_funcionario(select, registro, color):
    resultado = select.funcionarios(id_funcionario=int(registro))
    if resultado is None:
        print(f'{color.RED}Erro! Nenhum funcionário encontrado com o ID {registro}. Tente outro valor.{color.END}')
        return None
    nome_funcionario, = resultado
    return nome_funcionario


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
            print('Selecione uma das opções - Digite "back" para voltar ao menu de categorias')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))

            if comando.lower() == 'back':
                return

            elif comando.lower() == 'menu':
                menu.menu_funcionarios()

            lista_comandos_funcionarios = ['funcionarios', 'especialidades', 'pagamentos', 'menu', 'back']
            if comando.lower() not in lista_comandos_funcionarios:
                print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')

            if comando.lower() == 'funcionarios':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))

                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    op_func = select.consulta_funcionarios()
                    while True:
                        print('\n' + tabulate([('ativos', 'Mostra os funcionarios ainda ativos na empresa'),
                                                ('desligados', 'Mostra os funcionários que foram demitidos da empresa'),
                                                ('registro', 'Procurar por um funcionário específico usando o número de registro (ID)'),
                                                ('back', 'Volta para o menu de comandos')],
                                               headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        quest_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END}: ')).strip().lower()
                        if quest_filtro == 'back':
                            break
                        lista_filtro = ['ativos', 'desligados', 'registro', 'back']

                        if quest_filtro not in lista_filtro:
                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')

                        if quest_filtro == 'ativos':
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários ainda ativos na empresa..........{color.END}\n\n')
                            op_func.ativos()
                            break

                        elif quest_filtro == 'desligados':
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários que foram desligados da empresa..........{color.END}\n\n')
                            op_func.demitidos()
                            break

                        elif quest_filtro == 'registro':
                            id_funcionario = input('\nDigite o número de registro do funcionário (ID) > ')
                            nome_funcioario = obter_nome_funcionario(select, id_funcionario, color)
                            if nome_funcioario is None:
                                continue
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Informações sobre o funcionário "{nome_funcioario}"..........{color.END}\n\n')
                            op_func.by_id(id_funcionario)
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'n', 'nn'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os funcionários registrados no sistema..........{color.END}\n\n')
                    funcionarios = select.consulta_funcionarios()
                    funcionarios.all()

            elif comando.lower() == 'especialidades':
                writer_func(f'\n{color.LIGHT_GREEN}Consulta: Funcionários e suas especialidades..........{color.END}\n\n')
                dados = select.funcionario_dep_esp()
                print(tabulate(dados, headers=['FUNCIONÁRIO', 'DATA ADMISSÃO', 'DEPARTAMENTO', 'ESPECIALIDADE'], tablefmt='grid', stralign='left'))

            elif comando.lower() == 'pagamentos':
                writer_func(f'\n{color.LIGHT_GREEN}Consulta: Folha de pagamento dos funcionários..........{color.END}\n\n')
                dados = select.dados_fp()
                print(tabulate(dados, headers=['FUNCIONÁRIO', 'DATA ADMISSÃO', 'MÊS', 'SALÁRIO BRUTO', 'DESCONTOS', 'SALÁRIO LÍQUIDO', 'STATUS', 'SITUAÇÃO'], tablefmt='grid', stralign='left'))
    finally:
        if conexao is not None:
            conexao.close()
