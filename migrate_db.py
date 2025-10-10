"""
Script para migrar o banco de dados e adicionar as novas tabelas
"""
from app import app, db

def migrate_database():
    """Cria as novas tabelas no banco de dados"""
    with app.app_context():
        print("Criando tabelas...")
        db.create_all()
        print("OK - Tabelas criadas com sucesso!")
        print("\nTabelas disponiveis:")
        print("- users")
        print("- projects")
        print("- project_folders (NOVA)")
        print("- project_files (NOVA)")
        print("- file_versions (NOVA)")

if __name__ == '__main__':
    migrate_database()
