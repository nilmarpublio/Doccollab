#!/usr/bin/env python3
"""
Script para criar ambiente virtual e instalar dependências no PythonAnywhere
DocCollab - Deploy Final
"""

import sys
import os
import subprocess
import platform

def run_command(command):
    """Executar comando e retornar resultado"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_file_exists(file_path):
    """Verificar se arquivo existe"""
    return os.path.exists(file_path)

def main():
    print("🔧 Criando ambiente virtual e instalando dependências...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Execute este script no diretório raiz do DocCollab")
        sys.exit(1)
    
    print("\n📋 1. Verificando Python...")
    success, stdout, stderr = run_command("python3.10 --version")
    if success:
        print(f"✅ Python 3.10 encontrado: {stdout.strip()}")
    else:
        print("❌ Python 3.10 não encontrado")
        print("💡 Tentando com python3...")
        success, stdout, stderr = run_command("python3 --version")
        if success:
            print(f"✅ Python 3 encontrado: {stdout.strip()}")
            python_cmd = "python3"
        else:
            print("❌ Python 3 não encontrado")
            sys.exit(1)
    else:
        python_cmd = "python3.10"
    
    print(f"\n📋 2. Criando ambiente virtual com {python_cmd}...")
    success, stdout, stderr = run_command(f"{python_cmd} -m venv venv")
    if success:
        print("✅ Ambiente virtual criado com sucesso")
    else:
        print(f"❌ Falha ao criar ambiente virtual: {stderr}")
        sys.exit(1)
    
    print("\n📋 3. Verificando estrutura do ambiente virtual...")
    if check_file_exists("venv/bin/activate"):
        print("✅ Arquivo de ativação encontrado")
    else:
        print("❌ Arquivo de ativação não encontrado")
        sys.exit(1)
    
    print("\n📋 4. Ativando ambiente virtual...")
    # No Windows, o comando é diferente
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"💡 Execute manualmente: {activate_cmd}")
    
    print("\n📋 5. Verificando pip...")
    success, stdout, stderr = run_command(f"{python_cmd} -m pip --version")
    if success:
        print(f"✅ pip encontrado: {stdout.strip()}")
    else:
        print(f"❌ pip não encontrado: {stderr}")
        sys.exit(1)
    
    print("\n📋 6. Atualizando pip...")
    success, stdout, stderr = run_command(f"{python_cmd} -m pip install --upgrade pip")
    if success:
        print("✅ pip atualizado com sucesso")
    else:
        print(f"⚠️  Falha ao atualizar pip: {stderr}")
    
    print("\n📋 7. Verificando requirements.txt...")
    if check_file_exists("requirements.txt"):
        print("✅ requirements.txt encontrado")
        
        print("\n📋 8. Instalando dependências...")
        success, stdout, stderr = run_command(f"{python_cmd} -m pip install -r requirements.txt")
        if success:
            print("✅ Dependências instaladas com sucesso")
        else:
            print(f"❌ Falha ao instalar dependências: {stderr}")
            print("💡 Tentando instalar dependências individualmente...")
            
            # Lista de dependências essenciais
            dependencies = [
                "flask==2.3.3",
                "flask-socketio==5.3.6",
                "flask-sqlalchemy==3.0.5",
                "flask-babel==4.0.0",
                "flask-login==0.6.3",
                "python-dotenv==1.0.0",
                "babel==2.17.0",
                "pytz==2025.2",
                "click==8.3.0",
                "itsdangerous==2.2.0",
                "jinja2==3.1.6",
                "markupsafe==3.0.3",
                "werkzeug==2.3.7",
                "blinker==1.9.0",
                "colorama==0.4.6",
                "greenlet==3.2.4",
                "sqlalchemy==2.0.43",
                "typing-extensions==4.15.0"
            ]
            
            for dep in dependencies:
                print(f"💡 Instalando {dep}...")
                success, stdout, stderr = run_command(f"{python_cmd} -m pip install {dep}")
                if success:
                    print(f"✅ {dep} instalado")
                else:
                    print(f"❌ Falha ao instalar {dep}: {stderr}")
    else:
        print("❌ requirements.txt não encontrado")
        print("💡 Criando requirements.txt...")
        
        requirements_content = """flask==2.3.3
flask-socketio==5.3.6
flask-sqlalchemy==3.0.5
flask-babel==4.0.0
flask-login==0.6.3
python-dotenv==1.0.0
babel==2.17.0
pytz==2025.2
click==8.3.0
itsdangerous==2.2.0
jinja2==3.1.6
markupsafe==3.0.3
werkzeug==2.3.7
blinker==1.9.0
colorama==0.4.6
greenlet==3.2.4
sqlalchemy==2.0.43
typing-extensions==4.15.0"""
        
        try:
            with open("requirements.txt", "w") as f:
                f.write(requirements_content)
            print("✅ requirements.txt criado")
        except Exception as e:
            print(f"❌ Falha ao criar requirements.txt: {e}")
    
    print("\n📋 9. Verificando instalação...")
    success, stdout, stderr = run_command(f"{python_cmd} -c \"import flask; print('✅ Flask OK')\"")
    if success:
        print("✅ Flask importado com sucesso")
    else:
        print(f"❌ Falha ao importar Flask: {stderr}")
    
    print("\n📋 10. Testando aplicação...")
    success, stdout, stderr = run_command(f"{python_cmd} -c \"from app import create_app; print('✅ App import OK')\"")
    if success:
        print("✅ Aplicação importada com sucesso")
    else:
        print(f"❌ Falha ao importar aplicação: {stderr}")
        print("💡 Verifique se todos os arquivos existem")
    
    print("\n🎉 Ambiente virtual criado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Ative o ambiente virtual:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Execute: python update_db_versions.py")
    print("3. Execute: python update_db_chat.py")
    print("4. Configure o WSGI no PythonAnywhere")
    print("5. Reinicie a aplicação")
    print("\n🚀 DocCollab está pronto para produção!")

if __name__ == "__main__":
    main()
