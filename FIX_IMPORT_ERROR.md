# 🔧 CORREÇÃO DE ERRO DE IMPORTAÇÃO - PythonAnywhere

## 🚨 PROBLEMA IDENTIFICADO
```
If you're seeing an import error and don't know why,
we have a dedicated help page to help you debug: 
https://help.pythonanywhere.com/pages/DebuggingImportError/
```

Há um erro de importação que está impedindo a aplicação de funcionar.

## 🔍 DIAGNÓSTICO PASSO A PASSO

### **1. Verificar Logs de Erro Detalhados**
- Acesse: https://www.pythonanywhere.com/user/123nilmarcastro/files/var/log/123nilmarcastro.pythonanywhere.com.error.log
- Procure por mensagens de erro específicas

### **2. Verificar se Todos os Arquivos Existem**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar arquivos principais
ls -la app.py
ls -la models/__init__.py
ls -la models/version.py
ls -la models/chat_message.py
ls -la routes/__init__.py
ls -la routes/chat.py
ls -la services/latex_compiler.py
ls -la utils/permissions.py
```

### **3. Verificar se as Dependências Estão Instaladas**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Verificar dependências críticas
pip3.10 list | grep -i flask
pip3.10 list | grep -i socketio
pip3.10 list | grep -i sqlalchemy
pip3.10 list | grep -i babel
```

### **4. Testar Importação Passo a Passo**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importações básicas
python3.10 -c "import flask; print('✅ Flask OK')"
python3.10 -c "import flask_socketio; print('✅ Flask-SocketIO OK')"
python3.10 -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy OK')"
python3.10 -c "import flask_babel; print('✅ Flask-Babel OK')"
```

### **5. Testar Importação dos Modelos**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importação dos modelos
python3.10 -c "from models import db; print('✅ Models OK')"
python3.10 -c "from models.version import Version; print('✅ Version OK')"
python3.10 -c "from models.chat_message import ChatMessage; print('✅ ChatMessage OK')"
```

### **6. Testar Importação das Rotas**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importação das rotas
python3.10 -c "from routes.main import main_bp; print('✅ Main routes OK')"
python3.10 -c "from routes.auth import auth_bp; print('✅ Auth routes OK')"
python3.10 -c "from routes.chat import chat_bp; print('✅ Chat routes OK')"
```

### **7. Testar Importação da Aplicação**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Testar importação da aplicação
python3.10 -c "from app import create_app; print('✅ App import OK')"
```

## 🔧 SOLUÇÕES COMUNS

### **Solução 1: Instalar Dependências Ausentes**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Ativar ambiente virtual
source venv/bin/activate

# Instalar todas as dependências
pip3.10 install --user -r requirements.txt

# Instalar dependências específicas se necessário
pip3.10 install --user flask-socketio==5.3.6
pip3.10 install --user flask-babel==4.0.0
pip3.10 install --user flask-login==0.6.3
pip3.10 install --user flask-sqlalchemy==3.0.5
pip3.10 install --user python-dotenv==1.0.0
```

### **Solução 2: Corrigir Problemas de Caminho**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Verificar se estamos no diretório correto
pwd

# Verificar se o Python está no caminho correto
which python3.10

# Verificar se o PYTHONPATH está configurado
echo $PYTHONPATH
```

### **Solução 3: Criar Arquivos Ausentes**
Se algum arquivo estiver ausente, crie-o:

#### **Criar `models/version.py` se ausente:**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Criar arquivo
cat > models/version.py << 'EOF'
from datetime import datetime
from models import db

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(500), nullable=True)

    project = db.relationship('Project', backref=db.backref('versions', lazy=True))

    def __repr__(self):
        return f'<Version {self.version_number} for Project {self.project_id}>'
EOF
```

#### **Criar `models/chat_message.py` se ausente:**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Criar arquivo
cat > models/chat_message.py << 'EOF'
from datetime import datetime
from models import db

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship('Project', backref=db.backref('chat_messages', lazy=True))
    user = db.relationship('User', backref=db.backref('chat_messages', lazy=True))

    def __repr__(self):
        return f'<ChatMessage {self.id} from User {self.user_id}>'
EOF
```

### **Solução 4: Corrigir WSGI**
Use esta versão simplificada do WSGI:

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
    print(f"Error creating app: {e}")
    # Fallback to basic Flask app
    from flask import Flask
    application = Flask(__name__)
    application.config['SECRET_KEY'] = 'dev-secret-key'
```

### **Solução 5: Verificar Permissões**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Corrigir permissões
chmod -R 755 .
chown -R $USER:$USER .

# Verificar se os arquivos são legíveis
ls -la app.py
ls -la models/
ls -la routes/
```

## 🔍 VERIFICAÇÕES PÓS-CORREÇÃO

### **1. Testar a Aplicação Localmente**
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
- Use a versão simplificada acima
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

1. **Verifique os logs** de erro detalhados
2. **Execute os comandos de diagnóstico** acima
3. **Use a Solução 4** de WSGI simplificado
4. **Verifique se todas as dependências** estão instaladas
5. **Entre em contato com o suporte** do PythonAnywhere se necessário

## 🎉 RESULTADO ESPERADO

Após seguir estes passos, sua aplicação DocCollab deve funcionar corretamente:

- ✅ **Página inicial carrega**
- ✅ **Login funciona**
- ✅ **Editor LaTeX funciona**
- ✅ **Chat colaborativo funciona**
- ✅ **Sistema de versões funciona**

**Execute os passos de diagnóstico acima para identificar e resolver o erro de importação! 🔧**
