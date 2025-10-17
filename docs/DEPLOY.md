# 🚀 Guia de Deploy - DocCollab

Este guia detalha como fazer o deploy da aplicação DocCollab em um servidor DigitalOcean (ou qualquer servidor Ubuntu/Debian).

---

## 📋 Pré-requisitos

### No seu computador local:
- Git instalado
- SSH configurado
- Acesso ao código-fonte do DocCollab

### No servidor:
- Ubuntu 20.04 ou superior (ou Debian 10+)
- Mínimo 2GB RAM
- 20GB de espaço em disco
- Acesso root ou sudo
- IP público ou domínio configurado

---

## 🎯 Método 1: Deploy Automatizado (Recomendado)

### Passo 1: Preparar o script

No seu computador local, dentro da pasta `DocCollab`:

```bash
# Dar permissão de execução ao script
chmod +x deploy.sh
```

### Passo 2: Executar o deploy

```bash
# Sintaxe: ./deploy.sh [IP_SERVIDOR] [USUARIO] [DOMINIO_OPCIONAL]
./deploy.sh 142.93.123.45 root

# Ou com domínio:
./deploy.sh 142.93.123.45 root doccollab.com
```

### Passo 3: Aguardar conclusão

O script irá:
1. ✅ Atualizar o servidor
2. ✅ Instalar todas as dependências (Python, Nginx, TeX Live, etc.)
3. ✅ Transferir os arquivos da aplicação
4. ✅ Configurar ambiente virtual Python
5. ✅ Configurar Gunicorn + Supervisor
6. ✅ Configurar Nginx como proxy reverso
7. ✅ Configurar firewall (UFW)
8. ✅ Iniciar a aplicação

### Passo 4: Verificar

Acesse no navegador:
```
http://SEU_IP_OU_DOMINIO
```

Você deve ver a página inicial do DocCollab! 🎉

---

## 🔧 Método 2: Deploy Manual

Se preferir fazer passo a passo manualmente:

### 1. Conectar ao servidor

```bash
ssh root@SEU_IP
```

### 2. Atualizar sistema

```bash
apt-get update
apt-get upgrade -y
```

### 3. Instalar dependências

```bash
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    supervisor \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-lang-portuguese \
    git \
    curl
```

### 4. Criar estrutura de diretórios

```bash
mkdir -p /var/www/doccollab
mkdir -p /var/log/doccollab
```

### 5. Criar usuário da aplicação

```bash
useradd -r -s /bin/bash -d /var/www/doccollab doccollab
```

### 6. Clonar/transferir código

**Opção A: Git (se o repositório for público/privado com chave SSH)**
```bash
cd /var/www
git clone https://github.com/SEU_USUARIO/DocCollab.git doccollab
```

**Opção B: Rsync do seu computador local**
```bash
# No seu computador local:
rsync -avz --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' \
    ./DocCollab/ root@SEU_IP:/var/www/doccollab/
```

### 7. Configurar ambiente virtual

```bash
cd /var/www/doccollab
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 8. Configurar variáveis de ambiente

```bash
cp env.example .env
nano .env
```

Edite o arquivo `.env` e configure:
- `SECRET_KEY`: Gere uma chave aleatória forte
- `FLASK_ENV=production`
- Outras configurações conforme necessário

**Gerar SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 9. Criar diretórios e compilar traduções

```bash
mkdir -p instance uploads logs translations
source venv/bin/activate
pybabel compile -d translations
```

### 10. Ajustar permissões

```bash
chown -R doccollab:doccollab /var/www/doccollab
chmod -R 755 /var/www/doccollab
chmod -R 775 /var/www/doccollab/uploads
chmod -R 775 /var/www/doccollab/instance
chmod -R 775 /var/www/doccollab/logs
```

### 11. Configurar Supervisor

Criar `/etc/supervisor/conf.d/doccollab.conf`:

```ini
[program:doccollab]
directory=/var/www/doccollab
command=/var/www/doccollab/venv/bin/gunicorn --workers 4 --threads 2 --worker-class eventlet --bind 127.0.0.1:5000 --timeout 120 --access-logfile /var/log/doccollab/access.log --error-logfile /var/log/doccollab/error.log app:app
user=doccollab
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/doccollab/supervisor-error.log
stdout_logfile=/var/log/doccollab/supervisor-out.log
environment=PATH="/var/www/doccollab/venv/bin"
```

Ativar:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start doccollab
```

