import sqlite3
import hashlib
import os
from datetime import datetime

# Caminho absoluto para o banco de dados
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'usuarios.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def recriar_banco():
    """Remove e recria o banco de dados com a estrutura atualizada"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    iniciar_banco()
    print(f"Banco recriado em: {DB_PATH}")

def iniciar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de usuários (com tipo: supervisor ou funcionario)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'funcionario',
            ativo INTEGER DEFAULT 1,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de registro de ponto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_ponto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora_entrada TEXT,
            hora_saida TEXT,
            status TEXT DEFAULT 'offline',
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabela de escalas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escalas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            turno TEXT NOT NULL,
            tipo TEXT DEFAULT 'trabalho',
            aprovado INTEGER DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    # Tabela de notificações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Tabela de feedbacks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            resposta TEXT,
            data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            data_resposta TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== USUÁRIOS ====================

def cadastrar_usuario(usuario, senha, nome_completo, tipo='funcionario'):
    conn = get_connection()
    cursor = conn.cursor()
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    try:
        cursor.execute('''
            INSERT INTO usuarios (usuario, senha, nome_completo, tipo) 
            VALUES (?, ?, ?, ?)
        ''', (usuario, senha_hash, nome_completo, tipo))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Nome de usuário já existe."
    finally:
        conn.close()

def atualizar_usuario(usuario_id, nome_completo, usuario, senha=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if senha:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            cursor.execute('''
                UPDATE usuarios 
                SET nome_completo = ?, usuario = ?, senha = ?
                WHERE id = ?
            ''', (nome_completo, usuario, senha_hash, usuario_id))
        else:
            cursor.execute('''
                UPDATE usuarios 
                SET nome_completo = ?, usuario = ?
                WHERE id = ?
            ''', (nome_completo, usuario, usuario_id))
            
        conn.commit()
        return True, "Usuário atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Nome de usuário já existe."
    except Exception as e:
        return False, f"Erro ao atualizar: {str(e)}"
    finally:
        conn.close()

def deletar_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Soft delete (apenas desativa)
        cursor.execute('UPDATE usuarios SET ativo = 0 WHERE id = ?', (usuario_id,))
        conn.commit()
        return True, "Usuário removido com sucesso!"
    except Exception as e:
        return False, f"Erro ao remover: {str(e)}"
    finally:
        conn.close()

def verificar_usuario(usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    cursor.execute('''
        SELECT id, usuario, nome_completo, tipo 
        FROM usuarios 
        WHERE usuario = ? AND senha = ? AND ativo = 1
    ''', (usuario, senha_hash))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return True, "Login realizado com sucesso!", {
            'id': user[0],
            'usuario': user[1],
            'nome': user[2],
            'tipo': user[3]
        }
    else:
        return False, "Usuário ou senha incorretos.", None

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, usuario, nome_completo, tipo FROM usuarios WHERE ativo = 1')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, usuario, nome_completo, tipo 
        FROM usuarios 
        WHERE tipo = 'funcionario' AND ativo = 1
    ''')
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def buscar_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# ==================== NOTIFICAÇÕES ====================

def criar_notificacao(usuario_id, mensagem):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO notificacoes (usuario_id, mensagem) VALUES (?, ?)', (usuario_id, mensagem))
        conn.commit()
    finally:
        conn.close()

def listar_notificacoes(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, mensagem, data_criacao 
        FROM notificacoes 
        WHERE usuario_id = ? AND lida = 0 
        ORDER BY data_criacao DESC
    ''', (usuario_id,))
    notificacoes = cursor.fetchall()
    conn.close()
    return notificacoes

def marcar_notificacao_lida(notificacao_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE notificacoes SET lida = 1 WHERE id = ?', (notificacao_id,))
    conn.commit()
    conn.close()

# ==================== RELATÓRIOS ====================

def exportar_relatorio_ponto():
    """Retorna dados para relatório CSV: Nome, Data, Entrada, Saída"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.nome_completo, rp.data, rp.hora_entrada, rp.hora_saida
        FROM registros_ponto rp
        JOIN usuarios u ON rp.usuario_id = u.id
        ORDER BY rp.data DESC, u.nome_completo
    ''')
    dados = cursor.fetchall()
    conn.close()
    return dados

# ==================== FEEDBACKS ====================

def enviar_feedback(usuario_id, mensagem):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO feedbacks (usuario_id, mensagem) VALUES (?, ?)', (usuario_id, mensagem))
        conn.commit()
        return True, "Feedback enviado com sucesso!"
    except Exception as e:
        return False, f"Erro ao enviar: {str(e)}"
    finally:
        conn.close()

def responder_feedback(id, resposta):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE feedbacks 
            SET resposta = ?, data_resposta = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (resposta, id))
        conn.commit()
        return True, "Resposta enviada com sucesso!"
    except Exception as e:
        return False, f"Erro ao responder: {str(e)}"
    finally:
        conn.close()

def listar_feedbacks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.id, u.nome_completo, f.mensagem, f.data_criacao, f.resposta, f.data_resposta
        FROM feedbacks f
        JOIN usuarios u ON f.usuario_id = u.id
        ORDER BY f.data_criacao DESC
    ''')
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def listar_meus_feedbacks(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT mensagem, data_criacao, resposta, data_resposta
        FROM feedbacks
        WHERE usuario_id = ?
        ORDER BY data_criacao DESC
    ''', (usuario_id,))
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

# ==================== REGISTRO DE PONTO ====================

def bater_ponto_entrada(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    hora_atual = datetime.now().strftime('%H:%M:%S')
    
    # Verificar se já existe registro de hoje
    cursor.execute('''
        SELECT id FROM registros_ponto 
        WHERE usuario_id = ? AND data = ? AND hora_saida IS NULL
    ''', (usuario_id, data_hoje))
    registro = cursor.fetchone()
    
    if registro:
        conn.close()
        return False, "Você já bateu o ponto de entrada hoje!"
    
    try:
        cursor.execute('''
            INSERT INTO registros_ponto (usuario_id, data, hora_entrada, status) 
            VALUES (?, ?, ?, 'online')
        ''', (usuario_id, data_hoje, hora_atual))
        conn.commit()
        return True, f"Ponto de entrada registrado às {hora_atual}"
    except Exception as e:
        return False, f"Erro ao registrar ponto: {str(e)}"
    finally:
        conn.close()

def bater_ponto_saida(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    hora_atual = datetime.now().strftime('%H:%M:%S')
    
    # Buscar registro de entrada de hoje sem saída
    cursor.execute('''
        SELECT id FROM registros_ponto 
        WHERE usuario_id = ? AND data = ? AND hora_saida IS NULL
    ''', (usuario_id, data_hoje))
    registro = cursor.fetchone()
    
    if not registro:
        conn.close()
        return False, "Você precisa bater o ponto de entrada primeiro!"
    
    try:
        cursor.execute('''
            UPDATE registros_ponto 
            SET hora_saida = ?, status = 'offline'
            WHERE id = ?
        ''', (hora_atual, registro[0]))
        conn.commit()
        return True, f"Ponto de saída registrado às {hora_atual}"
    except Exception as e:
        return False, f"Erro ao registrar ponto: {str(e)}"
    finally:
        conn.close()

def verificar_status_ponto(usuario_id):
    """Retorna 'online' se o funcionário bateu entrada mas não saída, senão 'offline'"""
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT status FROM registros_ponto 
        WHERE usuario_id = ? AND data = ? AND hora_saida IS NULL
    ''', (usuario_id, data_hoje))
    registro = cursor.fetchone()
    
    conn.close()
    
    if registro:
        return 'online'
    return 'offline'

