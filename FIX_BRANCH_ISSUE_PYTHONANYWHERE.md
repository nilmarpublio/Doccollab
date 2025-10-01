# 🔧 Resolvendo Problema de Branch no PythonAnywhere

## 🚨 Problema Identificado
```
error: src refspec master does not match any
error: failed to push some refs to 'https://github.com/nilmarpublio/doccollab.git'
```

Este erro ocorre porque você está no branch `main` mas tentando fazer push para `master`.

## 🛠️ Soluções (Execute uma por vez)

### **Solução 1: Fazer Push para o Branch Correto (Recomendada)**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Verificar qual branch você está
git branch

# 2. Verificar status
git status

# 3. Fazer push para o branch correto (main)
git push origin main

# 4. Se der erro, configurar upstream
git push -u origin main
```

### **Solução 2: Mudar para o Branch Master**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Verificar branches disponíveis
git branch -a

# 2. Mudar para o branch master
git checkout master

# 3. Se não existir, criar a partir do main
git checkout -b master

# 4. Fazer push
git push origin master
```

### **Solução 3: Configurar Branch Padrão**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Verificar configuração atual
git remote -v

# 2. Configurar branch padrão
git config --global init.defaultBranch main

# 3. Fazer push para main
git push origin main

# 4. Se necessário, configurar upstream
git push -u origin main
```

### **Solução 4: Clone Limpo (Última Opção)**

```bash
# No console bash do PythonAnywhere
cd ~

# 1. Fazer backup do diretório atual
mv DocCollab DocCollab-backup-$(date +%Y%m%d-%H%M%S)

# 2. Clonar o repositório novamente
git clone https://github.com/nilmarpublio/Doccollab.git DocCollab

# 3. Entrar no diretório
cd DocCollab

# 4. Verificar branch
git branch

# 5. Fazer push
git push origin main
```

## 🔍 Verificações Pós-Correção

### **1. Verificar Branch Atual**
```bash
git branch
# Deve mostrar: * main
```

### **2. Verificar Status**
```bash
git status
# Deve mostrar: "nothing to commit, working tree clean"
```

### **3. Verificar Histórico**
```bash
git log --oneline -5
# Deve mostrar os últimos commits
```

### **4. Verificar Remote**
```bash
git remote -v
# Deve mostrar a URL do repositório
```

## ✅ Após Resolver o Problema de Branch

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

### **Erro: Branch não existe**
```bash
# Criar branch master a partir do main
git checkout -b master
git push origin master
```

### **Erro: Upstream não configurado**
```bash
# Configurar upstream
git push -u origin main
```

### **Erro: Permissão negada**
```bash
# Verificar configuração do Git
git config --list
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

## 📞 Suporte

Se ainda houver problemas:
1. Verifique o branch com `git branch`
2. Verifique o status com `git status`
3. Verifique o remote com `git remote -v`
4. Verifique o histórico com `git log --oneline -5`

## 🎉 Sucesso!

Após seguir estes passos, sua aplicação DocCollab estará rodando com todas as funcionalidades:

- ✅ Editor LaTeX profissional
- ✅ Chat colaborativo em tempo real
- ✅ Sistema de histórico de versões
- ✅ Interface responsiva moderna
- ✅ Sistema de usuários e planos
- ✅ Internacionalização completa

**DocCollab estará pronto para uso em produção! 🚀**
