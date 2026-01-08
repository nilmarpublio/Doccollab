6. PROMPT FINAL PARA O GITHUB COPILOT (TRECHO CRÍTICO)

Você deve usar este trecho literalmente exatamente como abaixo:

“Implemente um editor de documentos baseado exclusivamente em blocos semânticos estruturados.
O usuário nunca deve ver ou editar LaTeX.
Toda edição gera um AST JSON rigorosamente validado, que é a única fonte de verdade do sistema.
A geração de LaTeX e PDF deve ser totalmente automática, determinística e isolada do editor.”

# DocCollab‑v0 — Arquitetura e Design (Visão Técnica)

## 1. Objetivo

Documento de arquitetura para o DocCollab‑v0: plataforma para geração de documentos técnicos, científicos e de engenharia. O sistema deve manter compatibilidade com LaTeX, mas oferecer um editor intermediário que abstraia LaTeX do usuário e gere saída LaTeX auditável e compilável automaticamente.

## MODELO CONCEITUAL DEFINITIVO

O DocCollab‑v0 é um sistema de produção documental baseado em blocos semânticos com as seguintes garantias fundamentais:

- O usuário não escreve texto livre sem estrutura: todo conteúdo é composto por blocos semanticamente tipados (ex.: `title`, `section`, `equation`, `figure`).
- Cada bloco define:
  - `type`: tipo do bloco
  - `rules`: regras estruturais e metadados obrigatórios
  - `validation`: regras de validação aplicadas em tempo real e pré‑exportação
  - `translation`: mapeamento determinístico para LaTeX
- Tradução determinística: a conversão AST → LaTeX é previsível e reprodutível; o mesmo AST gera sempre o mesmo `.tex` (dado o mesmo template/versão).

Invariante de projeto

👉 Não existe “documento inválido” por construção — o editor impõe regras e validações que previnem estados inválidos. Erros críticos são detectados e bloqueiam exportação até correção.

Implicações práticas

## FASE 0 — PRINCÍPIO ABSOLUTO (NÃO NEGOCIÁVEL)

O AST JSON é a única fonte de verdade do sistema. Nada deve ser salvo, validado, transformado, exportado ou compilado fora do AST.

- Todas as operações do editor alteram a AST em memória; persistência é serialização da AST.
- Validações ocorrem sobre a AST; apenas AST validada segue para conversão e compilação.
- Metadados, estados de UI e caches são derivados ou sincronizados a partir da AST, nunca substituem-na.
- Artefatos gerados (`.tex`, `.pdf`, `.log`) incluem metadados que apontam de volta ao(s) ID(s) de bloco no AST para rastreabilidade.

Esse princípio reduz ambiguidade entre camadas, garante reprodutibilidade e facilita auditoria, versionamento e correção automática de erros.

## Pipeline Final (Sem Surpresas)

Fluxo mínimo e determinístico para geração de documento final:

- Blocos (Editor)
  ↓
- AST JSON (validado)
  ↓
- Gerador LaTeX (oculto)
  ↓
- Engine LaTeX Empacotada
  ↓
- PDF Final

Princípios e garantias:

- Nenhuma etapa “mágica”: cada transformação é explícita e auditável.
- Determinismo: mesmas entradas (AST + template + assets) produzem o mesmo `.tex` e o mesmo PDF.
- Mapeamento de erros: todo erro de compilação ou transformação é correlacionado ao bloco/ID de origem no AST, com mensagens amigáveis ao usuário.

Requisitos operacionais:

- O gerador LaTeX consome apenas AST validado; validações bloqueiam export quando regras críticas falham.
- O worker de compilação roda dentro de container isolado (imagem LaTeX empacotada), com limites de CPU, memória e tempo de execução.
- Artefatos gerados (`.tex`, `.log`, `.pdf`) são armazenados junto com metadados que incluem mapeamento de blocos → posições no `.tex` para facilitar diagnóstico.

Consequências para o design:

- O conversor (AST → LaTeX) deve produzir comentários/labels no `.tex` que apontem para IDs de bloco para facilitar rastreabilidade.
- Logs e erros do `pdflatex`/`xelatex` serão parseados e traduzidos para mensagens de editor, apontando blocos problemáticos.
- A UI do editor exibe erros e pontos sugeridos de correção vinculados ao bloco correspondente.

