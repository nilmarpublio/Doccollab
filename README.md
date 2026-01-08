``mdc
DocCollab — Repositório

Estrutura principal e arquivos iniciais para desenvolvimento.

Para testar localmente:

`ash
node server/converter-sample.js
`
# DocCollab

Repositório do DocCollab — ferramenta para gerar documentos científicos a partir de AST.

Como testar localmente

- Instalar dependências:

```bash
npm install
```

- Iniciar servidor de desenvolvimento:

```bash
npm start
# abre a API em http://localhost:3000
```

Deploy com Docker (mínimo)

1. Construir a imagem:

```bash
docker build -t doccollab:latest .
```

2. Executar o container:

```bash
docker run -p 3000:3000 --rm --name doccollab doccollab:latest
```

Observações

- O servidor expõe a API em `/:` e endpoints em `/api/*`.
- Logs são gravados em `server/logs` e arquivos temporários em `server/tmp`.
- Para uso em produção considere criar um processo supervisor (systemd), orquestração (Docker Compose/Kubernetes) e uma imagem de compilação separada se precisar de TeX completo.
