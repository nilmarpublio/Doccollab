# DocCollab

Uma plataforma colaborativa avançada para criação e edição de documentos LaTeX com chat em tempo real, sistema de versões e interface moderna.

## 🚀 Características Principais

### ✨ **Editor LaTeX Avançado**
- **CodeMirror** integrado com syntax highlighting
- **Auto-save** a cada 5 segundos
- **Compilação PDF** em tempo real
- **Toolbar** com formatação LaTeX (negrito, itálico, seções, listas)
- **Interface responsiva** e moderna

### 💬 **Chat Colaborativo em Tempo Real**
- **WebSocket** com Flask-SocketIO
- **Salas por projeto** para isolamento de conversas
- **Indicadores visuais** de usuários online
- **Indicador de digitação** em tempo real
- **Histórico persistente** de mensagens
- **Interface integrada** na sidebar do editor

### 📚 **Sistema de Histórico de Versões**
- **Snapshots automáticos** a cada compilação
- **Visualização** de versões anteriores
- **Comparação lado a lado** entre versões
- **Restauração** de versões específicas
- **Gerenciamento** completo de histórico

### 👥 **Sistema de Usuários e Planos**
- **Autenticação** completa com Flask-Login
- **Planos Free/Paid** com limitações
- **Gestão de projetos** por usuário
- **Sistema de permissões** baseado em planos

### 🌐 **Internacionalização (i18n)**
- **3 idiomas** suportados: Português, Inglês, Espanhol
- **Flask-Babel** para tradução dinâmica
- **Troca de idioma** em tempo real
- **Interface completamente traduzida**

### 📱 **Design Responsivo**
- **Layout adaptativo** para desktop, tablet e mobile
- **CSS Grid** para organização eficiente
- **Componentes modernos** com glassmorphism
- **Ícones profissionais** com Font Awesome

## 🏗️ Arquitetura do Sistema

### **Backend (Flask)**
```
DocCollab/
├── app.py                    # Aplicação principal com SocketIO
├── models/                   # Modelos do banco de dados
│   ├── user.py              # Usuários e autenticação
│   ├── project.py           # Projetos LaTeX
│   ├── subscription.py      # Planos e limitações
│   ├── version.py           # Histórico de versões
│   └── chat_message.py      # Mensagens do chat
├── routes/                   # Blueprints das rotas
│   ├── main.py              # Rotas principais e API
│   ├── auth.py              # Autenticação
│   └── chat.py              # Chat em tempo real
├── services/                 # Serviços especializados
│   ├── latex_compiler.py    # Compilação LaTeX
│   └── latex.py             # Utilitários LaTeX
├── utils/                    # Utilitários
│   ├── file_ops.py          # Operações de arquivo
│   └── permissions.py       # Decorators de permissão
└── templates/                # Templates HTML
    ├── base.html            # Template base
    ├── index.html           # Página inicial
    ├── dashboard.html       # Dashboard de projetos
    ├── editor.html          # Editor principal
    ├── pdf_viewer.html      # Visualizador PDF
    ├── version_*.html       # Páginas de versões
    └── auth/                # Páginas de autenticação
```

### **Frontend (HTML/CSS/JS)**
- **HTML5** semântico e acessível
- **CSS3** com Grid, Flexbox e animações
- **JavaScript vanilla** para interatividade
- **Socket.IO** para comunicação em tempo real
- **CodeMirror** para editor de código

## 🛠️ Instalação e Configuração

### **Pré-requisitos**
- Python 3.8+
- pip (gerenciador de pacotes)
- Git
- LaTeX (MiKTeX/TeX Live) para compilação

### **Instalação Local**

1. **Clone o repositório**
   ```bash
   git clone https://github.com/nilmarpublio/Doccollab.git
   cd DocCollab
   ```

2. **Crie e ative ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**
   ```bash
   # Copie o arquivo de exemplo
   cp env.example .env
   
   # Edite com suas configurações
   nano .env  # ou notepad .env no Windows
   ```

5. **Execute a aplicação**
   ```bash
   python app.py
   ```

6. **Acesse a aplicação**
   ```
   http://localhost:5000
   ```

### **Configuração das Variáveis de Ambiente**

```env
# Configurações do Flask
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True

# Banco de dados
DATABASE_URL=sqlite:///doccollab.db

# Compilação LaTeX
PDFLATEX=C:\texlive\2023\bin\windows\pdflatex.exe  # Windows
# PDFLATEX=/usr/bin/pdflatex  # Linux

# Usuário administrador
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123

# SocketIO (opcional)
SOCKETIO_ASYNC_MODE=eventlet
```

## 🚀 Deploy em Produção

### **PythonAnywhere**
1. Clone o repositório no servidor
2. Configure as variáveis de ambiente
3. Instale dependências: `pip3.10 install --user -r requirements.txt`
4. Configure o WSGI para usar `wsgi.py`
5. Execute `python3.10 update_db_versions.py` e `python3.10 update_db_chat.py`

### **Heroku**
```bash
# Instale Heroku CLI
heroku create doccollab-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python update_db_versions.py
heroku run python update_db_chat.py
```

### **Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📋 Funcionalidades Detalhadas

### **🎯 Editor LaTeX**
- **Syntax highlighting** para LaTeX
- **Auto-complete** de comandos
- **Auto-save** a cada 5 segundos
- **Compilação** com pdflatex
- **Preview PDF** em nova aba
- **Toolbar** com formatação rápida

