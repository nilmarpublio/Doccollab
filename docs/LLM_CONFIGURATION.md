# 🤖 Configuração do LLM (Large Language Model)

## 📋 **Visão Geral**

O **DocCollab Assistant** pode operar em três modos:

1. **🔌 OFFLINE** (padrão): 100% baseado em regras, sem dependências externas
2. **🔀 HYBRID**: Combina regras + LLM para casos complexos
3. **🌐 LLM_ONLY**: Usa apenas LLM externo

---

## 🚀 **Modo OFFLINE (Padrão)**

**Sem configuração necessária!** O sistema funciona completamente offline com:

- ✅ Detecção de intenções por palavras-chave
- ✅ Sugestões baseadas em regras
- ✅ Suporte completo a PT/EN/ES
- ✅ Zero custos de API
- ✅ Zero latência de rede
- ✅ 100% privado

### Funcionalidades Disponíveis

```python
# Comandos reconhecidos automaticamente:
- "olá" / "hello" / "hola" → Saudação
- "ajuda" / "help" / "ayuda" → Lista de funcionalidades
- "compilar" / "compile" → Sugestão de compilação
- "bibtex" / "citação" → Sugestão de geração BibTeX
- "lint" / "erros" / "verificar" → Sugestão de lint
```

---

## 🌐 **Habilitar LLM Externo**

### **1. Configurar Variáveis de Ambiente**

#### **Windows (PowerShell)**
```powershell
$env:LLM_PROVIDER = "openai"
$env:LLM_API_KEY = "sk-..."
$env:LLM_MODE = "hybrid"  # ou "llm_only"
```

#### **Linux/macOS (Bash)**
```bash
export LLM_PROVIDER=openai
export LLM_API_KEY=sk-...
export LLM_MODE=hybrid  # ou llm_only
```

#### **Arquivo `.env`** (recomendado)
```ini
# .env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key-here
LLM_MODE=hybrid

# Opcional
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
```

### **2. Provedores Suportados**

| Provedor | Valor `LLM_PROVIDER` | Requer API Key |
|----------|---------------------|----------------|
| **OpenAI** | `openai` | Sim (`sk-...`) |
| **Anthropic** | `anthropic` | Sim (`sk-ant-...`) |
| **Cohere** | `cohere` | Sim |
| **Local** | `local` | Não (Llama, etc.) |
| **Offline** | `none` | Não (padrão) |

### **3. Modos de Operação**

#### **🔌 OFFLINE** (`LLM_MODE=offline`)
```
Usuário → Regras → Resposta
```
- Sem custos
- Sem latência de rede
- Respostas instantâneas
- Funcionalidade limitada

#### **🔀 HYBRID** (`LLM_MODE=hybrid`) ⭐ **Recomendado**
```
Usuário → Regras (confiança < 70%) → LLM → Resposta
         ↓ (confiança ≥ 70%)
         Resposta
```
- Melhor custo-benefício
- Usa regras para casos simples
- LLM apenas para casos complexos
- Fallback automático

#### **🌐 LLM_ONLY** (`LLM_MODE=llm_only`)
```
Usuário → LLM → Resposta
```
- Respostas mais naturais
- Maior custo
- Requer conexão
- Sem fallback

---

## 🔧 **Implementação de Provedores**

### **OpenAI (GPT-4)**

1. **Instalar dependência:**
```bash
pip install openai
```

2. **Configurar `.env`:**
```ini
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4
```

3. **Implementar em `llm_client.py`:**
```python
if self.provider == LLMProvider.OPENAI:
    import openai
    openai.api_key = self.api_key
    
    response = openai.ChatCompletion.create(
        model=os.getenv('LLM_MODEL', 'gpt-4'),
        messages=[
            {
                "role": "system", 
                "content": f"You are a LaTeX assistant. Respond in {language}."
            },
            {
                "role": "user", 
                "content": user_message
            }
        ],
        temperature=float(os.getenv('LLM_TEMPERATURE', 0.7)),
        max_tokens=int(os.getenv('LLM_MAX_TOKENS', 500))
    )
    
    return {
        'text': response.choices[0].message.content,
        'actions': self._parse_actions(response),
        'source': 'llm',
        'confidence': 1.0
    }
```

### **Anthropic (Claude)**

1. **Instalar:**
```bash
pip install anthropic
```

