import modules.database_creator as database_creator
from modules.selections import Selectdata
import modules.menu as menu
from modules.commands import clientes, veiculos, funcionarios, produtos
import os
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

def preparar_banco():
    nome_banco = os.path.basename(DB_PATH)

    if os.path.exists(DB_PATH):
        resposta = input(
            f'{color.YELLOW}O banco de dados "{nome_banco}" já existe. '
            f'Deseja recriá-lo? Todos os dados serão apagados [S/N]: {color.END}'
        ).strip().lower()

        if resposta in ('s', 'sim', 'ss', 'yes', 'si'):
            database_creator.recriar_banco(DB_PATH)
            print(f'{color.LIGHT_GREEN}Banco de dados "{nome_banco}" recriado com sucesso.{color.END}')
        else:
            print(f'{color.LIGHT_GREEN}Banco de dados "{nome_banco}" existente será utilizado.{color.END}')
    else:
        database_creator.criar_banco(DB_PATH)
        print(f'{color.LIGHT_GREEN}Banco de dados "{nome_banco}" criado com sucesso.{color.END}')

try:
    preparar_banco()
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
                while True:
                    writer(f'{color.NEGATIVE}\nEscolha uma categoria para as consultas:{color.END}\n')
                    menu.categorias()

                    categoria = str(input(f'{color.NEGATIVE}SVPy-lite >{color.END} ')).strip().lower()
                    categorias_disponiveis = ['clientes', 'veiculos', 'funcionarios', 'produtos']

                    if categoria not in categorias_disponiveis:
                        print(f'\n{color.LIGHT_RED}Escolha uma categoria que esteja disponível na lista{color.END}\n')
                        continue

                    if categoria == 'clientes':
                        clientes.executar(select=select, color=color, writer_func=writer)
                    elif categoria == 'veiculos':
                        veiculos.executar(select=select, color=color, writer_func=writer)
                    elif categoria == 'funcionarios':
                        funcionarios.executar(select=select, color=color, writer_func=writer)
                    elif categoria == 'produtos':
                        produtos.executar(select=select, color=color, writer_func=writer)

                    break

            elif opcao == 2:
                print(f'\n{color.LIGHT_GREEN}Saindo do sistema SV-Py Lite...{color.END}\n')
                conexao.close()
                exit()

        except ValueError:
            print(f'{color.RED}O valor digitado é inválido!{color.END}')

except KeyboardInterrupt:
    exit()
