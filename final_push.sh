#!/bin/bash

# 🚀 Script de Push Final - DocCollab
# Deploy Final no PythonAnywhere

echo "🚀 Executando push final do DocCollab..."

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

print_status "Tentando fazer push para main..."

# Tentar fazer push para main
if git push origin main; then
    print_success "Push para main realizado com sucesso!"
elif git push -u origin main; then
    print_success "Push para main com upstream configurado!"
else
    print_warning "Falha no push para main. Tentando resolver problemas..."
    
    # Verificar se há arquivos .gitignore problemáticos
    print_status "Verificando arquivos problemáticos..."
    
    if [ -f "translations/pt/.gitignore" ]; then
        print_warning "Removendo arquivo .gitignore problemático em translations/pt/"
        rm -f translations/pt/.gitignore
    fi
    
    if [ -f "translations/en/.gitignore" ]; then
        print_warning "Removendo arquivo .gitignore problemático em translations/en/"
        rm -f translations/en/.gitignore
    fi
    
    if [ -f "translations/es/.gitignore" ]; then
        print_warning "Removendo arquivo .gitignore problemático em translations/es/"
        rm -f translations/es/.gitignore
    fi
    
    # Tentar push novamente
    print_status "Tentando push novamente..."
    if git push origin main; then
        print_success "Push realizado com sucesso após limpeza!"
    else
        print_error "Falha no push. Verifique a conexão e tente novamente."
        exit 1
    fi
fi

print_status "Verificando status final..."
git status

print_success "🎉 Push final concluído com sucesso!"
echo ""
print_status "📋 Próximos passos para completar o deploy:"
echo "1. Ative o ambiente virtual: source venv/bin/activate"
echo "2. Instale dependências: pip3.10 install --user -r requirements.txt"
echo "3. Atualize o banco: python3.10 update_db_versions.py"
echo "4. Atualize o banco: python3.10 update_db_chat.py"
echo "5. Configure o .env: cp env_pythonanywhere_production.txt .env"
echo "6. Configure o WSGI no PythonAnywhere"
echo "7. Configure os Static Files no PythonAnywhere"
echo "8. Reinicie a aplicação no PythonAnywhere"
echo ""
print_success "DocCollab está pronto para produção! 🚀"