2. **Configurar `.env`:**
```ini
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-...
LLM_MODEL=claude-3-opus-20240229
```

### **Modelos Locais (Llama, etc.)**

1. **Instalar:**
```bash
pip install llama-cpp-python
```

2. **Configurar `.env`:**
```ini
LLM_PROVIDER=local
LLM_MODEL_PATH=/path/to/model.gguf
```

---

## 📊 **Monitoramento**

### **Verificar Status do LLM**

```python
from services.llm_client import get_llm_client

client = get_llm_client()

print(f"Provider: {client.provider}")
print(f"Mode: {client.mode}")
print(f"Enabled: {client.is_enabled()}")
```

### **Logs de Uso**

Todos os usos do LLM são registrados em `logs/audit_YYYY-MM-DD.jsonl`:

```json
{
  "timestamp": "2025-10-07T12:34:56Z",
  "event_type": "assistant_message",
  "user_id": 1,
  "action": "LLM response",
  "details": {
    "provider": "openai",
    "mode": "hybrid",
    "tokens_used": 150
  }
}
```

---

## 🔒 **Segurança**

### **Boas Práticas**

1. ✅ **Nunca** commitar `.env` com API keys
2. ✅ Usar variáveis de ambiente em produção
3. ✅ Rotacionar API keys periodicamente
4. ✅ Monitorar custos de uso
5. ✅ Configurar rate limiting

### **Arquivo `.gitignore`**
```gitignore
.env
*.env
.env.local
logs/
```

### **Limites Recomendados**

```ini
# .env
LLM_MAX_TOKENS=500  # Evitar respostas muito longas
LLM_TEMPERATURE=0.7  # Equilíbrio entre criatividade e precisão
LLM_RATE_LIMIT=10  # Máximo 10 requisições/minuto
```

---

## 🧪 **Testes**

### **Testar Modo Offline**
```bash
# Sem variáveis de ambiente
python -c "from services.llm_client import get_llm_client; print(get_llm_client().mode)"
# Output: LLMMode.OFFLINE
```

### **Testar com LLM**
```bash
export LLM_API_KEY=sk-test
export LLM_PROVIDER=openai
python -c "from services.llm_client import get_llm_client; print(get_llm_client().is_enabled())"
# Output: True
```

### **Testar Resposta**
```python
from services.llm_client import get_llm_client

client = get_llm_client()
response = client.generate_response(
    "Como compilar meu documento?",
    language='pt'
)
print(response['text'])
```

---

## 📈 **Custos Estimados**

### **OpenAI GPT-4**
- **Input**: $0.03 / 1K tokens
- **Output**: $0.06 / 1K tokens
- **Média/resposta**: ~300 tokens = **$0.015**

### **Modo Hybrid (Recomendado)**
- **Regras**: 90% das requisições (grátis)
- **LLM**: 10% das requisições
- **Custo mensal** (1000 msgs): ~$1.50

### **Modo Offline**
- **Custo**: $0 💰
- **100% gratuito**

---

## ❓ **FAQ**

### **P: O que acontece se a API cair?**
**R:** No modo `hybrid`, o sistema automaticamente volta para regras. No modo `llm_only`, retorna erro.

### **P: Posso usar múltiplos provedores?**
**R:** Atualmente não, mas você pode alternar mudando `LLM_PROVIDER`.

### **P: Como desabilitar completamente o LLM?**
**R:** Remova ou comente `LLM_API_KEY` no `.env`. O sistema volta automaticamente para OFFLINE.

### **P: O modo offline é suficiente?**
**R:** Sim! Para 90% dos casos, as regras são suficientes e mais rápidas.

---

## 📝 **Próximos Passos**

1. ✅ Implementar provider OpenAI
2. ✅ Adicionar rate limiting
3. ✅ Implementar cache de respostas
4. ✅ Adicionar suporte a função calling (tools)
5. ✅ Implementar fallback automático

---

## 🤝 **Contribuindo**

Para adicionar um novo provedor:

1. Adicionar em `LLMProvider` enum
2. Implementar em `_llm_response()`
3. Documentar neste arquivo
4. Adicionar testes

---

## 📞 **Suporte**

- 📧 Email: support@doccollab.com
- 📚 Docs: https://docs.doccollab.com
- 💬 Discord: https://discord.gg/doccollab



