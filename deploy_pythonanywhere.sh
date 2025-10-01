#!/bin/bash

# 🚀 Script de Deploy Automatizado para PythonAnywhere
# DocCollab - Versão Final

echo "🚀 Iniciando deploy do DocCollab no PythonAnywhere..."

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

print_status "Atualizando código do GitHub..."
git pull origin master
if [ $? -eq 0 ]; then
    print_success "Código atualizado com sucesso"
else
    print_error "Falha ao atualizar código"
    exit 1
fi

print_status "Ativando ambiente virtual..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    print_success "Ambiente virtual ativado"
else
    print_error "Falha ao ativar ambiente virtual"
    exit 1
fi

print_status "Instalando/Atualizando dependências..."
pip3.10 install --user -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dependências instaladas com sucesso"
else
    print_error "Falha ao instalar dependências"
    exit 1
fi

print_status "Atualizando banco de dados - Versões..."
python3.10 update_db_versions.py
if [ $? -eq 0 ]; then
    print_success "Tabela de versões criada/atualizada"
else
    print_warning "Aviso: Falha ao atualizar tabela de versões (pode já existir)"
fi

print_status "Atualizando banco de dados - Chat..."
python3.10 update_db_chat.py
if [ $? -eq 0 ]; then
    print_success "Tabela de chat criada/atualizada"
else
    print_warning "Aviso: Falha ao atualizar tabela de chat (pode já existir)"
fi

print_status "Verificando instalação do LaTeX..."
which pdflatex
if [ $? -eq 0 ]; then
    print_success "LaTeX encontrado: $(which pdflatex)"
else
    print_warning "LaTeX não encontrado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y texlive-full
    if [ $? -eq 0 ]; then
        print_success "LaTeX instalado com sucesso"
    else
        print_error "Falha ao instalar LaTeX"
    fi
fi

print_status "Verificando arquivo .env..."
if [ -f ".env" ]; then
    print_success "Arquivo .env encontrado"
else
    print_warning "Arquivo .env não encontrado. Criando..."
    cp env.example .env
    print_warning "IMPORTANTE: Configure as variáveis no arquivo .env"
fi

print_status "Verificando estrutura do projeto..."
if [ -d "templates" ] && [ -d "static" ] && [ -d "models" ]; then
    print_success "Estrutura do projeto OK"
else
    print_error "Estrutura do projeto incompleta"
    exit 1
fi

print_success "🎉 Deploy preparado com sucesso!"
echo ""
echo "📋 Próximos passos manuais:"
echo "1. Acesse o PythonAnywhere Dashboard"
echo "2. Vá para Web → WSGI configuration file"
echo "3. Substitua o conteúdo pelo código fornecido em DEPLOY_PYTHONANYWHERE_FINAL.md"
echo "4. Configure as variáveis de ambiente no arquivo .env"
echo "5. Clique em 'Reload' para reiniciar a aplicação"
echo "6. Acesse: https://123nilmarcastro.pythonanywhere.com"
echo ""
echo "🔧 Configurações importantes:"
echo "- WSGI: Use o código fornecido no guia"
echo "- Static files: Adicione /socket.io/ → /home/123nilmarcastro/DocCollab/static"
echo "- Working directory: /home/123nilmarcastro/DocCollab"
echo ""
print_success "DocCollab está pronto para produção! 🚀"
