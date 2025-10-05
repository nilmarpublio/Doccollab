# 🚀 Deploy DocCollab em doccollab.agrobests.com.br

## 📋 O que você precisa fazer:

### 1️⃣ PREPARAR OS ARQUIVOS (Já fiz para você!)

**Arquivos prontos:**
- ✅ `doccollab-deploy.zip` - Arquivo principal
- ✅ `wsgi.py` - Configuração do servidor
- ✅ `.htaccess` - Redirecionamentos
- ✅ `requirements.txt` - Dependências Python

### 2️⃣ FAZER UPLOAD NA HOSTINGER

**Passo a passo:**

1. **Entre** no painel da Hostinger
2. **Vá** para "File Manager"
3. **Navegue** para `public_html`
4. **Faça upload** do arquivo `doccollab-deploy.zip`
5. **Clique** com botão direito no ZIP → "Extract Here"
6. **Delete** o arquivo ZIP após extrair

### 3️⃣ CONFIGURAR PYTHON APP

**Como fazer:**

1. **Procure** por "Python App" no painel
2. **Clique** em "Create Python App"
3. **Configure:**
   - **App Name:** `doccollab`
   - **Python Version:** `3.8` ou superior
   - **App Directory:** `public_html/doccollab-deploy`
   - **Startup File:** `wsgi.py`
4. **Clique** em "Create"

### 4️⃣ CONFIGURAR VARIÁVEIS DE AMBIENTE

**Edite o arquivo `.env`:**

1. **Abra** o File Manager
2. **Vá** para `public_html/doccollab-deploy`
3. **Clique** em `.env` para editar
4. **Mude** estas linhas:

```env
SECRET_KEY=CHANGE_THIS_TO_A_VERY_SECURE_RANDOM_KEY_123456789
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@agrobests.com.br
SEED_PASSWORD=admin123456
```

### 5️⃣ CONFIGURAR DOMÍNIO

**Como fazer:**

1. **Vá** para "Domains" no painel
2. **Clique** em "Manage" ao lado de `agrobests.com.br`
3. **Vá** para "Subdomains"
4. **Crie** subdomínio:
   - **Subdomain:** `doccollab`
   - **Document Root:** `public_html/doccollab-deploy`
5. **Salve** as configurações

### 6️⃣ ATIVAR A APLICAÇÃO

**Como fazer:**

1. **Volte** para "Python App"
2. **Clique** em "Start" na aplicação `doccollab`
3. **Aguarde** 2-3 minutos
4. **Teste** acessando: `https://doccollab.agrobests.com.br`

### 7️⃣ CONFIGURAR BANCO DE DADOS

**Como fazer:**

1. **Vá** para "Python App"
2. **Clique** em "Terminal" na aplicação `doccollab`
3. **Execute** este comando:
   ```bash
   python3 setup_db.py
   ```
4. **Aguarde** a mensagem "✅ Banco de dados configurado!"

## 🔧 Se der problema:

### ❌ Erro 500 - Internal Server Error
**Solução:**
1. Verifique se todas as pastas foram enviadas
2. Confirme se o Python App está ativo
3. Verifique os logs no painel

### ❌ Página não carrega
**Solução:**
1. Aguarde 5-10 minutos após ativar
2. Teste com `https://doccollab.agrobests.com.br`
3. Verifique se o subdomínio está configurado

### ❌ Não consegue fazer login
**Solução:**
1. Execute `python3 setup_db.py` no terminal
2. Use: `admin@agrobests.com.br` / `admin123456`

### ❌ Erro de permissão
**Solução:**
1. Vá para File Manager
2. Selecione a pasta `doccollab-deploy`
3. Clique em "Permissions"
4. Mude para `755`

## ✅ Checklist Final:

- [ ] Arquivos enviados ✅
- [ ] Python App criado ✅
- [ ] Subdomínio configurado ✅
- [ ] Variáveis configuradas ✅
- [ ] Aplicação ativada ✅
- [ ] Banco configurado ✅
- [ ] Site funcionando ✅

## 🎉 Pronto!

**Seu DocCollab estará disponível em:**
**https://doccollab.agrobests.com.br**

**Login de teste:**
- **Email:** `admin@agrobests.com.br`
- **Senha:** `admin123456`

---

**💡 Dica:** Se travar em algum passo, me fale exatamente onde parou que te ajudo!









