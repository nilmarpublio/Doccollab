# Script para preparar o deploy na Hostinger
# Execute este script no PowerShell

Write-Host "🚀 Preparando DocCollab para deploy na Hostinger..." -ForegroundColor Green

# Verificar se estamos na pasta correta
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Execute este script dentro da pasta DocCollab!" -ForegroundColor Red
    exit 1
}

# Criar pasta temporária
$tempDir = "deploy_temp"
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "📁 Copiando arquivos necessários..." -ForegroundColor Yellow

# Copiar arquivos essenciais
$filesToCopy = @(
    "app.py",
    "wsgi.py", 
    "requirements.txt",
    ".htaccess",
    "setup_db.py",
    "env.production.example",
    "babel.cfg",
    "COMO_FAZER_DEPLOY.md",
    "DEPLOY_HOSTINGER.md"
)

foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file -Destination $tempDir
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $file não encontrado" -ForegroundColor Yellow
    }
}

# Copiar pastas
$foldersToCopy = @(
    "models",
    "routes", 
    "services",
    "utils",
    "templates",
    "static",
    "translations"
)

foreach ($folder in $foldersToCopy) {
    if (Test-Path $folder) {
        Copy-Item $folder -Destination $tempDir -Recurse
        Write-Host "  ✅ $folder/" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $folder/ não encontrada" -ForegroundColor Yellow
    }
}

# Criar arquivo .env básico
$envContent = @"
# Configurações para produção na Hostinger
SECRET_KEY=CHANGE_THIS_SECRET_KEY_TO_SOMETHING_VERY_SECURE
DATABASE_URL=sqlite:///doccollab.db
PDFLATEX=/usr/bin/pdflatex
SEED_EMAIL=admin@seudominio.com
SEED_PASSWORD=admin123
"@

$envFile = Join-Path $tempDir ".env"
$envContent | Out-File -FilePath $envFile -Encoding UTF8
Write-Host "  ✅ .env criado" -ForegroundColor Green

# Criar ZIP
$zipName = "doccollab-deploy-$(Get-Date -Format 'yyyyMMdd-HHmm').zip"
Write-Host "📦 Criando arquivo ZIP..." -ForegroundColor Yellow

Compress-Archive -Path "$tempDir\*" -DestinationPath $zipName -Force

# Limpar pasta temporária
Remove-Item $tempDir -Recurse -Force

Write-Host ""
Write-Host "🎉 Deploy preparado com sucesso!" -ForegroundColor Green
Write-Host "📁 Arquivo criado: $zipName" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Faça upload do arquivo '$zipName' para a Hostinger" -ForegroundColor White
Write-Host "2. Extraia o arquivo na pasta public_html" -ForegroundColor White
Write-Host "3. Siga o guia em COMO_FAZER_DEPLOY.md" -ForegroundColor White
Write-Host ""
Write-Host "💡 Dica: O arquivo está pronto para upload!" -ForegroundColor Magenta
