# Roteiro de Preparação e Deploy — DocCollab

Este roteiro descreve passos mínimos para preparar o repositório e realizar o deploy em um ambiente com Docker. Inclui recomendações para produção e debugging.

1) Pré-requisitos
- Docker 20+ e Docker Compose (opcional)
- Node.js 18+ (para desenvolvimento local)
- (Opcional) TeX Live em imagem separada se for necessário compilar localmente PDFs com `pdflatex`.

2) Preparar ambiente local
- Instalar dependências:

```bash
npm install
```

- Testar servidor localmente:

```bash
npm start
# verificar: curl http://localhost:3000/api/health
```

3) Imagem Docker mínima (já incluída neste repo)
- Construir imagem:

```bash
docker build -t doccollab:latest .
```

- Executar container:

```bash
docker run -p 3000:3000 --rm --name doccollab doccollab:latest
```

4) Persistência e arquivos temporários
- O servidor grava `server/logs` e `server/tmp` localmente; em produção monte volumes Docker ou use storage externo (S3/MinIO) para persistência.

5) Compilação de LaTeX em produção
- Recomendo usar um worker/container separado contendo TeX Live completo para evitar aumentar a imagem da API.
- Exemplo rápido (Dockerfile do worker): use `texlive/texlive` ou crie imagem baseada em Debian com `texlive-full` apenas para o worker.

6) Docker Compose (exemplo)

```yaml
version: '3.8'
services:
  api:
    image: doccollab:latest
    ports:
      - "3000:3000"
    volumes:
      - ./server/logs:/usr/src/app/server/logs
      - ./server/tmp:/usr/src/app/server/tmp
    environment:
      - NODE_ENV=production
  worker:
    image: my-tex-worker:latest
    # worker que roda compilador LaTeX
```

7) Variáveis de ambiente úteis
- `PORT` — porta do servidor (default 3000)
- `NODE_ENV` — `production` para otimizações
- Para produção, configure `LOG_LEVEL`, `STORAGE_ENDPOINT`, `STORAGE_KEY` conforme seu backend.

8) Segurança e hardening
- Execute a imagem com um usuário não-root (o `Dockerfile` já usa `USER node`).
- Proteja endpoints sensíveis com TLS; coloque o container atrás de um proxy reverso (Nginx/Traefik) para TLS e rate-limiting.

9) Monitoramento e logs
- Remeta logs para um coletor (ex.: Filebeat, Prometheus + Grafana) em produção.
- Verifique `server/logs/client.log` e logs de compilação para diagnósticos.

10) Passos para release
- Bump da versão em `package.json`.
- Executar testes locais (se existirem).
- Construir imagem, rodar smoke tests (curl `/api/health`).
- Publicar imagem em registry (Docker Hub, GHCR) e atualizar orquestração.

11) Troubleshooting rápido
- `node server/index.cjs` em foreground para ver erros imediatos.
- Ver `server/logs` para logs persistidos.
- Se PDFs falharem, execute o processo de compilação dentro do worker manualmente para inspecionar saída do pdflatex.

Se quiser, eu posso: gerar um `docker-compose.yml` completo adaptado ao seu ambiente, criar um `Dockerfile` para o worker TeX, ou testar a construção da imagem aqui (requer Docker instalado no host). O que prefere agora?
