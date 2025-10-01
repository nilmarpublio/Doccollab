#!/usr/bin/env python3
"""
Script para resolver conflitos de histórico Git no PythonAnywhere
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
    print("🔧 Resolvendo conflitos de histórico Git...")
    
    # Comandos para resolver o problema
    commands = [
        # 1. Fazer backup do branch atual
        "git branch backup-$(date +%Y%m%d-%H%M%S)",
        
        # 2. Forçar o pull com --allow-unrelated-histories
        "git pull origin master --allow-unrelated-histories",
        
        # 3. Se ainda houver conflitos, fazer merge
        "git merge origin/master --allow-unrelated-histories",
        
        # 4. Verificar status
        "git status",
        
        # 5. Mostrar histórico
        "git log --oneline -10"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n📋 Executando comando {i}/{len(commands)}: {command}")
        
        success, stdout, stderr = run_command(command)
        
        if success:
            print(f"✅ Sucesso: {stdout}")
        else:
            print(f"❌ Erro: {stderr}")
            
            # Se for o comando de pull, tentar estratégia alternativa
            if "pull" in command:
                print("\n🔄 Tentando estratégia alternativa...")
                
                # Estratégia alternativa: reset hard
                alt_commands = [
                    "git fetch origin master",
                    "git reset --hard origin/master",
                    "git status"
                ]
                
                for alt_cmd in alt_commands:
                    print(f"📋 Executando: {alt_cmd}")
                    success, stdout, stderr = run_command(alt_cmd)
                    if success:
                        print(f"✅ Sucesso: {stdout}")
                    else:
                        print(f"❌ Erro: {stderr}")
                break
    
    print("\n🎉 Processo concluído!")
    print("\n📋 Próximos passos:")
    print("1. Verifique se os arquivos estão corretos")
    print("2. Execute: python3.10 update_db_versions.py")
    print("3. Execute: python3.10 update_db_chat.py")
    print("4. Configure o .env com as variáveis de produção")
    print("5. Reinicie a aplicação no PythonAnywhere")

if __name__ == "__main__":
    main()