def listar_funcionarios_online():
    """Lista todos os funcionários que estão com ponto aberto (online)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT u.id, u.nome_completo, u.usuario, rp.hora_entrada
        FROM registros_ponto rp
        JOIN usuarios u ON rp.usuario_id = u.id
        WHERE rp.data = ? AND rp.hora_saida IS NULL AND rp.status = 'online'
        ORDER BY rp.hora_entrada
    ''', (data_hoje,))
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def listar_funcionarios_offline():
    """Lista funcionários que já bateram saída hoje"""
    conn = get_connection()
    cursor = conn.cursor()
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT u.id, u.nome_completo, u.usuario, rp.hora_entrada, rp.hora_saida
        FROM registros_ponto rp
        JOIN usuarios u ON rp.usuario_id = u.id
        WHERE rp.data = ? AND rp.hora_saida IS NOT NULL
        ORDER BY rp.hora_saida DESC
    ''', (data_hoje,))
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def obter_historico_ponto(usuario_id, limite=30):
    """Retorna histórico de ponto do funcionário"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT data, hora_entrada, hora_saida, status
        FROM registros_ponto 
        WHERE usuario_id = ?
        ORDER BY data DESC, hora_entrada DESC
        LIMIT ?
    ''', (usuario_id, limite))
    historico = cursor.fetchall()
    conn.close()
    return historico

# ==================== ESCALAS ====================

def adicionar_escala(usuario_id, data, turno, tipo="trabalho"):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO escalas (usuario_id, data, turno, tipo) 
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, data, turno, tipo))
        conn.commit()
        return True, "Escala adicionada com sucesso!"
    except Exception as e:
        return False, f"Erro ao adicionar escala: {str(e)}"
    finally:
        conn.close()

def listar_escalas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.id, u.nome_completo, e.data, e.turno, e.tipo, e.aprovado 
        FROM escalas e 
        JOIN usuarios u ON e.usuario_id = u.id
        ORDER BY e.data
    ''')
    escalas = cursor.fetchall()
    conn.close()
    return escalas

def listar_escalas_funcionario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, data, turno, tipo, aprovado 
        FROM escalas 
        WHERE usuario_id = ?
        ORDER BY data
    ''', (usuario_id,))
    escalas = cursor.fetchall()
    conn.close()
    return escalas

def aprovar_escala(escala_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE escalas SET aprovado = 1 WHERE id = ?', (escala_id,))
        conn.commit()
        return True, "Escala aprovada com sucesso!"
    except Exception as e:
        return False, f"Erro ao aprovar escala: {str(e)}"
    finally:
        conn.close()

# ==================== HELPERS NOTIFICAÇÕES ====================

def obter_usuario_id_por_feedback(feedback_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT usuario_id FROM feedbacks WHERE id = ?', (feedback_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def obter_usuario_id_por_escala(escala_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT usuario_id FROM escalas WHERE id = ?', (escala_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Inicializa o banco ao importar o módulo
iniciar_banco()
