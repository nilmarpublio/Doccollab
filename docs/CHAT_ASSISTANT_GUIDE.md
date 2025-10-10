# 💬 **Guia do Assistente de Chat**

## 🤖 **Como Funciona**

O assistente de chat agora responde de forma **inteligente** usando o sistema `llm_client` com 3 modos:

1. **Offline (padrão)**: Respostas baseadas em regras, 100% local
2. **Hybrid**: Regras para casos simples + LLM para casos complexos
3. **LLM Only**: Apenas LLM externo (OpenAI/Anthropic)

---

## 🇧🇷 **RESPOSTAS EM PORTUGUÊS**

### **Saudações**
```
Você: olá
Bot: Olá! Como posso ajudar com seu documento LaTeX?

Você: oi
Bot: Olá! Como posso ajudar com seu documento LaTeX?
```

### **Ajuda**
```
Você: ajuda
Bot: Posso ajudar com:
- Inserir snippets
- Compilar documento
- Verificar erros (lint)
- Gerar BibTeX
- Aplicar refatorações

Você: o que você pode fazer?
Bot: Posso ajudar com:
- Inserir snippets
- Compilar documento
- Verificar erros (lint)
- Gerar BibTeX
- Aplicar refatorações
```

### **Compilação**
```
Você: como compilar?
Bot: Para compilar, use o botão "Compilar" ou envie o comando "compilar"

Você: compilar
Bot: Para compilar, use o botão "Compilar" ou envie o comando "compilar"
```

### **BibTeX**
```
Você: como gerar bibtex?
Bot: Para gerar BibTeX, use: "gerar bibtex para [descrição]"

Você: citação
Bot: Para gerar BibTeX, use: "gerar bibtex para [descrição]"

Você: referência
Bot: Para gerar BibTeX, use: "gerar bibtex para [descrição]"
```

### **Lint**
```
Você: como verificar erros?
Bot: Para verificar erros, use o botão "Lint" no painel lateral

Você: lint
Bot: Para verificar erros, use o botão "Lint" no painel lateral

Você: erros
Bot: Para verificar erros, use o botão "Lint" no painel lateral
```

### **Mensagens Desconhecidas**
```
Você: xyzabc123
Bot: Desculpe, não entendi. Digite "ajuda" para ver o que posso fazer.
```

---

## 🇺🇸 **ENGLISH RESPONSES**

### **Greetings**
```
You: hello
Bot: Hello! How can I help with your LaTeX document?

You: hi
Bot: Hello! How can I help with your LaTeX document?
```

### **Help**
```
You: help
Bot: I can help with:
- Insert snippets
- Compile document
- Check errors (lint)
- Generate BibTeX
- Apply refactoring

You: what can you do?
Bot: I can help with:
- Insert snippets
- Compile document
- Check errors (lint)
- Generate BibTeX
- Apply refactoring
```

### **Compilation**
```
You: how to compile?
Bot: To compile, use the "Compile" button or send the "compile" command

You: compile
Bot: To compile, use the "Compile" button or send the "compile" command
```

### **BibTeX**
```
You: how to generate bibtex?
Bot: To generate BibTeX, use: "generate bibtex for [description]"

You: citation
Bot: To generate BibTeX, use: "generate bibtex for [description]"
```

### **Lint**
```
You: how to check errors?
Bot: To check errors, use the "Lint" button in the side panel

You: lint
Bot: To check errors, use the "Lint" button in the side panel

You: check
Bot: To check errors, use the "Lint" button in the side panel
```

### **Unknown Messages**
```
You: asdfghjkl
Bot: Sorry, I didn't understand. Type "help" to see what I can do.
```

---

## 🇪🇸 **RESPUESTAS EN ESPAÑOL**

### **Saludos**
```
Tú: hola
Bot: ¡Hola! ¿Cómo puedo ayudar con su documento LaTeX?
```

### **Ayuda**
```
Tú: ayuda
Bot: Puedo ayudar con:
- Insertar snippets
- Compilar documento
- Verificar errores (lint)
- Generar BibTeX
- Aplicar refactorizaciones
```

### **Compilación**
```
Tú: cómo compilar?
Bot: Para compilar, use el botón "Compilar" o envíe el comando "compilar"

Tú: compilar
Bot: Para compilar, use el botón "Compilar" o envíe el comando "compilar"
```

### **BibTeX**
```
Tú: cómo generar bibtex?
Bot: Para generar BibTeX, use: "generar bibtex para [descripción]"
```

### **Lint**
```
Tú: cómo verificar errores?
Bot: Para verificar errores, use el botón "Lint" en el panel lateral

Tú: verificar
Bot: Para verificar errores, use el botón "Lint" en el panel lateral
```

---

## 🔄 **COMO MUDAR O IDIOMA**

### **Via Interface**
1. Clique no seletor de idioma na navbar
2. Escolha: Português / English / Español

### **Via Chat**
O assistente detecta automaticamente o idioma da sua mensagem!

```
# Português
Você: olá
Bot: (responde em português)

# English
You: hello
Bot: (responds in english)

# Español
Tú: hola
Bot: (responde en español)
```

