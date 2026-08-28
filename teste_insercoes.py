import os
import sqlite3
import datetime

from modules.database_creator import recriar_banco
from modules.insertions import InData

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'SV-Py_lite_updated.db')

print('Criando banco de dados para a sequência de testes...')
recriar_banco(DB_PATH)

conexao = sqlite3.connect(DB_PATH)
conexao.execute('PRAGMA foreign_keys = on')
insert = InData(conexao)

print('Iniciando sequência de testes de inserção...')

insert.endereco('Rua das Flores', '100', None, 'Centro', 'São Paulo', 'SP', '01001000')
endereco_cliente = insert.cursor.lastrowid
insert.endereco('Av. Reforma', '500', None, 'Centro', 'São Paulo', 'SP', '01002000')
endereco_fornecedor = insert.cursor.lastrowid
insert.endereco('Rua do Operário', '10', None, 'Centro', 'São Paulo', 'SP', '01003000')
endereco_funcionario = insert.cursor.lastrowid

insert.departamento('Mecânica')
ultimo_departamento = insert.cursor.lastrowid
print('DEPARTAMENTO:', ultimo_departamento)

novo_id_especialidade = conexao.execute('SELECT COALESCE(MAX(ID_ESPECIALIDADE), 0) + 1 FROM ESPECIALIDADE').fetchone()[0]
insert.especialidade(novo_id_especialidade, 'Mecânico')
ultimo_especialidade = insert.cursor.lastrowid
print('ESPECIALIDADE:', ultimo_especialidade)

novo_cpf_cliente = 12345678909 + ultimo_departamento
insert.cliente('Maria Souza', endereco_cliente, '11999990000', novo_cpf_cliente)
ultimo_cliente = insert.cursor.lastrowid
print('CLIENTE:', ultimo_cliente)

insert.fornecedor('AutoPeças Brasil', '12345678901234', '11999990000', endereco_fornecedor)
ultimo_fornecedor = insert.cursor.lastrowid
print('FORNECEDOR:', ultimo_fornecedor)

insert.funcionario(
    ultimo_departamento,
    ultimo_especialidade,
    'José da Silva',
    '15-01-2024',
    '25-08-2024',
    endereco_funcionario,
)
ultimo_funcionario = insert.cursor.lastrowid
print('FUNCIONARIO:', ultimo_funcionario)

insert.veiculo(ultimo_cliente, 'ABC1D23', 'Celta', 'Chevrolet', '9BG1324SSS1234567')
ultimo_veiculo = insert.cursor.lastrowid
print('VEICULO:', ultimo_veiculo)

insert.departamento('Estoque')
ultimo_departamento_produto = insert.cursor.lastrowid
insert.cursor.execute('INSERT INTO CATEGORIA_PRODUTO(NOME_CATEGORIA) VALUES (?)', ('Óleo',))
conexao.commit()
categoria_produto = insert.cursor.lastrowid
insert.produto(ultimo_fornecedor, 'Filtro de ar', categoria_produto, 10, 25.0)
ultimo_produto = insert.cursor.lastrowid
print('PRODUTO:', ultimo_produto)

insert.estoque(
    ultimo_produto,
    10,
    5,
    '01-08-2027',
    365,
)
print('ESTOQUE: registro criado para o produto', ultimo_produto)

data_conclusao = '03-08-2026'
data_inicio = '01-08-2026'
tempo_total_dias = (datetime.datetime.strptime(data_conclusao, '%d-%m-%Y') - datetime.datetime.strptime(data_inicio, '%d-%m-%Y')).days

insert.ordem_servico(
    ultimo_veiculo,
    ultimo_cliente,
    data_inicio,
    data_conclusao,
    tempo_total_dias,
    None,
    650.0,
    'Troca de filtro e revisão',
)
ultimo_os = insert.cursor.lastrowid
print('ORDEM_SERVICO:', ultimo_os)

insert.feedback(ultimo_cliente, 9, 'Atendimento excelente', '04-08-2026')
ultimo_feedback = insert.cursor.lastrowid
print('FEEDBACK:', ultimo_feedback)

ultimo_pagamento = insert.pagamento(
    ultimo_cliente,
    ultimo_os,
    None,
    'PIX',
    2,
    '03-08-2026',
    'Pago',
    400.0,
    'Reparo',
)
print('PAGAMENTO:', ultimo_pagamento)

parcelas = conexao.execute(
    'SELECT ID_CONTA_RECEBER, NUMERO_PARCELA, VALOR_PARCELA, DATA_VENCIMENTO_RECEBER, STATUS FROM CONTA_RECEBER WHERE ID_PAGAMENTO = ?',
    (ultimo_pagamento,),
).fetchall()
print('CONTA_RECEBER:', parcelas)

insert.conta_pagar('Compra de filtro de ar', 150.0, '20-08-2026', 'Pendente')
ultimo_conta_pagar = insert.cursor.lastrowid
print('CONTA_PAGAR:', ultimo_conta_pagar)

insert.atendimento(ultimo_cliente, ultimo_funcionario, '04-08-2026')
ultimo_atendimento = insert.cursor.lastrowid
print('ATENDIMENTO:', ultimo_atendimento)

insert.agenciamento_veiculo(
    ultimo_cliente,
    ultimo_veiculo,
    '05-08-2026',
    '12-08-2026',
    300.0,
    7,
    30.0,
    'Pendente',
)
ultimo_agenciamento = insert.cursor.lastrowid
print('AGENCIAMENTO_VEICULO:', ultimo_agenciamento)

data_pagamento = '04-05-2026'
insert.folha_pagamento(
    ultimo_funcionario,
    'Realizado',
    5,
    data_pagamento,
    1500.0,
    None,
    400.0   
)

print('\nResumo dos registros inseridos:')
for tabela, sql in [
    ('CLIENTE', 'SELECT COUNT(*) FROM CLIENTE'),
    ('FUNCIONARIO', 'SELECT COUNT(*) FROM FUNCIONARIO'),
    ('VEICULO', 'SELECT COUNT(*) FROM VEICULO'),
    ('PRODUTO', 'SELECT COUNT(*) FROM PRODUTO'),
    ('ORDEM_SERVICO', 'SELECT COUNT(*) FROM ORDEM_SERVICO'),
    ('PAGAMENTO', 'SELECT COUNT(*) FROM PAGAMENTO'),
    ('FEEDBACK', 'SELECT COUNT(*) FROM FEEDBACK'),
    ('CONTA_RECEBER', 'SELECT COUNT(*) FROM CONTA_RECEBER'),
    ('CONTA_PAGAR', 'SELECT COUNT(*) FROM CONTA_PAGAR'),
    ('ATENDIMENTO', 'SELECT COUNT(*) FROM ATENDIMENTO'),
    ('AGENCIAMENTO_VEICULO', 'SELECT COUNT(*) FROM AGENCIAMENTO_VEICULO'),
]:
    total = conexao.execute(sql).fetchone()[0]
    print(f'{tabela}: {total}')

conexao.close()
