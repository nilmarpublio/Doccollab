#!/usr/bin/env python3
"""
Script para corrigir traduções no PythonAnywhere
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔧 {description}")
    print(f"Comando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/123nilmarcastro/doccollab')
        if result.returncode == 0:
            print(f"✅ Sucesso: {result.stdout}")
        else:
            print(f"❌ Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False
    return True

def main():
    print("🚀 CORRIGINDO TRADUÇÕES NO PYTHONANYWHERE")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('/home/123nilmarcastro/doccollab'):
        print("❌ Diretório /home/123nilmarcastro/doccollab não encontrado!")
        return
    
    # Ativar ambiente virtual
    print("\n1. Ativando ambiente virtual...")
    os.environ['PATH'] = '/home/123nilmarcastro/doccollab/venv/bin:' + os.environ['PATH']
    os.environ['VIRTUAL_ENV'] = '/home/123nilmarcastro/doccollab/venv'
    
    # Verificar se pybabel está instalado
    if not run_command('which pybabel', 'Verificando pybabel'):
        print("❌ pybabel não encontrado. Instalando...")
        if not run_command('pip install babel', 'Instalando babel'):
            return
    
    # Verificar estrutura de traduções
    print("\n2. Verificando estrutura de traduções...")
    translations_dir = '/home/123nilmarcastro/doccollab/translations'
    if not os.path.exists(translations_dir):
        print("❌ Diretório translations não encontrado!")
        return
    
    # Listar conteúdo do diretório translations
    run_command('ls -la translations/', 'Conteúdo do diretório translations')
    
    # Verificar se existem arquivos .po
    run_command('find translations/ -name "*.po"', 'Procurando arquivos .po')
    
    # Tentar compilar traduções
    print("\n3. Compilando traduções...")
    if not run_command('pybabel compile -d translations -D messages', 'Compilando traduções'):
        print("\n4. Tentando extrair strings primeiro...")
        if run_command('pybabel extract -F babel.cfg -k _l -o messages.pot .', 'Extraindo strings'):
            print("\n5. Atualizando arquivos .po...")
            for lang in ['pt', 'en', 'es']:
                po_file = f'translations/{lang}/LC_MESSAGES/messages.po'
                if os.path.exists(po_file):
                    run_command(f'pybabel update -i messages.pot -d translations -l {lang}', f'Atualizando {lang}')
                else:
                    print(f"⚠️ Arquivo {po_file} não encontrado")
            
            print("\n6. Compilando traduções novamente...")
            run_command('pybabel compile -d translations -D messages', 'Compilando traduções')
    
    # Verificar se a aplicação funciona
    print("\n7. Testando aplicação...")
    if run_command('python -c "from app import create_app; app, socketio = create_app(); print(\'✅ App OK\')"', 'Testando aplicação'):
        print("\n🎉 SUCESSO! Aplicação funcionando!")
    else:
        print("\n❌ Aplicação com problemas. Verifique os logs.")
    
    print("\n" + "=" * 50)
    print("✅ Script de correção concluído!")

if __name__ == "__main__":
    main()
