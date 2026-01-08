# Manual do Editor — DocCollab

Este documento descreve o uso básico do editor do DocCollab: criação e edição de blocos, barra de ferramentas, atalhos e resolução de problemas comuns.

1. Visão geral
- O editor organiza o documento como uma lista de blocos (parágrafos, títulos, figuras, tabelas, bibliografia, etc.).
- Cada bloco tem um tipo (`paragraph`, `heading`, `figure`, `table`, `bibliography`, etc.).

2. Inserir e editar blocos
- Inserir via toolbar: selecione o local e clique no botão do tipo desejado.
- Inserir via teclado: pressione `Enter` para criar novo bloco abaixo do atual; `Shift+Enter` insere quebra de linha dentro do bloco.
- Editar: clique dentro do bloco para ativar o editor embutido. Use as ações inline (negrito, itálico, links) quando disponíveis.

3. Toolbar e comandos principais
- Salvar: botão de salvar sincroniza com o backend local (ou `Ctrl+S`).
- Desfazer/Refazer: `Ctrl+Z` / `Ctrl+Y`.
- Inserir imagem/figura: abre diálogo para upload; imagens são referenciadas no AST e devem ser enviadas ao storage externo se configurado.
- Inserir bibliografia: insere bloco do tipo `bibliography`. Observação: entradas não citadas podem impedir exclusões — veja Troubleshooting.

4. Gerenciamento de bibliografia
- Adicionar entrada: use o formulário de bibliografia para criar `bib` entries (id gerada automaticamente).
- Citar entrada: insira citações inline que referenciem o `id` da entrada; somente entradas citadas são consideradas usadas.
- Remover entrada: o editor pode bloquear exclusão se a entrada ainda estiver sendo citada — verifique mensagens de erro.

5. Importar / Exportar
- Exportar AST: botão `Export` gera JSON do AST atual pronto para processamento (LaTeX/Bib).
- Importar AST: carregar arquivo JSON irá substituir ou mesclar com o documento atual (aviso antes da substituição).

6. Atalhos úteis
- `Ctrl+S` — salvar
- `Ctrl+Z` / `Ctrl+Y` — desfazer/refazer
- `Enter` — novo bloco
- `Shift+Enter` — quebra de linha no bloco

7. Logs e diagnóstico
- O cliente registra eventos em `/api/client-log`, que o servidor armazena em `server/logs/client.log`.
- Para problemas de render ou compile, verifique também `server/logs` para saída do compilador LaTeX.

8. Troubleshooting comum
- Erro "Invalid block type: X": verifique se o tipo do bloco existe em `assets/js/editor/block-factory.js` e se os templates associados estão carregados.
- Erro ao compilar LaTeX (pdflatex): abra `server/logs` e examine o `compile log` para localizar o erro de TeX. Mensagens comuns: macros inválidas (uso de `#` em modo horizontal), imagens faltantes, ou pacotes não instalados.
- Entradas de bibliografia não excluídas: confirme se não há citações remanescentes no documento (procure pelo `id` no AST).

9. Boas práticas
- Salve frequentemente e exporte o AST antes de operações destrutivas (importar/limpar).
- Para colaboração, sincronize mudanças com o backend e compartilhe o AST em vez de editar HTML diretamente.

Se quiser, posso gerar um resumo em PDF ou adicionar imagens com capturas de tela das partes do editor.
