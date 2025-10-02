#!/bin/bash
# Script rápido para corrigir traduções no PythonAnywhere

echo "🚀 CORRIGINDO TRADUÇÕES NO PYTHONANYWHERE"
echo "=========================================="

# Ir para o diretório correto
cd ~/doccollab

# Ativar ambiente virtual
echo "1. Ativando ambiente virtual..."
source venv/bin/activate

# Instalar babel se necessário
echo "2. Verificando babel..."
pip install babel

# Verificar estrutura
echo "3. Verificando estrutura de traduções..."
ls -la translations/
find translations/ -name "*.po"

# Criar babel.cfg se não existir
if [ ! -f babel.cfg ]; then
    echo "4. Criando babel.cfg..."
    cat > babel.cfg << 'EOF'
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
EOF
fi

# Extrair strings
echo "5. Extraindo strings..."
pybabel extract -F babel.cfg -k _l -o messages.pot .

# Atualizar arquivos .po
echo "6. Atualizando arquivos .po..."
pybabel update -i messages.pot -d translations -l pt
pybabel update -i messages.pot -d translations -l en
pybabel update -i messages.pot -d translations -l es

# Compilar traduções
echo "7. Compilando traduções..."
pybabel compile -d translations -D messages

# Testar aplicação
echo "8. Testando aplicação..."
python -c "from app import create_app; app, socketio = create_app(); print('✅ App OK')"

echo "=========================================="
echo "✅ CORREÇÃO CONCLUÍDA!"
echo "Agora reinicie sua aplicação web no PythonAnywhere"
