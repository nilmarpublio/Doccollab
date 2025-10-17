# ✅ DocCollab - Pronto para Deploy!

## 🎉 Tudo Preparado!

Seu projeto DocCollab está **100% pronto** para deploy em produção!

---

## 📦 O que foi preparado?

### ✅ Scripts de Deploy
- **`deploy.sh`** - Deploy automatizado completo
- **`update.sh`** - Atualização rápida da aplicação

### ✅ Configuração
- **`env.example`** - Modelo de variáveis de ambiente
- **`requirements.txt`** - Todas as dependências Python

### ✅ Documentação Completa
- **`DEPLOY_QUICKSTART.md`** - Guia rápido (3 passos)
- **`docs/DEPLOY.md`** - Documentação completa
- **`PRE_DEPLOY_CHECKLIST.md`** - Checklist pré-deploy
- **`docs/DEPLOY_FILES.md`** - Guia de arquivos
- **`README.md`** - Documentação do sistema

---

## 🚀 Como Fazer o Deploy?

### Opção 1: Deploy Rápido (Recomendado)

```bash
# 1. Dar permissão ao script
chmod +x deploy.sh

# 2. Executar deploy
./deploy.sh SEU_IP root

# Exemplo:
./deploy.sh 142.93.123.45 root
```

**Pronto!** Em ~5 minutos sua aplicação estará no ar! 🎉

---

### Opção 2: Seguir o Guia Passo a Passo

1. Leia: `DEPLOY_QUICKSTART.md`
2. Revise: `PRE_DEPLOY_CHECKLIST.md`
3. Execute: `./deploy.sh SEU_IP root`
4. Configure SSL (opcional): `certbot --nginx -d seu-dominio.com`

---

## 📋 Checklist Rápido

Antes de fazer o deploy, certifique-se:

- [ ] Você tem um servidor Ubuntu 20.04+ (DigitalOcean, AWS, etc.)
- [ ] Você tem acesso SSH ao servidor (root ou sudo)
- [ ] O servidor tem mínimo 2GB RAM e 20GB disco
- [ ] Você tem o IP público do servidor

**Tudo certo?** Vamos ao deploy! 🚀

---

## 🎯 Passo a Passo Resumido

### 1. Preparar Script
```bash
cd DocCollab
chmod +x deploy.sh
```

### 2. Executar Deploy
```bash
./deploy.sh 142.93.123.45 root
```

### 3. Aguardar (~5 minutos)
O script irá:
- ✅ Instalar todas as dependências
- ✅ Configurar Nginx + Gunicorn + Supervisor
- ✅ Configurar firewall
- ✅ Iniciar a aplicação

### 4. Acessar
```
http://SEU_IP
```

### 5. Login Inicial
- **Email**: `admin@doccollab.com`
- **Senha**: `admin123`

⚠️ **IMPORTANTE**: Altere a senha imediatamente!

---

## 🔒 Configurar SSL (Opcional mas Recomendado)

Se você tem um domínio:

```bash
ssh root@SEU_IP
certbot --nginx -d seu-dominio.com
```

Pronto! Seu site estará em `https://seu-dominio.com` 🔐

---

## 🛠️ Comandos Úteis Pós-Deploy

### Ver logs em tempo real:
```bash
ssh root@SEU_IP 'tail -f /var/log/doccollab/error.log'
```

### Reiniciar aplicação:
```bash
ssh root@SEU_IP 'supervisorctl restart doccollab'
```

### Ver status:
```bash
ssh root@SEU_IP 'supervisorctl status doccollab'
```

### Atualizar aplicação:
```bash
chmod +x update.sh
./update.sh SEU_IP root
```

---

## 📚 Documentação Disponível

| Arquivo | Descrição |
|---------|-----------|
| `DEPLOY_QUICKSTART.md` | Guia rápido (3 passos) |
| `docs/DEPLOY.md` | Documentação completa |
| `PRE_DEPLOY_CHECKLIST.md` | Checklist pré-deploy |
| `docs/DEPLOY_FILES.md` | Guia de arquivos |
| `docs/ASSISTANT_README.md` | Assistente Virtual |
| `README.md` | Documentação geral |

---

## 🎓 Funcionalidades Incluídas

✅ **Sistema de Autenticação**
- Login/Logout
- Registro de usuários
- Gerenciamento de sessões

✅ **Editor LaTeX**
- Editor de código com syntax highlighting
- Compilação de documentos LaTeX
- Visualização de PDF
- Snippets prontos

✅ **Colaboração em Tempo Real**
- Socket.IO para comunicação instantânea
- Chat colaborativo
- Sincronização de edições

