# 🚀 Deploy Final no PythonAnywhere - DocCollab

## 📋 Checklist de Deploy

### ✅ **Funcionalidades Implementadas:**
- [x] Editor LaTeX com CodeMirror
- [x] Chat colaborativo em tempo real (SocketIO)
- [x] Sistema de histórico de versões
- [x] Planos Free/Paid com limitações
- [x] Internacionalização (PT/EN/ES)
- [x] Interface responsiva moderna
- [x] Compilação PDF com pdflatex
- [x] Sistema de autenticação completo

## 🔧 Passos para Deploy

### **1. Acesse o PythonAnywhere**
- Vá para: https://www.pythonanywhere.com
- Faça login na sua conta
- Acesse o **Dashboard**

### **2. Abra o Console Bash**
- Clique em **"Consoles"** no menu
- Clique em **"Bash"** para abrir um novo console

### **3. Navegue para o diretório do projeto**
```bash
cd ~/DocCollab
```

### **4. Atualize o código do GitHub**
```bash
git pull origin master
```

### **5. Ative o ambiente virtual**
```bash
source venv/bin/activate
```

### **6. Instale/Atualize dependências**
```bash
pip3.10 install --user -r requirements.txt
```

### **7. Atualize o banco de dados**
```bash
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

### **8. Configure as variáveis de ambiente**
```bash
nano .env
```

**Conteúdo do arquivo .env:**
```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123
SOCKETIO_ASYNC_MODE=eventlet
```

### **9. Configure o WSGI**
- Vá para **"Web"** no menu
- Clique em **"WSGI configuration file"**
- Substitua o conteúdo por:

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/123nilmarcastro/DocCollab'
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app import create_app
app, socketio = create_app()

# For PythonAnywhere, we need to use the app directly
# SocketIO will be handled separately
application = app

if __name__ == "__main__":
    socketio.run(app, debug=True)
```

### **10. Configure o Web App**
- Vá para **"Web"** no menu
- Em **"Source code"**, certifique-se que está apontando para: `/home/123nilmarcastro/DocCollab`
- Em **"Working directory"**, defina: `/home/123nilmarcastro/DocCollab`

### **11. Configure o SocketIO (IMPORTANTE)**
- Em **"Web"**, vá para **"Static files"**
- Adicione uma nova entrada:
  - **URL:** `/socket.io/`
  - **Directory:** `/home/123nilmarcastro/DocCollab/static`

### **12. Instale o LaTeX (se necessário)**
```bash
# No console bash
sudo apt-get update
sudo apt-get install texlive-full
```

### **13. Teste a aplicação**
- Vá para **"Web"** no menu
- Clique em **"Reload"** para reiniciar a aplicação
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

### **5. Teste de Responsividade**
- [ ] Desktop funciona
- [ ] Tablet funciona
- [ ] Mobile funciona

## 🐛 Troubleshooting

### **Erro: ModuleNotFoundError**
```bash
# Reinstale as dependências
pip3.10 install --user --upgrade -r requirements.txt
```

### **Erro: SocketIO não funciona**
- Verifique se o SocketIO está configurado no WSGI
- Certifique-se que o static file está configurado
- Reinicie a aplicação

### **Erro: LaTeX não compila**
```bash
# Verifique se o pdflatex está instalado
which pdflatex
# Deve retornar: /usr/bin/pdflatex
```

### **Erro: Banco de dados**
```bash
# Execute os scripts de atualização
python3.10 update_db_versions.py
python3.10 update_db_chat.py
```

## 📊 Monitoramento

### **Logs da Aplicação**
- Vá para **"Web"** → **"Log files"**
- Verifique **"Error log"** para erros
- Verifique **"Server log"** para informações

### **Uso de Recursos**
- Monitore **CPU** e **RAM** no dashboard
- Verifique **disco** disponível
- Acompanhe **tráfego** de rede

## 🎯 Funcionalidades Finais

### **✅ Editor LaTeX Completo**
- Syntax highlighting
- Auto-save
- Compilação PDF
- Toolbar de formatação

### **✅ Chat Colaborativo**
- Tempo real via WebSocket
- Salas por projeto
- Indicadores visuais
- Histórico persistente

### **✅ Sistema de Versões**
- Snapshots automáticos
- Comparação lado a lado
- Restauração de versões
- Gerenciamento completo

### **✅ Interface Moderna**
- Design responsivo
- 3 idiomas (PT/EN/ES)
- Ícones profissionais
- Animações suaves

### **✅ Sistema de Usuários**
- Autenticação segura
- Planos Free/Paid
- Permissões granulares
- Gestão de projetos

## 🚀 Deploy Concluído!

Após seguir todos os passos, sua aplicação DocCollab estará rodando com todas as funcionalidades implementadas:

**URL:** https://123nilmarcastro.pythonanywhere.com

**Funcionalidades Ativas:**
- ✅ Editor LaTeX profissional
- ✅ Chat colaborativo em tempo real
- ✅ Histórico de versões completo
- ✅ Interface responsiva moderna
- ✅ Sistema de usuários e planos
- ✅ Internacionalização completa

**🎉 DocCollab está pronto para uso em produção!**
