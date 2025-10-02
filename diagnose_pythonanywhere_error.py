#!/usr/bin/env python3
"""
Script de diagnóstico completo para PythonAnywhere
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔍 {description}")
    print(f"Comando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/123nilmarcastro/doccollab')
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

def check_file_exists(filepath, description):
    """Verifica se um arquivo existe"""
    print(f"\n📁 {description}")
    if os.path.exists(filepath):
        print(f"✅ {filepath} existe")
        return True
    else:
        print(f"❌ {filepath} NÃO existe")
        return False

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DO PYTHONANYWHERE")
    print("=" * 60)
    
    # Verificar diretório
    print(f"\n1. Verificando diretório atual: {os.getcwd()}")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('/home/123nilmarcastro/doccollab'):
        print("❌ Diretório /home/123nilmarcastro/doccollab não encontrado!")
        print("Execute: cd ~/doccollab")
        return
    
    # Verificar arquivos essenciais
    print("\n2. Verificando arquivos essenciais...")
    essential_files = [
        ('app.py', 'Arquivo principal da aplicação'),
        ('requirements.txt', 'Dependências'),
        ('babel.cfg', 'Configuração do Babel'),
        ('wsgi.py', 'Configuração WSGI'),
        ('models/__init__.py', 'Módulo models'),
        ('routes/__init__.py', 'Módulo routes'),
        ('services/asaas_integration.py', 'Integração ASAAS')
    ]
    
    missing_files = []
    for filepath, description in essential_files:
        if not check_file_exists(f'/home/123nilmarcastro/doccollab/{filepath}', description):
            missing_files.append(filepath)
    
    # Verificar ambiente virtual
    print("\n3. Verificando ambiente virtual...")
    venv_path = '/home/123nilmarcastro/doccollab/venv'
    if os.path.exists(venv_path):
        print("✅ Ambiente virtual existe")
        run_command('ls -la venv/bin/', 'Conteúdo do venv/bin')
    else:
        print("❌ Ambiente virtual não encontrado!")
        print("Execute: python3.10 -m venv venv")
        return
    
    # Ativar ambiente virtual e verificar Python
    print("\n4. Verificando Python e dependências...")
    os.environ['PATH'] = '/home/123nilmarcastro/doccollab/venv/bin:' + os.environ['PATH']
    os.environ['VIRTUAL_ENV'] = '/home/123nilmarcastro/doccollab/venv'
    
    run_command('python --version', 'Versão do Python')
    run_command('pip list', 'Pacotes instalados')
    
    # Verificar dependências específicas
    print("\n5. Verificando dependências específicas...")
    dependencies = ['flask', 'flask-sqlalchemy', 'flask-login', 'flask-babel', 'requests', 'flask-socketio']
    for dep in dependencies:
        run_command(f'pip show {dep}', f'Verificando {dep}')
    
    # Verificar traduções
    print("\n6. Verificando traduções...")
    run_command('ls -la translations/', 'Estrutura de traduções')
    run_command('find translations/ -name "*.mo"', 'Arquivos .mo compilados')
    
    # Tentar importar módulos
    print("\n7. Testando importações...")
    test_imports = [
        'import flask',
        'import flask_sqlalchemy',
        'import flask_login',
        'import flask_babel',
        'import requests',
        'import flask_socketio'
    ]
    
    for import_cmd in test_imports:
        run_command(f'python -c "{import_cmd}; print(\'✅ {import_cmd} OK\')"', f'Testando {import_cmd}')
    
    # Tentar importar a aplicação
    print("\n8. Testando importação da aplicação...")
    run_command('python -c "from app import create_app; print(\'✅ App import OK\')"', 'Importando app')
    
    # Verificar logs de erro
    print("\n9. Verificando logs de erro...")
    error_log = '/var/log/123nilmarcastro.pythonanywhere.com.error.log'
    if os.path.exists(error_log):
        run_command(f'tail -20 {error_log}', 'Últimas 20 linhas do log de erro')
    else:
        print("❌ Log de erro não encontrado")
    
    # Verificar configuração WSGI
    print("\n10. Verificando configuração WSGI...")
    if os.path.exists('/home/123nilmarcastro/doccollab/wsgi.py'):
        run_command('cat wsgi.py', 'Conteúdo do wsgi.py')
    
    # Verificar variáveis de ambiente
    print("\n11. Verificando variáveis de ambiente...")
    env_vars = ['SECRET_KEY', 'DATABASE_URL', 'PDFLATEX', 'ASAAS_API_KEY']
    for var in env_vars:
        value = os.environ.get(var, 'NÃO DEFINIDA')
        print(f"{var}: {'***' if value != 'NÃO DEFINIDA' else 'NÃO DEFINIDA'}")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO CONCLUÍDO!")
    
    if missing_files:
        print(f"\n❌ ARQUIVOS FALTANDO: {', '.join(missing_files)}")
        print("Execute: git pull origin master")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Verifique os erros acima")
    print("2. Execute os comandos de correção sugeridos")
    print("3. Reinicie a aplicação web no PythonAnywhere")

if __name__ == "__main__":
    main()
