@echo off
echo 🚀 Iniciando deploy do DocCollab...

REM Ativar ambiente virtual (se existir)
if exist "venv\Scripts\activate.bat" (
    echo 📦 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Executar scripts de atualização do banco
echo 🗄️ Atualizando banco de dados...
python update_db_versions.py
python update_db_chat.py

REM Criar diretórios necessários
echo 📁 Criando diretórios...
if not exist "projects" mkdir projects
if not exist "trash" mkdir trash
if not exist "versions" mkdir versions
if not exist "logs" mkdir logs
if not exist "static\uploads" mkdir static\uploads

REM Executar script de correção
echo 🔧 Aplicando correções...
python fix_deploy_issues.py

echo ✅ Deploy concluído!
echo 🌐 Acesse sua aplicação no navegador
pause

