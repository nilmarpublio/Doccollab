# Deploy sem Docker — DocCollab (PM2 + Proxy TLS)

Este guia descreve o processo recomendado para rodar o `DocCollab` em um host Windows sem Docker, usando `pm2` para gestão do processo e `Caddy` como proxy reverso (TLS automático). Inclui instruções para habilitar compilação LaTeX local (MiKTeX/TeX Live).

**Resumo da escolha (melhor opção):**
- `pm2` mantém o processo Node em produção com auto-restart e startup system-wide.
- `Caddy` simplifica HTTPS automático por domínio sem configuração complexa de TLS.
- Instalar MiKTeX/TeX Live no host para que a aplicação invoque `pdflatex` localmente (ou usar WSL2 com TeX Live).

## 1 — Pré-requisitos
- Windows 10/11 ou servidor Windows com privilégios admin.
- Node.js 18+ (já instalado no repositório atual foi usado).
- Acesso ao domínio (DNS) para uso do TLS via Caddy (opcional, necessário para HTTPS).

## 2 — Instalar dependências e preparar diretórios
Abra PowerShell como Administrador e execute no diretório do projeto:

```powershell
Set-Location D:\DocCollab-V0
npm ci --only=production
# criar diretórios de logs e tmp
New-Item -ItemType Directory -Path server\logs -Force
New-Item -ItemType Directory -Path server\tmp -Force
```

## 3 — Teste rápido (foreground)

```powershell
$env:NODE_ENV='production'
npm start
# testar health
Invoke-RestMethod http://localhost:3000/api/health
```

Se retornar versão/ok, o servidor está saudável.

## 4 — Instalar e configurar PM2 (produção)

```powershell
npm install -g pm2
# iniciar via npm script (usa command `npm start` definido em package.json)
pm2 start npm --name doccollab -- start
# observar logs
pm2 logs doccollab
# salvar e registrar startup
pm2 save
pm2 startup
# executar como admin o comando emitido por `pm2 startup` (irá registrar o serviço)
```

Notas:
- `pm2 save` grava a lista de processos para restore no boot.
- Use `pm2 monit` para monitoramento local.

## 5 — Instalar TeX (para geração de PDFs)
Opções Windows:
- MiKTeX (rápido install): https://miktex.org/download
- TeX Live (completo): https://www.tug.org/texlive/

Após instalação, verifique:

```powershell
pdflatex --version
```

Se o comando não for encontrado, adicione o diretório `bin` do TeX à `PATH` ou instale dentro do WSL2 e ajuste a chamada no worker.

## 6 — Proxy reverso e TLS com Caddy (recomendado)
Baixe Caddy (https://caddyserver.com/download) e crie `Caddyfile` em `C:\Caddy\Caddyfile` com exemplo:

```
example.com {
    reverse_proxy localhost:3000
}
```

Execute Caddy (Windows):

```powershell
# executar como serviço (opção recomendada) ou em foreground
caddy run --config C:\Caddy\Caddyfile
```

Caddy pedirá certificados via Let's Encrypt automaticamente. Se estiver em ambiente sem domínio, mantenha `localhost` sem TLS para testes.

## 7 — Firewall e portas
- Abra porta `3000` para conexões locais ou restrinja ao proxy.
- Se usar Caddy em porta 443/80, abra essas portas no firewall.

## 8 — Logs, rotacionamento e monitoramento
- `pm2` guarda logs em `%USERPROFILE%\.pm2\logs` mas o serviço do app também escreve em `server/logs`.
- Configure rotacionamento (ex.: logrotate no WSL, ou ferramenta Windows) para evitar disco cheio.

## 9 — Backup e persistência de arquivos temporários
- Mantenha `server/logs` e `server/tmp` em disco persistente (ou NFS/SMB) dependendo do ambiente.

## 10 — Comandos úteis
```powershell
# ver status pm2
pm2 list
pm2 logs doccollab
pm2 restart doccollab
pm2 stop doccollab
pm2 delete doccollab
# verificar health
Invoke-RestMethod http://localhost:3000/api/health
```

## 11 — Se preferir rodar a compilação LaTeX em um worker separado
- Instale TeX em uma máquina/VM separada ou WSL2 com TeX Live e exponha um endpoint/fila que a API envie jobs (mais seguro/isolado).

## 12 — Troubleshooting rápido
- `npm start` em foreground para ver erros diretos.
- Verifique `server/logs` e `%USERPROFILE%\.pm2\logs`.
- Se `pdflatex` falhar, execute manualmente o job em shell para inspecionar saída.

---
Guia criado automaticamente pelo assistente. Se quiser, eu:
- configuro `pm2` aqui (criar processo e registrar startup), ou
- gero um `service` do Windows via `nssm` em vez de `pm2 startup`, ou
- crio arquivo de exemplo `Caddyfile` adaptado ao seu domínio.
