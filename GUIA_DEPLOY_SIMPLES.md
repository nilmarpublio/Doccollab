# 🚀 Guia de Deploy Simples - DocCollab

## 🎯 Deploy Rápido (5 minutos)

### 1️⃣ **PREPARAR O PROJETO**

Execute no terminal (na pasta do projeto):
```bash
python fix_deploy_issues.py
```

Este script vai:
- ✅ Criar arquivo `.env` correto
- ✅ Corrigir arquivo `wsgi.py`
- ✅ Criar diretórios necessários
- ✅ Verificar dependências
- ✅ Testar aplicação

### 2️⃣ **ATUALIZAR BANCO DE DADOS**

```bash
python update_db_versions.py
python update_db_chat.py
```

### 3️⃣ **FAZER DEPLOY**

#### **Opção A: PythonAnywhere**
1. **Faça upload** dos arquivos para `/home/seuusuario/DocCollab/`
2. **Configure WSGI** para usar `wsgi.py`
3. **Configure Static Files:**
   - URL: `/static/` → Directory: `/home/seuusuario/DocCollab/static/`
   - URL: `/socket.io/` → Directory: `/home/seuusuario/DocCollab/static/`
4. **Reinicie** a aplicação

#### **Opção B: Hostinger**
1. **Faça upload** dos arquivos para `public_html/`
2. **Configure Python App** com entry point `wsgi.py`
3. **Ative** a aplicação

#### **Opção C: Heroku**
```bash
git add .
git commit -m "Deploy fix"
git push heroku main
```

## 🔧 **Problemas Comuns e Soluções**

### ❌ **Erro 500 - Internal Server Error**
**Solução:**
1. Verifique se o arquivo `.env` existe
2. Execute: `python fix_deploy_issues.py`
3. Reinicie a aplicação

### ❌ **Erro de Import - Module not found**
**Solução:**
1. Instale dependências: `pip install -r requirements.txt`
2. Verifique se está no diretório correto

### ❌ **Erro de SocketIO - WebSocket não funciona**
**Solução:**
1. Configure static files para `/socket.io/`
2. Verifique se o arquivo `wsgi.py` está correto

### ❌ **Erro de Banco de Dados**
**Solução:**
1. Execute: `python update_db_versions.py`
2. Execute: `python update_db_chat.py`
3. Verifique permissões da pasta `instance/`

## 📋 **Checklist de Deploy**

- [ ] Arquivo `.env` criado ✅
- [ ] Arquivo `wsgi.py` corrigido ✅
- [ ] Dependências instaladas ✅
- [ ] Banco de dados atualizado ✅
- [ ] Diretórios criados ✅
- [ ] Static files configurados ✅
- [ ] Aplicação reiniciada ✅
- [ ] Site funcionando ✅

## 🎉 **Teste Final**

1. **Acesse** seu site
2. **Faça login** com: `admin@doccollab.com` / `admin123456`
3. **Crie um projeto** e teste o editor
4. **Teste o chat** (abra duas abas)
5. **Teste as versões** (compile o projeto)

## 📞 **Ainda com Problemas?**

1. **Execute o diagnóstico:**
   ```bash
   python diagnose_deploy.py
   ```

2. **Verifique os logs** do seu provedor

3. **Me envie:**
   - Qual provedor está usando
   - Qual erro específico aparece
   - Print da tela se possível

## 🚀 **Deploy Automático**

Para deploy automático, execute:
```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows
deploy.bat
```

---

**🎯 Com este guia, seu DocCollab estará no ar em 5 minutos!**

