#!/bin/bash
# Script completo de deploy do DocCollab no DigitalOcean
# Data: 2025-10-09

set -e  # Parar em caso de erro

echo "=== Iniciando configuração do DocCollab ==="

# 1. Atualizar sistema
echo "1/10 Atualizando sistema..."
apt update
apt upgrade -y

# 2. Instalar dependências
echo "2/10 Instalando dependências..."
apt install -y python3 python3-pip python3-venv git nginx supervisor texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# 3. Criar usuário doccollab
echo "3/10 Criando usuário doccollab..."
if ! id "doccollab" &>/dev/null; then
    useradd -m -s /bin/bash doccollab
fi

# 4. Clonar repositório
echo "4/10 Clonando repositório..."
cd /home/doccollab
if [ -d "Doccollab" ]; then
    rm -rf Doccollab
fi
git clone https://github.com/nilmarpublio/Doccollab.git
cd Doccollab
git checkout feature/payment-system

# 5. Criar ambiente virtual
echo "5/10 Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# 6. Instalar dependências Python
echo "6/10 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# 7. Criar diretórios necessários
echo "7/10 Criando diretórios..."
mkdir -p /home/doccollab/Doccollab/projects
mkdir -p /home/doccollab/Doccollab/uploads
mkdir -p /home/doccollab/Doccollab/instance

# 8. Configurar permissões
echo "8/10 Configurando permissões..."
chown -R doccollab:doccollab /home/doccollab

# 9. Configurar Supervisor
echo "9/10 Configurando Supervisor..."
cat > /etc/supervisor/conf.d/doccollab.conf << 'EOF'
[program:doccollab]
directory=/home/doccollab/Doccollab
command=/home/doccollab/Doccollab/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
user=doccollab
group=doccollab
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/doccollab.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
environment=PYTHONPATH="/home/doccollab/Doccollab",FLASK_ENV="production"
EOF

# Criar arquivo de log
touch /var/log/doccollab.log
chown doccollab:doccollab /var/log/doccollab.log

# 10. Configurar firewall CORRETAMENTE
echo "10/10 Configurando firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 5000/tcp  # Flask (temporário)
ufw --force enable

# Recarregar Supervisor
supervisorctl reread
supervisorctl update
supervisorctl restart doccollab

echo ""
echo "=== ✅ Configuração completa! ==="
echo ""
echo "🌐 Acesse: http://143.198.101.113:5000"
echo ""
echo "📊 Para verificar status:"
echo "   sudo supervisorctl status doccollab"
echo ""
echo "📝 Para ver logs:"
echo "   sudo tail -f /var/log/doccollab.log"
echo ""

