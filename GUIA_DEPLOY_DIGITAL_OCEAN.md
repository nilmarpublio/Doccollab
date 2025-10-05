# 🚀 Deploy DocCollab na Digital Ocean - Guia Completo

## 📋 Pré-requisitos
- ✅ Conta na Digital Ocean
- ✅ Putty instalado (já tem!)
- ✅ Projeto DocCollab no GitHub (já tem!)
- ✅ Acesso ao painel da Digital Ocean

## 🎯 Passo a Passo COMPLETO

### **1️⃣ CRIAR DROPLET NA DIGITAL OCEAN**

#### **1.1 Configuração do Droplet**
1. **Acesse** o painel da Digital Ocean
2. **Clique** em "Create" → "Droplets"
3. **Escolha** a imagem: **Ubuntu 22.04 LTS**
4. **Escolha** o plano: **Basic** (recomendo $6/mês para começar)
5. **Escolha** a região mais próxima do Brasil (São Paulo se disponível)
6. **Adicione** sua chave SSH (se não tiver, vou te ajudar a criar)
7. **Nomeie** o droplet: `doccollab-server`
8. **Clique** em "Create Droplet"

#### **1.2 Aguardar Criação**
- Aguarde 2-3 minutos para o droplet ser criado
- Anote o **IP público** do droplet (ex: 164.90.123.456)

### **2️⃣ CONECTAR VIA SSH (PUTTY)**

#### **2.1 Configurar Conexão no Putty**
1. **Abra** o Putty
2. **Host Name:** Cole o IP do droplet (ex: 164.90.123.456)
3. **Port:** 22
4. **Connection Type:** SSH
5. **Clique** em "Open"

#### **2.2 Primeiro Login**
- **Username:** `root`
- **Password:** Cole a senha que a Digital Ocean enviou por email
- **IMPORTANTE:** Mude a senha na primeira conexão:
  ```bash
  passwd
  ```

### **3️⃣ CONFIGURAR SERVIDOR UBUNTU**

#### **3.1 Atualizar Sistema**
```bash
# Atualizar pacotes
apt update && apt upgrade -y

# Instalar dependências básicas
apt install -y python3 python3-pip python3-venv git nginx supervisor
```

#### **3.2 Instalar LaTeX**
```bash
# Instalar LaTeX completo
apt install -y texlive-full
```

#### **3.3 Criar Usuário para Aplicação**
```bash
# Criar usuário específico
adduser doccollab
usermod -aG sudo doccollab

# Trocar para o usuário
su - doccollab
```

### **4️⃣ CLONAR E CONFIGURAR PROJETO**

#### **4.1 Clonar Repositório**
```bash
# Ir para diretório home
cd /home/doccollab

# Clonar projeto do GitHub
git clone https://github.com/nilmarpublio/Doccollab.git
cd DocCollab
```

#### **4.2 Criar Ambiente Virtual**
```bash
# Criar venv
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

#### **4.3 Configurar Variáveis de Ambiente**
```bash
# Criar arquivo .env
nano .env
```

**Conteúdo do .env:**
```env
SECRET_KEY=doccollab-super-secret-key-2024-production-digitalocean
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123456
SOCKETIO_ASYNC_MODE=eventlet
DEBUG=False
FLASK_ENV=production
```

#### **4.4 Configurar Banco de Dados**
```bash
# Ativar venv
source venv/bin/activate

# Executar scripts de configuração
python update_db_versions.py
python update_db_chat.py
```

### **5️⃣ CONFIGURAR NGINX (SERVIDOR WEB)**

#### **5.1 Criar Configuração do Nginx**
```bash
# Voltar como root
exit

