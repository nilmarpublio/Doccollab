# 🚀 Deploy do DocCollab na Hostinger

## 📋 Pré-requisitos

1. **Conta na Hostinger** com hospedagem compartilhada ou VPS
2. **Python 3.8+** habilitado no painel
3. **Acesso SSH** (recomendado) ou **File Manager**

## 🔧 Passo a Passo

### 1. Preparar Arquivos

1. **Compacte o projeto** (exceto `venv/` e `__pycache__/`):
   ```bash
   # No Windows (PowerShell)
   Compress-Archive -Path "DocCollab" -DestinationPath "doccollab-deploy.zip" -Exclude "venv", "__pycache__"
   ```

2. **Arquivos essenciais** que devem estar incluídos:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `.htaccess`
   - `setup_db.py`
   - `env.production.example`
   - `models/` (pasta completa)
   - `routes/` (pasta completa)
   - `services/` (pasta completa)
   - `utils/` (pasta completa)
   - `templates/` (pasta completa)
   - `static/` (pasta completa)
   - `translations/` (pasta completa)

### 2. Upload para Hostinger

1. **Acesse o File Manager** no painel da Hostinger
2. **Navegue para** `public_html/` (ou subdomínio)
3. **Faça upload** do arquivo `doccollab-deploy.zip`
4. **Extraia** o arquivo na pasta `public_html/`

### 3. Configurar Variáveis de Ambiente

1. **Renomeie** `env.production.example` para `.env`
2. **Edite** o arquivo `.env` com suas configurações:
   ```env
   SECRET_KEY=uma-chave-secreta-muito-longa-e-aleatoria
   DATABASE_URL=sqlite:///doccollab.db
   PDFLATEX=/usr/bin/pdflatex
   SEED_EMAIL=admin@seudominio.com
   SEED_PASSWORD=senha-super-segura
   ```

### 4. Instalar Dependências

**Via SSH** (recomendado):
```bash
cd public_html/DocCollab
python3 -m pip install --user -r requirements.txt
```

**Via File Manager**:
- Use o **Python App** no painel da Hostinger
- Configure para usar `wsgi.py` como entry point

### 5. Configurar Banco de Dados

**Via SSH**:
```bash
cd public_html/DocCollab
python3 setup_db.py
```

**Via File Manager**:
- Execute `setup_db.py` através do painel Python

### 6. Configurar LaTeX (Opcional)

Se quiser compilação PDF:
1. **Instale LaTeX** no servidor (se disponível)
2. **Atualize** `PDFLATEX` no `.env` com o caminho correto
3. **Teste** a compilação no editor

### 7. Configurar Domínio

1. **Aponte** seu domínio para a pasta `public_html/DocCollab/`
2. **Configure** SSL (HTTPS) no painel da Hostinger
3. **Teste** o acesso: `https://seudominio.com`

## 🔒 Configurações de Segurança

### 1. Permissões de Arquivo
```bash
chmod 644 .env
chmod 755 wsgi.py
chmod 755 setup_db.py
chmod 755 -R static/
chmod 755 -R templates/
```

### 2. Proteger Arquivos Sensíveis
Adicione ao `.htaccess`:
```apache
# Proteger arquivos sensíveis
<Files ".env">
    Order allow,deny
    Deny from all
</Files>

<Files "*.db">
    Order allow,deny
    Deny from all
</Files>
```

## 🐛 Troubleshooting

### Erro 500 - Internal Server Error
1. **Verifique** os logs de erro no painel da Hostinger
2. **Confirme** se todas as dependências estão instaladas
3. **Teste** se `wsgi.py` está executando corretamente

### Erro de Importação
1. **Verifique** se o Python path está correto
2. **Confirme** se todos os arquivos foram enviados
3. **Teste** a importação localmente

### Banco de Dados não Cria
1. **Execute** `setup_db.py` manualmente
2. **Verifique** permissões de escrita na pasta
3. **Confirme** se o SQLite está disponível

## 📞 Suporte

Se encontrar problemas:
1. **Verifique** os logs de erro
2. **Teste** localmente primeiro
3. **Consulte** a documentação da Hostinger
4. **Entre em contato** com o suporte da Hostinger

## ✅ Checklist Final

- [ ] Arquivos enviados corretamente
- [ ] `.env` configurado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Domínio configurado
- [ ] SSL ativado
- [ ] Teste de login funcionando
- [ ] Teste de compilação PDF (se aplicável)

---

**🎉 Parabéns!** Seu DocCollab está no ar!









