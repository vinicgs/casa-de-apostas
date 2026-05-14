import sqlite3

def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    # Tabela de Usuários (Acesso)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Tabela de Clientes
    conn.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            emails TEXT,
            phones TEXT,
            registration_date TEXT NOT NULL
        )
    ''')
    # Tabela de Contatos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            id TEXT PRIMARY KEY,
            client_id TEXT NOT NULL,
            full_name TEXT NOT NULL,
            emails TEXT,
            phones TEXT,
            FOREIGN KEY (client_id) REFERENCES client(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