Essa seção garante que o produto entregue terá um pipeline repetível, auditável e com erros sempre atribuíveis à origem no editor — sem surpresas para o usuário final.

- Validações em tempo real reduzem a necessidade de depuração pós‑compilação.
- A AST serializável permite diffing, versionamento e reprodutibilidade de builds.
- Usuários avançados podem inspecionar e editar o `.tex` gerado, mas o fluxo principal permanece focado na edição semântica.

## 2. Princípios Fundamentais

1. Produtividade acima de tudo

- O usuário não precisa “pensar em LaTeX”.
- O sistema deve guiar a estrutura correta do documento por meio de sugestões, validações e snippets contextuais.

2. Separação total entre camadas

- Entrada do usuário: editor otimizado e orientado a blocos.
- Representação intermediária: AST/JSON estruturado (formato auditável e versionável).
- Saída LaTeX: gerada automaticamente pelo conversor, clara e auditável.
- PDF final: artefato compilado em ambiente isolado e reprodutível.

3. Infraestrutura como produto

- O DocCollab é um motor de documentos (document engine), não apenas um editor de texto.
- Priorizar APIs, automação, reprodutibilidade, cache e integração CI/CD desde o início.

4. 100% Web Technologies

- Frontend em HTML, CSS e JavaScript puro.
- Evitar frameworks JS pesados (React, Angular, Vue) para manter simplicidade, portabilidade e baixo acoplamento.

Esses princípios guiam todas as decisões de arquitetura, priorizando produtividade, previsibilidade e segurança sobre escolhas estéticas ou dependências pesadas.

## 3. Público‑Alvo

- Engenharia
- Ciências Exatas
- Ciências Aplicadas
- Estudantes universitários
- Pesquisadores
- Autores técnicos

## 4. Plataformas Suportadas

1. Prioridade

- Windows (Web App / PWA)
- Android (WebView / PWA)

2. Secundário (se não impactar o desenvolvimento)

- iOS

Observações:

- O alvo primário são plataformas que suportem PWA e navegadores modernos; garantir que a experiência funcione offline/limitada como PWA em Windows e Android.
- iOS é secundário devido às limitações do Safari/WebView; suportá‑lo apenas se não reduzir produtividade ou aumentar complexidade no frontend.

## 5. Internacionalização (i18n)

Idiomas obrigatórios desde o início:

- pt-BR
- en-US
- es-ES

Arquitetura i18n:

- Todos os textos ficam em arquivos JSON de idioma (`i18n/pt-BR.json`, `i18n/en-US.json`, `i18n/es-ES.json`).
- Nenhuma string hardcoded no frontend ou backend — todas as interfaces consomem chaves de i18n.
- O build/deploy inclui verificação de cobertura de string (script que valida chaves ausentes entre idiomas).
- Formato sugerido de arquivo de idioma (exemplo `en-US.json`):

  {
  "nav": { "compile": "Compile", "status": "Status" },
  "editor": { "placeholder": "Type here...", "addSection": "Add section" },
  "errors": { "compileFailed": "Compilation failed" }
  }

- Suporte a pluralização e placeholders via convenção simples (ex.: "items": "{count} items").
- Backend/API: mensagens e logs voltados ao usuário são retornados com chaves de i18n; texts enviados ao cliente são renderizados no idioma do usuário.

Observação de implementação:

- Para o MVP, implementar loader i18n simples em JS puro que carrega JSONs por demanda e expõe `t(key, params)`.
- Scripts de QA para garantir que novos textos adicionados ao código sejam refletidos nos arquivos de idioma.

## 6. Modelo de Monetização

- Sem assinatura
- Sem paywall
- Monetização exclusivamente via anúncios não intrusivos

Políticas e restrições dos anúncios:

- Anúncios nunca devem interromper a edição do usuário (sem modals, popups ou overlays que bloqueiem a área de edição).
- Anúncios não podem afetar o processo de compilação (nenhuma dependência de rede ou script terceiro durante a geração de `.tex` ou chamada da API de compilação).
- Anúncios não podem afetar a exportação de artefatos (PDF/.tex) — exportação deve ser determinística e independente de anúncios.

Implementação sugerida:

