# 🔍 Troubleshooting - Aplicação Não Atualizada

## 🚨 Problema Identificado
A aplicação não foi atualizada e está mostrando a versão anterior.

## 🔍 DIAGNÓSTICO PASSO A PASSO

### **1. Verificar se o Código foi Atualizado**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se os arquivos estão atualizados
ls -la

# Verificar se existem os novos arquivos
ls -la update_db_*.py
ls -la complete_deploy.py
```

### **2. Verificar se o Git Pull Funcionou**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar status do Git
git status

# Verificar último commit
git log --oneline -3

# Fazer pull manual se necessário
git pull origin main
```

### **3. Verificar se o Ambiente Virtual está Ativo**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se está ativo (deve mostrar o caminho do venv)
which python
```

### **4. Verificar se as Dependências foram Instaladas**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip3.10 install --user -r requirements.txt

# Verificar se Flask-SocketIO está instalado
pip3.10 list | grep -i socketio
```

### **5. Verificar se o Banco de Dados foi Atualizado**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Executar scripts de atualização
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **6. Verificar se o .env está Configurado**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se existe o arquivo .env
ls -la .env

# Se não existir, criar
cp env_pythonanywhere_production.txt .env

# Editar o arquivo
nano .env
```

**Conteúdo do .env:**
```env
SECRET_KEY=doccollab-super-secret-key-2024-production
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123456
SOCKETIO_ASYNC_MODE=eventlet
DEBUG=False
```

### **7. Verificar se o WSGI está Configurado Corretamente**
- Vá para **Web** → **WSGI configuration file**
- Verifique se o conteúdo está correto:

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

### **8. Verificar se os Static Files estão Configurados**
- Vá para **Web** → **Static files**
- Verifique se existem:
  - **URL:** `/static/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`
  - **URL:** `/socket.io/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **9. Reiniciar a Aplicação**
- Vá para **Web** → **Reload**
- Aguarde alguns segundos
- Acesse: https://123nilmarcastro.pythonanywhere.com

## 🔧 SOLUÇÕES ALTERNATIVAS

### **Solução 1: Clone Limpo**
```bash
# No console bash do PythonAnywhere
cd ~

# Fazer backup do diretório atual
mv DocCollab DocCollab-backup-$(date +%Y%m%d-%H%M%S)

# Clonar o repositório novamente
git clone https://github.com/nilmarpublio/Doccollab.git DocCollab

# Entrar no diretório
cd DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip3.10 install --user -r requirements.txt

# Atualizar banco de dados
python3.10 update_db_versions.py
python3.10 update_db_chat.py

# Configurar .env
cp env_pythonanywhere_production.txt .env
nano .env
```

### **Solução 2: Verificar Logs de Erro**
- Vá para **Web** → **Log files**
- Verifique **Error log** para erros
- Verifique **Server log** para informações

### **Solução 3: Verificar se a Aplicação está Rodando**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar a aplicação localmente
python3.10 app.py
```

## 🎯 VERIFICAÇÕES FINAIS

### **1. Verificar se a Página Inicial Mudou**
- Acesse: https://123nilmarcastro.pythonanywhere.com
- Deve mostrar a nova interface

### **2. Verificar se o Editor Funciona**
- Faça login
- Acesse um projeto
- Deve mostrar o novo editor com CodeMirror

### **3. Verificar se o Chat Funciona**
- No editor, deve aparecer o painel de chat na sidebar
- Deve permitir enviar mensagens

### **4. Verificar se as Versões Funcionam**
- No editor, deve aparecer o botão "History"
- Deve permitir visualizar histórico de versões

## 📞 SE AINDA HOUVER PROBLEMAS

1. **Verifique os logs** em Web → Log files
2. **Execute os comandos de diagnóstico** acima
3. **Use a Solução 1** (clone limpo) se necessário
4. **Verifique se todas as configurações** estão corretas

## 🎉 RESULTADO ESPERADO

Após seguir estes passos, sua aplicação DocCollab deve mostrar:

- ✅ **Nova interface** moderna e responsiva
- ✅ **Editor LaTeX** com CodeMirror
- ✅ **Chat colaborativo** na sidebar
- ✅ **Sistema de versões** funcional
- ✅ **Planos Free/Paid** implementados
- ✅ **Internacionalização** completa

**Siga os passos de diagnóstico acima para identificar e resolver o problema! 🔍**
