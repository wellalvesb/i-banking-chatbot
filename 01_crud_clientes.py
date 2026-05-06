# INFRAESTRUTURA RELACIONAL E CADASTRO COMPLETO (CRUD) - OPERADORA DE CRÉDITO
import sqlite3

DATABASE_NAME = 'operadora_fmu.db'

# 1. CREATE: Criação da Tabela (DDL)
conexao = sqlite3.connect(DATABASE_NAME)
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        vencimento_fatura TEXT NOT NULL
    )
''')

conexao.commit()
conexao.close()
print("--- SISTEMA DE GESTÃO: OPERADORA DE CRÉDITO ---")
print("[LOG DB] Tabela 'clientes' verificada/criada.")

# 2. INSERT: Cadastro de Cliente via Terminal (DML)
print("\n--- CADASTRO DE NOVO CLIENTE ---")
nome_in = input("Digite o nome: ").strip()
idade_in = input("Digite a idade: ").strip()
fatura_in = input("Vencimento (Ex: Dia 10): ").strip()

conexao = sqlite3.connect(DATABASE_NAME)
cursor = conexao.cursor()

try:
    cursor.execute('''
        INSERT INTO clientes (nome, idade, vencimento_fatura)
        VALUES (?, ?, ?)
    ''', (nome_in, int(idade_in), fatura_in))
    conexao.commit()
    print(f"[LOG DB] SUCESSO: Cliente '{nome_in}' cadastrado.")
except ValueError:
    print("[ERRO] Idade deve ser um número!")
finally:
    conexao.close()

# 3. SELECT: Listagem Geral (READ)
conexao = sqlite3.connect(DATABASE_NAME)
cursor = conexao.cursor()

print("\n--- BASE DE CLIENTES ATIVA ---")
cursor.execute('SELECT * FROM clientes')
dados = cursor.fetchall()
for d in dados:
    print(f"ID: {d[0]} | Nome: {d[1]} | Idade: {d[2]} | Fatura: {d[3]}")

conexao.close()

# 4. UPDATE: Demonstração de Atualização (Simulando alteração de vencimento do ID 1)
print("\n--- ATUALIZAÇÃO (SIMULAÇÃO) ---")
try:
    # Vamos atualizar o vencimento para 'Dia 15' do primeiro cliente (ID: 1)
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()
    cursor.execute('UPDATE clientes SET vencimento_fatura = ? WHERE id = ?', ('Dia 15', 1))
    conexao.commit()
    print("[LOG DB] Vencimento do ID 1 alterado para 'Dia 15'.")
except sqlite3.Error as e:
    print(f"[ERRO] Falha ao atualizar: {e}")
finally:
    conexao.close()

# 5. DELETE: Demonstração de Exclusão (Simulando remoção por Nome)
print("\n--- EXCLUSÃO (SIMULAÇÃO) ---")
nome_del = input("Para simular um DELETE, digite o NOME de um cliente (ou deixe vazio para pular): ").strip()

if nome_del:
    conexao = sqlite3.connect(DATABASE_NAME)
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM clientes WHERE nome = ?', (nome_del,))
    conexao.commit()
    print(f"[LOG DB] Registros com nome '{nome_del}' removidos.")
    conexao.close()

# 6. SELECT FINAL: Estado Final do Banco
conexao = sqlite3.connect(DATABASE_NAME)
cursor = conexao.cursor()
print("\n--- ESTADO FINAL DA BASE DE DADOS ---")
cursor.execute('SELECT * FROM clientes')
print(cursor.fetchall())
conexao.close()
