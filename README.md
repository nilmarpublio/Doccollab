# DocCollab

Uma plataforma colaborativa para criação e edição de documentos, desenvolvida com Flask.

## 🚀 Características

- Editor colaborativo em tempo real
- Interface moderna e responsiva
- Sistema de autenticação
- Armazenamento na nuvem
- Suporte a LaTeX (em desenvolvimento)

## 📁 Estrutura do Projeto

```
DocCollab/
├── app.py                 # Aplicação principal Flask
├── routes/               # Blueprints das rotas
│   ├── __init__.py
│   ├── main.py          # Rotas principais
│   └── auth.py          # Rotas de autenticação
├── models/              # Modelos do banco de dados
├── services/            # Serviços e lógica de negócio
├── utils/               # Utilitários e funções auxiliares
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── auth/
│       ├── login.html
│       └── register.html
├── static/              # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── .env                 # Variáveis de ambiente
├── env.example          # Exemplo de variáveis de ambiente
├── requirements.txt     # Dependências Python
└── README.md
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a passo para Windows 11

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd DocCollab
   ```

2. **Crie um ambiente virtual**
   ```bash
   # Opção 1: Usando venv (recomendado)
   python -m venv venv
   
   # Opção 2: Usando virtualenv
   pip install virtualenv
   virtualenv venv
   ```

3. **Ative o ambiente virtual**
   ```bash
   # No PowerShell
   .\venv\Scripts\Activate.ps1
   
   # No Command Prompt
   venv\Scripts\activate.bat
   
   # No Git Bash
   source venv/Scripts/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure as variáveis de ambiente**
   ```bash
   # Copie o arquivo de exemplo
   copy env.example .env
   
   # Edite o arquivo .env com suas configurações
   notepad .env
   ```

6. **Execute a aplicação**
   ```bash
   python app.py
   ```

7. **Acesse a aplicação**
   Abra seu navegador e acesse: `http://localhost:5000`

## 🔧 Configuração das Variáveis de Ambiente

Edite o arquivo `.env` com as seguintes configurações:

```env
# Configurações do Flask
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

# Configurações do Banco de Dados
DATABASE_URL=sqlite:///doccollab.db

# Configurações de Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app

# Configurações de Upload
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=static/uploads
```

## 🚀 Executando a Aplicação

### Desenvolvimento
```bash
python app.py
```

### Produção (usando Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Funcionalidades Implementadas

- ✅ Página inicial com design moderno
- ✅ Sistema de navegação
- ✅ Páginas de login e cadastro
- ✅ Estrutura base para autenticação
- ✅ Design responsivo
- ✅ Sistema de mensagens flash

## 🔮 Próximas Funcionalidades

- [ ] Sistema de autenticação completo
- [ ] Editor de documentos colaborativo
- [ ] Suporte a LaTeX
- [ ] Sistema de versionamento
- [ ] Upload de arquivos
- [ ] Compartilhamento de documentos
- [ ] API REST

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas, por favor abra uma issue no repositório.

---

**Desenvolvido com ❤️ usando Flask**
