#!/bin/bash

# ============================================================================
# Script de Atualização Rápida - DocCollab
# ============================================================================
# Este script atualiza a aplicação DocCollab já deployada
# 
# Uso: ./update.sh [SERVIDOR_IP] [USUARIO]
# Exemplo: ./update.sh 142.93.123.45 root
# ============================================================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
APP_DIR="/var/www/doccollab"

log_info "============================================"
log_info "Atualização DocCollab"
log_info "============================================"
log_info "Servidor: $SERVER_USER@$SERVER_IP"
log_info "============================================"
echo ""

# Perguntar confirmação
read -p "Deseja continuar com a atualização? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    log_warning "Atualização cancelada"
    exit 0
fi

# ============================================================================
# ETAPA 1: Backup
# ============================================================================
log_info "ETAPA 1: Criando backup..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    BACKUP_DIR="/var/backups/doccollab"
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    
    mkdir -p $BACKUP_DIR
    
    # Backup do banco de dados
    if [ -f /var/www/doccollab/instance/doccollab.db ]; then
        cp /var/www/doccollab/instance/doccollab.db \
           $BACKUP_DIR/doccollab-$TIMESTAMP.db
        echo "Backup criado: $BACKUP_DIR/doccollab-$TIMESTAMP.db"
    fi
    
    # Backup dos uploads
    if [ -d /var/www/doccollab/uploads ]; then
        tar -czf $BACKUP_DIR/uploads-$TIMESTAMP.tar.gz \
            -C /var/www/doccollab uploads
        echo "Backup uploads: $BACKUP_DIR/uploads-$TIMESTAMP.tar.gz"
    fi
ENDSSH

log_success "Backup criado!"

# ============================================================================
# ETAPA 2: Transferir arquivos atualizados
# ============================================================================
log_info "ETAPA 2: Transferindo arquivos atualizados..."

# Criar arquivo de exclusão
cat > /tmp/rsync-exclude.txt << EOF
__pycache__/
*.pyc
*.pyo
.Python
*.so
*.egg
*.egg-info/
.env
.venv/
venv/
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

# Rsync
rsync -avz --progress \
    --exclude-from=/tmp/rsync-exclude.txt \
    ./ $SERVER_USER@$SERVER_IP:$APP_DIR/

log_success "Arquivos transferidos!"

# ============================================================================
# ETAPA 3: Atualizar dependências e reiniciar
# ============================================================================
log_info "ETAPA 3: Atualizando dependências e reiniciando..."

ssh $SERVER_USER@$SERVER_IP << ENDSSH
    cd $APP_DIR
    
    # Ativar ambiente virtual
    source venv/bin/activate
    
    # Atualizar dependências
    echo "[1/4] Atualizando dependências..."
    pip install -r requirements.txt -q
    
    # Compilar traduções
    echo "[2/4] Compilando traduções..."
    pybabel compile -d translations
    
    # Ajustar permissões
    echo "[3/4] Ajustando permissões..."
    chown -R doccollab:doccollab $APP_DIR
    chmod -R 755 $APP_DIR
    chmod -R 775 $APP_DIR/uploads
    chmod -R 775 $APP_DIR/instance
    chmod -R 775 $APP_DIR/logs
    
    # Reiniciar aplicação
    echo "[4/4] Reiniciando aplicação..."
    supervisorctl restart doccollab
    
    # Aguardar inicialização
    sleep 3
    
    # Verificar status
    supervisorctl status doccollab
ENDSSH

log_success "Aplicação atualizada e reiniciada!"

# ============================================================================
# ETAPA 4: Verificar
# ============================================================================
log_info "ETAPA 4: Verificando aplicação..."

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    echo "=== Status Supervisor ==="
    supervisorctl status doccollab
    
    echo ""
    echo "=== Últimas 10 linhas do log ==="
    tail -n 10 /var/log/doccollab/error.log
ENDSSH

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
echo ""
log_success "============================================"
log_success "Atualização concluída com sucesso!"
log_success "============================================"
log_info "Aplicação disponível em: http://$SERVER_IP"
log_info ""
log_info "Comandos úteis:"
log_info "  - Ver logs: ssh $SERVER_USER@$SERVER_IP 'tail -f /var/log/doccollab/error.log'"
log_info "  - Status: ssh $SERVER_USER@$SERVER_IP 'supervisorctl status doccollab'"
log_info ""
log_warning "Se houver problemas, restaure o backup:"
log_warning "  ssh $SERVER_USER@$SERVER_IP 'ls -lh /var/backups/doccollab/'"
log_info "============================================"


