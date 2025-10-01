# 🚀 Deploy DocCollab no Glitch

## 📋 Passo a Passo Completo:

### 1️⃣ **Criar Conta no Glitch:**
1. **Acesse** https://glitch.com
2. **Clique** em "Sign up"
3. **Escolha** "Sign up with GitHub" (recomendado) ou "Sign up with email"
4. **Preencha** os dados e crie sua conta

### 2️⃣ **Criar Novo Projeto:**
1. **Clique** em "New Project"
2. **Escolha** "Import from GitHub" ou "Hello Python"
3. **Configure:**
   - **Project name:** `doccollab`
   - **Description:** `Collaborative LaTeX Editor`

### 3️⃣ **Fazer Upload dos Arquivos:**
1. **Delete** os arquivos padrão (se houver)
2. **Faça upload** de todos os arquivos do projeto
3. **Renomeie** `env_glitch.txt` para `.env`

### 4️⃣ **Configurar Variáveis de Ambiente:**
1. **Clique** em ".env" no editor
2. **Edite** as configurações:
   ```
   SECRET_KEY=sua-chave-secreta-aqui
   DATABASE_URL=sqlite:///doccollab.db
   PDFLATEX=/usr/bin/pdflatex
   SEED_EMAIL=admin@glitch.com
   SEED_PASSWORD=admin123456
   ```

### 5️⃣ **Configurar package.json:**
1. **Abra** o arquivo `package.json`
2. **Verifique** se está correto
3. **Salve** as alterações

### 6️⃣ **Configurar app_glitch.py:**
1. **Renomeie** `app_glitch.py` para `app.py`
2. **Delete** o arquivo `app.py` antigo (se houver)
3. **Salve** as alterações

### 7️⃣ **Instalar Dependências:**
1. **Abra** o terminal (Tools → Terminal)
2. **Execute** os comandos:
   ```bash
   pip install -r requirements.txt
   ```

### 8️⃣ **Configurar Banco de Dados:**
1. **Execute** o script de setup:
   ```bash
   python setup_glitch.py
   ```

### 9️⃣ **Testar:**
1. **Clique** em "Show" para ver o site
2. **Teste** o login com:
   - **Email:** `admin@glitch.com`
   - **Senha:** `admin123456`

## 🔧 **Se der problema:**

### ❌ Erro 500:
- **Verifique** se todas as dependências foram instaladas
- **Confirme** se o arquivo `.env` está configurado
- **Teste** se o banco foi criado

### ❌ Erro de importação:
- **Verifique** se todos os arquivos foram enviados
- **Confirme** se o Python path está correto

### ❌ Banco não funciona:
- **Execute** `python setup_glitch.py`
- **Verifique** se o arquivo `.env` está correto

## ✅ **Checklist Final:**

- [ ] Conta criada no Glitch ✅
- [ ] Projeto criado ✅
- [ ] Arquivos enviados ✅
- [ ] Dependências instaladas ✅
- [ ] Banco configurado ✅
- [ ] Site funcionando ✅

---

**🎉 Parabéns! Seu DocCollab estará no ar!**

**URL do seu projeto:** `https://doccollab.glitch.me`


