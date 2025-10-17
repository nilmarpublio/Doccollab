# ✅ Checklist de Testes - Modal PDF

## 📋 Instruções

Marque cada item após testar. Use este checklist para garantir que tudo está funcionando perfeitamente.

---

## 🚀 Pré-requisitos

- [ ] Servidor Flask rodando (`python app.py`)
- [ ] Navegador aberto em `http://localhost:5000`
- [ ] LaTeX instalado no sistema (pdflatex)
- [ ] Conta criada e login efetuado

---

## 1️⃣ Teste Básico de Compilação

### Passos:
1. [ ] Acessar `http://localhost:5000/editor`
2. [ ] Escrever código LaTeX simples:
   ```latex
   \documentclass{article}
   \begin{document}
   Hello World!
   \end{document}
   ```
3. [ ] Clicar no botão "Compilar" (ou F5)
4. [ ] Aguardar 3-5 segundos

### Resultado Esperado:
- [ ] Notificação "Compilando..." aparece
- [ ] Notificação de sucesso aparece
- [ ] Modal abre automaticamente
- [ ] PDF é exibido no iframe
- [ ] Título do modal mostra nome do arquivo

**Status:** ⬜ Passou | ⬜ Falhou

---

## 2️⃣ Teste do Botão SALVAR (💾)

### Passos:
1. [ ] Com modal aberto, localizar botão verde "Salvar"
2. [ ] Passar mouse sobre o botão
3. [ ] Clicar no botão

