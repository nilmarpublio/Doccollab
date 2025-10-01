# 🔧 CORREÇÃO DE ERRO - PythonAnywhere

## 🚨 PROBLEMA IDENTIFICADO
```
There was an error loading your PythonAnywhere-hosted site. There may be a bug in your code.
Error code: Unhandled Exception
```

## 🔍 DIAGNÓSTICO PASSO A PASSO

### **1. Verificar Logs de Erro**
- Acesse: https://www.pythonanywhere.com/user/123nilmarcastro/files/var/log/123nilmarcastro.pythonanywhere.com.error.log
- Verifique as últimas linhas do arquivo de erro

### **2. Verificar Logs do Servidor**
- Acesse: https://www.pythonanywhere.com/user/123nilmarcastro/files/var/log/123nilmarcastro.pythonanywhere.com.server.log
- Verifique as últimas linhas do arquivo de servidor

### **3. Verificar Configuração WSGI**
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

### **4. Verificar se os Arquivos Existem**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar arquivos principais
ls -la app.py
ls -la models/
ls -la routes/
ls -la templates/
ls -la static/
```

### **5. Verificar se as Dependências Estão Instaladas**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Verificar dependências
pip3.10 list | grep -i flask
pip3.10 list | grep -i socketio
pip3.10 list | grep -i sqlalchemy
```

### **6. Testar a Aplicação Localmente**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importação
python3.10 -c "from app import create_app; print('✅ Import OK')"

# Testar criação da aplicação
python3.10 -c "from app import create_app; app, socketio = create_app(); print('✅ App OK')"
```

## 🔧 SOLUÇÕES COMUNS

### **Solução 1: Erro de Importação**
Se houver erro de importação, verifique se todos os arquivos existem:

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se todos os arquivos necessários existem
ls -la models/version.py
ls -la models/chat_message.py
ls -la routes/chat.py
ls -la services/latex_compiler.py
```

### **Solução 2: Erro de Dependências**
Se houver erro de dependências, reinstale:

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip3.10 install --user -r requirements.txt

# Instalar dependências específicas se necessário
pip3.10 install --user flask-socketio
pip3.10 install --user flask-babel
pip3.10 install --user flask-login
pip3.10 install --user flask-sqlalchemy
```

### **Solução 3: Erro de Banco de Dados**
Se houver erro de banco de dados, atualize:

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar banco de dados
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **Solução 4: Erro de Configuração**
Se houver erro de configuração, verifique o .env:

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar arquivo .env
ls -la .env

# Se não existir, criar
cp env_pythonanywhere_production.txt .env

# Editar com configurações corretas
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

### **Solução 5: Erro de Permissões**
Se houver erro de permissões, corrigir:

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Corrigir permissões
chmod -R 755 .
chown -R $USER:$USER .
```

## 🔄 SOLUÇÃO ALTERNATIVA - WSGI Simplificado

Se o WSGI atual não funcionar, use esta versão simplificada:

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
try:
    from app import create_app
    app, socketio = create_app()
    application = app
except Exception as e:
    print(f"Error: {e}")
    # Fallback to basic Flask app
    from flask import Flask
    application = Flask(__name__)
```

## 🔍 VERIFICAÇÕES PÓS-CORREÇÃO

### **1. Verificar se a Aplicação Funciona**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar a aplicação
python3.10 -c "from app import create_app; app, socketio = create_app(); print('✅ Aplicação OK')"
```

### **2. Verificar se o WSGI está Configurado**
- Vá para **Web** → **WSGI configuration file**
- Verifique se não há erros de sintaxe
- Salve as alterações

### **3. Verificar se os Static Files estão Configurados**
- Vá para **Web** → **Static files**
- Verifique se existem:
  - **URL:** `/static/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`
  - **URL:** `/socket.io/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **4. Reiniciar Aplicação**
- Vá para **Web** → **Reload**
- Aguarde alguns segundos
- Acesse: https://123nilmarcastro.pythonanywhere.com

## 📞 SE AINDA HOUVER PROBLEMAS

1. **Verifique os logs** de erro e servidor
2. **Execute os comandos de diagnóstico** acima
3. **Use a Solução Alternativa** de WSGI simplificado
4. **Verifique se todas as configurações** estão corretas
5. **Entre em contato com o suporte** do PythonAnywhere se necessário

## 🎉 RESULTADO ESPERADO

Após seguir estes passos, sua aplicação DocCollab deve funcionar corretamente:

- ✅ **Página inicial carrega**
- ✅ **Login funciona**
- ✅ **Editor LaTeX funciona**
- ✅ **Chat colaborativo funciona**
- ✅ **Sistema de versões funciona**

**Execute os passos de diagnóstico acima para identificar e resolver o erro! 🔧**
