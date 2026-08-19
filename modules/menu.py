from tabulate import tabulate

def menu_clientes():
    lista_consulta_clientes = [('info_cliente', 'Traz todas as informações sobre os clientes cadastrados'), 
                                ('cliente_ult_os', 'Traz informações sobre os clientes e suas ordens de serviço'),
                                ('cliente_pay', 'Traz informações sobre clientes que realizaram pagamentos'),
                                ('cliente_agen', 'Traz informações sobre clientes que solicitaram um agenciamento'),
                                ('atendimento', 'Traz informações sobre o atendimento ao cliente'),
                                ('qtde_veiculos', 'Traz informações sobre a quantidade de veículos que cada cliente possui')]
    
    tabela = tabulate(lista_consulta_clientes, headers=['COMANDO', 'DESCRIÇÃO'], tablefmt='grid', stralign='left')
    return print(f'\n{tabela}\n')

if __name__ == '__main__':
    menu_clientes()