import modules.database_creator as database_creator
import modules.insertions as insertions
from modules.selections import Selectdata
import modules.menu as menu
import os
from tabulate import tabulate
import sqlite3


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

            opcao = int(input('SVPy-lite > '))

            if opcao not in (1, 2, 3):
                print('Opção inválida! Digite uma opção entre 1 e 3.')
            elif opcao == 1:
                print('\nMostrando o menu de comandos de clientes')
                menu.menu_clientes()
                
                while True:
                    print('\nSelecione uma das opções - Digite "back" para voltar ao menu principal')
                    comando = str(input('SVPy-lite/commands > '))
                    lista_comandos = ['info_clinete', 'clinete_ult_os', 'cliente_pay', 'cliente_agen', 'atendimento', 'qtde_veiculos', 'back']
                    
                    if comando.lower() not in lista_comandos:
                        print('\nOpção inválida! Digite um dos comandos disponíveis.')
                    if comando.lower() == 'back':
                        break
                    if comando.lower() == 'info_cliente':
                        select.client_info()
                        

        except ValueError:
            print('O valor digitado é inválido!')

except KeyboardInterrupt:
    exit()