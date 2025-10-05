#!/bin/bash
# Deploy Script for DocCollab on DigitalOcean
# Execute this script on your DigitalOcean droplet

set -e  # Exit on any error

echo "🚀 Starting DocCollab deployment on DigitalOcean..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Use a regular user with sudo privileges."
    exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git curl wget unzip

# Install LaTeX
print_status "Installing LaTeX (this may take a while)..."
sudo apt install -y texlive-full

# Install Node.js
print_status "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create application directory
print_status "Setting up application directory..."
mkdir -p /home/$USER/DocCollab
cd /home/$USER/DocCollab

# Clone repository (if not already exists)
if [ ! -d "DocCollab" ]; then
    print_status "Cloning repository..."
    git clone https://github.com/nilmarpublio/Doccollab.git
fi

cd DocCollab

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn

# Configure environment
print_status "Configuring environment..."
if [ ! -f ".env" ]; then
    cp env_digitalocean.txt .env
    print_warning "Please edit .env file with your production settings"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p projects trash versions logs static/uploads

# Set permissions
print_status "Setting permissions..."
chmod +x app.py
chmod 755 static/
chmod 755 templates/

# Configure Nginx
print_status "Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/doccollab
sudo ln -sf /etc/nginx/sites-available/doccollab /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Configure Supervisor
print_status "Configuring Supervisor..."
sudo cp supervisor.conf /etc/supervisor/conf.d/doccollab.conf

# Update Supervisor configuration
print_status "Updating Supervisor configuration..."
sudo supervisorctl reread
sudo supervisorctl update

# Start services
print_status "Starting services..."
sudo systemctl reload nginx
sudo supervisorctl start doccollab

# Check status
print_status "Checking service status..."
sudo supervisorctl status doccollab

# Setup log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/doccollab > /dev/null <<EOF
/var/log/doccollab.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        sudo supervisorctl restart doccollab
    endscript
}
EOF

# Setup firewall (if UFW is available)
if command -v ufw &> /dev/null; then
    print_status "Configuring firewall..."
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw --force enable
fi

# Create systemd service for auto-start
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/doccollab.service > /dev/null <<EOF
[Unit]
Description=DocCollab Application
After=network.target

[Service]
Type=forking
User=$USER
Group=$USER
WorkingDirectory=/home/$USER/DocCollab
ExecStart=/usr/bin/supervisorctl start doccollab
ExecStop=/usr/bin/supervisorctl stop doccollab
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable doccollab

# Final checks
print_status "Running final checks..."

# Check if application is running
if sudo supervisorctl status doccollab | grep -q "RUNNING"; then
    print_success "DocCollab is running!"
else
    print_error "DocCollab failed to start. Check logs:"
    sudo tail -20 /var/log/doccollab.log
    exit 1
fi

# Check if Nginx is running
if systemctl is-active --quiet nginx; then
    print_success "Nginx is running!"
else
    print_error "Nginx failed to start"
    exit 1
fi

# Display information
print_success "Deployment completed successfully!"
echo ""
echo "📋 Deployment Information:"
echo "  • Application: http://$(curl -s ifconfig.me)"
echo "  • Logs: sudo tail -f /var/log/doccollab.log"
echo "  • Status: sudo supervisorctl status doccollab"
echo "  • Restart: sudo supervisorctl restart doccollab"
echo "  • Nginx: sudo systemctl status nginx"
echo ""
echo "🔧 Next Steps:"
echo "  1. Configure your domain name in Nginx"
echo "  2. Set up SSL with Let's Encrypt"
echo "  3. Update .env with production values"
echo "  4. Test all functionality"
echo ""
print_success "DocCollab is now running on DigitalOcean! 🎉"
