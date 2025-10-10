#!/bin/bash

# Script para atualizar a aplicação DocCollab na DigitalOcean
# Execute este script após fazer commit das mudanças no GitHub

echo "🚀 Iniciando atualização do DocCollab na DigitalOcean..."

# 1. Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script no diretório DocCollab"
    exit 1
fi

# 2. Fazer commit das mudanças locais
echo "📝 Fazendo commit das mudanças locais..."
git add .
git commit -m "Fix: Corrigir funções de tradução e redirecionamento após login

- Removidas todas as funções de tradução _() dos templates
- Corrigido redirecionamento após login para dashboard
- Corrigidos erros de BuildError para rotas inexistentes
- Aplicação funcionando corretamente localmente"

# 3. Fazer push para o GitHub
echo "📤 Enviando mudanças para o GitHub..."
git push origin main

# 4. Instruções para DigitalOcean
echo ""
echo "✅ Mudanças enviadas para o GitHub com sucesso!"
echo ""
echo "📋 Próximos passos na DigitalOcean:"
echo "1. Acesse seu droplet na DigitalOcean"
echo "2. Navegue até o diretório da aplicação:"
echo "   cd /var/www/doccollab"
echo ""
echo "3. Faça backup da versão atual:"
echo "   sudo cp -r . ../doccollab_backup_\$(date +%Y%m%d_%H%M%S)"
echo ""
echo "4. Atualize o código do GitHub:"
echo "   git pull origin main"
echo ""
echo "5. Instale dependências se necessário:"
echo "   pip3 install -r requirements.txt"
echo ""
echo "6. Reinicie o serviço:"
echo "   sudo systemctl restart doccollab"
echo "   sudo systemctl status doccollab"
echo ""
echo "7. Verifique os logs se houver problemas:"
echo "   sudo journalctl -u doccollab -f"
echo ""
echo "🎉 Atualização concluída!"


