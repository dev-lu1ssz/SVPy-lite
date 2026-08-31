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
            comando = str(input(f'{color.NEGATIVE}SVPy-lite/commands/funcionarios >{color.END} '))

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
                                                ('registro', 'Procurar por um funcionário específico usando o número de registro'),
                                                ('nome', 'Filtrar por nome do funcionário'),
                                                ('cidade', 'Filtrar por cidade do funcionário'),
                                                ('uf', 'Filtrar por UF do endereço do funcionário'),
                                                ('cep', 'Filtrar por CEP do funcionário'),
                                                ('logradouro', 'Filtrar por logradouro do endereço do funcionário'),
                                                ('data_admissao', 'Filtrar pela data de admissão'),
                                                ('data_demissao', 'Filtrar pela data de demissão'),
                                                ('departamento', 'Filtrar pelo nome do departamento'),
                                                ('especialidade', 'Filtrar pelo nome da especialidade'),
                                                ('combinado', 'Combina um ou mais filtros disponíveis'),
                                                ('back', 'Volta para o menu de comandos')],
                                               headers=['Filtro', 'Descrição'], tablefmt='grid', stralign='left'))

                        quest_filtro = str(input(f'\n{color.NEGATIVE}Escolha o filtro que deseja utilizar >{color.END}: ')).strip().lower()
                        if quest_filtro == 'back':
                            break
                        lista_filtro = ['ativos', 'desligados', 'registro', 'nome', 'cidade', 'uf', 'cep', 'logradouro', 'data_admissao', 'data_demissao', 'departamento', 'especialidade', 'combinado']

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
                            id_funcionario = input('\nDigite o número de registro do funcionário > ')
                            nome_funcioario = obter_nome_funcionario(select, id_funcionario, color)
                            if nome_funcioario is None:
                                continue
                            writer_func(f'\n{color.LIGHT_GREEN}Consulta: Informações sobre o funcionário "{nome_funcioario}"..........{color.END}\n\n')
                            op_func.by_id(id_funcionario)
                            break

                        elif quest_filtro == 'nome':
                            nome = input('Digite o nome do funcionário > ').strip()
                            writer_func(f'\nConsulta: Funcionários com o nome "{nome}"..........\n\n')
                            consulta = select.consulta_funcionarios(nome_funcionario=nome)
                            consulta.all()
                            break

                        elif quest_filtro == 'cidade':
                            cidade = input('Digite a cidade > ').strip()
                            writer_func(f'\nConsulta: Funcionários da cidade "{cidade}"..........\n\n')
                            consulta = select.consulta_funcionarios(cidade=cidade)
                            consulta.all()
                            break

                        elif quest_filtro == 'uf':
                            uf = input('Digite a UF > ').strip().upper()
                            writer_func(f'\nConsulta: Funcionários da UF "{uf}"..........\n\n')
                            consulta = select.consulta_funcionarios(uf=uf)
                            consulta.all()
                            break

                        elif quest_filtro == 'cep':
                            cep = input('Digite o CEP > ').strip()
                            writer_func(f'\nConsulta: Funcionários com o CEP "{cep}"..........\n\n')
                            consulta = select.consulta_funcionarios(cep=cep)
                            consulta.all()
                            break

                        elif quest_filtro == 'logradouro':
                            logradouro = input('Digite o logradouro > ').strip()
                            writer_func(f'\nConsulta: Funcionários com o logradouro "{logradouro}"..........\n\n')
                            consulta = select.consulta_funcionarios(logradouro=logradouro)
                            consulta.all()
                            break

                        elif quest_filtro == 'data_admissao':
                            data = input('Digite a data de admissão (AAAA-MM-DD) > ').strip()
                            writer_func(f'\nConsulta: Funcionários admitidos na data "{data}"..........\n\n')
                            consulta = select.consulta_funcionarios(data_admissao=data)
                            consulta.all()
                            break

                        elif quest_filtro == 'data_demissao':
                            data = input('Digite a data de demissão (AAAA-MM-DD) > ').strip()
                            writer_func(f'\nConsulta: Funcionários demitidos na data "{data}"..........\n\n')
                            consulta = select.consulta_funcionarios(data_demissao=data)
                            consulta.all()
                            break

                        elif quest_filtro == 'departamento':
                            departamento = input('Digite o nome do departamento > ').strip()
                            writer_func(f'\nConsulta: Funcionários do departamento "{departamento}"..........\n\n')
                            consulta = select.consulta_funcionarios(nome_departamento=departamento)
                            consulta.all()
                            break

                        elif quest_filtro == 'especialidade':
                            especialidade = input('Digite o nome da especialidade > ').strip()
                            writer_func(f'\nConsulta: Funcionários da especialidade "{especialidade}"..........\n\n')
                            consulta = select.consulta_funcionarios(nome_especialidade=especialidade)
                            consulta.all()
                            break

                        elif quest_filtro == 'combinado':
                            filtros = {}
                            id_func = input('Digite o registro do funcionário (opcional) > ').strip()
                            if id_func:
                                filtros['id_funcionario'] = int(id_func)
                            nome = input('Digite o nome do funcionário (opcional) > ').strip() or None
                            if nome:
                                filtros['nome_funcionario'] = nome
                            cidade = input('Digite a cidade (opcional) > ').strip() or None
                            if cidade:
                                filtros['cidade'] = cidade
                            uf = input('Digite a UF (opcional) > ').strip().upper() or None
                            if uf:
                                filtros['uf'] = uf
                            cep = input('Digite o CEP (opcional) > ').strip() or None
                            if cep:
                                filtros['cep'] = cep
                            logradouro = input('Digite o logradouro (opcional) > ').strip() or None
                            if logradouro:
                                filtros['logradouro'] = logradouro
                            data_admissao = input('Digite a data de admissão (opcional) > ').strip() or None
                            if data_admissao:
                                filtros['data_admissao'] = data_admissao
                            data_demissao = input('Digite a data de demissão (opcional) > ').strip() or None
                            if data_demissao:
                                filtros['data_demissao'] = data_demissao
                            departamento = input('Digite o nome do departamento (opcional) > ').strip() or None
                            if departamento:
                                filtros['nome_departamento'] = departamento
                            especialidade = input('Digite o nome da especialidade (opcional) > ').strip() or None
                            if especialidade:
                                filtros['nome_especialidade'] = especialidade
                            if not filtros:
                                print(f'{color.RED}Nenhum filtro foi informado. Retornando ao menu.{color.END}')
                                continue
                            writer_func(f'\nConsulta: Funcionários com os filtros selecionados..........\n\n')
                            consulta = select.consulta_funcionarios(**filtros)
                            consulta.all()
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