✅ **Assistente Virtual Inteligente**
- Modo offline (regras)
- Modo hybrid (regras + IA)
- Modo LLM (IA completa)
- Suporte PT/EN/ES

✅ **LaTeX Linter**
- Detecção de erros
- Sugestões de correção
- Regras configuráveis

✅ **Gerenciamento de Projetos**
- Criar/Renomear/Excluir projetos
- Upload de arquivos
- Versionamento

✅ **Internacionalização (i18n)**
- Português
- Inglês
- Espanhol

✅ **Segurança**
- Sanitização de comandos LaTeX
- Proteção contra comandos perigosos
- Auditoria de ações
- Permissões granulares

---

## 🌐 Requisitos do Servidor

### Mínimo:
- **OS**: Ubuntu 20.04+ ou Debian 10+
- **RAM**: 2GB
- **Disco**: 20GB
- **CPU**: 1 core

### Recomendado:
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 4GB
- **Disco**: 40GB
- **CPU**: 2 cores

### Software (instalado automaticamente):
- Python 3.8+
- Nginx
- Supervisor
- TeX Live (LaTeX)
- Git

---

## 💡 Dicas Importantes

### 1. Backup
O script de atualização (`update.sh`) cria backups automáticos em:
```
/var/backups/doccollab/
```

### 2. Logs
Todos os logs estão em:
```
/var/log/doccollab/
```

### 3. Banco de Dados
O banco SQLite está em:
```
/var/www/doccollab/instance/doccollab.db
```

### 4. Uploads
Arquivos enviados pelos usuários estão em:
```
/var/www/doccollab/uploads/
```

---

## 🆘 Problemas Comuns

### Erro 502 Bad Gateway
```bash
ssh root@SEU_IP 'supervisorctl restart doccollab'
```

### Aplicação não inicia
```bash
ssh root@SEU_IP 'tail -n 50 /var/log/doccollab/error.log'
```

### Permissões negadas
```bash
ssh root@SEU_IP 'chown -R doccollab:doccollab /var/www/doccollab'
```

### Socket.IO não funciona
```bash
ssh root@SEU_IP 'nginx -t && systemctl reload nginx'
```

---

## 📞 Suporte

Se encontrar problemas:

1. ✅ Consulte `docs/DEPLOY.md` (seção Troubleshooting)
2. ✅ Verifique os logs: `/var/log/doccollab/error.log`
3. ✅ Revise o checklist: `PRE_DEPLOY_CHECKLIST.md`
4. ✅ Teste localmente antes de fazer deploy

---

## 🎯 Próximos Passos Após Deploy

1. **Alterar senha do admin**
   - Login: `admin@doccollab.com` / `admin123`
   - Ir em Perfil → Alterar Senha

2. **Configurar SSL** (se tiver domínio)
   ```bash
   certbot --nginx -d seu-dominio.com
   ```

3. **Criar usuários de teste**
   - Registrar novos usuários
   - Testar funcionalidades

4. **Testar compilação LaTeX**
   - Criar projeto
   - Escrever documento LaTeX
   - Compilar e verificar PDF

5. **Testar assistente virtual**
   - Abrir chat
   - Enviar mensagens
   - Testar comandos

6. **Configurar backups automáticos**
   - Criar cron job para backup diário
   - Testar restauração

---

## ✨ Recursos Adicionais

### Habilitar LLM (IA)

Se quiser usar IA real (OpenAI, etc.):

1. Obter API Key
2. Editar `/var/www/doccollab/.env`:
   ```
   LLM_MODE=llm
   LLM_API_KEY=sua-chave-aqui
   LLM_MODEL=gpt-3.5-turbo
   ```
3. Reiniciar: `supervisorctl restart doccollab`

### Aumentar Performance

Editar `/etc/supervisor/conf.d/doccollab.conf`:
```ini
# Aumentar workers (fórmula: 2 x CPU cores + 1)
command=.../gunicorn --workers 8 --threads 4 ...
```

---

## 🎉 Conclusão

Você está pronto para fazer o deploy do DocCollab! 🚀

**Comando para iniciar:**
```bash
chmod +x deploy.sh
./deploy.sh SEU_IP root
```

**Tempo estimado**: ~5 minutos  
**Dificuldade**: Fácil (automatizado)  
**Resultado**: Aplicação LaTeX colaborativa completa no ar! 🎊

---

**Boa sorte com seu deploy!** 🍀

Se tiver dúvidas, consulte a documentação completa em `docs/DEPLOY.md`