- Exibir anúncios somente em áreas periféricas da interface (sidebars, rodapé) isoladas do editor.
- Carregar anúncios de forma assíncrona e segura; scripts de anúncios rodando estritamente em iframe sandboxed para evitar acesso ao DOM do editor.
- Garantir que o pipeline de build (frontend → API → worker) nunca dependa de provedores de anúncios ou de rede de anúncios.
- Fornecer um modo de testes/CI com anúncios desabilitados para garantir reprodutibilidade.

Observação legal e privacidade:

- Implementar políticas claras de privacidade e consentimento; respeitar GDPR/CPRA quando aplicável.
- Não usar anúncios que coletem dados sensíveis do conteúdo do documento.

## 7. Arquitetura Geral do Sistema

Camadas

1. UI Layer

- Landing Page
- Dashboard
- Editor
- Preview

2. Document Engine

- Parser do editor otimizado
- Gerador de AST
- Conversor AST → LaTeX

3. Compilation Engine

- LaTeX → PDF
- Tratamento de erros sem expor LaTeX cru ao usuário

4. Storage

- LocalStorage / IndexedDB (primeira fase)
- Estrutura preparada para cloud no futuro

## 8. Landing Page — Etapas e Conteúdo

Objetivo

- Explicar o método, não apenas o produto.

Seções obrigatórias

1. Proposta de Valor


    - “Crie documentos técnicos com rigor científico sem lutar contra LaTeX”

2. Problema


    - Overleaf é poderoso, mas improdutivo para iniciantes e lento para especialistas

3. Solução


    - Editor estruturado + compilação automática

4. Fluxo do Sistema


    - Escrever → Estruturar → Compilar → PDF

5. Call to Action


    - “Criar Documento”

Requisitos de implementação

- A Landing Page deve ser estática, rápida e sem animações pesadas.
- HTML estático otimizado (pré-carregamento mínimo, CSS leve, assets comprimidos).
- Incluir exemplos visuais minimalistas do fluxo (imagens estáticas ou SVG), evitando heavy JS.

## 9. Dashboard do Usuário

Funções

- Criar novo documento
- Listar documentos existentes
- Abrir / Renomear / Excluir
- Selecionar idioma padrão
- Selecionar tipo de documento

Tipos de Documento

- Artigo científico
- Relatório técnico
- TCC / Dissertação
- Manual de engenharia
- Documento genérico

Observações de implementação:

- O dashboard deve ser eficiente: lista paginada/virtualizada para grandes quantidades de documentos.
- Operações mutáveis (renomear/excluir) devem pedir confirmação e suportar undo simples.
- Preferir chamadas assíncronas à API para operações e cache local (IndexedDB) para performance offline limitada.

## 10. Editor Otimizado (Núcleo do Produto)

Conceito

- O editor não é LaTeX.
- Ele é um editor semântico estruturado (editor orientado a blocos e significado).

Funcionalidades

- Blocos estruturais:
  - Título
  - Autor
  - Resumo
  - Seção
  - Sub-seção
  - Equação
  - Figura
  - Tabela
  - Referência bibliográfica
- Atalhos de produtividade para inserção/transformação rápida de blocos.
- Validação estrutural em tempo real (avisos e correções sugeridas).
- Nenhuma necessidade de escrever comandos LaTeX; o usuário edita semanticamente.

Representação Interna

Cada documento é convertido e armazenado como um JSON estruturado (AST). Exemplo:

{
"type": "section",
"title": "Introdução",
"content": [
{
"type": "paragraph",
"text": "Texto técnico aqui"
}
]
}

Observações de implementação:

- O editor opera em memória sobre a AST; todas as operações do usuário alteram a AST, que é serializável.
- O conversor (AST → LaTeX) é responsável por mapear blocos para comandos LaTeX seguros e auditáveis.
- Recomendado: operações imutáveis e difs para facilitar undo/redo e sincronização colaborativa futura.

## 11. Conversão para LaTeX

Pipeline

1. Editor → AST


    - O editor serializa a AST em formato JSON validado.

2. AST → Template LaTeX


    - Conversor aplica template selecionado, mapeando blocos para regiões do `.tex`.

3. Inserção automática de:


    - Pacotes: lista de `\usepackage{...}` baseada em metadados e blocos usados.
    - Estrutura correta: preâmbulo, classes, seções, labels e referências.
    - Bibliografia: geração de `.bib` ou integração com gerenciadores (BibTeX/Biber) conforme template.
    - Layout científico padrão: margens, fontes e estilos conforme template escolhido.

Regras e garantias