# Criar arquivo de configuração
nano /etc/nginx/sites-available/doccollab
```

**Conteúdo da configuração:**
```nginx
server {
    listen 80;
    server_name SEU_IP_AQUI;  # Substitua pelo IP do droplet

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/doccollab/DocCollab/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### **5.2 Ativar Site**
```bash
# Criar link simbólico
ln -s /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/

# Remover site padrão
rm /etc/nginx/sites-enabled/default

# Testar configuração
nginx -t

# Reiniciar nginx
systemctl restart nginx
systemctl enable nginx
```

### **6️⃣ CONFIGURAR SUPERVISOR (GERENCIADOR DE PROCESSOS)**

#### **6.1 Criar Configuração do Supervisor**
```bash
# Criar arquivo de configuração
nano /etc/supervisor/conf.d/doccollab.conf
```

**Conteúdo da configuração:**
```ini
[program:doccollab]
command=/home/doccollab/DocCollab/venv/bin/python /home/doccollab/DocCollab/app.py
directory=/home/doccollab/DocCollab
user=doccollab
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/doccollab.log
environment=PATH="/home/doccollab/DocCollab/venv/bin"
```

#### **6.2 Ativar Aplicação**
```bash
# Recarregar supervisor
supervisorctl reread
supervisorctl update

# Iniciar aplicação
supervisorctl start doccollab

# Verificar status
supervisorctl status doccollab
```

### **7️⃣ CONFIGURAR FIREWALL**

```bash
# Configurar UFW
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable
```

### **8️⃣ TESTAR APLICAÇÃO**

#### **8.1 Verificar Status**
```bash
# Verificar se nginx está rodando
systemctl status nginx

# Verificar se aplicação está rodando
supervisorctl status doccollab

# Ver logs da aplicação
tail -f /var/log/doccollab.log
```

#### **8.2 Acessar no Navegador**
- **URL:** `http://SEU_IP_AQUI`
- **Teste:** Página inicial deve carregar
- **Login:** Use admin@doccollab.com / admin123456

### **9️⃣ CONFIGURAR DOMÍNIO (OPCIONAL)**

#### **9.1 Se tiver domínio próprio:**
1. **Configure** DNS apontando para o IP do droplet
2. **Edite** arquivo nginx: `nano /etc/nginx/sites-available/doccollab`
3. **Substitua** `SEU_IP_AQUI` pelo seu domínio
4. **Reinicie** nginx: `systemctl restart nginx`

#### **9.2 Configurar SSL (HTTPS) - Recomendado:**
```bash
# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obter certificado SSL
certbot --nginx -d seudominio.com

# Testar renovação automática
certbot renew --dry-run
```

## 🔧 COMANDOS ÚTEIS PARA MANUTENÇÃO

### **Reiniciar Aplicação**
```bash
supervisorctl restart doccollab
```

### **Ver Logs**
```bash
tail -f /var/log/doccollab.log
```

### **Atualizar Código**
```bash
cd /home/doccollab/DocCollab
git pull
supervisorctl restart doccollab
```

### **Verificar Status**
```bash
# Status da aplicação
supervisorctl status doccollab

# Status do nginx
systemctl status nginx

# Uso de recursos
htop
```

## ✅ CHECKLIST FINAL

- [ ] Droplet criado na Digital Ocean
- [ ] Conectado via SSH (Putty)
- [ ] Ubuntu atualizado
- [ ] LaTeX instalado
- [ ] Projeto clonado do GitHub
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] Banco de dados configurado
- [ ] Nginx configurado
- [ ] Supervisor configurado
- [ ] Firewall configurado
- [ ] Aplicação rodando
- [ ] Site acessível no navegador
- [ ] Login funcionando
- [ ] Editor LaTeX funcionando
- [ ] Chat funcionando

## 🎉 RESULTADO FINAL

Após completar todos os passos, você terá:

- ✅ **DocCollab rodando na Digital Ocean**
- ✅ **Editor LaTeX profissional**
- ✅ **Chat colaborativo em tempo real**
- ✅ **Sistema de histórico de versões**
- ✅ **Interface responsiva moderna**
- ✅ **Sistema de usuários e planos**
- ✅ **Internacionalização completa**
- ✅ **SSL/HTTPS configurado (se usar domínio)**

## 📞 SUPORTE

Se houver algum problema:

1. **Verifique os logs:** `tail -f /var/log/doccollab.log`
2. **Verifique status:** `supervisorctl status doccollab`
3. **Verifique nginx:** `systemctl status nginx`
4. **Me envie** o erro específico que está acontecendo

**Sua aplicação DocCollab estará 100% funcional na Digital Ocean! 🚀**