---

## 🧠 **PALAVRAS-CHAVE RECONHECIDAS**

### **Português**
- **Saudações**: olá, oi, bom dia, boa tarde
- **Ajuda**: ajuda, help, o que pode fazer
- **Compilar**: compilar, compile, compilação
- **BibTeX**: bibtex, citação, citation, referência, bibliografia
- **Lint**: lint, erros, errors, verificar, check

### **English**
- **Greetings**: hello, hi, good morning, good afternoon
- **Help**: help, what can you do, commands
- **Compile**: compile, compilation, build
- **BibTeX**: bibtex, citation, reference, bibliography
- **Lint**: lint, errors, check, verify

### **Español**
- **Saludos**: hola, buenos días, buenas tardes
- **Ayuda**: ayuda, help, qué puedes hacer
- **Compilar**: compilar, compilación
- **BibTeX**: bibtex, citación, referencia, bibliografía
- **Lint**: lint, errores, verificar

---

## 📊 **CONFIANÇA DAS RESPOSTAS**

O assistente retorna um `confidence score` para cada resposta:

| Tipo de Mensagem | Confidence | Descrição |
|------------------|-----------|-----------|
| Saudação exata | 1.0 | 100% de certeza |
| Comando conhecido | 0.9 | 90% de certeza |
| Mensagem desconhecida | 0.3 | 30% de certeza |

No modo **Hybrid**, se `confidence < 0.7`, o sistema pode usar o LLM externo (se configurado).

---

## ⚙️ **HABILITAR LLM EXTERNO**

Para respostas mais naturais e contextuais, configure um LLM:

### **1. OpenAI (GPT-4)**
```ini
# .env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_MODE=hybrid
```

### **2. Anthropic (Claude)**
```ini
# .env
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-your-key-here
LLM_MODE=hybrid
```

### **3. Local (Llama, etc.)**
```ini
# .env
LLM_PROVIDER=local
LLM_MODEL_PATH=/path/to/model.gguf
LLM_MODE=hybrid
```

📖 **Guia completo**: [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md)

---

## 🎯 **AÇÕES SUGERIDAS**

O assistente pode sugerir **ações** que você pode executar:

```json
{
  "content": "Para compilar, use o botão 'Compilar'",
  "actions": [
    {
      "type": "suggest_compile",
      "label": "Compilar Agora",
      "icon": "▶"
    }
  ]
}
```

**Tipos de ações**:
- `suggest_compile` - Sugerir compilação
- `suggest_lint` - Sugerir verificação
- `suggest_bibtex` - Sugerir geração BibTeX

---

## 🔍 **EXEMPLOS DE CONVERSAS**

### **Exemplo 1: Primeira vez**
```
Você: olá, sou novo aqui
Bot: Olá! Como posso ajudar com seu documento LaTeX?

Você: o que você faz?
Bot: Posso ajudar com:
- Inserir snippets
- Compilar documento
- Verificar erros (lint)
- Gerar BibTeX
- Aplicar refatorações

Você: como compilo meu documento?
Bot: Para compilar, use o botão "Compilar" ou envie o comando "compilar"
```

### **Exemplo 2: Workflow completo**
```
Você: olá
Bot: Olá! Como posso ajudar com seu documento LaTeX?

Você: preciso adicionar uma referência
Bot: Para gerar BibTeX, use: "gerar bibtex para [descrição]"

Você: como verifico se tem erros?
Bot: Para verificar erros, use o botão "Lint" no painel lateral

Você: e depois compilo?
Bot: Para compilar, use o botão "Compilar" ou envie o comando "compilar"
```

### **Exemplo 3: Multilíngue**
```
You: hello
Bot: Hello! How can I help with your LaTeX document?

Você: mudei para português
Bot: (continua em português) Olá! Como posso ajudar com seu documento LaTeX?

Tú: ahora en español
Bot: (continua em español) ¡Hola! ¿Cómo puedo ayudar con su documento LaTeX?
```

---

## 🐛 **TROUBLESHOOTING**

### **Bot não responde**
1. Verifique se está conectado (ícone de status)
2. Recarregue a página (F5)
3. Verifique o console do navegador (F12)

### **Bot responde em inglês mas quero português**
1. Mude o idioma na navbar
2. Ou use palavras em português na mensagem

### **Bot diz "não entendi" sempre**
- Verifique se está usando palavras-chave reconhecidas
- Tente mensagens mais diretas: "ajuda", "compilar", etc.

### **Quero respostas mais naturais**
Configure um LLM externo (veja seção "Habilitar LLM Externo")

---

## 📞 **SUPORTE**

Se o assistente não estiver funcionando como esperado:

1. Verifique logs: `logs/audit_*.jsonl`
2. Teste com: `python verify_installation.py`
3. Reporte issues: [GitHub Issues](https://github.com/your-org/doccollab/issues)

---

**Última atualização**: 2025-10-07  
**Versão**: 1.0.0  
**Status**: ✅ **Funcional com respostas inteligentes!**



