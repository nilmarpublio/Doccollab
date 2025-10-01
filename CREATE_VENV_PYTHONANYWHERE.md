# 🔧 CRIAR AMBIENTE VIRTUAL - PythonAnywhere

## 🚨 PROBLEMA IDENTIFICADO
```
bash: venv/bin/activate: No such file or directory
```

O ambiente virtual não existe no PythonAnywhere. Vamos criá-lo e instalar todas as dependências.

## 🔧 SOLUÇÃO PASSO A PASSO

### **1. Criar Ambiente Virtual**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Criar ambiente virtual
python3.10 -m venv venv

# Verificar se foi criado
ls -la venv/
```

### **2. Ativar Ambiente Virtual**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se está ativo (deve mostrar (venv) no prompt)
which python
```

### **3. Atualizar pip**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip
```

### **4. Instalar Dependências**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências do requirements.txt
pip install -r requirements.txt

# Verificar se foram instaladas
pip list
```

### **5. Instalar Dependências Específicas (se necessário)**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências específicas
pip install flask==2.3.3
pip install flask-socketio==5.3.6
pip install flask-sqlalchemy==3.0.5
pip install flask-babel==4.0.0
pip install flask-login==0.6.3
pip install python-dotenv==1.0.0
pip install babel==2.17.0
pip install pytz==2025.2
pip install click==8.3.0
pip install itsdangerous==2.2.0
pip install jinja2==3.1.6
pip install markupsafe==3.0.3
pip install werkzeug==2.3.7
pip install blinker==1.9.0
pip install colorama==0.4.6
pip install greenlet==3.2.4
pip install sqlalchemy==2.0.43
pip install typing-extensions==4.15.0
```

### **6. Verificar Instalação**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importações
python -c "import flask; print('✅ Flask OK')"
python -c "import flask_socketio; print('✅ Flask-SocketIO OK')"
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy OK')"
python -c "import flask_babel; print('✅ Flask-Babel OK')"
python -c "import flask_login; print('✅ Flask-Login OK')"
python -c "import dotenv; print('✅ Python-dotenv OK')"
```

### **7. Testar Aplicação**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importação da aplicação
python -c "from app import create_app; print('✅ App import OK')"

# Testar criação da aplicação
python -c "from app import create_app; app, socketio = create_app(); print('✅ App creation OK')"
```

### **8. Atualizar Banco de Dados**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Executar scripts de atualização do banco
python update_db_versions.py
python update_db_chat.py
```

### **9. Configurar WSGI**
Vá para **Web** → **WSGI configuration file** e use:

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
app, socketio = create_app()
application = app
```

### **10. Configurar Static Files**
Vá para **Web** → **Static files** e adicione:

- **URL:** `/static/`
- **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **11. Reiniciar Aplicação**
- Vá para **Web** → **Reload**
- Aguarde alguns segundos
- Acesse: https://123nilmarcastro.pythonanywhere.com

## 🔍 VERIFICAÇÕES PÓS-CRIAÇÃO

### **1. Verificar Estrutura do Ambiente Virtual**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar estrutura
ls -la venv/
ls -la venv/bin/
ls -la venv/lib/
```

### **2. Verificar Dependências Instaladas**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Listar pacotes instalados
pip list | grep -i flask
pip list | grep -i socketio
pip list | grep -i sqlalchemy
pip list | grep -i babel
```

### **3. Testar Funcionalidade Completa**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar aplicação completa
python -c "
from app import create_app
from models import db
app, socketio = create_app()
with app.app_context():
    db.create_all()
    print('✅ Aplicação completa OK')
"
```

## 🎉 RESULTADO ESPERADO

Após seguir estes passos:

- ✅ **Ambiente virtual criado**
- ✅ **Todas as dependências instaladas**
- ✅ **Aplicação funciona localmente**
- ✅ **Banco de dados atualizado**
- ✅ **WSGI configurado**
- ✅ **Static files configurados**
- ✅ **Aplicação online funcionando**

## 📞 SE AINDA HOUVER PROBLEMAS

1. **Verifique se o Python 3.10 está disponível:**
   ```bash
   python3.10 --version
   ```

2. **Verifique se o pip está funcionando:**
   ```bash
   python3.10 -m pip --version
   ```

3. **Verifique se há espaço em disco:**
   ```bash
   df -h
   ```

4. **Verifique se há permissões adequadas:**
   ```bash
   ls -la ~/DocCollab/
   ```

**Execute os passos acima para criar o ambiente virtual e instalar todas as dependências! 🔧**
