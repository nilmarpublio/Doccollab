# 🔧 SOLUÇÃO MANUAL - Arquivos Ausentes

## 🚨 PROBLEMA IDENTIFICADO
```
ls: cannot access 'update_db_*.py': No such file or directory
```

Os arquivos de atualização do banco de dados não existem no PythonAnywhere.

## 🚀 SOLUÇÃO IMEDIATA

### **Passo 1: Verificar se o Código foi Atualizado**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar status do Git
git status

# Verificar último commit
git log --oneline -3

# Fazer pull manual
git pull origin main
```

### **Passo 2: Se o Git Pull Falhar**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se há mudanças não commitadas
git status

# Se houver conflitos, resolver
git stash
git pull origin main
git stash pop
```

### **Passo 3: Se Ainda Não Funcionar - Clone Limpo**
```bash
# No console bash do PythonAnywhere
cd ~

# Fazer backup do diretório atual
mv DocCollab DocCollab-backup-$(date +%Y%m%d-%H%M%S)

# Clonar o repositório novamente
git clone https://github.com/nilmarpublio/Doccollab.git DocCollab

# Entrar no diretório
cd DocCollab

# Verificar se os arquivos existem
ls -la update_db_*.py
```

### **Passo 4: Criar Arquivos Manualmente (Se Necessário)**

#### **Criar `update_db_versions.py`:**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Criar arquivo
nano update_db_versions.py
```

**Conteúdo do arquivo:**
```python
#!/usr/bin/env python3
"""
Script para atualizar o banco de dados com suporte a versões
DocCollab - Deploy Final
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.version import Version

def update_database():
    """Atualizar o banco de dados com a tabela de versões"""
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Banco de dados atualizado com sucesso!")
            print("✅ Tabela de versões criada")
            
            # Verificar se há projetos existentes
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"📊 Encontrados {len(projects)} projetos existentes")
                print("ℹ️  Projetos existentes receberão snapshots de versão na próxima compilação")
            else:
                print("📝 Nenhum projeto existente encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar banco de dados: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("🔄 Atualizando banco de dados com suporte a versões...")
    success = update_database()
    
    if success:
        print("\n🎉 Funcionalidade de histórico de versões disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Snapshots automáticos na compilação")
        print("   - Visualizador de histórico de versões")
        print("   - Comparação de versões")
        print("   - Restauração de versões")
    else:
        print("\n❌ Falha na atualização do banco de dados")
        sys.exit(1)
```

#### **Criar `update_db_chat.py`:**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Criar arquivo
nano update_db_chat.py
```

**Conteúdo do arquivo:**
```python
#!/usr/bin/env python3
"""
Script para atualizar o banco de dados com suporte a chat
DocCollab - Deploy Final
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.chat_message import ChatMessage

def update_database():
    """Atualizar o banco de dados com a tabela de chat"""
    app, socketio = create_app()
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Banco de dados atualizado com sucesso!")
            print("✅ Tabela de chat criada")
            
            # Verificar se há projetos existentes
            from models.project import Project
            projects = Project.query.all()
            
            if projects:
                print(f"📊 Encontrados {len(projects)} projetos existentes")
                print("ℹ️  Projetos existentes terão chat habilitado")
            else:
                print("📝 Nenhum projeto existente encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar banco de dados: {e}")
            return False
            
    return True

if __name__ == "__main__":
    print("🔄 Atualizando banco de dados com suporte a chat...")
    success = update_database()
    
    if success:
        print("\n🎉 Funcionalidade de chat colaborativo disponível!")
        print("📋 Funcionalidades adicionadas:")
        print("   - Chat em tempo real via WebSocket")
        print("   - Salas por projeto")
        print("   - Indicadores de usuários online")
        print("   - Histórico persistente de mensagens")
        print("   - Indicador de digitação")
    else:
        print("\n❌ Falha na atualização do banco de dados")
        sys.exit(1)
```

### **Passo 5: Executar os Scripts**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Executar scripts de atualização
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **Passo 6: Verificar se Funcionou**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se os arquivos existem
ls -la update_db_*.py

# Verificar se a aplicação funciona
python3.10 -c "from app import create_app; print('✅ Aplicação OK')"
```

## 🔍 VERIFICAÇÕES PÓS-ATUALIZAÇÃO

### **1. Verificar se a Aplicação Funciona**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar a aplicação
python3.10 -c "from app import create_app; app, socketio = create_app(); print('✅ Aplicação importada com sucesso')"
```

### **2. Verificar se o Banco de Dados foi Atualizado**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Verificar tabelas
python3.10 -c "from app import create_app; from models import db; app, socketio = create_app(); app.app_context().push(); print('Tabelas:', db.metadata.tables.keys())"
```

### **3. Configurar WSGI**
- Vá para **Web** → **WSGI configuration file**
- Substitua o conteúdo por:

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/123nilmarcastro/DocCollab'
if path not in sys.path:
    sys.path.append(path)

# Change to the project directory
os.chdir(path)

# Import your Flask app
from app import create_app

# Create the Flask app and SocketIO instance
app, socketio = create_app()

# For PythonAnywhere, we need to use the app directly
application = app
```

### **4. Configurar Static Files**
- Vá para **Web** → **Static files**
- Adicione:
  - **URL:** `/static/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`
- Adicione:
  - **URL:** `/socket.io/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **5. Reiniciar Aplicação**
- Vá para **Web** → **Reload**
- Aguarde alguns segundos
- Acesse: https://123nilmarcastro.pythonanywhere.com

## 🎉 RESULTADO ESPERADO

Após seguir estes passos, sua aplicação DocCollab deve mostrar:

- ✅ **Nova interface** moderna e responsiva
- ✅ **Editor LaTeX** com CodeMirror
- ✅ **Chat colaborativo** na sidebar
- ✅ **Sistema de versões** funcional
- ✅ **Planos Free/Paid** implementados
- ✅ **Internacionalização** completa

**Execute os passos acima para resolver o problema dos arquivos ausentes! 🔧**
