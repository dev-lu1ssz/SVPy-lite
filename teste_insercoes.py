import os
import sqlite3
import datetime

from modules.database_creator import main as criar_banco
from modules.insertions import InData

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'SV-Py_lite_updated.db')

if not os.path.exists(DB_PATH):
    print('Base de dados não encontrada. Criando base de dados...')
    criar_banco()

conexao = sqlite3.connect(DB_PATH)
conexao.execute('PRAGMA foreign_keys = on')
insert = InData(conexao)

print('Iniciando sequência de testes de inserção...')

insert.departamento('Mecânica')
ultimo_departamento = insert.cursor.lastrowid
print('DEPARTAMENTO:', ultimo_departamento)

novo_id_especialidade = conexao.execute('SELECT COALESCE(MAX(ID_ESPECIALIDADE), 0) + 1 FROM ESPECIALIDADE').fetchone()[0]
insert.especialidade(novo_id_especialidade, 'Mecânico')
ultimo_especialidade = insert.cursor.lastrowid
print('ESPECIALIDADE:', ultimo_especialidade)

novo_cpf_cliente = 12345678909 + ultimo_departamento
insert.cliente('Maria Souza', 'Rua das Flores, 100', 12345678909, novo_cpf_cliente)
ultimo_cliente = insert.cursor.lastrowid
print('CLIENTE:', ultimo_cliente)

insert.fornecedor('AutoPeças Brasil', '12345678901234', 11999990000, 'Av. Reforma, 500')
ultimo_fornecedor = insert.cursor.lastrowid
print('FORNECEDOR:', ultimo_fornecedor)

insert.funcionario(
    ultimo_departamento,
    ultimo_especialidade,
    'José da Silva',
    '2024-01-15',
    '2024-08-25',
    'Rua do Operário, 10',
)
ultimo_funcionario = insert.cursor.lastrowid
print('FUNCIONARIO:', ultimo_funcionario)

insert.veiculo(ultimo_cliente, 'ABC1D23', 'Celta', 'Chevrolet', '9BG1324SSS1234567')
ultimo_veiculo = insert.cursor.lastrowid
print('VEICULO:', ultimo_veiculo)

insert.produto(
    ultimo_fornecedor,
    'Filtro de ar',
    'Óleo',
    10,
    25.0,
)
ultimo_produto = insert.cursor.lastrowid
print('PRODUTO:', ultimo_produto)

insert.estoque(
    ultimo_fornecedor,
    ultimo_produto,
    10,
    5,
    '2027-08-01',
    365,
)
print('ESTOQUE: registro criado para o produto', ultimo_produto)

data_conclusao = datetime.datetime(2026, 8, 3)
data_inicio = datetime.datetime(2026, 8, 1)
tempo_total_dias = (data_conclusao - data_inicio).days

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

insert.feedback(ultimo_cliente, 9, 'Atendimento excelente', '2026-08-04')
ultimo_feedback = insert.cursor.lastrowid
print('FEEDBACK:', ultimo_feedback)

ultimo_pagamento = insert.pagamento(
    ultimo_cliente,
    ultimo_os,
    None,
    'PIX',
    2,
    '2026-08-03',
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

insert.conta_pagar('Compra de filtro de ar', 150.0, '2026-08-20', 'Pendente')
ultimo_conta_pagar = insert.cursor.lastrowid
print('CONTA_PAGAR:', ultimo_conta_pagar)

insert.atendimento(ultimo_cliente, ultimo_funcionario, '2026-08-04')
ultimo_atendimento = insert.cursor.lastrowid
print('ATENDIMENTO:', ultimo_atendimento)

insert.agenciamento_veiculo(
    ultimo_cliente,
    ultimo_veiculo,
    '2026-08-05',
    300.0,
    7,
    30.0,
    'Pendente',
)
ultimo_agenciamento = insert.cursor.lastrowid
print('AGENCIAMENTO_VEICULO:', ultimo_agenciamento)

data_pagamento = datetime.datetime(2026, 5, 4)
insert.folha_pagamento(
    ultimo_funcionario,
    'Pago',
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
