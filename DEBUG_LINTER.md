# 🔍 Debug do Linter - Guia de Correção

## 🎯 Correções Implementadas

### ✅ Problemas Corrigidos:

1. **Sincronização de Scroll**
   - Números de linha agora acompanham o scroll
   - Marcadores de erro acompanham o scroll
   - Atualização automática ao rolar o texto

2. **Validação de Números de Linha**
   - Verifica se linha existe antes de criar marcador
   - Oculta marcadores de linhas inválidas
   - Logs de debug no console

3. **Cálculo Preciso de Posição**
   - Considera `lineHeight` real do CSS
   - Considera `paddingTop` do editor
   - Considera `scrollTop` atual
   - Fallback inteligente se `lineHeight` for 'normal'

---

## 🧪 Como Testar com Logs de Debug

### 1️⃣ **Abrir Console do Navegador**

**Chrome/Edge:**
- Pressione `F12`
- Ou `Ctrl + Shift + I`
- Vá para a aba "Console"

**Firefox:**
- Pressione `F12`
- Ou `Ctrl + Shift + K`
- Vá para a aba "Console"

### 2️⃣ **Escrever LaTeX com Erro**

Cole este código no editor:
```latex
\documentclass{article}
\begin{document}

Linha 4 OK
Linha 5 OK  
Linha 6 tem erro \textbf{sem fechar
Linha 7 OK
Linha 8 OK

\end{document}
```

### 3️⃣ **Aguardar 2 Segundos**

O linter roda automaticamente após você parar de digitar.

### 4️⃣ **Verificar Logs no Console**

Você verá algo assim:
```
[Linter] Processando resultados: {errors: 1, warnings: 0, totalLines: 10}
[Linter] Erro na linha 6: \textbf{ não foi fechado corretamente
[Linter] Criando marcador para linha 6
[Linter] Linha 6: top=120px (lineHeight=24px, scroll=0px, padding=10px)
[Linter] Total: 1 erros, 0 avisos
```

### 5️⃣ **Verificar se Linha Está Correta**

Compare:
- **No Log:** `Erro na linha 6`
- **No Editor:** A linha 6 deve ter o marcador vermelho
- **Números de Linha:** Devem mostrar "6" ao lado esquerdo

---

## 🐛 Troubleshooting

### Problema 1: Marcador em Linha Errada

**Sintoma:**
- Linter diz "linha 20"
- Marcador aparece na linha 22

**Solução:**
Verifique no console:
```javascript
[Linter] Erro na linha 20: mensagem do erro
[Linter] Criando marcador para linha 20
[Linter] Linha 20: top=XXXpx (lineHeight=XXpx, scroll=XXpx, padding=XXpx)
```

Se o cálculo estiver correto, o problema pode ser:
1. **Backend retornando linha errada** - O linter do Python pode estar contando errado
2. **Linhas vazias no início** - Podem desalinhar a contagem

**Como fixar:**
```javascript
// No console, execute:
const editor = document.getElementById('latexEditor');
const lines = editor.value.split('\n');
console.log('Total de linhas:', lines.length);
lines.forEach((line, idx) => {
  console.log(`Linha ${idx + 1}: "${line}"`);
});
```

### Problema 2: Marcador Não Acompanha Scroll

**Sintoma:**
- Marcador fica fixo ao rolar

**Solução:**
1. Recarregue a página (F5)
2. Verifique no console se há erros JavaScript
3. Teste rolar lentamente e observar se logs aparecem:
   ```
   [Linter] Linha X: top=YYYpx ...
   ```

### Problema 3: Números de Linha Descasados

**Sintoma:**
- Documento tem 71 linhas
- Números de linha mostram só 60

**Diagnóstico:**
No console, execute:
```javascript
const editor = document.getElementById('latexEditor');
const lineNumbers = document.getElementById('lineNumbers');

console.log('Linhas no editor:', editor.value.split('\n').length);
console.log('Divs de números:', lineNumbers.querySelectorAll('.line-number').length);
```

**Deve mostrar o mesmo número!**

Se não mostrar:
```javascript
// Forçar atualização
window.latexEditor.updateLineNumbers();
```

---

## 🔧 Comandos Úteis no Console

### Ver Estado Atual do Linter:
```javascript
console.log('Linter UI:', window.linterUI);
console.log('Marcadores ativos:', window.linterUI?.lintMarkers.length);
```

### Forçar Atualização de Marcadores:
```javascript
window.linterUI?.updateAllMarkerPositions();
```

### Ver Linhas do Documento:
```javascript
const editor = document.getElementById('latexEditor');
editor.value.split('\n').forEach((line, idx) => {
  console.log(`${idx + 1}: ${line}`);
});
```

### Limpar Todos os Marcadores:
```javascript
window.linterUI?.clearMarkers();
```

### Executar Lint Manualmente:
```javascript
window.linterUI?.runLint();
```

---

## 📊 Informações Técnicas

### Estrutura de Marcador:
```javascript
{
  marker: <div>,      // Fundo colorido
  icon: <div>,        // Ícone ⚠️
  lineNum: 6          // Número da linha (1-based)
}
```

### Cálculo de Posição:
```javascript
top = paddingTop + (lineNum - 1) * lineHeight - scrollTop
```

Onde:
- `paddingTop`: Espaçamento superior do editor (px)
- `lineNum - 1`: Converte 1-based para 0-based
- `lineHeight`: Altura de cada linha (px)
- `scrollTop`: Quanto o editor foi rolado (px)

---

## 📝 Checklist de Verificação

Após recarregar a página, teste:

- [ ] Escrever LaTeX com erro
- [ ] Aguardar 2 segundos
- [ ] Marcador vermelho aparece
- [ ] Marcador está na linha correta
- [ ] Rolar o editor para cima
- [ ] Marcador acompanha a linha
- [ ] Rolar o editor para baixo
- [ ] Marcador continua acompanhando
- [ ] Passar mouse sobre ⚠️
- [ ] Tooltip mostra mensagem de erro
- [ ] Números de linha sincronizados

---

## 🎯 Se Ainda Não Funcionar

Execute no console:
```javascript
// 1. Ver configuração do editor
const editor = document.getElementById('latexEditor');
const style = getComputedStyle(editor);
console.log({
  lineHeight: style.lineHeight,
  fontSize: style.fontSize,
  paddingTop: style.paddingTop,
  scrollTop: editor.scrollTop
});

// 2. Ver marcadores atuais
console.log('Marcadores:', window.linterUI?.lintMarkers);

// 3. Forçar recálculo
window.linterUI?.lintMarkers.forEach(item => {
  if (item.lineNum) {
    console.log(`Marcador linha ${item.lineNum}`);
    window.linterUI.updateMarkerPosition(item.marker, item.icon, item.lineNum);
  }
});
```

---

## 📞 Relatando Bugs

Se encontrar um bug, inclua:

1. **Console logs** (copiar e colar)
2. **Número da linha que o linter reportou**
3. **Número da linha onde o marcador apareceu**
4. **Total de linhas do documento**
5. **Screenshot (se possível)**

---

**Última atualização:** Outubro 2025  
**Versão:** 2.0 - Com logs de debug