- O usuário não vê LaTeX, mas o sistema gera LaTeX limpo, versionável e compatível com `pdflatex`/`xelatex`.
- O conversor deve sanear entradas (escape de texto onde necessário) e evitar injeção de comandos LaTeX arbitrários.
- Gerar `.tex` com markers/comentários que permitam auditoria e edição manual por usuários avançados.

Observações de implementação

- Implementar transformações por bloco (módulos responsáveis por mapear cada tipo de bloco para LaTeX).
- Gerar bibliografia automaticamente e anexar `\bibliography{...}` no template; oferecer opção de arquivo `.bib` exportável.
- Fornecer um modo de "inspeção" que mostra o `.tex` gerado (somente leitura por padrão) e links para baixar artefatos.

## 12. Compilação e Geração de PDF

Processo

- O LaTeX gerado pelo conversor é compilado em ambiente isolado (container) para garantir segurança e reprodutibilidade.
- O worker de compilação executa a pipeline (pdflatex/xelatex, BibTeX/Biber se aplicável) e coleta artefatos (`.pdf`, `.log`, `.aux`, `.toc`).

Tratamento de erros

- Erros de compilação são interpretados e mapeados para mensagens amigáveis.
- O sistema deve traduzir mensagens técnicas do `.log` para linguagem humana e apontar o bloco AST correspondente no editor.
  - Ex.: se há erro em uma equação, mapear para o bloco de tipo `equation` e destacar sua localização.
- Fornecer sugestões acionáveis (por exemplo: pacotes faltando, ambiente não fechado) sem expor LaTeX cru ao usuário por padrão.

Preview

- Preview incremental em PDF: renderização parcial/rápida para seções modificadas quando possível.
- Atualização sob demanda (não a cada tecla): o editor deve disparar compilação incremental por evento (ex.: salvar, botão "Atualizar preview" ou intervalo configurável).
- Garantir que preview não bloqueie o pipeline de compilação final (jobs separados: preview vs. full build).

Observações de implementação

- Usar caches de compilação e hashes do AST/template para acelerar builds repetidos.
- Limitar recursos de preview para não esgotar quotas do worker (timeouts e limites de memória/CPU).
- Registrar e expor logs estruturados por `jobId` para diagnóstico e reprodução de falhas.

## 13. Exportação Final

Formatos suportados (MVP / roadmap):

- PDF (obrigatório) — artefato final de distribuição.
- LaTeX (`.tex`) — arquivo `.tex` gerado pelo conversor, para usuários avançados.
- OFF (estrutura intermediária futura) — formato binário/compactado para representar o documento completo com recursos (imagens, bibliografia) para import/export entre instâncias.
- JSON (AST) — exportação do AST serializado, permitindo reimportação, diffing e versionamento.

Recomendações:

- Sempre gerar e armazenar todos os artefatos (`.pdf`, `.tex`, `.json`) por job, permitindo download e auditoria.
- Incluir metadados no arquivo exportado (hash do build, versão do template, idioma, data, jobId) para reprodutibilidade.
- Fornecer exportação via API e via UI (download direto e links assinados quando armazenado em object storage).

## 14. Qualidade e Rigor

Objetivo

- Garantir que nenhum documento inválido seja exportado; manter integridade, consistência e conformidade com padrões acadêmicos/engenharia.

Validações obrigatórias

- Estrutura: verificar presença de elementos essenciais (título, autor(es), resumo para certos tipos de documento, seções ordenadas).
- Referências: checar correspondência entre citações in-text e entradas na bibliografia; avisar sobre citações órfãs ou referências não citadas.
- Numeração: validar sequência correta de numeração de seções, figuras, tabelas e equações; detectar saltos ou duplicações inesperadas.
- Coerência de seções: garantir hierarquia correta (por exemplo, não permitir sub-seção sem seção pai) e detectar conteúdos vazios ou placeholders não preenchidos.

Fluxo de validação

1. Validações em tempo real no editor (avisos não bloqueantes) — permitir correções rápidas.
2. Validação pré-exportação (simulacro de build leve) — bloqueante se houver erros críticos.
3. Relatório detalhado ao usuário com itens corrigíveis, apontando blocos AST responsáveis e links para ações no editor.

Política de bloqueio

## O QUE ESTÁ FORA (IMPORTANTÍSSIMO)

