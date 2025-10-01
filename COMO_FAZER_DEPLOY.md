# 🚀 Como Colocar o DocCollab no Ar - Guia Simples

## 📋 O que você vai precisar:
1. **Conta na Hostinger** (já tem ✅)
2. **Acesso ao painel** da Hostinger
3. **Arquivos do projeto** (vou te ajudar a preparar)

## 🎯 Passo a Passo SUPER SIMPLES:

### 1️⃣ PREPARAR OS ARQUIVOS (Vou fazer isso para você)

**O que fazer:**
- Vou criar um arquivo ZIP com tudo que precisa
- Você só vai fazer upload desse arquivo

### 2️⃣ FAZER UPLOAD NA HOSTINGER

**Como fazer:**
1. **Entre** no painel da Hostinger
2. **Clique** em "File Manager" 
3. **Vá** para a pasta `public_html`
4. **Faça upload** do arquivo ZIP que preparei
5. **Extraia** o arquivo ZIP lá dentro

### 3️⃣ CONFIGURAR O PYTHON

**Como fazer:**
1. **Procure** por "Python App" no painel
2. **Crie** uma nova aplicação Python
3. **Escolha** a versão Python 3.8 ou superior
4. **Configure** o entry point como `wsgi.py`

### 4️⃣ CONFIGURAR AS VARIÁVEIS

**Como fazer:**
1. **Abra** o arquivo `.env` no File Manager
2. **Mude** as seguintes linhas:
   ```
   SECRET_KEY=sua-chave-secreta-aqui
   SEED_EMAIL=admin@seudominio.com
   SEED_PASSWORD=suasenha123
   ```

### 5️⃣ ATIVAR A APLICAÇÃO

**Como fazer:**
1. **Volte** para o Python App
2. **Clique** em "Start" ou "Ativar"
3. **Aguarde** alguns minutos
4. **Teste** acessando seu domínio

## 🔧 Se der algum problema:

### ❌ Erro 500
- **Verifique** se todas as pastas foram enviadas
- **Confirme** se o Python está ativo

### ❌ Página não carrega
- **Aguarde** 5-10 minutos após ativar
- **Teste** com `https://seudominio.com`

### ❌ Não consegue fazer login
- **Execute** o script `setup_db.py` no painel
- **Verifique** se o banco foi criado

## 📞 Precisa de ajuda?

**Se travar em algum passo:**
1. **Me fale** exatamente onde parou
2. **Tire print** da tela se possível
3. **Vou te ajudar** a resolver

## ✅ Checklist Final:

- [ ] Arquivos enviados ✅
- [ ] Python ativado ✅  
- [ ] Variáveis configuradas ✅
- [ ] Aplicação rodando ✅
- [ ] Site funcionando ✅

---

**🎉 Depois disso seu DocCollab estará no ar!**