### 12. Configurar Nginx

Criar `/etc/nginx/sites-available/doccollab`:

```nginx
server {
    listen 80;
    server_name SEU_DOMINIO_OU_IP;
    
    client_max_body_size 16M;
    
    access_log /var/log/nginx/doccollab-access.log;
    error_log /var/log/nginx/doccollab-error.log;
    
    location /static {
        alias /var/www/doccollab/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /uploads {
        alias /var/www/doccollab/uploads;
        expires 7d;
    }
    
    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

Ativar site:
```bash
ln -s /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

### 13. Configurar Firewall

```bash
ufw enable
ufw allow ssh
ufw allow 'Nginx Full'
ufw status
```

---

## 🔒 Configurar SSL (HTTPS) - Recomendado

### Usando Let's Encrypt (Certbot)

```bash
# Instalar Certbot
apt-get install -y certbot python3-certbot-nginx

# Obter certificado SSL
certbot --nginx -d seu-dominio.com

# Renovação automática já está configurada!
```

Após isso, seu site estará disponível em `https://seu-dominio.com` 🔐

---

## 📊 Comandos Úteis

### Ver logs em tempo real
```bash
# Logs da aplicação
tail -f /var/log/doccollab/error.log

# Logs do Supervisor
tail -f /var/log/doccollab/supervisor-error.log

# Logs do Nginx
tail -f /var/log/nginx/doccollab-error.log
```

### Gerenciar aplicação
```bash
# Status
supervisorctl status doccollab

# Reiniciar
supervisorctl restart doccollab

# Parar
supervisorctl stop doccollab

# Iniciar
supervisorctl start doccollab
```

### Atualizar aplicação
```bash
# No seu computador local:
./deploy.sh SEU_IP root

# Ou manualmente no servidor:
cd /var/www/doccollab
git pull  # Se usar Git
source venv/bin/activate
pip install -r requirements.txt
pybabel compile -d translations
supervisorctl restart doccollab
```

### Backup do banco de dados
```bash
# Criar backup
cp /var/www/doccollab/instance/doccollab.db \
   /var/backups/doccollab-$(date +%Y%m%d-%H%M%S).db

# Restaurar backup
cp /var/backups/doccollab-YYYYMMDD-HHMMSS.db \
   /var/www/doccollab/instance/doccollab.db
supervisorctl restart doccollab
```

---

## 🐛 Troubleshooting

### Aplicação não inicia

1. **Verificar logs:**
   ```bash
   tail -n 50 /var/log/doccollab/error.log
   ```

2. **Verificar status do Supervisor:**
   ```bash
   supervisorctl status doccollab
   ```

3. **Testar manualmente:**
   ```bash
   cd /var/www/doccollab
   source venv/bin/activate
   python app.py
   ```

### Erro 502 Bad Gateway

1. **Verificar se Gunicorn está rodando:**
   ```bash
   supervisorctl status doccollab
   ps aux | grep gunicorn
   ```

2. **Verificar logs do Nginx:**
   ```bash
   tail -n 50 /var/log/nginx/doccollab-error.log
   ```

3. **Reiniciar serviços:**
   ```bash
   supervisorctl restart doccollab
   systemctl restart nginx
   ```

### Erro de compilação LaTeX

1. **Verificar se TeX Live está instalado:**
   ```bash
   which pdflatex
   pdflatex --version
   ```

2. **Instalar pacotes adicionais:**
   ```bash
   apt-get install -y texlive-full
   ```

3. **Verificar permissões:**
   ```bash
   ls -la /var/www/doccollab/uploads
   ```

### Socket.IO não funciona

