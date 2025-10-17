# 💬 Chat Colaborativo - Sistema Completo

Sistema de chat em tempo real para grupos de trabalho, desenvolvido com **Flask puro + SQLite**.

---

## 🚀 Características

✅ **Autenticação Segura** - Login/registro com senhas hash (bcrypt)  
✅ **Grupos de Trabalho** - Até 5 grupos por usuário  
✅ **Chat em Tempo Real** - Polling automático a cada 3 segundos  
✅ **Upload de Arquivos** - Imagens, PDFs, documentos (máx. 10MB)  
✅ **Drag & Drop** - Arraste arquivos diretamente no chat  
✅ **Busca Global** - Encontre mensagens por palavra-chave  
✅ **Histórico Persistente** - Mensagens armazenadas por 1 ano  
✅ **Painel Admin** - Estatísticas e logs de atividade  
✅ **Design Moderno** - Interface responsiva com Bootstrap 5  
✅ **Notificações** - Toast notifications elegantes  

---

## 📁 Estrutura do Projeto

```
DocCollab/
├── app.py                      # Aplicação Flask principal
├── database/
│   ├── schema.sql              # Estrutura do banco de dados
│   ├── init_db.py              # Script de inicialização
│   └── chat.db                 # Banco SQLite (criado automaticamente)
├── utils/
│   ├── db.py                   # Conexão com o banco
│   ├── auth.py                 # Autenticação e segurança
│   └── helpers.py              # Funções auxiliares
├── templates/
│   ├── base.html               # Template base
│   ├── login.html              # Página de login
│   ├── register.html           # Página de registro
│   ├── chat.html               # Interface principal do chat
│   └── admin.html              # Painel de administração
├── static/
│   ├── css/style.css           # Estilos customizados
│   └── js/main.js              # JavaScript principal
└── uploads/                    # Arquivos enviados pelos usuários
```

---

## ⚙️ Instalação

### 1️⃣ **Requisitos**

- Python 3.8+
- pip

### 2️⃣ **Instalar Dependências**

```bash
pip install flask werkzeug
```

### 3️⃣ **Inicializar o Banco de Dados**

```bash
cd DocCollab
python database/init_db.py
```

Você verá:
```
✅ Banco de dados criado com sucesso!
📍 Localização: D:\OurDocs\DocCollab\database\chat.db

🔐 Credenciais de acesso:
   Admin: admin@chat.com / admin123
   Teste: joao@chat.com / teste123
```

### 4️⃣ **Rodar o Servidor**

```bash
python app.py
```

O servidor estará rodando em: **http://localhost:5000**

---

## 🔐 Credenciais de Teste

| Tipo | Email | Senha |
|------|-------|-------|
| **Admin** | admin@chat.com | admin123 |
| **Usuário** | joao@chat.com | teste123 |

---

## 📖 Como Usar

### **1. Login**
- Acesse `http://localhost:5000`
- Use as credenciais de teste ou crie uma nova conta

### **2. Criar Grupo**
- Clique em **"Novo Grupo"** na sidebar
- Digite o nome e descrição (opcional)
- Você será o administrador do grupo

### **3. Adicionar Membros** (Admin)
- Entre no grupo criado
- Clique em **"Gerenciar Membros"**
- Digite o email do usuário e clique em "Adicionar"

### **4. Enviar Mensagens**
- Digite no campo de texto e pressione Enter
- Ou clique no ícone de envio

### **5. Enviar Arquivos**
- Clique no ícone 📎 (clipe)
- Ou arraste o arquivo diretamente na área de mensagens
- Tipos suportados: PNG, JPG, PDF, DOC, TXT, ZIP

### **6. Buscar Mensagens**
- Clique na busca (ou Ctrl+K)
- Digite a palavra-chave
- Resultados aparecem em tempo real

### **7. Painel Admin** (apenas admin@chat.com)
- Menu → Administração
- Veja estatísticas
- Acompanhe atividades dos usuários

---

## 🛠️ Funcionalidades Técnicas

### **Backend (Flask Puro)**
- Rotas RESTful sem frameworks extras
- SQLite com queries SQL diretas
- Context managers para conexões
- Logs de atividade automáticos

### **Frontend**
- Bootstrap 5 para UI
- Font Awesome para ícones
- JavaScript vanilla (sem jQuery)
- Polling a cada 3 segundos para mensagens

### **Segurança**
- Senhas com hash bcrypt
- Sessões protegidas
- Verificação de permissões em todas as rotas
- Upload de arquivos com validação de tipo

### **Banco de Dados**
- 6 tabelas: users, groups, group_members, messages, activity_log
- Índices para otimização
- Foreign keys com CASCADE
- Timestamps automáticos

---

## 🔄 Manutenção

### **Limpar Mensagens Antigas**

Mensagens com mais de 1 ano serão mantidas por padrão. Para alterar:

```python
# Em utils/helpers.py
def clean_old_messages(days=365):  # Altere aqui
```

Execute manualmente:
```python
from utils.helpers import clean_old_messages
clean_old_messages(days=30)  # Deletar mensagens com mais de 30 dias
```

### **Backup do Banco**

```bash
cp database/chat.db database/chat_backup.db
```

### **Reset Completo**

```bash
python database/init_db.py
```
⚠️ Isso apaga TODOS os dados!

---

## 📊 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/groups/create` | Criar grupo |
| POST | `/api/groups/<id>/members/add` | Adicionar membro |
| DELETE | `/api/groups/<id>/members/<user_id>/remove` | Remover membro |
| GET | `/api/messages/<group_id>` | Buscar mensagens |
| POST | `/api/messages/send` | Enviar mensagem |
| POST | `/api/messages/upload` | Upload de arquivo |
| DELETE | `/api/messages/<id>/delete` | Deletar mensagem |
| GET | `/api/search?q=<query>` | Buscar mensagens |

---

## 🎨 Personalização

### **Cores**

Edite `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;     /* Azul-roxo */
    --secondary-color: #764ba2;   /* Roxo */
    --success-color: #28a745;     /* Verde */
    /* ... */
}
```

### **Limite de Grupos**

Em `app.py`, função `api_create_group()`:
```python
if count['count'] >= 5:  # Altere aqui
```

### **Tamanho Máximo de Arquivo**

Em `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
```

---

## 🐛 Solução de Problemas

### **Erro: Banco de dados não encontrado**
```bash
python database/init_db.py
```

### **Erro: Módulo não encontrado**
```bash
pip install flask werkzeug
```

### **Porta 5000 ocupada**

Em `app.py`, última linha:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Altere a porta
```

### **Mensagens não atualizam automaticamente**
- Verifique o console do navegador (F12)
- O polling deve estar ativo (a cada 3 segundos)

---

## 📝 Licença

Projeto educacional - Use livremente para aprendizado.

---

## 👨‍💻 Desenvolvido com

- **Flask** - Microframework Python
- **SQLite** - Banco de dados embutido
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Ícones
- **Vanilla JavaScript** - Sem dependências extras

---

## ✅ Status

**SISTEMA COMPLETO E FUNCIONAL** ✨

Todas as funcionalidades especificadas no prompt foram implementadas:
- ✅ Chat em tempo real (polling)
- ✅ Upload de arquivos (drag & drop)
- ✅ Notificações visuais
- ✅ Histórico persistente
- ✅ CRUD completo de grupos e usuários
- ✅ Autenticação segura
- ✅ Painel de administração
- ✅ Sistema de busca
- ✅ Interface responsiva

---

**🚀 Acesse agora: http://localhost:5000**

**Login: admin@chat.com / admin123**