### **💬 Chat Colaborativo**
- **Mensagens em tempo real** via WebSocket
- **Salas isoladas** por projeto
- **Indicadores visuais** de usuários online
- **Histórico persistente** no banco de dados
- **Interface integrada** na sidebar

### **📚 Controle de Versões**
- **Snapshots automáticos** a cada compilação
- **Numeração sequencial** de versões
- **Visualização** de código anterior
- **Comparação** lado a lado
- **Restauração** de versões específicas

### **👥 Gestão de Usuários**
- **Registro** e login seguro
- **Planos Free/Paid** com limitações
- **Projetos privados** por usuário
- **Sistema de permissões** granular

### **🌐 Internacionalização**
- **3 idiomas** completos
- **Troca dinâmica** de idioma
- **Interface traduzida** 100%
- **Suporte a RTL** (futuro)

## 🔧 API Endpoints

### **Autenticação**
- `POST /auth/login` - Login
- `POST /auth/register` - Registro
- `GET /auth/logout` - Logout

### **Projetos**
- `GET /dashboard` - Lista projetos
- `POST /create-project` - Criar projeto
- `POST /project/<id>/rename` - Renomear
- `POST /project/<id>/delete` - Excluir

### **Editor**
- `GET /project/<id>/editor` - Abrir editor
- `POST /project/<id>/save` - Salvar arquivo
- `POST /project/<id>/compile` - Compilar PDF
- `GET /project/<id>/pdf` - Visualizar PDF

### **Chat (WebSocket)**
- `join_project` - Entrar na sala
- `leave_project` - Sair da sala
- `send_message` - Enviar mensagem
- `typing` - Indicador de digitação

### **Versões**
- `GET /project/<id>/versions` - Listar versões
- `GET /project/<id>/version/<vid>` - Ver versão
- `GET /project/<id>/compare` - Comparar versões
- `POST /project/<id>/version/<vid>/restore` - Restaurar

## 🎨 Tecnologias Utilizadas

### **Backend**
- **Flask 2.3.3** - Framework web
- **Flask-SQLAlchemy 3.0.5** - ORM
- **Flask-Login 0.6.3** - Autenticação
- **Flask-Babel 4.0.0** - Internacionalização
- **Flask-SocketIO 5.3.6** - WebSocket
- **SQLite/PostgreSQL** - Banco de dados

### **Frontend**
- **HTML5** - Estrutura semântica
- **CSS3** - Estilos e animações
- **JavaScript ES6+** - Interatividade
- **Socket.IO** - Comunicação real-time
- **CodeMirror 5.65.2** - Editor de código
- **Font Awesome 6.4.0** - Ícones

### **Ferramentas**
- **LaTeX** - Compilação de documentos
- **Git** - Controle de versão
- **Python 3.8+** - Linguagem principal

## 📊 Limitações por Plano

### **🆓 Plano Gratuito**
- ✅ 1 projeto ativo
- ✅ 1 arquivo .tex por projeto
- ✅ Chat colaborativo
- ✅ Histórico de versões
- ✅ Compilação PDF
- ❌ Upload de imagens
- ❌ Múltiplos arquivos

### **💎 Plano Pago**
- ✅ Projetos ilimitados
- ✅ Arquivos ilimitados
- ✅ Upload de imagens
- ✅ Chat colaborativo
- ✅ Histórico de versões
- ✅ Compilação PDF
- ✅ Colaboração em tempo real

## 🧪 Testes

### **Teste Local**
```bash
# Execute a aplicação
python app.py

# Acesse no navegador
http://localhost:5000

# Teste com múltiplos usuários
# Abra várias abas/navegadores
```

### **Teste de Chat**
1. Abra o editor em duas abas
2. Faça login com usuários diferentes
3. Digite mensagens em uma aba
4. Veja aparecer na outra aba em tempo real

### **Teste de Versões**
1. Compile um projeto (cria versão 1)
2. Faça mudanças no código
3. Compile novamente (cria versão 2)
4. Acesse o histórico de versões
5. Compare e restaure versões

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### **Padrões de Código**
- **Python:** PEP 8
- **JavaScript:** ES6+ com comentários
- **CSS:** BEM methodology
- **HTML:** Semântico e acessível

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🐛 Reportar Bugs

Se encontrar algum problema:

1. **Verifique** se já existe uma issue similar
2. **Crie** uma nova issue com:
   - Descrição detalhada do problema
   - Passos para reproduzir
   - Screenshots (se aplicável)
   - Informações do sistema

## 📞 Suporte

- **GitHub Issues:** Para bugs e sugestões
- **Email:** contato@doccollab.com
- **Documentação:** [Wiki do projeto](https://github.com/nilmarpublio/Doccollab/wiki)

## 🎯 Roadmap

### **Próximas Versões**
- [ ] **v2.1** - Suporte a múltiplos arquivos LaTeX
- [ ] **v2.2** - Upload de imagens e bibliografias
- [ ] **v2.3** - Colaboração em tempo real no editor
- [ ] **v2.4** - Templates LaTeX pré-definidos
- [ ] **v2.5** - Export para Word/PDF
- [ ] **v3.0** - API REST completa
- [ ] **v3.1** - Integração com Git
- [ ] **v3.2** - Plugins e extensões

---

**Desenvolvido com ❤️ usando Flask, SocketIO e muito café ☕**

*DocCollab - Colaboração inteligente para documentos LaTeX*