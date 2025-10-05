#!/bin/bash
# SSL Setup Script for DocCollab on DigitalOcean
# Configure Let's Encrypt SSL certificate

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check if domain is provided
if [ -z "$1" ]; then
    print_error "Please provide your domain name as an argument"
    echo "Usage: ./setup_ssl.sh yourdomain.com"
    exit 1
fi

DOMAIN=$1

print_status "Setting up SSL for domain: $DOMAIN"

# Install Certbot
print_status "Installing Certbot..."
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Stop Nginx temporarily
print_status "Stopping Nginx temporarily..."
sudo systemctl stop nginx

# Get SSL certificate
print_status "Obtaining SSL certificate..."
sudo certbot certonly --standalone -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# Update Nginx configuration for SSL
print_status "Updating Nginx configuration for SSL..."
sudo tee /etc/nginx/sites-available/doccollab > /dev/null <<EOF
# HTTP redirect to HTTPS
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Logs
    access_log /var/log/nginx/doccollab_access.log;
    error_log /var/log/nginx/doccollab_error.log;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript;
    
    # Static files
    location /static {
        alias /home/doccollab/DocCollab/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
        
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Socket.IO WebSocket support
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Deny access to sensitive files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~ \.(env|log|ini|conf)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }
    
    location = /robots.txt {
        log_not_found off;
        access_log off;
    }
}
EOF

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Start Nginx
print_status "Starting Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

# Setup automatic renewal
print_status "Setting up automatic SSL renewal..."
sudo tee /etc/cron.d/certbot > /dev/null <<EOF
0 12 * * * root /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx"
EOF

# Test renewal
print_status "Testing certificate renewal..."
sudo certbot renew --dry-run

print_success "SSL setup completed successfully!"
echo ""
echo "🔒 SSL Information:"
echo "  • Domain: https://$DOMAIN"
echo "  • Certificate: /etc/letsencrypt/live/$DOMAIN/"
echo "  • Auto-renewal: Configured"
echo ""
echo "🔧 Next Steps:"
echo "  1. Update your domain DNS to point to this server"
echo "  2. Test the HTTPS connection"
echo "  3. Update your .env file with the new domain"
echo ""
print_success "DocCollab is now running with SSL! 🎉"
