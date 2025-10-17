# 📝 **LaTeX Snippets - Catálogo Completo**

## 📋 **10 Snippets Prontos para Uso**

Todos os snippets estão prontos para inserção no editor LaTeX através do assistente virtual.

---

## 📊 **01. Tabela** (`01_table.tex`)

**Categoria**: Tables  
**Descrição**: Tabela formatada com caption e label

```latex
\begin{table}[htbp]
    \centering
    \caption{Título da Tabela}
    \label{tab:exemplo}
    \begin{tabular}{|l|c|r|}
        \hline
        \textbf{Coluna 1} & \textbf{Coluna 2} & \textbf{Coluna 3} \\
        \hline
        Linha 1 & Dados A & 123 \\
        Linha 2 & Dados B & 456 \\
        Linha 3 & Dados C & 789 \\
        \hline
    \end{tabular}
\end{table}
```

**Uso**: Inserir tabelas com bordas e alinhamento personalizado

---

## 🖼️ **02. Figura** (`02_figure.tex`)

**Categoria**: Figures  
**Descrição**: Figura com imagem, caption e label

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{imagem.png}
    \caption{Descrição da figura}
    \label{fig:exemplo}
\end{figure}
```

**Uso**: Inserir imagens com legendas  
**Requer**: `\usepackage{graphicx}`

---

## ➗ **03. Equações Alinhadas** (`03_align_equations.tex`)

**Categoria**: Math  
**Descrição**: Ambiente align para equações alinhadas (moderno, substitui eqnarray)

```latex
\begin{align}
    f(x) &= x^2 + 2x + 1 \label{eq:quadratica} \\
    g(x) &= \sin(x) + \cos(x) \label{eq:trigonometrica} \\
    h(x) &= e^x + \ln(x) \label{eq:exponencial}
\end{align}
```

**Uso**: Alinhar múltiplas equações  
**Requer**: `\usepackage{amsmath}`

---

## 📚 **04. Template BibTeX** (`04_bibtex_template.tex`)

**Categoria**: Bibliography  
**Descrição**: Exemplo de uso de citações com BibTeX

```latex
% No preâmbulo, adicione:
% \usepackage{natbib}
% \bibliographystyle{plain}

% No texto:
Segundo \citet{Goodfellow2016}, o deep learning revolucionou a IA.
Estudos recentes \citep{Smith2023, Jones2024} confirmam essa tendência.

% No final do documento:
\bibliography{references}
```

**Uso**: Inserir citações bibliográficas  
**Requer**: `\usepackage{natbib}`

---

## 🔢 **05. Lista Enumerada** (`05_enumerate.tex`)

**Categoria**: Lists  
**Descrição**: Lista numerada com itens

```latex
\begin{enumerate}
    \item Primeiro item da lista
    \item Segundo item com subitens:
    \begin{enumerate}
        \item Subitem 2.1
        \item Subitem 2.2
    \end{enumerate}
    \item Terceiro item
    \item Quarto item
\end{enumerate}
```

**Uso**: Criar listas ordenadas com subitens

---

## 📌 **06. Nota de Rodapé** (`06_footnote.tex`)

**Categoria**: Text  
**Descrição**: Adiciona nota de rodapé ao texto

```latex
Este é um texto com uma nota de rodapé\footnote{Esta é a nota de rodapé explicativa.}.

% Para múltiplas notas:
Texto com primeira nota\footnote{Primeira nota.} e segunda nota\footnote{Segunda nota.}.
```

**Uso**: Adicionar notas explicativas no rodapé

---

## 🎓 **07. Teorema e Demonstração** (`07_theorem_proof.tex`)

**Categoria**: Math  
**Descrição**: Ambiente para teoremas e provas matemáticas

```latex
% No preâmbulo, adicione:
% \usepackage{amsthm}
% \newtheorem{theorem}{Teorema}

\begin{theorem}[Pitágoras]
\label{thm:pitagoras}
Em um triângulo retângulo, o quadrado da hipotenusa é igual à soma dos quadrados dos catetos.
\end{theorem}

\begin{proof}
Seja $c$ a hipotenusa e $a, b$ os catetos. Então:
\begin{equation}
    c^2 = a^2 + b^2
\end{equation}
\end{proof}
```

**Uso**: Apresentar teoremas matemáticos com demonstrações  
**Requer**: `\usepackage{amsthm}`

---

## 💻 **08. Algoritmo** (`08_algorithm.tex`)

**Categoria**: Algorithms  
**Descrição**: Ambiente para pseudocódigo de algoritmos

```latex
% No preâmbulo, adicione:
% \usepackage{algorithm}
% \usepackage{algpseudocode}

