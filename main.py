import modules.database_creator as database_creator
import modules.insertions as insertions
from modules.selections import Selectdata
import modules.menu as menu
from modules.commands import clientes, veiculos, funcionarios
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
                    clientes.executar(select=select, color=color, writer_func=writer)

                elif categoria.lower() == 'veiculos':
                    veiculos.executar(select=select, color=color, writer_func=writer)

                elif categoria.lower() == 'funcionarios':
                    funcionarios.executar(select=select, color=color, writer_func=writer)
                    continue

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
