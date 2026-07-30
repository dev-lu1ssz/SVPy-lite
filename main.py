import modules.database_creator as database_creator
import os

if 'SV-Py_lite_2.db' not in os.listdir('database'):
    print('Base de dados não encontrada. Criando base de dados SV-Py')
    database_creator.main()
    
    if 'SV-Py_lite_2.db' not in os.listdir('database'):
        print('Ocorreu algum erro ao tentar criar a base de dados no diretório "database"')
        exit()

try:
    while True:
        print('\nSeja bem vindo ao seu Sistema de Gerenciamento de Banco de Dados da Speed-Veiculos montado com SQLite!\n')
        print('Escolha uma das opções abaixo:')
        print('''
            [1] - Consultar todas as tabelas existentes no banco de dados
            [2] - Consultar uma tabela em específico
            [3] - Adicionar dados a uma tabela
            [4] - Sair
        ''')
        
        opcao = str(input('SVPy-lite > '))

except KeyboardInterrupt:
    exit()