1. **Verificar configuração do Nginx:**
   ```bash
   nginx -t
   cat /etc/nginx/sites-available/doccollab | grep socket.io
   ```

2. **Verificar se eventlet está instalado:**
   ```bash
   cd /var/www/doccollab
   source venv/bin/activate
   pip list | grep eventlet
   ```

### Permissões negadas

```bash
# Corrigir permissões
chown -R doccollab:doccollab /var/www/doccollab
chmod -R 755 /var/www/doccollab
chmod -R 775 /var/www/doccollab/uploads
chmod -R 775 /var/www/doccollab/instance
chmod -R 775 /var/www/doccollab/logs
supervisorctl restart doccollab
```

---

## ⚙️ Configurações Avançadas

### Aumentar workers do Gunicorn

Editar `/etc/supervisor/conf.d/doccollab.conf`:
```ini
# Fórmula: (2 x núcleos de CPU) + 1
command=.../gunicorn --workers 8 --threads 4 ...
```

Depois:
```bash
supervisorctl reread
supervisorctl update
supervisorctl restart doccollab
```

### Configurar domínio personalizado

1. **Apontar DNS:**
   - Criar registro A: `doccollab.com` → `SEU_IP`
   - Criar registro A: `www.doccollab.com` → `SEU_IP`

2. **Atualizar Nginx:**
   ```bash
   nano /etc/nginx/sites-available/doccollab
   # Alterar: server_name doccollab.com www.doccollab.com;
   nginx -t
   systemctl reload nginx
   ```

3. **Configurar SSL:**
   ```bash
   certbot --nginx -d doccollab.com -d www.doccollab.com
   ```

### Habilitar LLM (Assistente com IA)

1. **Obter API Key** (OpenAI, Anthropic, etc.)

2. **Editar `.env`:**
   ```bash
   nano /var/www/doccollab/.env
   ```
   
   Adicionar:
   ```
   LLM_MODE=llm
   LLM_API_KEY=sua-chave-aqui
   LLM_API_URL=https://api.openai.com/v1/chat/completions
   LLM_MODEL=gpt-3.5-turbo
   ```

3. **Reiniciar:**
   ```bash
   supervisorctl restart doccollab
   ```

---

## 📈 Monitoramento

### Instalar htop
```bash
apt-get install -y htop
htop
```

### Verificar uso de disco
```bash
df -h
du -sh /var/www/doccollab/*
```

### Verificar uso de memória
```bash
free -h
```

### Logs de acesso
```bash
# Ver IPs mais frequentes
awk '{print $1}' /var/log/nginx/doccollab-access.log | sort | uniq -c | sort -rn | head

# Ver páginas mais acessadas
awk '{print $7}' /var/log/nginx/doccollab-access.log | sort | uniq -c | sort -rn | head
```

---

## 🔐 Segurança

### Checklist de Segurança

- [ ] Alterar senha do usuário admin
- [ ] Configurar SSL/HTTPS
- [ ] Configurar firewall (UFW)
- [ ] Desabilitar login root via SSH
- [ ] Configurar fail2ban
- [ ] Backups automáticos
- [ ] Atualizar sistema regularmente
- [ ] Usar senhas fortes
- [ ] Limitar tentativas de login

### Configurar Fail2Ban

```bash
apt-get install -y fail2ban

cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOF

systemctl restart fail2ban
```

---

## 📞 Suporte

Se encontrar problemas:

1. Consulte a seção **Troubleshooting** acima
2. Verifique os logs detalhadamente
3. Consulte a documentação do projeto: `docs/README.md`
4. Abra uma issue no repositório

---

## 📝 Notas Finais

- **Usuário admin padrão**: `admin@doccollab.com` / `admin123` (ALTERE IMEDIATAMENTE!)
- **Porta padrão**: 80 (HTTP) ou 443 (HTTPS)
- **Banco de dados**: SQLite em `/var/www/doccollab/instance/doccollab.db`
- **Uploads**: `/var/www/doccollab/uploads/`

**Boa sorte com seu deploy! 🚀**