As seguintes decisões e funcionalidades estão oficialmente fora do escopo inicial do DocCollab‑v0:

- ❌ Editor WYSIWYG genérico
- ❌ Texto livre sem semântica
- ❌ “Modo LaTeX” — não haverá um modo onde o usuário edite LaTeX diretamente
- ❌ Colaboração em tempo real (edição concorrente) — versão futura condicionada a infraestrutura de sincronização
- ❌ Dependência de backend para edição local — o editor funciona sem necessidade de backend para edição básica/exportar AST
- ❌ Estética como prioridade — foco em produtividade e previsibilidade; refinamentos visuais são secundários

Documentar essas exclusões é crítico para manter as decisões de projeto claras e evitar escopo inflacionado durante o MVP.

- Erros críticos (ex.: bibliografia ausente quando exigida pelo template, LaTeX inválido detectado no estágio de conversão) impedem exportação até correção.
- Avisos (ex.: referência não citada) são mostrados mas não bloqueiam exportação por padrão; opção para tratar avisos como erros em perfis de qualidade estritos.

Automação e QA

- Integrar checagens automáticas em pipelines CI para documentos armazenados em repositórios (validação de pré-merge).
- Manter testes unitários para regras de validação (casos de referência, numeração, hierarquia).

## 15. Diretrizes para o GitHub Copilot

- Gerar código modular: priorizar módulos pequenos e coesos com responsabilidades bem definidas.
- Sem dependência de frameworks JS: frontend em HTML/CSS/JS puro; evitar React/Angular/Vue no MVP.
- Funções pequenas, testáveis: cada função deve ter um propósito claro e cobertura de testes unitários.
- Comentários explicando o porquê, não apenas o “como”: justificar decisões de design e casos de borda.
- Priorizar legibilidade e previsibilidade: código explicável, sem mágicas; favorecer clareza sobre micro-otimizações.

Recomendações operacionais

- Gerar sempre testes unitários ao criar lógica crítica (converter, validações, worker).
- Evitar dependências externas desnecessárias; quando usadas, documentar rationale e risco.
- Seguir convenções de nomeação e estrutura de pastas simples para facilitar manutenção.

## 3. Componentes (alto nível)

- Cliente `editor`: editor intermediário (web) que manipula um formato estruturado (JSON/AST) — não LaTeX.
- API Server: endpoints REST para submissão, status, fetch de artefatos, autenticação e gerenciamento de templates.
- Job Queue: broker (ex.: Redis/RabbitMQ) para fila de compilação assíncrona.
- Worker/Compilador: workers que recebem jobs, convertem o formato intermediário para LaTeX e invocam compilador (Docker/pdflatex/xelatex) em sandbox.
- Storage de Artefatos: object storage (S3/MinIO) para PDFs, logs e .tex.
- Templates: repositório de templates LaTeX com placeholders e metadados.
- Metadata DB: banco leve (Postgres/SQLite) para jobs, versões e histórico.

## 4. Fluxo de dados

1. Usuário edita e salva documento no `editor` (formato intermediário - FI).
2. `editor` chama `POST /api/compile` com FI + parâmetros (template, engine).
3. API persiste job e enfileira ID no Job Queue.
4. Worker obtém job, valida entrada, executa conversão FI → `.tex` (converter), e executa compilador dentro de um container isolado.
5. Worker armazena artefatos em Storage e atualiza status/resultados na Metadata DB.
6. Cliente consulta `GET /api/status/:id` e baixa `GET /api/result/:id`.

## 5. API (Mínimo Viável)

- POST /api/compile
  - Body: { document: <FI JSON>, template: <template_id>, engine: "pdflatex|xelatex" }
  - Response: { jobId }
- GET /api/status/:jobId
  - Response: { status: queued|running|success|failed, progress, message }
- GET /api/result/:jobId
  - Response: redirects / JSON com links para artifacts { pdfUrl, texUrl, logUrl }
- GET /api/templates
  - Lista templates disponíveis

Autenticação inicial: token simples (API key) para MVP; OAuth2 para produção.

## 6. Formato intermediário (FI) — especificação básica

FI = JSON estruturado que representa blocos documentais:

- metadata: { title, authors: [], date, packages: [] }
- content: [ block ]

Block types (exemplos):

