# 🧪 Teste do LaTeX Linter

## Como Testar

1. Abra o editor LaTeX
2. Cole um dos exemplos abaixo
3. Clique no botão "LaTeX Linter" (canto inferior direito)
4. Verifique os erros detectados

---

## ✅ Exemplo 1: Erros de Sintaxe

```latex
\documentclass{article}
\begin{document}

Teste de $ não fechado

Teste de chave não fechada: \textbf{negrito

\begin{itemize}
\item Item 1
% Faltando \end{itemize}

\end{document}
```

**Erros esperados:**
- ❌ $ não fechado (modo matemático)
- ❌ Chave { não fechada
- ❌ Ambiente não fechado (itemize)

---

## ✅ Exemplo 2: Comandos Obsoletos

```latex
\documentclass{article}
\begin{document}

% Comando obsoleto
\begin{eqnarray}
  x + y = z
\end{eqnarray}

% Estilo obsoleto
$$ E = mc^2 $$

% Fontes antigas
{\bf Texto em negrito}
{\it Texto em itálico}

\end{document}
```

**Avisos esperados:**
- ⚠️ Ambiente eqnarray está obsoleto (use align)
- ⚠️ Use \[ \] ao invés de $$
- ⚠️ Comando de fonte obsoleto (use \textbf{}, \textit{})

---

## ✅ Exemplo 3: Pacotes Faltantes

```latex
\documentclass{article}
\begin{document}

% Sem \usepackage{graphicx}
\includegraphics{imagem.png}

% Sem \usepackage{amsmath}
\begin{align}
  x + y = z
\end{align}

% Sem \usepackage{hyperref}
\url{https://example.com}

\end{document}
```

**Erros esperados:**
- ❌ Comando \includegraphics requer pacote graphicx
- ❌ Ambiente align requer pacote amsmath
- ❌ Comando \url requer pacote hyperref

---

## ✅ Exemplo 4: Boas Práticas

```latex
\documentclass{article}
\begin{document}

% Espaço normal antes de \ref (deveria ser ~)
Veja a Figura \ref{fig:exemplo}

% Aspas erradas
"Texto entre aspas"

% Múltiplas linhas vazias


Parágrafo após múltiplas linhas

\end{document}
```

**Sugestões esperadas:**
- 💡 Use ~ (espaço não quebrável) antes de \ref
- 💡 Use aspas tipográficas LaTeX (``texto'')
- 💡 Use apenas uma linha vazia entre parágrafos

---

## ✅ Exemplo 5: Figuras e Tabelas sem Label

```latex
\documentclass{article}
\usepackage{graphicx}
\begin{document}

\begin{figure}[h]
  \centering
  \includegraphics{imagem.png}
  \caption{Minha figura}
  % Faltando \label{fig:...}
\end{figure}

\begin{table}[h]
  \centering
  \begin{tabular}{|c|c|}
    \hline
    A & B \\
    \hline
  \end{tabular}
  \caption{Minha tabela}
  % Faltando \label{tab:...}
\end{table}

\end{document}
```

**Avisos esperados:**
- ⚠️ Figura sem \label para referência
- ⚠️ Tabela sem \label para referência

---

## ✅ Exemplo 6: Referências e Citações Vazias

```latex
\documentclass{article}
\begin{document}

Veja a Figura \ref{} % Referência vazia

Segundo \cite{} % Citação vazia

\end{document}
```

**Erros esperados:**
- ❌ \ref vazio
- ❌ \cite vazio

---

## ✅ Exemplo 7: Formatação

```latex
\documentclass{article}
\begin{document}

Linha com espaços no final    

  Indentação inconsistente (1-3 espaços)

\end{document}
```

**Sugestões esperadas:**
- 💡 Espaços em branco no final da linha
- 💡 Indentação inconsistente (use 2 ou 4 espaços)

---

## 🎯 Teste Completo (Múltiplos Erros)

Cole este documento para testar vários erros ao mesmo tempo:

```latex
\documentclass{article}
\begin{document}

% Erro 1: $ não fechado
Equação inline: $ x + y = z

% Erro 2: eqnarray obsoleto
\begin{eqnarray}
  a + b = c
\end{eqnarray}

% Erro 3: $$ obsoleto
$$ E = mc^2 $$

% Erro 4: Pacote faltante
\includegraphics{imagem.png}

% Erro 5: Figura sem label
\begin{figure}[h]
  \caption{Minha figura}
\end{figure}

% Erro 6: Referência vazia
Veja a Figura \ref{}

% Erro 7: Espaço antes de \ref
Veja a Figura \ref{fig:teste}

% Erro 8: Aspas erradas
"Texto entre aspas"

% Erro 9: Fontes antigas
{\bf Negrito} e {\it Itálico}

% Erro 10: Chave não fechada
\textbf{texto sem fechar

\end{document}
```

**Resultado esperado:**
- ❌ 4-6 erros (severity: error)
- ⚠️ 4-6 avisos (severity: warning)
- 💡 2-3 sugestões (severity: suggestion)

---

## 🐛 Se o Linter Não Detectar Nada

1. **Verifique o console do navegador (F12)**:
   - Procure por erros JavaScript
   - Verifique se a requisição `/api/lint` foi feita

2. **Verifique os logs do servidor**:
   - Procure por erros Python
   - Verifique se o arquivo `lint_rules.json` foi encontrado

3. **Teste manualmente a API**:
   ```bash
   curl -X POST http://localhost:5000/api/lint \
     -H "Content-Type: application/json" \
     -d '{"content": "$ teste", "filename": "test.tex"}'
   ```

4. **Reinicie o servidor**:
   - Pare o servidor (Ctrl+C)
   - Inicie novamente: `python app.py`

---

## 📝 Notas

- O linter detecta **erros de sintaxe**, **comandos obsoletos**, **pacotes faltantes** e **boas práticas**
- Alguns erros podem ser **corrigidos automaticamente** (botão "Corrigir")
- Use o botão "Aplicar Todas as Correções" para corrigir todos os problemas de uma vez
- O linter **não substitui** o compilador LaTeX - ele apenas detecta problemas comuns

---

**Pronto para testar! 🚀**

Cole um dos exemplos acima no editor e clique no botão do Linter!






