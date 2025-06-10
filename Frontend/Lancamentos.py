import sqlite3

# Conectar (cria o arquivo se não existir)
conn = sqlite3.connect("Lancamentos.db")
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lancamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Tipo TEXT NOT NULL,
        Data DATE NOT NULL,
        Descricao TEXT NOT NULL,
        Valor REAL NOT NULL,
        Metodo TEXT NOT NULL
    )
""")

conn.commit()
print("Tabela verificada/criada com sucesso.")

# Agora lista as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabelas encontradas:", cursor.fetchall())

conn.close()
