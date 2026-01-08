# Manual do Usuário - DocCollab v0

## Índice

1. [Introdução](#introdução)
2. [Iniciando o Sistema](#iniciando-o-sistema)
3. [Interface do Editor](#interface-do-editor)
4. [Criando um Novo Documento](#criando-um-novo-documento)
5. [Editando Conteúdo](#editando-conteúdo)
6. [Formatação de Texto](#formatação-de-texto)
7. [Inserindo Elementos](#inserindo-elementos)
8. [Trabalhando com Equações](#trabalhando-com-equações)
9. [Inserindo Figuras](#inserindo-figuras)
10. [Compilando para PDF](#compilando-para-pdf)
11. [Salvando e Abrindo Documentos](#salvando-e-abrindo-documentos)
12. [Atalhos de Teclado](#atalhos-de-teclado)
13. [Solução de Problemas](#solução-de-problemas)

---

## Introdução

O **DocCollab** é um editor de documentos científicos baseado em AST (Abstract Syntax Tree) que permite criar documentos estruturados e compilá-los para PDF usando LaTeX. Todo o conteúdo é armazenado como estrutura semântica, garantindo consistência e facilitando a edição colaborativa.

### Características Principais

- ✅ Editor WYSIWYG (What You See Is What You Get)
- ✅ Compilação em tempo real para PDF
- ✅ Suporte a equações LaTeX
- ✅ Estrutura semântica com seções e subseções
- ✅ Formatação inline (negrito, itálico, código)
- ✅ Inserção de figuras e tabelas
- ✅ Salvamento automático local (IndexedDB)
- ✅ Paginação e quebras de página
- ✅ Suporte multilíngue (pt-BR, en-US, es-ES)

---

## Iniciando o Sistema

### Requisitos

- Node.js instalado (versão 14 ou superior)
- Navegador moderno (Chrome, Edge, Firefox)
- LaTeX instalado (TeX Live, MiKTeX ou similar)

### Iniciando o Servidor

1. Abra o terminal na pasta do projeto
2. Execute o comando:
   ```bash
   node server/server.cjs
   ```
3. O servidor iniciará na porta 3000
4. Abra o navegador e acesse: `http://127.0.0.1:3000/app.html?new=1`

---

## Interface do Editor

A interface está dividida em três áreas principais:

### 1. Barra Lateral Esquerda (Toolbar)

Contém botões para:

- **Formatação**: Negrito (B), Itálico (I), Código ({ })
- **Exclusão**: Botão 🗑 para apagar blocos
- **Inserção**: Botões para adicionar novos elementos

### 2. Área de Edição (Centro)

- Campo do documento editável
- Visualização em tempo real do conteúdo

### 3. Painel de Preview (Direita)

- Visualização do PDF compilado
- Atualiza automaticamente após compilação

### Barra Superior

- **Seletor de idioma**: Alterna entre pt-BR, en-US, es-ES
- **Botão "Novo documento"**: Cria documento em branco
- **Botão "Compilar"**: Gera o PDF
- **Botão "Abrir documento"**: Abre documentos salvos
- **Seletor de documentos**: Lista documentos disponíveis

---

## Criando um Novo Documento

### Método 1: Documento de Exemplo

1. Acesse: `http://127.0.0.1:3000/app.html?new=1`
2. O sistema carrega um documento de demonstração completo
3. Edite o conteúdo conforme necessário

### Método 2: Documento em Branco

1. Clique no botão **"Novo documento"** na barra superior
2. A página recarrega com campos vazios:
   - **Título do documento** (placeholder visível)
   - **Autor** (placeholder visível)
   - **Resumo (Abstract)** (placeholder visível)
   - **Nova Seção** com um parágrafo vazio

---

## Editando Conteúdo

### Editando Campos

1. **Clique diretamente** em qualquer texto para editá-lo
2. **Digite normalmente** - o cursor permanece estável
3. **Pressione Tab** ou clique fora para sair do campo
4. O conteúdo é **salvo automaticamente** a cada 1.2 segundos

### Campos Editáveis

- Título do documento (H1)
- Autor
- Abstract/Resumo
- Títulos de seções (H2)
- Títulos de subseções (H3)
- Parágrafos de texto
- Equações LaTeX
- Legendas de figuras

### Placeholders

Campos vazios mostram texto cinza para orientação:

- "Título do documento"
- "Autor"
- "Resumo (Abstract)"
- "Escreva aqui..."
- "Título da seção"
- "Título da subseção"

---

## Formatação de Texto

### Usando Botões da Toolbar

1. **Selecione o texto** que deseja formatar
2. Clique no botão correspondente:
   - **B**: Negrito
   - **I**: Itálico
   - **{ }**: Código

### Usando Atalhos de Teclado

- **Ctrl+B**: Negrito
- **Ctrl+I**: Itálico
- (Código não tem atalho - use o botão)

### Resultado no LaTeX

- Negrito → `\textbf{texto}`
- Itálico → `\emph{texto}`
- Código → `\texttt{texto}`

---

## Inserindo Elementos

Todos os botões de inserção estão na barra lateral esquerda com o prefixo **➕**:

### ➕ Sec (Inserir Seção)

1. Posicione o cursor em qualquer lugar do documento
2. Clique em **"➕ Sec"**
3. Uma nova seção é inserida como irmã da seção atual
4. Digite o título da seção no campo H2

### ➕ Sub (Inserir Subseção)

1. Posicione o cursor dentro de uma seção
2. Clique em **"➕ Sub"**
3. Uma subseção é criada dentro da seção atual
4. Digite o título da subseção no campo H3

### ➕ ¶ (Inserir Parágrafo)

1. Posicione o cursor onde deseja o parágrafo
2. Clique em **"➕ ¶"**
3. Um parágrafo vazio é inserido
4. Digite o conteúdo

### ➕ Σ (Inserir Equação)

1. Clique em **"➕ Σ"**
2. Um campo de equação aparece (estilo `<pre>`)
3. Digite a equação em **sintaxe LaTeX pura**
   - Exemplo: `a^2 + b^2 = c^2`
4. **NÃO** use delimitadores (`\begin{equation}` é adicionado automaticamente)

### ➕ 🖼 (Inserir Figura)

1. Clique em **"➕ 🖼"**
2. Preencha dois campos editáveis:
   - **Caminho da imagem**: `imagens/foto.jpg`
   - **Legenda**: "Descrição da figura"
3. Coloque a imagem na pasta `server/tmp/` ou em subpasta relativa
4. Formatos suportados: `.png`, `.jpg`, `.jpeg`, `.pdf`

### ➕ ⌗ (Inserir Tabela)

1. Clique em **"➕ ⌗"**
2. Um bloco de tabela é criado
3. Edite o conteúdo da tabela (implementação básica)

### ➕ 📄 (Inserir Quebra de Página)

1. Clique em **"➕ 📄"**
2. Uma linha tracejada aparece no editor com o texto "— Quebra de Página —"
3. No PDF, gera um `\newpage` (nova página)

### ➕ ✎ (Inserir Citação)

1. Clique em **"➕ ✎"**
2. Digite o texto da citação
3. (Funcionalidade de bibliografia ainda em desenvolvimento)

### ➕ 📚 (Inserir Bibliografia)

1. Clique em **"➕ 📚"**
2. Um bloco de bibliografia é criado
3. Adicione entradas manualmente

---

## Trabalhando com Equações

### Sintaxe LaTeX

O editor aceita **equações LaTeX puras** sem delimitadores. Exemplos:

#### Equação Simples

```
a^2 + b^2 = c^2
```

#### Equação com Frações

```
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

#### Equação com Somatório

```
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
```

#### Equação com Integral

```
\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
```

### Resultado no PDF

Todas as equações são renderizadas dentro de `\begin{equation}...\end{equation}` automaticamente, com numeração automática e label único baseado no ID do bloco.

### Dicas

- ✅ Use caracteres especiais LaTeX: `\alpha`, `\beta`, `\sum`, `\int`
- ✅ Use chaves `{}` para agrupar: `x^{2y}`
- ✅ Use `\frac{numerador}{denominador}` para frações
- ❌ **NÃO** use `$`, `$$`, `\[`, `\]` - são adicionados automaticamente

---

## Inserindo Figuras

### Preparação

1. Coloque a imagem na pasta `server/tmp/`
   - Exemplo: `server/tmp/minha-imagem.png`
2. Ou crie uma subpasta:
   - Exemplo: `server/tmp/figuras/diagrama.jpg`

### Inserindo no Editor

1. Clique em **"➕ 🖼"**
2. Edite o campo **src** (caminho da imagem):
   - Caminho absoluto: `minha-imagem.png`
   - Caminho relativo: `figuras/diagrama.jpg`
3. Edite o campo **caption** (legenda):
   - Exemplo: "Diagrama de fluxo do sistema"

### Resultado no LaTeX

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\linewidth]{minha-imagem.png}
\caption{Diagrama de fluxo do sistema}
\label{blk:figure_123}
\end{figure}
```

### Formatos Suportados

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- PDF (`.pdf`) - ideal para gráficos vetoriais

### Troubleshooting

- ❌ **Imagem não aparece**: Verifique se o arquivo existe em `server/tmp/`
- ❌ **Caminho errado**: Use caminho relativo ao diretório onde o `.tex` é compilado
- ✅ **Boa prática**: Use nomes de arquivo sem espaços e acentos

---

## Compilando para PDF

### Método 1: Botão Compilar

1. Clique no botão **"Compilar"** na barra superior
2. O sistema:
   - Gera o arquivo `.tex` a partir do AST
   - Executa `pdflatex` (ou `xelatex` se necessário)
   - Exibe o PDF no painel direito
3. **Aguarde** a compilação (pode levar 3-10 segundos)

### Método 2: Compilação Automática

- O sistema tenta compilar automaticamente 300ms após montar o editor
- Útil para preview rápido ao abrir um documento

### Erros de Compilação

Se houver erro:

1. **Fundo vermelho** aparece nos blocos com erro
2. **Mensagem de erro** é exibida no Console (F12)
3. Corrija o erro e compile novamente
4. O background vermelho **desaparece automaticamente** após compilação bem-sucedida

### Logs de Compilação

- Abra o Console do navegador (F12 → Console)
- Procure por:
  - `preview: sending AST to /api/compile`
  - Mensagens de erro do LaTeX

---

## Salvando e Abrindo Documentos

### Salvamento Automático

- O sistema salva **automaticamente** a cada 1.2 segundos após edições
- Usa **IndexedDB** do navegador (armazenamento local)
- Cada versão salva inclui:
  - AST completo
  - Timestamp
  - Arquivo `.tex` gerado (opcional)

### Salvamento Manual

Não há botão "Salvar" - o salvamento é sempre automático.

### Abrindo Documentos Salvos

1. Use o **seletor dropdown** na barra superior
2. Selecione o documento desejado
3. Clique em **"Abrir documento"**
4. O documento é carregado no editor

### Listagem de Documentos

- O seletor mostra todos os documentos salvos no IndexedDB
- Formato: ID do documento ou título (se disponível)

### Exportando PDF

1. Compile o documento
2. O PDF aparece no painel direito
3. Clique com botão direito → **"Salvar como..."**
4. Escolha o local e nome do arquivo

### Limpando Documentos Salvos

Não há interface para deletar documentos. Use o Console:

```javascript
// Abrir IndexedDB e listar documentos
indexedDB.databases();
```

Ou use as ferramentas de desenvolvedor (F12 → Application → IndexedDB).

---

## Atalhos de Teclado

### Formatação

| Atalho   | Ação    |
| -------- | ------- |
| `Ctrl+B` | Negrito |
| `Ctrl+I` | Itálico |

### Exclusão

| Atalho        | Ação                                 |
| ------------- | ------------------------------------ |
| `Ctrl+Delete` | Apagar bloco atual (com confirmação) |

### Navegação

| Atalho  | Ação                                        |
| ------- | ------------------------------------------- |
| `Tab`   | Sair do campo atual                         |
| `Enter` | Nova linha (dentro de parágrafos/abstracts) |

### Desenvolvimento

| Atalho              | Ação                                    |
| ------------------- | --------------------------------------- |
| `F12`               | Abrir DevTools (Console, Network, etc.) |
| `Ctrl+Shift+R`      | Hard refresh (limpar cache)             |
| `Ctrl+Shift+Delete` | Limpar cache do navegador               |

---

### Mapa completo de atalhos (editor)

Observação: Windows/Linux = `Ctrl`, macOS = `⌘` (Meta). Atalhos são ignorados quando o foco está em campos de formulário (`input`, `textarea`) ou em áreas `contentEditable`.

- Formatação

  - `Ctrl/⌘ + B` — Negrito
  - `Ctrl/⌘ + I` — Itálico
  - `Ctrl/⌘ + K` — Código inline
  - `Ctrl/⌘ + Shift + K` — Bloco de código / inserir equação (dependendo do contexto)

- Manipulação de blocos

  - `Ctrl/⌘ + D` — Duplicar bloco selecionado
  - `Ctrl/⌘ + Shift + ArrowUp` — Mover bloco para cima
  - `Ctrl/⌘ + Shift + ArrowDown` — Mover bloco para baixo
  - `Ctrl/⌘ + Delete` — Remover bloco (confirmação)

- Compilação

  - `Ctrl/⌘ + Enter` — Compilar (aciona o botão Compilar)

- Inserção de elementos
  - `Ctrl/⌘ + Alt + 1` — Inserir Seção
  - `Ctrl/⌘ + Alt + 2` — Inserir Subseção
  - `Ctrl/⌘ + Alt + P` — Inserir Parágrafo
  - `Ctrl/⌘ + Alt + E` — Inserir Equação
  - `Ctrl/⌘ + Alt + F` — Inserir Figura
  - `Ctrl/⌘ + Alt + T` — Inserir Tabela
  - `Ctrl/⌘ + Alt + Q` — Inserir Quebra de Página
  - `Ctrl/⌘ + Alt + C` — Inserir Citação
  - `Ctrl/⌘ + Alt + B` — Inserir Bibliografia

Boas práticas:

- Os atalhos disparam os mesmos handlers que os botões da toolbar (consistência de comportamento).
- Ao acionar por atalho, o sistema mostra feedback visual mínimo (destaque no botão ou toast).

---

## Autenticação e Contas

O sistema oferece um protótipo de autenticação local com criação de conta (signup) e login. Essa funcionalidade é destinada a testes locais e armazena usuários em `server/tmp/users.json`.

### Fluxo de cadastro (signup)

1. Clique em **Cadastre-se para usar Gratuitamente** na página inicial.
2. Preencha Nome, E-mail e Senha.
3. Ao submeter, o cliente chama `POST /api/signup` no servidor local. Se o e-mail não existir, o servidor cria o usuário com senha hasheada e retorna sucesso.
4. Após criação, o cliente tenta fazer login automaticamente (`/api/login`) e, em caso de sucesso, salva `authToken`, `userId` e `userName` no `localStorage` e redireciona para o editor.

### Fluxo de login

1. Clique em **Login** na topbar e preencha e-mail e senha.
2. O cliente envia `POST /api/login`. Em caso de credenciais válidas, o servidor responde com `{ success: true, userId, token, name }`.
3. O cliente armazena o `token` e `userId` em `localStorage` e redireciona para `/editor.html`.
4. Em caso de falha, o cliente mostra o alerta `Login inválido !!!`.

### Sessão e Topbar

- Quando um token está presente em `localStorage` o botão da topbar exibe o nome do usuário (abreviado se necessário) e um botão `Sair`.
- Clicar em `Sair` remove `authToken`, `userId` e `userName` do `localStorage` e recarrega a página.

### Observações de segurança

- Este mecanismo é um protótipo local — não use em produção. Senhas são hasheadas com `bcryptjs`, mas não há gestão de sessões segura, expiração ou proteção CSRF.
- Para produção, substitua por um serviço de autenticação com armazenamento seguro (banco de dados), HTTPS e tokens JWT com expiração.

## API local (endpoints relevantes)

- `POST /api/signup` — corpo JSON: `{ name, email, password }` — cria usuário localmente (resposta `{ success: true, userId }`).
- `POST /api/login` — corpo JSON: `{ email, password }` — valida credenciais (resposta `{ success: true, userId, token, name }`).

Os arquivos de usuários são persistidos em `server/tmp/users.json` (formato JSON, array de objetos com `id`, `name`, `email`, `passwordHash`, `createdAt`).

## Solução de Problemas

### Problema: Página mostra "Carregando editor..." e não carrega

**Causa**: Erro de sintaxe no JavaScript ou cache desatualizado.

**Solução**:

1. Pressione `F12` → aba **Console**
2. Procure por erros em vermelho
3. Faça hard refresh: `Ctrl+Shift+R` ou `Ctrl+F5`
4. Se persistir, limpe o cache: `Ctrl+Shift+Delete` → últimas 1 hora

---

### Problema: Botão "Novo documento" não funciona

**Causa**: Event listeners duplicados ou código desatualizado.

**Solução**:

1. Faça hard refresh: `Ctrl+Shift+R`
2. Verifique o Console (F12) por erros
3. Feche completamente o navegador e abra novamente
4. Tente em modo anônimo/privado: `Ctrl+Shift+N`

---

### Problema: Campos vazios não aparecem

**Causa**: CSS não carregou ou placeholders não estão no estilo.

**Solução**:

1. Faça hard refresh: `Ctrl+Shift+R`
2. Verifique no DevTools (F12 → Elements) se o CSS foi carregado
3. Procure por `editor.css` na aba Network
4. Se status for 404, verifique o caminho do arquivo

---

### Problema: Cursor pula para o início ao digitar

**Causa**: `renderAll()` sendo chamado durante edição (bug corrigido).

**Solução**:

1. Atualize o código para a última versão
2. A correção remove `renderAll()` de `updateBlock()`
3. Faça hard refresh após atualizar

---

### Problema: Equação dá erro de compilação

**Causa**: Sintaxe LaTeX incorreta ou caracteres escapados.

**Solução**:

1. Verifique a sintaxe LaTeX: [Overleaf Math](https://www.overleaf.com/learn/latex/Mathematical_expressions)
2. **NÃO** use `\begin{equation}` ou delimitadores - são adicionados automaticamente
3. Use apenas conteúdo puro: `x^2 + y^2 = z^2`
4. Verifique chaves balanceadas: `\frac{a}{b}`

---

### Problema: Figura não aparece no PDF

**Causa**: Arquivo não existe no caminho especificado ou formato incompatível.

**Solução**:

1. Verifique se o arquivo existe em `server/tmp/`
2. Use caminho relativo correto: `minha-imagem.png` ou `figuras/foto.jpg`
3. Formatos suportados: `.png`, `.jpg`, `.jpeg`, `.pdf`
4. Evite espaços e acentos no nome do arquivo
5. Compile novamente após corrigir o caminho

---

### Problema: PDF não compila (erro genérico)

**Causa**: LaTeX não instalado, erro de sintaxe no `.tex`, ou timeout.

**Solução**:

1. Verifique se LaTeX está instalado:
   ```bash
   pdflatex --version
   ```
2. Abra o Console (F12) e procure por logs de compilação
3. Verifique o arquivo `.tex` gerado em `server/tmp/doc-*.tex`
4. Tente compilar manualmente no terminal:
   ```bash
   cd server/tmp
   pdflatex doc-1234567890.tex
   ```
5. Leia a mensagem de erro do LaTeX para identificar o problema

---

### Problema: Erro "INVALID_TITLE_COUNT"

**Causa**: Tentativa de deletar o único bloco de título do documento.

**Solução**:

- Todo documento precisa ter exatamente **1 título**
- Não delete o bloco de título
- Se precisar de documento sem título, deixe o campo vazio

---

### Problema: Salvamento não está funcionando

**Causa**: IndexedDB bloqueado, modo privado, ou erro de permissão.

**Solução**:

1. Verifique se está em **modo normal** (não privado/anônimo)
2. Abra DevTools → Application → IndexedDB → `doccollab-db`
3. Verifique se há entradas em `documents` e `versions`
4. Se IndexedDB estiver vazio, o salvamento não está funcionando
5. Tente outro navegador (Chrome/Edge geralmente funcionam melhor)

---

### Problema: Preview do PDF não atualiza

**Causa**: Cache do iframe ou erro de compilação silencioso.

**Solução**:

1. Clique novamente em **"Compilar"**
2. Verifique o Console por erros
3. Recarregue a página inteira: `F5`
4. Se o iframe estiver vazio, o PDF não foi gerado

---

### Problema: Servidor não inicia

**Causa**: Porta 3000 já em uso ou Node.js não instalado.

**Solução**:

1. Verifique se Node.js está instalado:
   ```bash
   node --version
   ```
2. Verifique se a porta está livre:
   ```powershell
   netstat -ano | findstr :3000
   ```
3. Mate o processo que está usando a porta:
   ```powershell
   taskkill /F /PID <PID>
   ```
4. Ou altere a porta no arquivo `server/server.cjs`:
   ```javascript
   const PORT = process.env.PORT || 3001;
   ```

---

## Boas Práticas

### Estrutura de Documentos

1. **Sempre comece com**:
   - Título
   - Autor
   - Abstract (resumo)
2. Use **seções** para organizar conteúdo principal
3. Use **subseções** para dividir seções longas
4. Use **parágrafos** para texto corrido
5. Use **equações** para fórmulas matemáticas
6. Use **figuras** para ilustrações
7. Use **quebras de página** para controlar layout

### Editando

- ✅ Salve frequentemente (automático, mas compile regularmente)
- ✅ Compile após mudanças significativas
- ✅ Teste equações logo após inserir
- ✅ Verifique o PDF antes de exportar
- ❌ Evite HTML inline no texto (use formatação do editor)
- ❌ Não insira equações com delimitadores externos

### Performance

- Documentos grandes (>50 blocos) podem demorar para compilar
- Use hard refresh (`Ctrl+Shift+R`) após atualizações de código
- Limpe o cache do navegador periodicamente
- Feche abas não utilizadas para melhor performance

---

## Recursos Avançados

### Personalização de Idioma

1. Use o **seletor de idioma** no topo da página
2. Idiomas disponíveis: `pt-BR`, `en-US`, `es-ES`
3. A interface é traduzida automaticamente

### Paginação Automática

- O sistema adiciona números de página no rodapé do PDF
- Usa o pacote `fancyhdr` do LaTeX
- Páginas centralizadas no rodapé

### Salvamento de Versões

- Cada salvamento cria uma nova versão no IndexedDB
- Versões incluem timestamp e AST completo
- (Funcionalidade de histórico ainda não implementada na UI)

---

## Limitações Conhecidas

### Funcionalidades Não Implementadas

- ❌ Edição colaborativa em tempo real
- ❌ Histórico de versões (UI)
- ❌ Deletar documentos pela interface
- ❌ Upload de imagens via UI
- ❌ Tabelas complexas (apenas estrutura básica)
- ❌ Citações e bibliografia automáticas (BibTeX)
- ❌ Exportar para outros formatos (DOCX, HTML, etc.)
- ❌ Spell checker

### Restrições Técnicas

- ⚠️ Requer LaTeX instalado no sistema
- ⚠️ Compilação pode ser lenta (3-10 segundos)
- ⚠️ Salvamento local apenas (sem sincronização em nuvem)
- ⚠️ Limite de tamanho de documento (depende do navegador)

---

## Suporte e Contato

### Reportando Bugs

1. Abra o Console do navegador (F12)
2. Reproduza o erro
3. Copie as mensagens de erro
4. Descreva os passos para reproduzir
5. Envie para o desenvolvedor

### Logs do Sistema

- **Client logs**: Console do navegador (F12)
- **Server logs**: `server/logs/client.log`
- **Compilation logs**: Terminal onde `server.cjs` está rodando

### Informações Úteis ao Reportar

- Sistema operacional (Windows, macOS, Linux)
- Navegador e versão (Chrome 143, Edge 120, etc.)
- Versão do Node.js (`node --version`)
- Versão do LaTeX (`pdflatex --version`)
- Mensagens de erro completas

---

## Glossário

**AST (Abstract Syntax Tree)**: Árvore de sintaxe abstrata que representa a estrutura semântica do documento.

**Block**: Unidade semântica do documento (título, parágrafo, seção, etc.).

**contentEditable**: Atributo HTML que torna elementos editáveis diretamente no navegador.

**IndexedDB**: Banco de dados local do navegador para armazenamento persistente.

**LaTeX**: Sistema de preparação de documentos científicos de alta qualidade tipográfica.

**Placeholder**: Texto de orientação exibido em campos vazios.

**Hard Refresh**: Recarregamento de página ignorando cache (`Ctrl+Shift+R`).

**Toolbar**: Barra de ferramentas com botões de ação.

**Inline Formatting**: Formatação aplicada a partes de texto (negrito, itálico).

**Block-level Element**: Elemento estrutural do documento (seção, parágrafo).

---

## Histórico de Versões

### v0.1 (31/12/2025)

- ✅ Editor baseado em AST
- ✅ Compilação LaTeX para PDF
- ✅ Salvamento automático (IndexedDB)
- ✅ Formatação inline (negrito, itálico, código)
- ✅ Inserção de seções, subseções, parágrafos
- ✅ Suporte a equações LaTeX
- ✅ Inserção de figuras
- ✅ Quebra de página
- ✅ Paginação automática
- ✅ Placeholders para campos vazios
- ✅ Botão de deletar blocos
- ✅ Suporte multilíngue (pt-BR, en-US, es-ES)

---

**DocCollab v0** - Sistema de Edição Colaborativa de Documentos Científicos  
Desenvolvido com HTML, CSS, JavaScript (ES6) e Node.js  
LaTeX para compilação de PDF
