# Script PowerShell para atualizar os templates no servidor DigitalOcean
# Execute este script no Windows para enviar os arquivos para o servidor

Write-Host "🚀 Atualizando templates do DocCollab no servidor..." -ForegroundColor Green

# Configurações do servidor
$serverIP = "64.23.136.220"
$serverUser = "root"
$serverPath = "/home/doccollab/Doccollab"

Write-Host "📡 Conectando ao servidor $serverIP..." -ForegroundColor Yellow

# Comando para atualizar o dashboard
$dashboardCommand = @"
# Parar o serviço
supervisorctl stop doccollab

# Fazer backup
cp -r $serverPath/templates $serverPath/templates_backup_$(date +%Y%m%d_%H%M%S)

# Atualizar dashboard.html
cat > $serverPath/templates/dashboard.html << 'DASHBOARD_EOF'
$(Get-Content "templates/dashboard.html" -Raw)
DASHBOARD_EOF

# Ajustar permissões
chown -R doccollab:doccollab $serverPath/templates
chmod -R 644 $serverPath/templates

# Reiniciar serviço
supervisorctl start doccollab

# Verificar status
sleep 3
supervisorctl status doccollab

echo "✅ Dashboard atualizado com sucesso!"
"@

Write-Host "📝 Enviando comando para atualizar dashboard..." -ForegroundColor Yellow

# Executar comando via SSH
$dashboardCommand | ssh $serverUser@$serverIP

Write-Host "✅ Atualização concluída!" -ForegroundColor Green
Write-Host "🌐 Acesse: http://$serverIP" -ForegroundColor Cyan
