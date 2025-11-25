import sqlite3
import hashlib

def iniciar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_usuario(usuario, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    try:
        cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha_hash))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Nome de usuário já existe."
    finally:
        conn.close()

def verificar_usuario(usuario, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha_hash))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return True, "Login realizado com sucesso!"
    else:
        return False, "Usuário ou senha incorretos."

# Inicializa o banco ao importar o módulo
iniciar_banco()
