"""
Inicialização do Banco de Dados SQLite
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_database():
    """Cria as tabelas e insere dados iniciais"""
    # Remover banco antigo se existir
    if os.path.exists(DB_PATH):
        print(f"⚠️  Removendo banco existente: {DB_PATH}")
        os.remove(DB_PATH)
    
    # Conectar ao banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Executar schema.sql
    print("📁 Criando tabelas...")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
    
    # Inserir usuário administrador
    print("👤 Criando usuário administrador...")
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO users (name, email, password_hash, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('Administrador', 'admin@chat.com', admin_password, 1))
    admin_id = cursor.lastrowid
    
    # Inserir usuário de teste
    print("👤 Criando usuário de teste...")
    test_password = generate_password_hash('teste123')
    cursor.execute('''
        INSERT INTO users (name, email, password_hash, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('João Silva', 'joao@chat.com', test_password, 0))
    user_id = cursor.lastrowid
    
    # Criar grupo de teste
    print("👥 Criando grupo de teste...")
    cursor.execute('''
        INSERT INTO groups (name, description, owner_id)
        VALUES (?, ?, ?)
    ''', ('Grupo Geral', 'Grupo de boas-vindas', admin_id))
    group_id = cursor.lastrowid
    
    # Adicionar membros ao grupo
    print("➕ Adicionando membros ao grupo...")
    cursor.execute('''
        INSERT INTO group_members (group_id, user_id, role)
        VALUES (?, ?, ?)
    ''', (group_id, admin_id, 'admin'))
    
    cursor.execute('''
        INSERT INTO group_members (group_id, user_id, role)
        VALUES (?, ?, ?)
    ''', (group_id, user_id, 'member'))
    
    # Inserir mensagem de boas-vindas
    print("💬 Criando mensagem de boas-vindas...")
    cursor.execute('''
        INSERT INTO messages (group_id, user_id, content)
        VALUES (?, ?, ?)
    ''', (group_id, admin_id, 'Bem-vindo ao sistema de chat colaborativo! 🎉'))
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados criado com sucesso!")
    print(f"📍 Localização: {DB_PATH}")
    print("\n🔐 Credenciais de acesso:")
    print("   Admin: admin@chat.com / admin123")
    print("   Teste: joao@chat.com / teste123")

if __name__ == '__main__':
    init_database()

