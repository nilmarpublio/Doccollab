# 🔧 Resolvendo Conflito de Histórico Git no PythonAnywhere

## 🚨 Problema Identificado
```
fatal: refusing to merge unrelated histories
```

Este erro ocorre quando o repositório local no PythonAnywhere tem um histórico diferente do repositório remoto.

## 🛠️ Soluções (Execute uma por vez)

### **Solução 1: Merge com Históricos Não Relacionados (Recomendada)**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Fazer backup do estado atual
git branch backup-$(date +%Y%m%d-%H%M%S)

# 2. Forçar o pull com --allow-unrelated-histories
git pull origin master --allow-unrelated-histories

# 3. Se houver conflitos, resolva e faça commit
git add .
git commit -m "Merge unrelated histories"

# 4. Verificar se tudo está OK
git status
git log --oneline -5
```

### **Solução 2: Reset Hard (Mais Drástica)**

```bash
# No console bash do PythonAnywhere
cd ~/DocCollab

# 1. Fazer backup do estado atual
git branch backup-$(date +%Y%m%d-%H%M%S)

# 2. Buscar as mudanças remotas
git fetch origin master

# 3. Resetar para o estado remoto
git reset --hard origin/master

# 4. Verificar se tudo está OK
git status
git log --oneline -5
```

### **Solução 3: Clone Limpo (Última Opção)**

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

## ✅ Após Resolver o Conflito

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

## 🔍 Verificações Pós-Deploy

### **1. Teste Básico**
- [ ] Página inicial carrega
- [ ] Login funciona
- [ ] Registro funciona
- [ ] Dashboard aparece

### **2. Teste do Editor**
- [ ] Editor LaTeX abre
- [ ] CodeMirror funciona
- [ ] Auto-save ativo
- [ ] Compilação PDF funciona

### **3. Teste do Chat**
- [ ] Chat aparece na sidebar
- [ ] Mensagens são enviadas
- [ ] Indicador de online funciona
- [ ] Histórico carrega

### **4. Teste de Versões**
- [ ] Compilação cria versão
- [ ] Histórico de versões funciona
- [ ] Comparação funciona
- [ ] Restauração funciona

## 🐛 Troubleshooting

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

### **Erro: SocketIO não funciona**
- Verifique se o SocketIO está configurado no WSGI
- Certifique-se que o static file está configurado
- Reinicie a aplicação

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