- { type: "section", level: 1, title: "Introdução", content: [ ... ] }
- { type: "paragraph", text: "..." }
- { type: "equation", latex: "E = mc^2" } (latex raw para equações)
- { type: "figure", src: <data-url|upload-ref>, caption: "...", width: "0.6\\textwidth" }
- { type: "table", headers: [...], rows: [[...]] }
- { type: "cite", key: "smith2020" }

Comentários:

- FI deve ser legível e auditável. Conversor mapeia blocos FI para LaTeX estruturado.

## 7. Conversor (FI → LaTeX)

Requisitos:

- Produzir `.tex` compilável com pdflatex/xelatex.
- Inserir `\label` e `\ref` conforme metadados.
- Gerar preâmbulo baseado em `metadata.packages` e `template`.
- Validar e sanear entrada (evitar injeção de comandos nocivos).

Estratégia:

- Implementar transformações por bloco (pattern-based).
- Fornecer hooks para manipulação de pacotes e comandos customizados.

## 8. Ambiente de compilação e sandboxing

- Cada job roda dentro de um container (Docker) com imagem mínima contendo TeX Live básico.
- Limites: CPU, memória, tempo de execução (ex.: 60s/4 CPUs/1GB como padrão configurável).
- Montagem somente de diretório temporário; nenhum acesso à rede externo por padrão (opcional via whitelist para CTAN).
- Captura de stdout/stderr e arquivos auxiliares (`.log`, `.aux`, `.toc`).

## 9. Armazenamento e artefatos

- Artefatos: PDF final, `.tex` gerado, `.log` e outros arquivos auxiliares.
- Storage: usar S3/MinIO; URL assinado para download seguro.
- Metadata DB guarda TTL e políticas de retenção.

## 10. Observabilidade e métricas

- Métricas-chave: tempo médio de build, taxa de sucesso, filas pendentes, utilização de worker.
- Logs estruturados por jobId (JSON) e traces para investigação.
- Exportar métricas para Prometheus/Grafana (MVP: logs + counters simples).

## 11. Segurança

- Sanitização do FI para bloquear comandos LaTeX arbitrários por padrão.
- Execução de compilador em sandbox containerizado sem rede.
- Escopo de permissão para templates/pacotes customizados apenas para usuários confiáveis.

## 12. Escalabilidade e Resiliência

- Workers stateless; horizontalizáveis.
- Broker (Redis/RabbitMQ) com retry/backoff e DLQ (dead-letter queue).
- Cache de dependências (pacotes LaTeX) para reduzir latência.

## 13. Reprodutibilidade

- Registrar ambiente de compilação (hash da imagem Docker, versão do TeX Live).
- Hash do FI + template → permite cache de artefatos.

## 14. Testes e validação

- Unit tests para o conversor (FI → LaTeX) com casos: seções, equações, figuras, tabelas e referências.
- Teste E2E: enviar FI simples, confirmar PDF gerado e comparar estrutura básica (número de seções, presença de equação).
- Testes de segurança: fuzzing do FI para detectar injeção.

## 15. MVP — escopo refinado

- Editor single-document minimal (web) que gera FI.
- API Server com endpoints de compile/status/result.
- Worker containerizado usando pdflatex; Storage em disco local ou MinIO.
- Conversor cobrindo blocos essenciais.
- Templates: 2 modelos (artigo técnico, relatório de engenharia).

## 16. Operação e Deploy (MVP)

- Compose/Docker: API, Worker, Redis e MinIO para desenvolvimento local.
- Produção: Kubernetes opcional com autoscaling para workers.

## 17. Riscos e mitigação

- Risco: LaTeX complexo que falha em tradução automática → Mitigação: permitir download do `.tex` e logs; oferecer edição manual do `.tex` para usuários avançados.
- Risco: arquivos maliciosos → Mitigação: validação rigorosa e containers imutáveis.

## 18. Próximos passos imediatos

1. Implementar conversor protótipo em `server/lib/converter.js` (FI → LaTeX).
2. Scaffold API mínimo (`POST /api/compile`, `GET /api/status/:id`, `GET /api/result/:id`).
3. Docker Compose para worker + broker + storage.
4. Teste E2E com documento exemplo.

---

Documento gerado para orientar o desenvolvimento do MVP e decisões de infraestrutura. Para seguir, posso gerar o esboço do `converter` em JavaScript, o `Dockerfile` da imagem de compilação, ou o scaffold do servidor API — qual você prefere agora?
