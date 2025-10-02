# 🚀 Deploy DocCollab no PythonAnywhere

## 📋 Passo a Passo Completo:

### 1️⃣ **Criar Conta no PythonAnywhere:**
1. **Acesse** https://pythonanywhere.com
2. **Clique** em "Create a Beginner account"
3. **Preencha** os dados:
   - **Username:** (escolha um nome de usuário)
   - **Email:** (seu email)
   - **Password:** (sua senha)
4. **Clique** em "Create account"

### 2️⃣ **Fazer Upload dos Arquivos:**
1. **Entre** no painel do PythonAnywhere
2. **Clique** em "Files"
3. **Navegue** para a pasta home
4. **Crie** uma pasta chamada `doccollab`
5. **Faça upload** de todos os arquivos do projeto

### 3️⃣ **Configurar Variáveis de Ambiente:**
1. **Renomeie** `env_pythonanywhere.txt` para `.env`
2. **Edite** o arquivo `.env` com suas configurações

### 4️⃣ **Instalar Dependências:**
1. **Vá** para "Consoles"
2. **Clique** em "Bash"
3. **Execute** os comandos:
   ```bash
   cd doccollab
   pip3.10 install --user -r requirements.txt
   ```

### 5️⃣ **Configurar Banco de Dados:**
1. **Execute** o script de setup:
   ```bash
   python3.10 setup_pythonanywhere.py
   ```

### 6️⃣ **Configurar Web App:**
1. **Vá** para "Web"
2. **Clique** em "Add a new web app"
3. **Escolha** "Flask"
4. **Configure:**
   - **Python version:** 3.10
   - **Source code:** `/home/seuusuario/doccollab`
   - **WSGI file:** `/home/seuusuario/doccollab/app_pythonanywhere.py`
5. **Salve** as configurações

### 7️⃣ **Testar:**
1. **Acesse** seu domínio: `https://seuusuario.pythonanywhere.com`
2. **Teste** o login com:
   - **Email:** `admin@pythonanywhere.com`
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
- **Execute** `python3.10 setup_pythonanywhere.py`
- **Verifique** se o arquivo `.env` está correto

## ✅ **Checklist Final:**

- [ ] Conta criada no PythonAnywhere ✅
- [ ] Arquivos enviados ✅
- [ ] Dependências instaladas ✅
- [ ] Banco configurado ✅
- [ ] Web app configurado ✅
- [ ] Site funcionando ✅

---

**🎉 Parabéns! Seu DocCollab estará no ar!**



