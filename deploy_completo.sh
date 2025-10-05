#!/bin/bash
# Script Completo de Deploy DocCollab na DigitalOcean
# Execute este script na console da DigitalOcean

set -e  # Para parar se houver erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Funções para output colorido
print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}  $1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${BLUE}[PASSO $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script deve ser executado como root"
    echo "Execute: sudo su"
    exit 1
fi

print_header "🚀 DEPLOY DOCCCOLLAB NA DIGITALOCEAN"
echo ""

# PASSO 1: Atualizar sistema
print_step "1" "Atualizando sistema..."
apt update -y
apt upgrade -y
print_success "Sistema atualizado"

# PASSO 2: Instalar dependências
print_step "2" "Instalando dependências..."
apt install -y python3 python3-pip python3-venv nginx supervisor git curl wget unzip htop
print_success "Dependências básicas instaladas"

# PASSO 3: Instalar LaTeX
print_step "3" "Instalando LaTeX (pode demorar alguns minutos)..."
apt install -y texlive-full
print_success "LaTeX instalado"

# PASSO 4: Instalar Node.js
print_step "4" "Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs
print_success "Node.js instalado"

# PASSO 5: Criar usuário da aplicação
print_step "5" "Criando usuário da aplicação..."
if ! id "doccollab" &>/dev/null; then
    adduser --disabled-password --gecos "" doccollab
    usermod -aG sudo doccollab
    print_success "Usuário doccollab criado"
else
    print_warning "Usuário doccollab já existe"
fi

# PASSO 6: Configurar diretório da aplicação
print_step "6" "Configurando diretório da aplicação..."
mkdir -p /home/doccollab/DocCollab
cd /home/doccollab

# PASSO 7: Clonar repositório
print_step "7" "Clonando repositório..."
if [ ! -d "DocCollab" ]; then
    git clone https://github.com/nilmarpublio/Doccollab.git
    print_success "Repositório clonado"
else
    print_warning "Repositório já existe, atualizando..."
    cd DocCollab
    git pull origin main
    cd ..
fi

cd DocCollab

# PASSO 8: Configurar ambiente virtual
print_step "8" "Configurando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
print_success "Ambiente virtual criado"

# PASSO 9: Instalar dependências Python
print_step "9" "Instalando dependências Python..."
pip install -r requirements.txt
pip install gunicorn
print_success "Dependências Python instaladas"

# PASSO 10: Configurar arquivo .env
print_step "10" "Configurando variáveis de ambiente..."
cat > .env << 'EOF'
# Configuração de Produção para DigitalOcean
SECRET_KEY=doccollab-super-secret-key-2024-digitalocean-production-change-this
DEBUG=False
TESTING=False
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@doccollab.com
SEED_PASSWORD=admin123456
SOCKETIO_ASYNC_MODE=eventlet
FLASK_ENV=production
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
PERMANENT_SESSION_LIFETIME=86400
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
CORS_ORIGINS=*
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization
PROJECTS_ROOT=projects
TRASH_ROOT=trash
VERSIONS_ROOT=versions
FREE_PLAN_MAX_PROJECTS=1
FREE_PLAN_MAX_FILES=1
PAID_PLAN_MAX_PROJECTS=999999
PAID_PLAN_MAX_FILES=999999
CHAT_MESSAGE_LIMIT=500
CHAT_HISTORY_LIMIT=1000
CHAT_TYPING_TIMEOUT=3000
VERSION_SNAPSHOT_ON_COMPILE=True
VERSION_MAX_HISTORY=50
VERSION_AUTO_CLEANUP=True
LATEX_MAX_RUNS=2
LATEX_TIMEOUT=30
LATEX_OUTPUT_DIR=output
BABEL_DEFAULT_LOCALE=pt
BABEL_SUPPORTED_LOCALES=pt,en,es
BABEL_TRANSLATION_DIRECTORIES=translations
EOF
print_success "Arquivo .env configurado"

# PASSO 11: Criar diretórios necessários
print_step "11" "Criando diretórios necessários..."
mkdir -p projects trash versions logs static/uploads
print_success "Diretórios criados"

# PASSO 12: Configurar permissões
print_step "12" "Configurando permissões..."
chown -R doccollab:doccollab /home/doccollab/DocCollab
chmod +x app.py
chmod 755 static/
chmod 755 templates/
print_success "Permissões configuradas"

# PASSO 13: Configurar Nginx
print_step "13" "Configurando Nginx..."
cat > /etc/nginx/sites-available/doccollab << 'EOF'
server {
    listen 80;
    server_name _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript;
    
    # Static files
    location /static {
        alias /home/doccollab/DocCollab/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Socket.IO WebSocket support
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
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Ativar site
ln -sf /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testar configuração
nginx -t
print_success "Nginx configurado"

# PASSO 14: Configurar Supervisor
print_step "14" "Configurando Supervisor..."
cat > /etc/supervisor/conf.d/doccollab.conf << 'EOF'
[program:doccollab]
command=/home/doccollab/DocCollab/venv/bin/python app.py
directory=/home/doccollab/DocCollab
user=doccollab
group=doccollab
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/doccollab.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
environment=PATH="/home/doccollab/DocCollab/venv/bin:/usr/local/bin:/usr/bin:/bin"
environment=PYTHONPATH="/home/doccollab/DocCollab"
environment=FLASK_ENV="production"
EOF

# Atualizar Supervisor
supervisorctl reread
supervisorctl update
print_success "Supervisor configurado"

# PASSO 15: Configurar firewall
print_step "15" "Configurando firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    print_success "Firewall configurado"
else
    print_warning "UFW não disponível, pulando configuração do firewall"
fi

# PASSO 16: Iniciar serviços
print_step "16" "Iniciando serviços..."
systemctl reload nginx
systemctl enable nginx
supervisorctl start doccollab
print_success "Serviços iniciados"

# PASSO 17: Configurar log rotation
print_step "17" "Configurando rotação de logs..."
cat > /etc/logrotate.d/doccollab << 'EOF'
/var/log/doccollab.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 doccollab doccollab
    postrotate
        supervisorctl restart doccollab
    endscript
}
EOF
print_success "Rotação de logs configurada"

# PASSO 18: Verificar status
print_step "18" "Verificando status dos serviços..."

# Verificar Nginx
if systemctl is-active --quiet nginx; then
    print_success "Nginx está rodando"
else
    print_error "Nginx não está rodando"
    systemctl status nginx
fi

# Verificar DocCollab
if supervisorctl status doccollab | grep -q "RUNNING"; then
    print_success "DocCollab está rodando"
else
    print_error "DocCollab não está rodando"
    supervisorctl status doccollab
    echo "Últimas linhas do log:"
    tail -20 /var/log/doccollab.log
fi

# Obter IP do servidor
SERVER_IP=$(curl -s ifconfig.me)

print_header "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo ""
echo "📋 Informações do Deploy:"
echo "  • Servidor: $SERVER_IP"
echo "  • Aplicação: http://$SERVER_IP"
echo "  • Usuário admin: admin@doccollab.com"
echo "  • Senha admin: admin123456"
echo ""
echo "🔧 Comandos Úteis:"
echo "  • Ver status: supervisorctl status doccollab"
echo "  • Ver logs: tail -f /var/log/doccollab.log"
echo "  • Reiniciar: supervisorctl restart doccollab"
echo "  • Status Nginx: systemctl status nginx"
echo ""
echo "🌐 Próximos Passos:"
echo "  1. Acesse http://$SERVER_IP para testar"
echo "  2. Configure seu domínio (opcional)"
echo "  3. Configure SSL com Let's Encrypt (opcional)"
echo ""
print_success "DocCollab está rodando na DigitalOcean! 🚀"
