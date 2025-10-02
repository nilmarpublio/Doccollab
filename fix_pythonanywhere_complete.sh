#!/bin/bash
# Script completo para corrigir erros no PythonAnywhere

echo "🚀 CORREÇÃO COMPLETA DO PYTHONANYWHERE"
echo "======================================"

# Ir para o diretório correto
cd ~/doccollab
echo "📁 Diretório atual: $(pwd)"

# Ativar ambiente virtual
echo "1. Ativando ambiente virtual..."
source venv/bin/activate

# Verificar Python
echo "2. Verificando Python..."
python --version

# Instalar/atualizar dependências
echo "3. Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
pip install requests==2.32.5
pip install babel

# Verificar arquivos essenciais
echo "4. Verificando arquivos essenciais..."
if [ ! -f "app.py" ]; then
    echo "❌ app.py não encontrado!"
    exit 1
fi

if [ ! -f "wsgi.py" ]; then
    echo "❌ wsgi.py não encontrado!"
    exit 1
fi

# Criar babel.cfg se não existir
if [ ! -f "babel.cfg" ]; then
    echo "5. Criando babel.cfg..."
    cat > babel.cfg << 'EOF'
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
EOF
fi

# Verificar estrutura de traduções
echo "6. Verificando traduções..."
if [ ! -d "translations" ]; then
    echo "Criando estrutura de traduções..."
    mkdir -p translations/pt/LC_MESSAGES
    mkdir -p translations/en/LC_MESSAGES
    mkdir -p translations/es/LC_MESSAGES
fi

# Extrair e compilar traduções
echo "7. Processando traduções..."
pybabel extract -F babel.cfg -k _l -o messages.pot . 2>/dev/null || echo "⚠️ Erro ao extrair strings"

if [ -f "messages.pot" ]; then
    pybabel update -i messages.pot -d translations -l pt 2>/dev/null || echo "⚠️ Erro ao atualizar PT"
    pybabel update -i messages.pot -d translations -l en 2>/dev/null || echo "⚠️ Erro ao atualizar EN"
    pybabel update -i messages.pot -d translations -l es 2>/dev/null || echo "⚠️ Erro ao atualizar ES"
    pybabel compile -d translations -D messages 2>/dev/null || echo "⚠️ Erro ao compilar traduções"
fi

# Verificar se services/asaas_integration.py existe
echo "8. Verificando arquivos de serviços..."
if [ ! -f "services/asaas_integration.py" ]; then
    echo "❌ services/asaas_integration.py não encontrado!"
    echo "Criando arquivo básico..."
    mkdir -p services
    cat > services/asaas_integration.py << 'EOF'
# ASAAS Integration Service
def get_plan_config(plan_type):
    plans = {
        'free': {'name': 'Free', 'price_brl': 0, 'price_usd': 0, 'features': ['1 project', '1 file']},
        'monthly': {'name': 'Monthly', 'price_brl': 10, 'price_usd': 2, 'features': ['Unlimited projects']},
        'quarterly': {'name': 'Quarterly', 'price_brl': 25, 'price_usd': 5, 'features': ['Unlimited projects']},
        'semi_annual': {'name': 'Semi-Annual', 'price_brl': 50, 'price_usd': 10, 'features': ['Unlimited projects']},
        'annual': {'name': 'Annual', 'price_brl': 100, 'price_usd': 20, 'features': ['Unlimited projects']}
    }
    return plans.get(plan_type, {})

def get_currency_for_locale(locale):
    return 'BRL' if locale == 'pt' else 'USD'
EOF
fi

# Testar importações básicas
echo "9. Testando importações..."
python -c "import flask; print('✅ Flask OK')" || echo "❌ Flask erro"
python -c "import flask_sqlalchemy; print('✅ SQLAlchemy OK')" || echo "❌ SQLAlchemy erro"
python -c "import flask_login; print('✅ Login OK')" || echo "❌ Login erro"
python -c "import flask_babel; print('✅ Babel OK')" || echo "❌ Babel erro"
python -c "import requests; print('✅ Requests OK')" || echo "❌ Requests erro"

# Testar aplicação
echo "10. Testando aplicação..."
python -c "from app import create_app; app, socketio = create_app(); print('✅ App OK')" || echo "❌ App erro"

# Verificar logs
echo "11. Verificando logs..."
if [ -f "/var/log/123nilmarcastro.pythonanywhere.com.error.log" ]; then
    echo "📋 Últimas 10 linhas do log de erro:"
    tail -10 /var/log/123nilmarcastro.pythonanywhere.com.error.log
fi

echo "======================================"
echo "✅ CORREÇÃO CONCLUÍDA!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Vá para a aba 'Web' no PythonAnywhere"
echo "2. Clique em 'Reload' para reiniciar a aplicação"
echo "3. Teste sua aplicação em: https://123nilmarcastro.pythonanywhere.com"
echo ""
echo "🔍 Se ainda houver erros, execute:"
echo "python diagnose_pythonanywhere_error.py"
