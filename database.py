import sqlite3

conn = sqlite3.connect('financeiro.db')

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        tipo TEXT NOT NULL,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    );
""")

categorias_iniciais = [
    ('Salário',),
    ('Alimentação',),
    ('Transporte',),
    ('Moradia',),
    ('Lazer',),
    ('Outras Receitas',),
    ('Outras Despesas',)
]

cursor.executemany("INSERT OR IGNORE INTO categorias (nome) VALUES (?)", categorias_iniciais)


conn.commit()
conn.close()

print("\nBanco de dados criado e configurado com sucesso!")
