#!/bin/bash

# 🔧 Script de Correção Rápida - Problema de Branch
# DocCollab - Deploy Final

echo "🔧 Resolvendo problema de branch..."

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

print_status "Verificando branch atual..."
git branch

print_status "Verificando status do Git..."
git status

print_status "Verificando remote..."
git remote -v

print_status "Tentando fazer push para main..."
if git push origin main; then
    print_success "Push para main realizado com sucesso!"
elif git push -u origin main; then
    print_success "Push para main com upstream configurado!"
else
    print_warning "Falha no push para main. Tentando criar branch master..."
    
    # Tentar criar branch master
    if git checkout -b master; then
        print_success "Branch master criado com sucesso!"
        
        if git push origin master; then
            print_success "Push para master realizado com sucesso!"
        else
            print_error "Falha no push para master"
            exit 1
        fi
    else
        print_error "Falha ao criar branch master"
        exit 1
    fi
fi

print_status "Verificando status final..."
git status
git branch

print_success "🎉 Problema de branch resolvido!"
echo ""
print_status "📋 Próximos passos:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Instale dependências: pip3.10 install --user -r requirements.txt"
echo "3. Atualize o banco: python3.10 update_db_versions.py"
echo "4. Atualize o banco: python3.10 update_db_chat.py"
echo "5. Configure o .env: cp env_pythonanywhere_production.txt .env"
echo "6. Configure o WSGI no PythonAnywhere"
echo "7. Reinicie a aplicação"
echo ""
print_success "DocCollab está pronto para produção! 🚀"
