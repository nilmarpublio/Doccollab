# Deploy (Rápido)

Este documento descreve os passos mínimos para preparar a máquina host e fazer o deploy do projeto usando Docker Compose.

1) Pré-requisitos no host (Windows)
  - Habilitar virtualização no BIOS/UEFI (Intel VT-x ou AMD-V).
  - Executar o script `scripts/enable-wsl2-windows.ps1` como Administrador para ativar WSL2 e Virtual Machine Platform.
  - Reiniciar o sistema se solicitado.
  - Instalar/abrir Docker Desktop e aguardar até o ícone ficar verde.

2) Build e execução dos containers
```powershell
Set-Location D:\DocCollab-V0
docker-compose build --no-cache
docker-compose up -d
docker-compose ps
Invoke-RestMethod http://localhost:3000/api/health
```

3) Permissões de volumes (caso necessário)
```powershell
icacls .\server\logs /grant "Users:(OI)(CI)F" /T
icacls .\server\tmp /grant "Users:(OI)(CI)F" /T
```

4) Notas operacionais
  - `docker/tex-worker/Dockerfile` instala `texlive` e `poppler-utils` para compilação LaTeX.
  - `docker-compose.yml` contém healthchecks para `api` e `worker`.
  - Em produção, configure proxy reverso (nginx/Caddy) com TLS e monitore os containers.

Se preferir, execute `scripts/enable-wsl2-windows.ps1` e depois me avise que o Docker Desktop está ativo; eu procedo para construir as imagens e subir os serviços daqui.
