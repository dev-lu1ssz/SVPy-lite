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
        writer_func(f'\n{color.GREEN}Mostrando o menu de comandos dos produtos{color.END}')
        time.sleep(1)
        menu.menu_produtos()
        
        while True:
            print('Selecione uma das opções - Digite "back" para voltar ao menu de categorias')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands/produtos >{color.END} '))
            listas_comandos_produtos = ['produtos', 'minimo', 'compras', 'estoque', 'categoria', 'fornecedor', 'back', 'menu']
            
            if comando.lower() == 'back':
                return
            
            elif comando.lower() == 'menu':
                menu.menu_produtos()
                
            if comando.lower() not in listas_comandos_produtos:
                print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')
            
            if comando.lower() == 'produtos':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    print('\n' + tabulate([('nome', 'Filtrar utilizando o nome do produto'),
                                            ('categoria', 'Filtrar pela categoria do produto'),
                                            ('preco', 'Filtrar pelo preço unitário do produto'),
                                            ('registro', 'Filtrar utilizando o número de registro do produto'),
                                            ('back', 'Volta para o menu de comandos')],
                                            headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='center') + '\n')
                    
                    while True:
                        opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()
                        if opcao_filtro == 'back':
                            break
                        lista_opcao_filtro = ['nome', 'categoria', 'preco', 'registro']
                        
                        if opcao_filtro not in lista_opcao_filtro:
                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')
                        
                        if opcao_filtro.lower() == 'nome':
                            nome = str(input('\nDigite o nome do produto > ')).capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto "{nome}" no banco de dados..........{color.END}\n\n')
                            select.consulta_produto(nome_produto=nome)
                            break

                        elif opcao_filtro.lower() == 'categoria':
                            categoria = str(input('\nDigite a categoria do produto > ')).capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Produtos da categoria "{categoria}"..........{color.END}\n\n')
                            select.consulta_produto(categoria=categoria)
                            break

                        elif opcao_filtro.lower() == 'preco':
                            preco = float(input('\nDigite o preço unitário do produto > '))
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Produtos com preço unitário "{preco}"..........{color.END}\n\n')
                            select.consulta_produto(preco_unitario=preco)
                            break
                        
                        elif opcao_filtro.lower() == 'registro':
                            registro = int(input('\nDigite o número de registro do produto > '))
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto N° {registro}..........{color.END}\n\n')
                            select.consulta_produto(id_produto=registro)
                            break
                
                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros de produtos..........{color.END}\n\n')
                    select.produtos_e_fornecedores()
            
            if comando.lower() == 'minimo':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                
                if quest_filtro.lower() in ('sim', 'ss', 's', 'yes', 'si'):
                    print('\n' + tabulate([('nome', 'Filtrar utilizando o nome do produto'),
                                            ('back', 'Volta para o menu de comandos')],
                                        headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='center') + '\n')
                    while True:
                        opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} ')).strip().lower()
                        if opcao_filtro == 'back':
                            break
                        lista_opcao_filtro = ['nome']

                        if opcao_filtro not in lista_opcao_filtro:
                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')

                        if opcao_filtro.lower() == 'nome':
                            nome = str(input('\nDigite o nome do produto > ')).capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros do produto "{nome}" no banco de dados..........{color.END}\n\n')
                            select.consulta_estoque_min(nome_produto=nome)
                            break
                if quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os registros de produtos e sua quantidade em estoque..........{color.END}\n\n')
                    select.consulta_estoque_min()
                    select.consulta_estoque_min(abaixo=True)

            elif comando.lower() == 'compras':
                writer_func(f'\n{color.LIGHT_GREEN}Consulta: Produtos disponíveis no estoque..........{color.END}\n\n')
                dados = select.produtos_estoque()
                print(tabulate(dados, headers=['PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'QTDE EM ESTOQUE', 'VALIDADE (DIAS)'], tablefmt='grid', stralign='left'))

            elif comando.lower() == 'categoria':
                categoria = input('Digite a categoria do produto > ').strip()
                dados = select.total_produtos_categoria(categoria)
                print(tabulate(dados, headers=['CATEGORIA', 'TOTAL DE PRODUTOS', 'PREÇO TOTAL'], tablefmt='grid', stralign='left'))

            elif comando.lower() == 'fornecedor':
                nome = input('Digite o nome do fornecedor (ou Enter para ignorar) > ').strip() or None
                cnpj = input('Digite o CNPJ (ou Enter para ignorar) > ').strip() or None
                dados = select.consulta_fornecedor(nome=nome, cnpj=cnpj)
                print(tabulate(dados, headers=['ID', 'NOME', 'CNPJ', 'TELEFONE', 'ID ENDEREÇO'], tablefmt='grid', stralign='left'))

            elif comando.lower() == 'compra_produto':
                dados = select.pagamento_produto()
                print(tabulate(dados, headers=['CLIENTE', 'CPF', 'PRODUTO', 'CATEGORIA', 'FORNECEDOR', 'CNPJ', 'DATA', 'PREÇO UNITÁRIO', 'QUANTIDADE', 'VALOR TOTAL', 'STATUS', 'MÉTODO'], tablefmt='grid', stralign='left'))
    finally:
        if conexao is not None:
            conexao.close()