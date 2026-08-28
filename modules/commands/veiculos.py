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
        writer_func(f'\n{color.GREEN}Mostrando o menu de comandos de veículos{color.END}')
        time.sleep(1)
        menu.menu_veiculos()

        while True:
            print('Selecione uma das opções - Digite "back" para voltar ao menu principal')
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands >{color.END} '))
            lista_comandos = ['info_veiculo', 'ordem_servico', 'back', 'menu']

            if comando.lower() not in lista_comandos:
                print(f'\n{color.RED}Opção inválida! Digite "menu" para ver a lista de comandos disponíveis.{color.END}')

            if comando.lower() == 'back':
                break

            elif comando.lower() == 'menu':
                menu.menu_veiculos()

            elif comando.lower() == 'info_veiculo':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                    while True:
                        print(f'\n{tabulate([("placa", "Utiliza a placa do veículo como filtro"),
                                ("marca", "Retorna todos os veículos de uma marca específica"),
                            ("modelo", "Retorna todos os veículos de um modelo específico"),
                            ("combinado", "Combina marca e modelo")],
                                headers=["Filtro", "Descrição"], tablefmt="grid", stralign="left")}\n')

                        opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                        lista_filtros_veiculos = ['placa', 'marca', 'modelo']

                        if opcao_filtro not in lista_filtros_veiculos:
                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')

                        if opcao_filtro.lower() == 'placa':
                            placa = input('\nDigite a placa do veículo > ').upper()
                            writer_func(f'{color.LIGHT_GREEN}\nConsulta: Veiculo com a placa "{placa}"..........{color.END}\n\n')
                            select.consulta_carro(placa=placa)
                            break

                        elif opcao_filtro.lower() == 'marca':
                            marca = str(input('\nDigite a marca do veículo > ')).capitalize()
                            writer_func(f'\nConsulta: Todos os veículos da marca "{marca}"..........{color.END}\n\n')
                            select.consulta_carro(marca=marca)
                            break

                        elif opcao_filtro.lower() == 'modelo':
                            modelo = str(input('\nDigite o modelo do veículo > ')).capitalize()
                            writer_func(f'\nConsulta: Todos os veículos do modelo "{modelo}"..........{color.END}\n\n')
                            select.consulta_carro(modelo=modelo)
                            break

                        elif opcao_filtro.lower() == 'combinado':
                            marca = input('\nDigite a marca do veículo > ').strip().capitalize()
                            modelo = input('Digite o modelo do veículo > ').strip().capitalize()
                            select.consulta_carro(marca=marca, modelo=modelo)
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os veículos registrados no sistema..........{color.END}\n\n')
                    select.consulta_carro()

            elif comando.lower() == 'ordem_servico':
                quest_filtro = str(input('Deseja realizar uma consulta com filtro ? [S/N]: '))
                if quest_filtro.lower() in ('sim', 's', 'ss', 'yes', 'si'):
                    while True:
                        print('\n' + tabulate([('id_cliente', 'Filtrar OS solicitadas por clientes usando o número de registro'),
                                                ('cpf', 'Filtrar OS solicitadas por clientes usando o CPF'),
                                                ('modelo', 'Filtrar pelo modelo do veículo'),
                                                ('marca', 'Filtrar pela marca do veículo'),
                                                ('inicio', 'Filtrar pela data de início da OS'),
                                                ('conclusao', 'Filtrar pela data de conclusão da OS'),
                                                ('tempo_reparo', 'Filtrar pelo tempo total de reparo'),
                                                ('combinado', 'Combina dois ou mais filtros')],
                                               headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))
                        opcao_filtro = str(input(f'{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END} '))
                        lista_filtros_os = ['cpf', 'id_cliente', 'modelo', 'marca', 'inicio', 'conclusao', 'tempo_reparo']

                        if opcao_filtro not in lista_filtros_os:
                            print(f'\n{color.LIGHT_RED}O filtro selecionado é inválido! Veja novamente a lista e escolha o filtro que deseja utilizar{color.END}')

                        if opcao_filtro.lower() == 'id_cliente':
                            registro = input('\nDigite o registro do cliente (ID) > ')
                            nome_cliente, = select.nome_cliente(id_cliente=int(registro))
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas pelo(a) cliente "{nome_cliente}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(id_cliente=int(registro))
                            break

                        elif opcao_filtro.lower() == 'cpf':
                            registro = input('\nDigite o CPF do cliente (Somente números) > ')
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas pelo(a) cliente dono do CPF "{registro}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(cpf_cliente=registro)
                            break

                        elif opcao_filtro.lower() == 'modelo':
                            registro = input('\nDigite o modelo do veículo > ').capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas para veículos do modelo "{registro}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(modelo=registro)
                            break

                        elif opcao_filtro.lower() == 'marca':
                            registro = input('\nDigite a marca do veículo > ').capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas para veículos da marca "{registro}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(marca=registro)
                            break

                        elif opcao_filtro.lower() == 'inicio':
                            registro = input('\nDigite a data de início da OS > ')
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS solicitadas na data "{registro}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(data_inicio=registro)
                            break

                        elif opcao_filtro.lower() == 'conclusao':
                            registro = input('\nDigite a data de conclusão da OS > ').capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS que foram finalizadas na data "{registro}"..........{color.END}\n\n')
                            select.os_cliente_veiculo(data_conclusao=registro)
                            break

                        elif opcao_filtro.lower() == 'tempo_reparo':
                            registro = input('\nDigite o tempo total de reparo do veículo (dias) > ').capitalize()
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todas OS que duraram por {registro} dias..........{color.END}\n\n')
                            select.os_cliente_veiculo(tempo_reparo=registro)
                            break

                        elif opcao_filtro.lower() == 'combinado':
                            id_cliente = input('ID do cliente (Enter para ignorar) > ').strip()
                            modelo = input('Modelo (Enter para ignorar) > ').strip().capitalize()
                            marca = input('Marca (Enter para ignorar) > ').strip().capitalize()
                            tempo_reparo = input('Tempo de reparo (Enter para ignorar) > ').strip()
                            if not any((id_cliente, modelo, marca, tempo_reparo)):
                                print(f'{color.LIGHT_RED}Informe pelo menos um filtro.{color.END}')
                                continue
                            select.os_cliente_veiculo(
                                id_cliente=int(id_cliente) if id_cliente else None,
                                modelo=modelo or None,
                                marca=marca or None,
                                tempo_reparo=int(tempo_reparo) if tempo_reparo else None,
                            )
                            break

                elif quest_filtro.lower() in ('nao', 'não', 'nn', 'n', 'no'):
                    writer_func(f'\n{color.LIGHT_GREEN}Consulta: Todos os veículos registrados no sistema..........{color.END}\n\n')
                    select.os_cliente_veiculo()
    finally:
        if conexao is not None:
            conexao.close()
