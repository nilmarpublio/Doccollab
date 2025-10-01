#!/usr/bin/env python3
"""
Script para resolver problemas de permissão Git no PythonAnywhere
DocCollab - Deploy Final
"""

import subprocess
import sys
import os

def run_command(command, cwd=None):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 Resolvendo problemas de permissão Git...")
    
    # Comandos para resolver o problema
    commands = [
        # 1. Verificar status atual
        "git status",
        
        # 2. Limpar cache do Git
        "git rm -r --cached .",
        
        # 3. Adicionar arquivos novamente
        "git add .",
        
        # 4. Verificar se há arquivos problemáticos
        "find . -name '.gitignore' -type f",
        
        # 5. Remover arquivos .gitignore problemáticos se existirem
        "find . -name '.gitignore' -type f -delete",
        
        # 6. Adicionar arquivos novamente
        "git add .",
        
        # 7. Verificar status final
        "git status",
        
        # 8. Fazer commit se necessário
        "git commit -m 'Fix git permissions and add all files'",
        
        # 9. Push para o repositório
        "git push origin master"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n📋 Executando comando {i}/{len(commands)}: {command}")
        
        success, stdout, stderr = run_command(command)
        
        if success:
            print(f"✅ Sucesso: {stdout}")
        else:
            print(f"❌ Erro: {stderr}")
            
            # Se for um erro de permissão, tentar resolver
            if "Permission denied" in stderr:
                print("\n🔄 Tentando resolver problema de permissão...")
                
                # Comandos para resolver permissões
                perm_commands = [
                    "chmod -R 755 .",
                    "chown -R $USER:$USER .",
                    "git config --global --add safe.directory .",
                    "git add ."
                ]
                
                for perm_cmd in perm_commands:
                    print(f"📋 Executando: {perm_cmd}")
                    success, stdout, stderr = run_command(perm_cmd)
                    if success:
                        print(f"✅ Sucesso: {stdout}")
                    else:
                        print(f"❌ Erro: {stderr}")
    
    print("\n🎉 Processo concluído!")
    print("\n📋 Próximos passos:")
    print("1. Verifique se o git status está limpo")
    print("2. Execute: python3.10 update_db_versions.py")
    print("3. Execute: python3.10 update_db_chat.py")
    print("4. Configure o .env com as variáveis de produção")
    print("5. Reinicie a aplicação no PythonAnywhere")

if __name__ == "__main__":
    main()
