# 📁 Arquivos de Deploy - Guia Rápido

Este documento lista todos os arquivos relacionados ao deploy do DocCollab.

---

## 📄 Arquivos Criados

### 1. **`deploy.sh`** 🚀
**Localização**: `DocCollab/deploy.sh`  
**Descrição**: Script principal de deploy automatizado  
**Uso**:
```bash
chmod +x deploy.sh
./deploy.sh SEU_IP root
```

**O que faz**:
- ✅ Prepara servidor (instala dependências)
- ✅ Transfere arquivos
- ✅ Configura ambiente virtual Python
- ✅ Configura Gunicorn + Supervisor
- ✅ Configura Nginx
- ✅ Configura firewall
- ✅ Inicia aplicação

---

### 2. **`update.sh`** 🔄
**Localização**: `DocCollab/update.sh`  
**Descrição**: Script de atualização rápida (para aplicação já deployada)  
**Uso**:
```bash
chmod +x update.sh
./update.sh SEU_IP root
```

**O que faz**:
- ✅ Cria backup automático
- ✅ Transfere apenas arquivos alterados
- ✅ Atualiza dependências
- ✅ Recompila traduções
- ✅ Reinicia aplicação

---

### 3. **`env.example`** ⚙️
**Localização**: `DocCollab/env.example`  
**Descrição**: Modelo de arquivo de configuração  
**Uso**:
```bash
cp env.example .env
nano .env  # Editar conforme necessário
```

**Variáveis principais**:
- `SECRET_KEY`: Chave secreta do Flask
- `FLASK_ENV`: production/development
- `LLM_MODE`: offline/hybrid/llm
- `DATABASE_URL`: Caminho do banco de dados

---

### 4. **`requirements.txt`** 📦
**Localização**: `DocCollab/requirements.txt`  
**Descrição**: Lista de dependências Python  
**Conteúdo**:
- Flask 2.3.3
- Flask-SocketIO 5.3.6
- Flask-Babel 4.0.0
- SQLAlchemy 2.0.43
- E outras...

---

### 5. **`docs/DEPLOY.md`** 📖
**Localização**: `DocCollab/docs/DEPLOY.md`  
**Descrição**: Documentação completa de deploy  
**Conteúdo**:
- Pré-requisitos detalhados
- Deploy automatizado (passo a passo)
- Deploy manual (passo a passo)
- Configuração SSL
- Comandos úteis
- Troubleshooting extensivo
- Configurações avançadas
- Monitoramento
- Segurança

---

### 6. **`DEPLOY_QUICKSTART.md`** ⚡
**Localização**: `DocCollab/DEPLOY_QUICKSTART.md`  
**Descrição**: Guia rápido de deploy (3 passos)  
**Para quem**: Usuários que querem deploy rápido sem detalhes

---

### 7. **`PRE_DEPLOY_CHECKLIST.md`** ✅
**Localização**: `DocCollab/PRE_DEPLOY_CHECKLIST.md`  
**Descrição**: Checklist completo pré-deploy  
**Seções**:
- Preparação local
- Servidor
- Segurança
- Deploy
- Monitoramento
- Documentação
- Plano de rollback

---

## 🎯 Fluxo de Deploy Recomendado

### Para Deploy Inicial:

1. **Revisar checklist**:
   ```bash
   cat PRE_DEPLOY_CHECKLIST.md
   ```

2. **Ler guia rápido**:
   ```bash
   cat DEPLOY_QUICKSTART.md
   ```

3. **Executar deploy**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh SEU_IP root
   ```

4. **Configurar SSL** (se tiver domínio):
   ```bash
   ssh root@SEU_IP
   certbot --nginx -d seu-dominio.com
   ```

5. **Alterar senha admin**:
   - Acessar: `http://SEU_IP`
   - Login: `admin@doccollab.com` / `admin123`
   - Alterar senha no perfil

---

### Para Atualizações:

1. **Fazer backup local** (opcional):
   ```bash
   git commit -am "Versão antes da atualização"
   git tag v1.0.0
   ```

2. **Executar atualização**:
   ```bash
   chmod +x update.sh
   ./update.sh SEU_IP root
   ```

3. **Verificar**:
   ```bash
   ssh root@SEU_IP 'supervisorctl status doccollab'
   ```

---

## 📊 Estrutura no Servidor

Após o deploy, a estrutura no servidor será:

```
/var/www/doccollab/
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências
├── .env                   # Configurações (criado no deploy)
├── venv/                  # Ambiente virtual Python
├── templates/             # Templates HTML
├── static/                # Arquivos estáticos (CSS, JS)
├── services/              # Serviços (assistente, linter, etc.)
├── models/                # Modelos do banco de dados
├── translations/          # Traduções (PT/EN/ES)
├── instance/              # Dados da aplicação
│   └── doccollab.db      # Banco de dados SQLite
├── uploads/               # Arquivos enviados pelos usuários
├── logs/                  # Logs da aplicação
└── docs/                  # Documentação

/etc/supervisor/conf.d/
└── doccollab.conf         # Configuração Supervisor

/etc/nginx/sites-available/
└── doccollab              # Configuração Nginx

/var/log/doccollab/
├── error.log              # Logs de erro
├── access.log             # Logs de acesso
├── supervisor-error.log   # Logs do Supervisor
└── supervisor-out.log     # Output do Supervisor
```

---

## 🔧 Comandos Essenciais

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

### Backup manual:
```bash
ssh root@SEU_IP 'cp /var/www/doccollab/instance/doccollab.db /var/backups/doccollab-$(date +%Y%m%d).db'
```

### Restaurar backup:
```bash
ssh root@SEU_IP 'cp /var/backups/doccollab-YYYYMMDD.db /var/www/doccollab/instance/doccollab.db && supervisorctl restart doccollab'
```

---

## 🆘 Troubleshooting Rápido

### Aplicação não inicia:
```bash
ssh root@SEU_IP 'tail -n 50 /var/log/doccollab/error.log'
```

### Erro 502 Bad Gateway:
```bash
ssh root@SEU_IP 'supervisorctl restart doccollab && systemctl restart nginx'
```

### Permissões negadas:
```bash
ssh root@SEU_IP 'chown -R doccollab:doccollab /var/www/doccollab && supervisorctl restart doccollab'
```

### Socket.IO não funciona:
```bash
ssh root@SEU_IP 'nginx -t && systemctl reload nginx'
```

---

## 📚 Documentação Completa

Para informações detalhadas, consulte:

- **Deploy completo**: `docs/DEPLOY.md`
- **Assistente Virtual**: `docs/ASSISTANT_README.md`
- **README principal**: `README.md`
- **Guia do Chat**: `docs/CHAT_ASSISTANT_GUIDE.md`

---

## 🎓 Recursos Adicionais

### Vídeos/Tutoriais (criar se necessário):
- [ ] Vídeo: Deploy inicial
- [ ] Vídeo: Atualização
- [ ] Vídeo: Configuração SSL
- [ ] Vídeo: Troubleshooting

### Scripts Adicionais (criar se necessário):
- [ ] Script de backup automático (cron)
- [ ] Script de monitoramento
- [ ] Script de rollback
- [ ] Script de migração de dados

---

## ✅ Checklist Rápido

Antes do deploy:
- [ ] `requirements.txt` atualizado
- [ ] `env.example` completo
- [ ] Traduções compiladas
- [ ] Testado localmente

Durante o deploy:
- [ ] Script executado sem erros
- [ ] Aplicação acessível
- [ ] Login funciona
- [ ] Compilação LaTeX funciona

Após o deploy:
- [ ] Senha admin alterada
- [ ] SSL configurado (se domínio)
- [ ] Backup configurado
- [ ] Logs verificados

---

**Pronto para o deploy! 🚀**

```bash
./deploy.sh SEU_IP root
```






