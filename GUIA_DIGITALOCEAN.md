# 🚀 Deploy DocCollab na DigitalOcean

## 📋 **Pré-requisitos**
- ✅ Conta na DigitalOcean
- ✅ Projeto "DocCollab" criado
- ✅ Droplet Ubuntu 20.04+ configurado
- ✅ Acesso SSH ao servidor

## 🎯 **Passo a Passo Completo**

### **1. Conectar ao Servidor**
```bash
ssh root@SEU_IP_DO_SERVIDOR
```

### **2. Atualizar Sistema**
```bash
apt update && apt upgrade -y
```

### **3. Instalar Dependências**
```bash
# Python 3.9+
apt install python3 python3-pip python3-venv nginx supervisor git -y

# LaTeX (para compilação PDF)
apt install texlive-full -y

# Node.js (para build tools)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install nodejs -y
```

### **4. Criar Usuário da Aplicação**
```bash
adduser doccollab
usermod -aG sudo doccollab
su - doccollab
```

### **5. Clonar Repositório**
```bash
cd /home/doccollab
git clone https://github.com/nilmarpublio/Doccollab.git
cd DocCollab
```

### **6. Configurar Ambiente Virtual**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **7. Configurar Variáveis de Ambiente**
```bash
cp env_digitalocean.txt .env
nano .env
```

### **8. Configurar Nginx**
```bash
sudo nano /etc/nginx/sites-available/doccollab
```

### **9. Configurar Supervisor**
```bash
sudo nano /etc/supervisor/conf.d/doccollab.conf
```

### **10. Ativar Configurações**
```bash
sudo ln -s /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start doccollab
```

## 🔧 **Configurações Específicas**

### **Nginx Config:**
```nginx
server {
    listen 80;
    server_name SEU_DOMINIO.com;

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

### **Supervisor Config:**
```ini
[program:doccollab]
command=/home/doccollab/DocCollab/venv/bin/python app.py
directory=/home/doccollab/DocCollab
user=doccollab
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/doccollab.log
environment=PATH="/home/doccollab/DocCollab/venv/bin"
```

## 🔐 **SSL com Let's Encrypt (Opcional)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d SEU_DOMINIO.com
```

## 📊 **Monitoramento**
```bash
# Ver logs da aplicação
sudo tail -f /var/log/doccollab.log

# Ver status do supervisor
sudo supervisorctl status

# Reiniciar aplicação
sudo supervisorctl restart doccollab
```

## 🎉 **Resultado Final**
- ✅ DocCollab rodando em produção
- ✅ Nginx servindo arquivos estáticos
- ✅ Supervisor gerenciando o processo
- ✅ SSL configurado (se aplicado)
- ✅ Logs centralizados

## 🚨 **Troubleshooting**

### **Erro 502 Bad Gateway:**
```bash
sudo supervisorctl status doccollab
sudo tail -f /var/log/doccollab.log
```

### **Erro de Permissão:**
```bash
sudo chown -R doccollab:doccollab /home/doccollab/DocCollab
```

### **Porta em Uso:**
```bash
sudo netstat -tlnp | grep :5000
sudo kill -9 PID_DO_PROCESSO
```

---

**🎯 Com este guia, seu DocCollab estará rodando perfeitamente na DigitalOcean!**
