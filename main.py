import modules.database_creator as database_creator
import modules.insertions as insertions
import os

if 'SV-Py_lite_updated.db' not in os.listdir('database'):
    print('Base de dados não encontrada. Criando base de dados SV-Py')
    database_creator.main()
    
    if 'SV-Py_lite_updated.db' not in os.listdir('database'):
        print('Ocorreu algum erro ao tentar criar a base de dados no diretório "database"')
        exit()

try:
    opcao = 0
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
        
        except ValueError:
            print('O valor digitado é inválido!')

except KeyboardInterrupt:
    exit()