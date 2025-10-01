#!/bin/bash

# 🚀 Script de Correção Imediata - Autenticação GitHub
# DocCollab - Deploy Final

echo "🚀 Executando correção imediata de autenticação GitHub..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
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

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    print_error "Execute este script no diretório raiz do DocCollab"
    exit 1
fi

print_status "Configurando credenciais Git..."

# Configurar credenciais básicas
git config --global user.name "nilmarpublio"
git config --global user.email "nilmarpublio@github.com"
git config --global credential.helper store

print_success "Credenciais configuradas!"

print_status "Verificando configuração..."
git config --list | grep -E "(user|credential)"

print_warning "IMPORTANTE: Para fazer push, você precisa criar um Personal Access Token:"
echo ""
echo "1. Acesse: https://github.com/settings/tokens"
echo "2. Clique em 'Generate new token' → 'Generate new token (classic)'"
echo "3. Marque 'repo' (acesso completo ao repositório)"
echo "4. Clique em 'Generate token'"
echo "5. COPIE O TOKEN (você só verá uma vez!)"
echo ""

print_status "Depois execute um destes comandos:"
echo ""
echo "OPÇÃO 1 - Push com token na URL:"
echo "git push https://SEU_TOKEN@github.com/nilmarpublio/Doccollab.git main"
echo ""
echo "OPÇÃO 2 - Push normal (use token como senha):"
echo "git push origin main"
echo "   - Username: nilmarpublio"
echo "   - Password: [cole o token aqui]"
echo ""

print_status "Verificando remote atual..."
git remote -v

print_success "Configuração concluída!"
echo ""
print_status "📋 Próximos passos:"
echo "1. Crie um Personal Access Token no GitHub"
echo "2. Execute um dos comandos de push acima"
echo "3. Complete o deploy seguindo os guias anteriores"
echo ""
print_success "DocCollab está quase pronto para produção! 🚀"
