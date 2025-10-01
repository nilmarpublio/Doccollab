# 🔐 Resolvendo Problema de Autenticação GitHub

## 🚨 Problema Identificado
```
Username for 'https://github.com': nilmarpubblio
Password for 'https://nilmarpubblio@github.com': 
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/nilmarpublio/doccollab.git/'
```

O GitHub não aceita mais senhas para operações Git. É necessário usar um **Personal Access Token (PAT)**.

## 🛠️ Soluções (Execute uma por vez)

### **Solução 1: Usar Personal Access Token (Recomendada)**

#### **Passo 1: Criar Personal Access Token no GitHub**
1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Preencha:
   - **Note:** "DocCollab PythonAnywhere"
   - **Expiration:** 90 days (ou conforme necessário)
   - **Scopes:** Marque `repo` (acesso completo ao repositório)
4. Clique em **"Generate token"**
5. **COPIE O TOKEN** (você só verá uma vez!)

#### **Passo 2: Configurar Token no PythonAnywhere**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Configurar credenciais (use o token como senha)
git config --global credential.helper store

# Fazer push (use o token como senha quando solicitado)
git push origin main
```

**Quando solicitado:**
- **Username:** `nilmarpubblio`
- **Password:** `[cole o token aqui]`

### **Solução 2: Usar SSH (Alternativa)**

#### **Passo 1: Gerar Chave SSH**
```bash
# No console bash do PythonAnywhere
cd ~

# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu@email.com"

# Quando solicitado, pressione Enter para usar local padrão
# Digite uma senha ou pressione Enter para não usar senha
```

#### **Passo 2: Adicionar Chave ao GitHub**
```bash
# Mostrar chave pública
cat ~/.ssh/id_ed25519.pub

# Copie a saída completa
```

1. Acesse: https://github.com/settings/ssh/new
2. Cole a chave pública no campo **"Key"**
3. Dê um título como "PythonAnywhere DocCollab"
4. Clique em **"Add SSH key"**

#### **Passo 3: Configurar Repositório para SSH**
```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Alterar URL para SSH
git remote set-url origin git@github.com:nilmarpublio/Doccollab.git

# Fazer push
git push origin main
```

### **Solução 3: Usar Token na URL (Rápida)**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Fazer push com token na URL
git push https://[SEU_TOKEN]@github.com/nilmarpublio/Doccollab.git main

# Substitua [SEU_TOKEN] pelo token que você criou
```

### **Solução 4: Configurar Credenciais Permanentemente**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# Configurar credenciais
git config --global user.name "nilmarpubblio"
git config --global user.email "seu@email.com"

# Configurar helper de credenciais
git config --global credential.helper store

# Fazer push (digite o token como senha)
git push origin main
```

## 🔍 Verificações Pós-Correção

### **1. Verificar Configuração**
```bash
git config --list
```

### **2. Verificar Remote**
```bash
git remote -v
```

### **3. Verificar Status**
```bash
git status
```

## ✅ Após Resolver a Autenticação

### **1. Ativar Ambiente Virtual**
```bash
cd ~/DocCollab
source venv/bin/activate
```

### **2. Instalar Dependências**
```bash
pip3.10 install --user -r requirements.txt
```

### **3. Atualizar Banco de Dados**
```bash
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **4. Configurar .env**
```bash
# Copiar arquivo de exemplo
cp env_pythonanywhere_production.txt .env

# Editar com suas configurações
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

### **5. Configurar WSGI**
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

### **6. Configurar Static Files**
- Vá para **Web** → **Static files**
- Adicione:
  - **URL:** `/static/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`
- Adicione:
  - **URL:** `/socket.io/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **7. Reiniciar Aplicação**
- Vá para **Web** → **Reload**
- Aguarde alguns segundos
- Acesse: https://123nilmarcastro.pythonanywhere.com

## 🐛 Troubleshooting

### **Erro: Token inválido**
- Verifique se o token foi copiado corretamente
- Verifique se o token tem as permissões corretas (`repo`)
- Verifique se o token não expirou

### **Erro: SSH não funciona**
- Verifique se a chave SSH foi adicionada ao GitHub
- Teste a conexão: `ssh -T git@github.com`

### **Erro: Credenciais não salvas**
```bash
# Limpar credenciais salvas
git config --global --unset credential.helper
git config --global credential.helper store
```

## 📞 Suporte

Se ainda houver problemas:
1. Verifique se o token tem as permissões corretas
2. Verifique se a conta GitHub está ativa
3. Tente criar um novo token
4. Verifique a URL do repositório

## 🎉 Sucesso!

Após resolver a autenticação, sua aplicação DocCollab estará rodando com:

- ✅ Editor LaTeX profissional
- ✅ Chat colaborativo em tempo real
- ✅ Sistema de histórico de versões
- ✅ Interface responsiva moderna
- ✅ Sistema de usuários e planos
- ✅ Internacionalização completa

**DocCollab estará pronto para uso em produção! 🚀**
