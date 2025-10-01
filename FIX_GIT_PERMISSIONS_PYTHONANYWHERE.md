# 🔧 Resolvendo Problemas de Permissão Git no PythonAnywhere

## 🚨 Problema Identificado
```
warning: unable to access 'translations/pt/.gitignore': Permission denied
warning: unable to access 'translations/en/.gitignore': Permission denied
warning: unable to access 'translations/es/.gitignore': Permission denied
```

Este erro ocorre quando o Git tenta acessar arquivos que não existem ou têm problemas de permissão.

## 🛠️ Soluções (Execute uma por vez)

### **Solução 1: Limpar Cache e Re-adicionar Arquivos (Recomendada)**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Verificar status atual
git status

# 2. Limpar cache do Git
git rm -r --cached .

# 3. Adicionar arquivos novamente
git add .

# 4. Verificar se há arquivos problemáticos
find . -name '.gitignore' -type f

# 5. Remover arquivos .gitignore problemáticos se existirem
find . -name '.gitignore' -type f -delete

# 6. Adicionar arquivos novamente
git add .

# 7. Verificar status final
git status

# 8. Fazer commit se necessário
git commit -m "Fix git permissions and add all files"

# 9. Push para o repositório
git push origin master
```

### **Solução 2: Corrigir Permissões**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Corrigir permissões de todos os arquivos
chmod -R 755 .

# 2. Corrigir propriedade dos arquivos
chown -R $USER:$USER .

# 3. Configurar diretório seguro
git config --global --add safe.directory .

# 4. Adicionar arquivos
git add .

# 5. Verificar status
git status

# 6. Fazer commit
git commit -m "Fix permissions and add files"

# 7. Push
git push origin master
```

### **Solução 3: Reset e Re-clone (Última Opção)**

```bash
# No console bash do PythonAnywhere
cd ~

# 1. Fazer backup do diretório atual
mv DocCollab DocCollab-backup-$(date +%Y%m%d-%H%M%S)

# 2. Clonar o repositório novamente
git clone https://github.com/nilmarpublio/Doccollab.git DocCollab

# 3. Entrar no diretório
cd DocCollab

# 4. Verificar se tudo está OK
git status
git log --oneline -5
```

## 🔍 Verificações Pós-Correção

### **1. Verificar Status do Git**
```bash
git status
# Deve mostrar: "nothing to commit, working tree clean"
```

### **2. Verificar Histórico**
```bash
git log --oneline -5
# Deve mostrar os últimos commits
```

### **3. Verificar Arquivos**
```bash
ls -la
# Deve mostrar todos os arquivos e pastas
```

### **4. Verificar Pastas de Tradução**
```bash
ls -la translations/pt/
ls -la translations/en/
ls -la translations/es/
# Deve mostrar apenas as pastas LC_MESSAGES
```

## ✅ Após Resolver os Problemas de Permissão

### **1. Ativar Ambiente Virtual**
```bash
cd ~/DocCollab
source venv/bin/activate
```

### **2. Instalar/Atualizar Dependências**
```bash
pip3.10 install --user -r requirements.txt
```

### **3. Atualizar Banco de Dados**
```bash
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **4. Configurar Variáveis de Ambiente**
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

### **Erro: Permission denied**
```bash
# Corrigir permissões
chmod -R 755 .
chown -R $USER:$USER .
```

### **Erro: ModuleNotFoundError**
```bash
# Reinstale as dependências
pip3.10 install --user --upgrade -r requirements.txt
```

### **Erro: LaTeX não compila**
```bash
# Verifique se o pdflatex está instalado
which pdflatex
# Deve retornar: /usr/bin/pdflatex

# Se não estiver, instale
sudo apt-get update
sudo apt-get install texlive-full
```

### **Erro: Banco de dados**
```bash
# Execute os scripts de atualização
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

## 📞 Suporte

Se ainda houver problemas:
1. Verifique os logs em **Web** → **Log files**
2. Execute `git status` para verificar o estado
3. Execute `git log --oneline -5` para ver o histórico
4. Verifique se todos os arquivos estão presentes com `ls -la`

## 🎉 Sucesso!

Após seguir estes passos, sua aplicação DocCollab estará rodando com todas as funcionalidades:

- ✅ Editor LaTeX profissional
- ✅ Chat colaborativo em tempo real
- ✅ Sistema de histórico de versões
- ✅ Interface responsiva moderna
- ✅ Sistema de usuários e planos
- ✅ Internacionalização completa

**DocCollab estará pronto para uso em produção! 🚀**
