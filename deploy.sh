#!/bin/bash

# ============================================================================
# Script de Deploy Automatizado - DocCollab
# ============================================================================
# Este script automatiza o deploy da aplicação DocCollab no DigitalOcean
# 
# Uso: ./deploy.sh [SERVIDOR_IP] [USUARIO]
# Exemplo: ./deploy.sh 142.93.123.45 root
# ============================================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar argumentos
if [ "$#" -lt 2 ]; then
    log_error "Uso: $0 [SERVIDOR_IP] [USUARIO]"
    log_info "Exemplo: $0 142.93.123.45 root"
    exit 1
fi

SERVER_IP=$1
SERVER_USER=$2
APP_NAME="doccollab"
APP_DIR="/var/www/$APP_NAME"
DOMAIN=${3:-$SERVER_IP}  # Usar IP se domínio não fornecido

log_info "============================================"
log_info "Deploy DocCollab"
log_info "============================================"
log_info "Servidor: $SERVER_USER@$SERVER_IP"
log_info "Diretório: $APP_DIR"
log_info "Domínio: $DOMAIN"
log_info "============================================"
echo ""

# Perguntar confirmação
read -p "Deseja continuar com o deploy? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    log_warning "Deploy cancelado pelo usuário"
    exit 0
fi

# ============================================================================
# ETAPA 1: Preparar servidor
# ============================================================================
log_info "ETAPA 1: Preparando servidor..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    # Atualizar sistema
    echo "[1/5] Atualizando sistema..."
    apt-get update -qq
    apt-get upgrade -y -qq
    
    # Instalar dependências
    echo "[2/5] Instalando dependências..."
    apt-get install -y -qq \
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
    
    # Criar diretórios
    echo "[3/5] Criando estrutura de diretórios..."
    mkdir -p /var/www/doccollab
    mkdir -p /var/log/doccollab
    
    # Criar usuário para a aplicação (se não existir)
    echo "[4/5] Configurando usuário da aplicação..."
    if ! id -u doccollab > /dev/null 2>&1; then
        useradd -r -s /bin/bash -d /var/www/doccollab doccollab
    fi
    
    echo "[5/5] Servidor preparado!"
ENDSSH

log_success "Servidor preparado com sucesso!"

# ============================================================================
# ETAPA 2: Transferir arquivos
# ============================================================================
log_info "ETAPA 2: Transferindo arquivos..."

# Criar arquivo temporário com lista de arquivos a ignorar
cat > /tmp/rsync-exclude.txt << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env
.venv/
venv/
ENV/
.git/
.gitignore
.vscode/
.idea/
*.db
instance/
logs/
*.log
node_modules/
.DS_Store
EOF

# Rsync para transferir arquivos
rsync -avz --progress \
    --exclude-from=/tmp/rsync-exclude.txt \
    ./ $SERVER_USER@$SERVER_IP:$APP_DIR/

log_success "Arquivos transferidos com sucesso!"

# ============================================================================
# ETAPA 3: Configurar aplicação
# ============================================================================
log_info "ETAPA 3: Configurando aplicação..."

ssh $SERVER_USER@$SERVER_IP << ENDSSH
    cd $APP_DIR
    
    # Criar ambiente virtual
    echo "[1/6] Criando ambiente virtual..."
    python3 -m venv venv
    
    # Ativar ambiente virtual e instalar dependências
    echo "[2/6] Instalando dependências Python..."
    source venv/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    pip install gunicorn -q
    
    # Criar arquivo .env se não existir
    echo "[3/6] Configurando variáveis de ambiente..."
    if [ ! -f .env ]; then
        cp env.example .env
        # Gerar SECRET_KEY aleatória
        SECRET_KEY=\$(python3 -c "import secrets; print(secrets.token_hex(32))")
        sed -i "s/your-secret-key-here-change-this-in-production/\$SECRET_KEY/" .env
        sed -i "s/FLASK_ENV=production/FLASK_ENV=production/" .env
    fi
    
    # Criar diretórios necessários
    echo "[4/6] Criando diretórios da aplicação..."
    mkdir -p instance uploads logs translations
    
    # Compilar traduções
    echo "[5/6] Compilando traduções..."
    source venv/bin/activate
    pybabel compile -d translations
    
    # Ajustar permissões
    echo "[6/6] Ajustando permissões..."
    chown -R doccollab:doccollab $APP_DIR
    chmod -R 755 $APP_DIR
    chmod -R 775 $APP_DIR/uploads
    chmod -R 775 $APP_DIR/instance
    chmod -R 775 $APP_DIR/logs
    
    echo "Aplicação configurada!"
