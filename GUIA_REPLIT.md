# 🚀 Deploy DocCollab no Replit

## 📋 Passo a Passo Completo:

### 1️⃣ **Criar Conta no Replit:**
1. **Acesse** https://replit.com
2. **Clique** em "Sign up"
3. **Escolha** "Sign up with Google" ou "Sign up with email"
4. **Preencha** os dados e crie sua conta

### 2️⃣ **Criar Novo Repl:**
1. **Clique** em "Create Repl"
2. **Escolha** "Python" como linguagem
3. **Configure:**
   - **Name:** `doccollab`
   - **Description:** `Collaborative LaTeX Editor`

### 3️⃣ **Fazer Upload dos Arquivos:**
1. **Delete** os arquivos padrão (main.py, etc.)
2. **Faça upload** de todos os arquivos do projeto
3. **Renomeie** `env_replit.txt` para `.env`

### 4️⃣ **Configurar Variáveis de Ambiente:**
1. **Clique** em "Secrets" (ícone de cadeado)
2. **Adicione** as variáveis:
   - `SECRET_KEY` = `sua-chave-secreta-aqui`
   - `DATABASE_URL` = `sqlite:///doccollab.db`
   - `PDFLATEX` = `/usr/bin/pdflatex`
   - `SEED_EMAIL` = `admin@replit.com`
   - `SEED_PASSWORD` = `admin123456`

### 5️⃣ **Configurar app_replit.py:**
1. **Renomeie** `app_replit.py` para `main.py`
2. **Delete** o arquivo `app.py` antigo (se houver)
3. **Salve** as alterações

### 6️⃣ **Instalar Dependências:**
1. **Abra** o terminal (Tools → Shell)
2. **Execute** os comandos:
   ```bash
   pip install -r requirements.txt
   ```

### 7️⃣ **Configurar Banco de Dados:**
1. **Execute** o script de setup:
   ```bash
   python setup_replit.py
   ```

### 8️⃣ **Executar o Projeto:**
1. **Clique** em "Run" para executar
2. **Aguarde** o projeto carregar
3. **Clique** em "Open in new tab" para ver o site

### 9️⃣ **Testar:**
1. **Acesse** o site que abriu
2. **Teste** o login com:
   - **Email:** `admin@replit.com`
   - **Senha:** `admin123456`

## 🔧 **Se der problema:**

### ❌ Erro 500:
- **Verifique** se todas as dependências foram instaladas
- **Confirme** se as variáveis de ambiente estão configuradas
- **Teste** se o banco foi criado

### ❌ Erro de importação:
- **Verifique** se todos os arquivos foram enviados
- **Confirme** se o Python path está correto

### ❌ Banco não funciona:
- **Execute** `python setup_replit.py`
- **Verifique** se as variáveis de ambiente estão corretas

## ✅ **Checklist Final:**

- [ ] Conta criada no Replit ✅
- [ ] Repl criado ✅
- [ ] Arquivos enviados ✅
- [ ] Dependências instaladas ✅
- [ ] Banco configurado ✅
- [ ] Site funcionando ✅

---

**🎉 Parabéns! Seu DocCollab estará no ar!**

**URL do seu projeto:** `https://doccollab.seuusuario.repl.co`



