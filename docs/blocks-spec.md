# Spec de Blocos — DocCollab‑v0

Este documento descreve os blocos estruturais permitidos, seu formato JSON (AST), campos obrigatórios e validações básicas.

Formato geral

- Cada bloco é um objeto JSON com pelo menos a propriedade `type`.
- Blocos que contêm conteúdo aninhado usam o campo `content`, que é uma lista de blocos.

Exemplos de blocos permitidos

1) Título

{
  "type": "title",
  "text": "Título do Documento"
}

Validações:
- `text`: string não vazia

2) Autor

{
  "type": "author",
  "name": "Nome Completo",
  "affiliation": "Instituição",
  "email": "email@dominio.com"
}

Validações:
- `name`: string não vazia
- `email`: formato básico de e‑mail (opcionalmente obrigatório dependendo do template)

3) Resumo (abstract)

{
  "type": "abstract",
  "content": [
    { "type": "paragraph", "text": "Resumo técnico do trabalho." }
  ]
}

Validações:
- `content`: array não vazio
- cada item em `content` deve ser um bloco válido (p.ex. `paragraph`)

4) Seção

{
  "type": "section",
  "title": "Introdução",
  "content": []
}

Validações:
- `title`: string não vazia
- `content`: array (pode estar vazio)

5) Sub-seção

{
  "type": "subsection",
  "title": "Contexto",
  "content": []
}

Validações:
- `title`: string não vazia
- Deve existir uma seção pai em níveis válidos (validação contextual)

6) Parágrafo

{
  "type": "paragraph",
  "text": "Texto técnico estruturado."
}

Validações:
- `text`: string (pode ser vazia em rascunhos, mas avisar)

7) Equação

{
  "type": "equation",
  "latex": "E = mc^2",
  "numbered": true
}

Notas:
- O campo `latex` é preenchido pelo editor matemático; o usuário não edita LaTeX diretamente no fluxo padrão.

Validações:
- `latex`: string não vazia
- `numbered`: boolean

8) Figura

{
  "type": "figure",
  "src": "image.png",
  "caption": "Descrição da figura",
  "label": "fig:model"
}

Validações:
- `src`: referência válida (upload id, data URL ou caminho relativo)
- `caption`: string
- `label`: opcional, deve ser única dentro do documento

9) Tabela

{
  "type": "table",
  "caption": "Tabela de Resultados",
  "data": [
    ["Coluna 1", "Coluna 2"],
    ["Valor A", "Valor B"]
  ]
}

Validações:
- `data`: matriz não vazia; todas as linhas devem ter o mesmo número de colunas

10) Citação (referência bibliográfica)

{
  "type": "citation",
  "key": "knuth1984"
}

Validações:
- `key`: string correspondendo a uma entrada na bibliografia (`.bib`) ou no gerenciador de referências

Regras transversais e notas de validação

- Unicidade de labels: `label` de figuras/tabelas/equações deve ser única (ou automaticamente disambiguada).
- Referências cruzadas: cada `citation.key` referenciado deve existir na bibliografia; cada `\ref` gerado deve mapear para um `label` válido.
- Hierarquia: `subsection` não pode existir sem uma `section` pai; verificar durante validação AST.
- Numeração: a numeração de seções/figuras/tabelas/equações é derivada durante a conversão e validada quanto a saltos/duplicatas.

Boas práticas para o conversor

- Cada tipo de bloco deve ter um módulo de conversão dedicado (por ex., `convertParagraph`, `convertFigure`, `convertEquation`).
- O conversor aplica escaping de texto onde necessário (p.ex. caracteres especiais em LaTeX).
- O conversor injeta `\label{...}` e `\caption{...}` onde aplicável usando os campos `label` e `caption`.
- O conversor deve gerar `.tex` com comentários que mapeiem trechos para offsets/IDs do AST para facilitar diagnósticos.

Exemplo completo mínimo (documento AST)

{
  "type": "document",
  "metadata": { "title": "Exemplo", "authors": [{ "name": "Ana" }] },
  "content": [
    { "type": "title", "text": "Exemplo" },
    { "type": "abstract", "content": [ { "type": "paragraph", "text": "Resumo..." } ] },
    { "type": "section", "title": "Introdução", "content": [ { "type": "paragraph", "text": "Texto de introdução." } ] }
  ]
}

Próximos passos sugeridos

- Implementar `docs/blocks-spec.md` como fonte de verdade para o editor e para validações automáticas.
- Gerar testes unitários que validem exemplos válidos e inválidos (cobertura de regras).
- Mapear cada bloco a uma função do conversor no `server/lib/converter.js`.

---

Arquivo gerado automaticamente com base nas especificações fornecidas. Ajustes de campos e validações podem ser adicionados conforme necessidade do template ou requisitos do tipo de documento.

## Editor por Blocos — Regras Formais

Princípios

- Não existe "texto solto": todo conteúdo deve pertencer a um bloco válido.
- Cada ação do usuário é modelada como operação atômica que aplica uma mutação na AST:
  - `create` — cria um bloco
  - `move` — move um bloco entre posições/parentes
  - `edit` — edita campos de um bloco
  - `remove` — remove um bloco

Regras obrigatórias (impostas pelo editor)

- Apenas 1 `title` por documento — tentativa de criar um segundo título deve ser bloqueada ou reconciliada.
- O `abstract` (resumo) deve existir antes da primeira `section` quando o template exigir; o editor força a posição correta ao inserir o resumo.
- `subsection` não pode existir sem uma `section` pai — o editor deve impedir criação/remoção que violem hierarquia.
- `equation` não pode existir fora de uma `section` (ou outro container válido) — criação/colocação indevida é prevenida.
- `citation` só aparece na bibliografia se houver pelo menos uma `citation` referenciando sua `key` no documento; referências órfãs são removidas/avisadas.

Garantia do sistema

👉 O editor impede erros antes que eles existam — estados inválidos da AST são prevenidos por validações imediatas e restrições de UI. Validações adicionais ocorrem no momento de salvar/exportar.

Validação e UX

- Validações são exibidas em tempo real como avisos ou erros inline, indicando o bloco afetado e a ação recomendada.
- Operações que causariam erro crítico são bloqueadas com explicação e ação sugerida (por exemplo, mover uma `subsection` para um local sem `section` pai mostrará uma opção para criar a `section` automaticamente).
- O histórico de operações e difs permite undo/redo seguro e facilita correção automática quando aplicável.