ENDSSH

log_success "Aplicação configurada com sucesso!"

# ============================================================================
# ETAPA 4: Configurar Gunicorn + Supervisor
# ============================================================================
log_info "ETAPA 4: Configurando Gunicorn e Supervisor..."

# Criar arquivo de configuração do Supervisor
ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    cat > /etc/supervisor/conf.d/doccollab.conf << 'EOF'
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
EOF

    # Recarregar Supervisor
    supervisorctl reread
    supervisorctl update
    supervisorctl restart doccollab
    
    echo "Gunicorn e Supervisor configurados!"
ENDSSH

log_success "Gunicorn e Supervisor configurados!"

# ============================================================================
# ETAPA 5: Configurar Nginx
# ============================================================================
log_info "ETAPA 5: Configurando Nginx..."

ssh $SERVER_USER@$SERVER_IP << ENDSSH
    cat > /etc/nginx/sites-available/doccollab << 'EOF'
server {
    listen 80;
    server_name $DOMAIN;
    
    client_max_body_size 16M;
    
    # Logs
    access_log /var/log/nginx/doccollab-access.log;
    error_log /var/log/nginx/doccollab-error.log;
    
    # Servir arquivos estáticos
    location /static {
        alias /var/www/doccollab/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /uploads {
        alias /var/www/doccollab/uploads;
        expires 7d;
    }
    
    # Socket.IO
    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Proxy para aplicação Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
EOF

    # Ativar site
    ln -sf /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    
    # Testar configuração
    nginx -t
    
    # Recarregar Nginx
    systemctl reload nginx
    
    echo "Nginx configurado!"
ENDSSH

log_success "Nginx configurado!"

# ============================================================================
# ETAPA 6: Configurar Firewall
# ============================================================================
log_info "ETAPA 6: Configurando firewall..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    # Configurar UFW
    ufw --force enable
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 'Nginx Full'
    ufw status
    
    echo "Firewall configurado!"
ENDSSH

log_success "Firewall configurado!"

# ============================================================================
# ETAPA 7: Verificar status
# ============================================================================
log_info "ETAPA 7: Verificando status dos serviços..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    echo "=== Status Supervisor ==="
    supervisorctl status doccollab
    
    echo ""
    echo "=== Status Nginx ==="
    systemctl status nginx --no-pager | head -n 10
    
    echo ""
    echo "=== Últimas linhas do log ==="
    tail -n 20 /var/log/doccollab/error.log
ENDSSH

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
echo ""
log_success "============================================"
log_success "Deploy concluído com sucesso!"
log_success "============================================"
log_info "Aplicação disponível em: http://$DOMAIN"
log_info ""
log_info "Comandos úteis:"
log_info "  - Ver logs: ssh $SERVER_USER@$SERVER_IP 'tail -f /var/log/doccollab/error.log'"
log_info "  - Reiniciar app: ssh $SERVER_USER@$SERVER_IP 'supervisorctl restart doccollab'"
log_info "  - Status: ssh $SERVER_USER@$SERVER_IP 'supervisorctl status doccollab'"
log_info ""
log_warning "IMPORTANTE:"
log_warning "1. Configure SSL com Let's Encrypt: certbot --nginx -d $DOMAIN"
log_warning "2. Altere a senha do usuário admin (admin@doccollab.com / admin123)"
log_warning "3. Configure backups regulares do banco de dados"
log_info "============================================"






