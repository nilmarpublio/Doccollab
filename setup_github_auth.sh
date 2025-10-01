#!/bin/bash

# 🔐 Script de Configuração de Autenticação GitHub
# DocCollab - Deploy Final

echo "🔐 Configurando autenticação GitHub..."

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

print_status "Configurando credenciais Git..."

# Configurar credenciais básicas
git config --global user.name "nilmarpubblio"
git config --global user.email "nilmarpubblio@github.com"

# Configurar helper de credenciais
git config --global credential.helper store

print_success "Credenciais configuradas!"

print_status "Verificando configuração..."
git config --list | grep -E "(user|credential)"

print_warning "IMPORTANTE: Para fazer push, você precisa:"
echo ""
echo "1. Criar um Personal Access Token no GitHub:"
echo "   - Acesse: https://github.com/settings/tokens"
echo "   - Clique em 'Generate new token' → 'Generate new token (classic)'"
echo "   - Marque 'repo' (acesso completo ao repositório)"
echo "   - Clique em 'Generate token'"
echo "   - COPIE O TOKEN (você só verá uma vez!)"
echo ""
echo "2. Fazer push com o token:"
echo "   git push origin main"
echo "   - Username: nilmarpubblio"
echo "   - Password: [cole o token aqui]"
echo ""

print_status "Alternativa: Usar SSH"
echo ""
echo "Se preferir usar SSH:"
echo "1. Gere uma chave SSH: ssh-keygen -t ed25519 -C 'seu@email.com'"
echo "2. Adicione a chave ao GitHub: https://github.com/settings/ssh/new"
echo "3. Altere a URL: git remote set-url origin git@github.com:nilmarpublio/Doccollab.git"
echo "4. Faça push: git push origin main"
echo ""

print_status "Verificando remote atual..."
git remote -v

print_success "Configuração concluída!"
echo ""
print_status "📋 Próximos passos:"
echo "1. Crie um Personal Access Token no GitHub"
echo "2. Execute: git push origin main"
echo "3. Use o token como senha quando solicitado"
echo "4. Complete o deploy seguindo os guias anteriores"
echo ""
print_success "DocCollab está quase pronto para produção! 🚀"