\begin{algorithm}
\caption{Algoritmo de Exemplo}
\label{alg:exemplo}
\begin{algorithmic}[1]
\Procedure{BuscaBinaria}{$A, n, x$}
    \State $low \gets 0$
    \State $high \gets n - 1$
    \While{$low \leq high$}
        \State $mid \gets \lfloor (low + high) / 2 \rfloor$
        \If{$A[mid] = x$}
            \State \Return $mid$
        \ElsIf{$A[mid] < x$}
            \State $low \gets mid + 1$
        \Else
            \State $high \gets mid - 1$
        \EndIf
    \EndWhile
    \State \Return $-1$
\EndProcedure
\end{algorithmic}
\end{algorithm}
```

**Uso**: Apresentar algoritmos em pseudocódigo  
**Requer**: `\usepackage{algorithm}`, `\usepackage{algpseudocode}`

---

## 🔢 **09. Matriz** (`09_matrix.tex`)

**Categoria**: Math  
**Descrição**: Diferentes tipos de matrizes em LaTeX

```latex
% Matriz com parênteses
\begin{equation}
A = \begin{pmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{pmatrix}
\end{equation}

% Matriz com colchetes
\begin{equation}
B = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
\end{equation}

% Determinante (barras)
\begin{equation}
\det(C) = \begin{vmatrix}
c_{11} & c_{12} \\
c_{21} & c_{22}
\end{vmatrix}
\end{equation}
```

**Uso**: Apresentar matrizes matemáticas  
**Requer**: `\usepackage{amsmath}`

---

## 🖼️ **10. Subfiguras** (`10_subfigure.tex`)

**Categoria**: Figures  
**Descrição**: Múltiplas figuras lado a lado com legendas individuais

```latex
% No preâmbulo, adicione:
% \usepackage{subcaption}

\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{imagem1.png}
        \caption{Primeira subfigura}
        \label{fig:sub1}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{imagem2.png}
        \caption{Segunda subfigura}
        \label{fig:sub2}
    \end{subfigure}
    \caption{Comparação entre duas imagens}
    \label{fig:comparacao}
\end{figure}
```

**Uso**: Comparar múltiplas imagens lado a lado  
**Requer**: `\usepackage{subcaption}`

---

## 📊 **Resumo por Categoria**

| Categoria | Snippets | IDs |
|-----------|----------|-----|
| **Tables** | 1 | 01 |
| **Figures** | 2 | 02, 10 |
| **Math** | 3 | 03, 07, 09 |
| **Bibliography** | 1 | 04 |
| **Lists** | 1 | 05 |
| **Text** | 1 | 06 |
| **Algorithms** | 1 | 08 |

---

## 🚀 **Como Usar**

### **Via Assistente Virtual**

```javascript
// No editor, abra o painel do assistente e digite:
"Inserir snippet de tabela"
// ou
"Adicionar figura"
// ou
"Criar equações alinhadas"
```

### **Via API REST**

```http
GET /api/snippets?category=Math
```

```javascript
// Resposta:
{
  "success": true,
  "snippets": [
    {
      "id": "03_align_equations",
      "name": "Equações Alinhadas",
      "category": "Math",
      "content": "\\begin{align}\n..."
    }
  ]
}
```

### **Via Socket.IO**

```javascript
socket.emit('assistant_action', {
  action_id: '123-abc',
  action_type: 'insert_snippet',
  state: 'applied_local',
  payload: {
    snippet_id: '03_align_equations'
  }
});
```

---

## 📝 **Customização**

Todos os snippets podem ser customizados:

1. Edite os arquivos `.tex` em `assistant/snippets/`
2. Adicione novos snippets seguindo o padrão:
   - `NN_nome.tex` (NN = número sequencial)
   - Comentário com categoria e descrição
3. O assistente detecta automaticamente novos snippets

---

## 🤝 **Contribuindo**

Para adicionar novos snippets:

1. Crie arquivo `.tex` em `assistant/snippets/`
2. Siga o formato:
```latex
% Snippet: Nome do Snippet
% Categoria: Nome da Categoria
% Descrição: Descrição breve

[Código LaTeX aqui]
```
3. Teste com o assistente
4. Documente neste README

---

**Total de Snippets**: 10  
**Última Atualização**: 2025-10-07  
**Status**: ✅ Completo