### Resultado Esperado:
- [ ] Botão fica verde ao passar o mouse (#28a745)
- [ ] Botão sobe 2px ao hover
- [ ] Download do PDF inicia automaticamente
- [ ] Arquivo `.pdf` é salvo no computador
- [ ] Notificação "PDF baixado com sucesso!" aparece

**Status:** ⬜ Passou | ⬜ Falhou

---

## 3️⃣ Teste do Botão IMPRIMIR (🖨️)

### Passos:
1. [ ] Com modal aberto, localizar botão azul "Imprimir"
2. [ ] Passar mouse sobre o botão
3. [ ] Clicar no botão

### Resultado Esperado:
- [ ] Botão fica azul ao passar o mouse (#007bff)
- [ ] Botão sobe 2px ao hover
- [ ] Diálogo de impressão do navegador abre
- [ ] OU nova aba abre com PDF (fallback)

**Status:** ⬜ Passou | ⬜ Falhou

---

## 4️⃣ Teste do Botão VOLTAR (◀️)

### Passos:
1. [ ] Com modal aberto, localizar botão cinza "Voltar ao Editor"
2. [ ] Passar mouse sobre o botão
3. [ ] Clicar no botão

### Resultado Esperado:
- [ ] Botão fica cinza ao passar o mouse (#6c757d)
- [ ] Botão sobe 2px ao hover
- [ ] Modal fecha suavemente (animação fade out)
- [ ] Editor LaTeX permanece visível
- [ ] Documento não foi modificado
- [ ] Scroll permanece na mesma posição

**Status:** ⬜ Passou | ⬜ Falhou

---

## 5️⃣ Teste do Botão FECHAR (❌)

### Passos:
1. [ ] Com modal aberto, localizar botão circular X (canto direito)
2. [ ] Passar mouse sobre o botão
3. [ ] Clicar no botão

### Resultado Esperado:
- [ ] Botão fica vermelho ao passar o mouse (#dc3545)
- [ ] Botão gira 90° ao hover
- [ ] Modal fecha suavemente
- [ ] Editor LaTeX permanece visível
- [ ] Iframe é limpo após 300ms

**Status:** ⬜ Passou | ⬜ Falhou

---

## 6️⃣ Teste do Atalho ESC

### Passos:
1. [ ] Compilar documento (modal abre)
2. [ ] Pressionar tecla **ESC**

### Resultado Esperado:
- [ ] Modal fecha imediatamente
- [ ] Editor permanece no estado anterior
- [ ] Nenhum erro no console

**Status:** ⬜ Passou | ⬜ Falhou

---

## 7️⃣ Teste de Responsividade - Desktop

### Passos:
1. [ ] Abrir em navegador desktop (> 768px)
2. [ ] Compilar documento
3. [ ] Observar layout

### Resultado Esperado:
- [ ] Modal ocupa 90% da tela (max 1200px)
- [ ] Botões mostram ícones + texto
- [ ] Layout horizontal no header
- [ ] PDF preenche todo o corpo do modal
- [ ] Animações são suaves

**Status:** ⬜ Passou | ⬜ Falhou

---

## 8️⃣ Teste de Responsividade - Mobile

### Passos:
1. [ ] Redimensionar janela para < 768px (ou usar DevTools)
2. [ ] Compilar documento
3. [ ] Observar layout

### Resultado Esperado:
- [ ] Modal ocupa 95% da tela
- [ ] Botões mostram apenas ícones (sem texto)
- [ ] Layout vertical no header
- [ ] Botões são touch-friendly (min 40px)
- [ ] Scroll funciona corretamente

**Status:** ⬜ Passou | ⬜ Falhou

---

## 9️⃣ Teste de Animações

### Passos:
1. [ ] Compilar documento
2. [ ] Observar entrada do modal
3. [ ] Fechar modal
4. [ ] Observar saída do modal

### Resultado Esperado:
- [ ] Fade in suave (0.2s)
- [ ] Slide up suave (0.3s)
- [ ] Fade out ao fechar
- [ ] Sem travamentos
- [ ] 60 FPS consistente

**Status:** ⬜ Passou | ⬜ Falhou

---

## 🔟 Teste de Hover Effects

### Passos:
1. [ ] Abrir modal
2. [ ] Passar mouse sobre cada botão lentamente

### Resultado Esperado:

**Botão Salvar:**
- [ ] Cor muda para verde (#28a745)
- [ ] Eleva 2px
- [ ] Shadow aumenta
- [ ] Transição suave (0.3s)

**Botão Imprimir:**
- [ ] Cor muda para azul (#007bff)
- [ ] Eleva 2px
- [ ] Shadow aumenta
- [ ] Transição suave (0.3s)

**Botão Voltar:**
- [ ] Cor muda para cinza (#6c757d)
- [ ] Eleva 2px
- [ ] Shadow aumenta
- [ ] Transição suave (0.3s)

**Botão Fechar:**
- [ ] Cor muda para vermelho (#dc3545)
- [ ] Gira 90°
- [ ] Transição suave (0.3s)

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣1️⃣ Teste de Console (Erros)

### Passos:
1. [ ] Abrir DevTools (F12)
2. [ ] Ir para aba Console
3. [ ] Compilar documento
4. [ ] Testar todos os botões

### Resultado Esperado:
- [ ] Nenhum erro no console
- [ ] Nenhum warning crítico
- [ ] Logs de debug (se ativados) aparecem
- [ ] Sem exceções JavaScript

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣2️⃣ Teste de Performance

### Passos:
1. [ ] Abrir DevTools > Performance
2. [ ] Iniciar gravação
3. [ ] Compilar documento
4. [ ] Abrir modal
5. [ ] Fechar modal
6. [ ] Parar gravação

### Resultado Esperado:
- [ ] FPS consistente (55-60)
- [ ] Tempo de abertura < 300ms
- [ ] Tempo de fechamento < 300ms
- [ ] Sem memory leaks
- [ ] Sem long tasks (> 50ms)

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣3️⃣ Teste de Múltiplas Compilações

### Passos:
1. [ ] Compilar documento 1 vez
2. [ ] Fechar modal
3. [ ] Compilar novamente
4. [ ] Fechar modal
5. [ ] Repetir 5x

### Resultado Esperado:
- [ ] Modal abre/fecha corretamente todas as vezes
- [ ] PDF é atualizado a cada compilação
- [ ] Sem degradação de performance
- [ ] Memória não aumenta excessivamente

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣4️⃣ Teste de Overlay e Blur

### Passos:
1. [ ] Compilar documento
2. [ ] Observar fundo ao redor do modal

### Resultado Esperado:
- [ ] Fundo escuro (70% opacidade)
- [ ] Efeito blur visível
- [ ] Editor LaTeX visível (mas desfocado)
- [ ] Clicar no overlay fecha o modal

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣5️⃣ Teste de Diferentes Navegadores

### Chrome:
- [ ] Modal funciona
- [ ] Animações suaves
- [ ] Botões responsivos
- [ ] Download funciona
- [ ] Impressão funciona

### Firefox:
- [ ] Modal funciona
- [ ] Animações suaves
- [ ] Botões responsivos
- [ ] Download funciona
- [ ] Impressão funciona

### Edge:
- [ ] Modal funciona
- [ ] Animações suaves
- [ ] Botões responsivos
- [ ] Download funciona
- [ ] Impressão funciona

### Safari (se disponível):
- [ ] Modal funciona
- [ ] Animações suaves
- [ ] Botões responsivos
- [ ] Download funciona
- [ ] Impressão funciona

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣6️⃣ Teste de Documento Complexo

### Passos:
1. [ ] Criar documento LaTeX com:
   - Múltiplas seções
   - Imagens
   - Tabelas
   - Equações
   - Bibliografia
2. [ ] Compilar

### Resultado Esperado:
- [ ] PDF é gerado corretamente
- [ ] Modal exibe PDF completo
- [ ] Todas as páginas são visíveis
- [ ] Scroll funciona no iframe
- [ ] Download preserva formatação

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣7️⃣ Teste de Erro de Compilação

### Passos:
1. [ ] Escrever LaTeX com erro intencional:
   ```latex
   \documentclass{article}
   \begin{document}
   Teste \textbf{sem fechar
   \end{document}
   ```
2. [ ] Tentar compilar

### Resultado Esperado:
- [ ] Notificação de erro aparece
- [ ] Modal NÃO abre
- [ ] Mensagem de erro é clara
- [ ] Editor permanece editável

**Status:** ⬜ Passou | ⬜ Falhou

---

## 1️⃣8️⃣ Teste de Acessibilidade

### Passos:
1. [ ] Usar apenas teclado (sem mouse)
2. [ ] Compilar com Enter
3. [ ] Navegar pelos botões com Tab
4. [ ] Ativar botões com Enter/Space
5. [ ] Fechar com ESC

### Resultado Esperado:
- [ ] Todos os botões são acessíveis via Tab
- [ ] Ordem de foco é lógica
- [ ] Enter/Space ativam botões
- [ ] ESC fecha modal
- [ ] Visual de foco é visível

**Status:** ⬜ Passou | ⬜ Falhou

---

## 🎯 Demo Interativa

### Passos:
1. [ ] Acessar `http://localhost:5000/static/demo_modal.html`
2. [ ] Clicar em "Ver Demonstração"
3. [ ] Testar todos os botões

### Resultado Esperado:
- [ ] Modal abre
- [ ] Botões mudam de cor ao hover
- [ ] Alerts aparecem ao clicar botões
- [ ] Modal fecha com X ou ESC
- [ ] Design é idêntico ao modal real

**Status:** ⬜ Passou | ⬜ Falhou

---

## 📊 Resumo dos Testes

```
┌────────────────────────────────────────────┐
│  Total de Testes: 19                       │
├────────────────────────────────────────────┤
│  ✅ Passaram: ___ / 19                     │
│  ❌ Falharam: ___ / 19                     │
│  ⏭️ Pulados: ___ / 19                      │
├────────────────────────────────────────────┤
│  Taxa de Sucesso: ____%                    │
└────────────────────────────────────────────┘
```

---

## 🐛 Registro de Bugs (se houver)

### Bug #1:
- **Descrição:**
- **Passos para reproduzir:**
- **Resultado esperado:**
- **Resultado obtido:**
- **Severidade:** ⬜ Crítico | ⬜ Alto | ⬜ Médio | ⬜ Baixo

### Bug #2:
- **Descrição:**
- **Passos para reproduzir:**
- **Resultado esperado:**
- **Resultado obtido:**
- **Severidade:** ⬜ Crítico | ⬜ Alto | ⬜ Médio | ⬜ Baixo

---

## ✅ Aprovação Final

- [ ] **TODOS os testes passaram**
- [ ] **Nenhum bug crítico encontrado**
- [ ] **Performance aceitável**
- [ ] **Design conforme especificação**
- [ ] **Documentação completa**

---

## 🎉 Conclusão

Data do teste: ___/___/2025  
Testado por: ______________  
Navegador principal: ______________  
Sistema operacional: ______________  

**Status Final:**
- ⬜ ✅ **APROVADO** - Pronto para produção
- ⬜ ⚠️ **APROVADO COM RESSALVAS** - Pequenos ajustes necessários
- ⬜ ❌ **REPROVADO** - Requer correções significativas

---

**Assinatura:** _______________________  
**Data:** ___/___/2025

---

## 📝 Notas Adicionais

(Espaço para observações, sugestões ou comentários)

```
_____________________________________________________________

_____________________________________________________________

_____________________________________________________________

_____________________________________________________________
```

---

**Desenvolvido com ❤️ para DocCollab**  
*Checklist v1.0 - Outubro 2025*

