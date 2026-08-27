import os
import sqlite3
import sys
import time
from turtle import color
from turtle import color

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
        writer(f'\n{color.GREEN}Mostrando o menu de comandos dos produtos{color.END}')
        time.sleep(1)
        menu.menu_produtos()
        
        while True:
            print('Selecione uma das opções - Digite "back" para voltar ao menu principal')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
            listas_comandos_produtos = ['info_produtos', 'estoque_min', 'compra_produto', 'produtos_estoque', 'categoria', 'fornecedor', 'back', 'menu']
            
            if comando.lower() == 'back':
                break
            
            elif comando.lower() == 'menu':
                menu.menu_produtos()
                
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
    finally:
        if conexao is not None:
            conexao.close()