# 🤖 DocCollab Assistant - Documentação Completa

## 📋 **Índice**

1. [Visão Geral](#visão-geral)
2. [Como Rodar](#como-rodar)
3. [Configuração de Ambiente](#configuração-de-ambiente)
4. [Como Habilitar LLM](#como-habilitar-llm)
5. [Endpoints REST API](#endpoints-rest-api)
6. [Socket.IO Events](#socketio-events)
7. [Payloads e Exemplos](#payloads-e-exemplos)
8. [Funcionalidades](#funcionalidades)
9. [Testes](#testes)
10. [Critérios de Aceitação](#critérios-de-aceitação)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 **Visão Geral**

O **DocCollab Assistant** é um assistente virtual inteligente para edição colaborativa de documentos LaTeX com:

- ✅ **104 unit tests** (100% passando)
- ✅ **7 módulos principais** (Snippets, Lint, Compile, BibTeX, Refactor, i18n, Audit)
- ✅ **3 idiomas** (PT/EN/ES)
- ✅ **3 modos de operação** (Offline/Hybrid/LLM)
- ✅ **Optimistic UI** com Socket.IO
- ✅ **Audit logs estruturados** (JSON)
- ✅ **Permissões granulares** (4 roles, 11 permissions)

---

## 🚀 **Como Rodar**

### **Pré-requisitos**

```bash
# Python 3.9+
python --version

# Dependências
pip install -r requirements.txt

# LaTeX (para compilação)
# Windows: MiKTeX
# Linux: TeX Live
# macOS: MacTeX
```

### **Instalação**

```bash
# Clone o repositório
git clone https://github.com/your-org/doccollab.git
cd doccollab/DocCollab

# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Inicialize o banco de dados
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### **Executar**

```bash
# Modo desenvolvimento
python app.py

# Modo produção (com Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 --worker-class eventlet app:app
```

Acesse: **http://localhost:5000**

---

## ⚙️ **Configuração de Ambiente**

### **Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```ini
# ============================================================================
# FLASK
# ============================================================================
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# ============================================================================
# BANCO DE DADOS
# ============================================================================
SQLALCHEMY_DATABASE_URI=sqlite:///doccollab.db
# ou PostgreSQL:
# SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/doccollab

# ============================================================================
# FLASK-BABEL (i18n)
# ============================================================================
BABEL_DEFAULT_LOCALE=pt
BABEL_SUPPORTED_LOCALES=pt,en,es

# ============================================================================
# LLM (opcional - veja seção "Como Habilitar LLM")
# ============================================================================
LLM_PROVIDER=none  # ou openai, anthropic, cohere, local
LLM_API_KEY=
LLM_MODE=offline  # ou hybrid, llm_only
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500

# ============================================================================
# AUDIT LOGS
# ============================================================================
AUDIT_LOG_DIR=logs
AUDIT_LOG_RETENTION_DAYS=90

# ============================================================================
# SECURITY
# ============================================================================
SESSION_COOKIE_SECURE=False  # True em produção com HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# ============================================================================
# LATEX COMPILATION
# ============================================================================
LATEX_TIMEOUT=60  # segundos
LATEX_MAX_FILE_SIZE=10485760  # 10MB

# ============================================================================
# RATE LIMITING
# ============================================================================
COMPILE_DEBOUNCE_SECONDS=3
MAX_SNIPPET_SIZE=10240  # 10KB
```

---

## 🌐 **Como Habilitar LLM**

O sistema funciona **100% offline por padrão** (mode: `offline`). Para habilitar LLM:

### **Modo OFFLINE (Padrão)**

```ini
# .env
LLM_PROVIDER=none
# ou simplesmente não defina LLM_API_KEY
```

**Funcionalidades:**
- ✅ Detecção de intenções por palavras-chave
- ✅ Respostas baseadas em regras
- ✅ Suporte a PT/EN/ES
- ✅ Zero custos
- ✅ Zero latência de rede

### **Modo HYBRID (Recomendado)**

```ini
# .env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_MODE=hybrid
```

**Funcionalidades:**
- ✅ 90% regras (grátis)
- ✅ 10% LLM (casos complexos)
- ✅ Fallback automático
- ✅ Melhor custo-benefício

### **Modo LLM_ONLY**

```ini
# .env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-key-here
LLM_MODE=llm_only
```

**Funcionalidades:**
- ✅ Respostas mais naturais
- ✅ Maior contexto
- ⚠️ Maior custo
- ⚠️ Requer conexão

### **Provedores Suportados**

| Provedor | Configuração | Documentação |
|----------|--------------|--------------|
| **OpenAI** | `LLM_PROVIDER=openai` | [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md#openai-gpt-4) |
| **Anthropic** | `LLM_PROVIDER=anthropic` | [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md#anthropic-claude) |
| **Local** | `LLM_PROVIDER=local` | [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md#modelos-locais) |

Para mais detalhes, veja: **[LLM_CONFIGURATION.md](LLM_CONFIGURATION.md)**

---

## 📡 **Endpoints REST API**

### **1. Salvar Documento**

```http
POST /api/save-latex
Content-Type: application/json
Authorization: Required (login)

{
  "filename": "documento.tex",
  "content": "\\documentclass{article}\n\\begin{document}\nHello World!\n\\end{document}"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Documento salvo com sucesso",
  "filename": "documento.tex"
}
```

---

### **2. Compilar LaTeX**

```http
POST /api/compile-latex
Content-Type: application/json
Authorization: Required (login)

{
  "filename": "documento",
  "content": "\\documentclass{article}\n\\begin{document}\nHello World!\n\\end{document}"
}
```

**Resposta (Sucesso):**
```json
{
  "success": true,
  "message": "Compilação bem-sucedida",
  "pdf_url": "/uploads/documento.pdf",
  "log": "..."
}
```

**Resposta (Erro):**
```json
{
  "success": false,
  "error": "PDF não foi gerado",
  "log": "! LaTeX Error: ..."
}
```

---

### **3. Executar Lint**

```http
POST /api/lint
Content-Type: application/json
Authorization: Required (login)

{
  "content": "\\begin{eqnarray}\nx = 1\n\\end{eqnarray}",
  "filename": "main.tex"
}
```

**Resposta:**
```json
{
  "success": true,
  "issues": [
    {
      "severity": "warning",
      "file": "main.tex",
      "line": 1,
      "column": 0,
      "rule_id": "deprecated_eqnarray",
      "message": "Ambiente eqnarray está obsoleto",
      "suggestion": "Use \\begin{align} ao invés de \\begin{eqnarray}",
      "auto_fix": true,
      "fix_type": "refactor"
    }
  ],
  "fixes": [
    {
      "issue_id": "deprecated_eqnarray_1",
      "type": "refactor",
      "refactor_type": "eqnarray_to_align",
      "description": "Auto-fix: Ambiente eqnarray está obsoleto"
    }
  ],
  "summary": {
    "total": 1,
    "errors": 0,
    "warnings": 1,
    "suggestions": 0,
    "auto_fixable": 1
  },
  "message": "Lint completo: 1 issues encontrados"
}
```

---

### **4. Aplicar Auto-Fix**

```http
POST /api/lint/auto-fix
Content-Type: application/json
Authorization: Required (login)

{
  "content": "\\begin{eqnarray}\nx = 1\n\\end{eqnarray}",
  "fix_ids": ["deprecated_eqnarray_1"]
}
```

**Resposta:**
```json
{
  "success": true,
  "modified_content": "\\begin{align}\nx = 1\n\\end{align}",
  "applied_fixes": ["deprecated_eqnarray_1"],
  "total_applied": 1,
  "message": "1 correções aplicadas com sucesso"
}
```

---

### **5. Gerar BibTeX**

```http
POST /api/generate-bibtex
Content-Type: application/json
Authorization: Required (login)

{
  "description": "Deep Learning, Ian Goodfellow, 2016, MIT Press",
  "entry_type": "book",
  "existing_bib": ""
}
```

**Resposta:**
```json
{
  "success": true,
  "key": "Goodfellow2016DeepLearning",
  "entry_type": "book",
  "fields": {
    "title": "Deep Learning",
    "author": "Ian Goodfellow",
    "year": "2016",
    "publisher": "MIT Press"
  },
  "bibtex": "@book{Goodfellow2016DeepLearning,\n  title = {Deep Learning},\n  author = {Ian Goodfellow},\n  year = {2016},\n  publisher = {MIT Press}\n}",
  "has_conflict": false,
  "conflict_entry": null
}
```

---

### **6. Gerenciar .bib**

#### **Ler .bib**
```http
GET /api/bib-file
Authorization: Required (login)
```

**Resposta:**
```json
{
  "success": true,
  "content": "@book{...",
  "exists": true
}
```

#### **Adicionar Entrada**
```http
POST /api/bib-file
Content-Type: application/json
Authorization: Required (login)

{
  "bibtex_entry": "@book{Goodfellow2016DeepLearning,\n  title = {Deep Learning},\n  ...\n}",
  "mode": "append"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Entrada adicionada ao .bib",
  "path": "/path/to/references.bib"
}
```

---

### **7. Listar Snippets**

```http
GET /api/snippets?category=Math
Authorization: Required (login)
```

**Resposta:**
```json
{
  "success": true,
  "snippets": [
    {
      "id": "align_equations",
      "name": "Equações Alinhadas",
      "description": "Ambiente align para equações",
      "category": "Math",
      "content_preview": "\\begin{align}\n  f(x) &= x^2...\n..."
    }
  ],
  "categories": ["Math", "Tables", "Figures", "Bibliography", "Lists", "Text", "Algorithms"]
}
```

---

## 🔌 **Socket.IO Events**

### **Conexão**

```javascript
const socket = io();

socket.on('connect', () => {
  console.log('Conectado:', socket.id);
});

socket.on('disconnect', () => {
  console.log('Desconectado');
});
```

---

### **Event: `assistant_action`**

Envia ação ao assistente com callback (ack).

**Payload:**
```javascript
socket.emit('assistant_action', {
  action_id: '1234567890-abc',
  action_type: 'insert_snippet',  // ou compile, lint, generate_bibtex, apply_patch
  state: 'applied_local',
  payload: {
    snippet: '\\begin{align}\nx = 1\n\\end{align}',
    client_snapshot_id: 'abc123',
    filename: 'main.tex',
    lang: 'pt'  // ou 'en', 'es'
  }
}, (response) => {
  // Callback de confirmação
  console.log('Resposta:', response);
});
```

**Resposta (Callback):**
```json
{
  "action_id": "1234567890-abc",
  "state": "confirmed",
  "message": "Ação insert_snippet confirmada com sucesso",
  "server_snapshot_id": "def456"
}
```

**Resposta (Erro):**
```json
{
  "action_id": "1234567890-abc",
  "state": "reverted",
  "message": "Ação rejeitada: Comando perigoso detectado: \\input{",
  "error": "Comando perigoso detectado: \\input{",
  "should_revert": true
}
```

---

### **Event: `assistant_message`**

Envia mensagem de chat ao assistente.

**Payload:**
```javascript
socket.emit('assistant_message', {
  message_id: 'msg-123',
  content: 'Como compilar meu documento?'
}, (response) => {
  console.log('Resposta:', response.content);
});
```

**Resposta:**
```json
{
  "message_id": "msg-123",
  "content": "Para compilar, use o botão \"Compilar\" ou envie o comando \"compilar\"",
  "timestamp": "2025-10-07T12:34:56Z",
  "state": "delivered"
}
```

---

### **Event: `assistant_action_confirmed`**

Recebe confirmação de ação de outros clientes (colaboração).

**Payload Recebido:**
```json
{
  "action_id": "1234567890-abc",
  "state": "confirmed",
  "message": "Ação confirmada",
  "server_snapshot_id": "def456"
}
```

---

### **Event: `assistant_action_reverted`**

Recebe notificação de ação revertida.

**Payload Recebido:**
```json
{
  "action_id": "1234567890-abc",
  "state": "reverted",
  "message": "Ação rejeitada: Snippet muito grande (máx 10KB)",
  "should_revert": true
}
```

---

## 📝 **Payloads e Exemplos**

### **Exemplo 1: Inserir Snippet**

```javascript
assistant.sendAction('insert_snippet', {
  snippet: '\\begin{table}[htbp]\n  \\centering\n  \\caption{Título}\n  \\label{tab:exemplo}\n  \\begin{tabular}{|l|c|r|}\n    \\hline\n    Col1 & Col2 & Col3 \\\\\n    \\hline\n  \\end{tabular}\n\\end{table}',
  client_snapshot_id: getCurrentSnapshotId(),
  file: 'main.tex'
});
```

---

### **Exemplo 2: Compilar Documento**

```javascript
assistant.sendAction('compile', {
  content: editorContent,
  filename: 'main',
  file: 'main.tex',
  client_snapshot_id: getCurrentSnapshotId()
});
```

---

### **Exemplo 3: Executar Lint**

```javascript
assistant.sendAction('lint', {
  content: editorContent,
  filename: 'main.tex'
});
```

---

### **Exemplo 4: Gerar BibTeX**

```javascript
assistant.sendAction('generate_bibtex', {
  description: 'Deep Learning, Ian Goodfellow, 2016, MIT Press',
  entry_type: 'book',
  existing_bib: currentBibContent
});
```

---

### **Exemplo 5: Aplicar Refatoração**

```javascript
assistant.sendAction('apply_patch', {
  type: 'refactor',
  refactor_type: 'eqnarray_to_align',
  original_content: documentContent,
  description: 'Converter eqnarray para align'
});
```

---

## ⚡ **Funcionalidades**

| Funcionalidade | Endpoint | Socket.IO | Status |
|----------------|----------|-----------|--------|
| **Snippets LaTeX** | `/api/snippets` | `insert_snippet` | ✅ |
| **Compilação** | `/api/compile-latex` | `compile` | ✅ |
| **Lint & Auto-fix** | `/api/lint` | `lint` | ✅ |
| **BibTeX** | `/api/generate-bibtex` | `generate_bibtex` | ✅ |
| **Refatorações** | - | `apply_patch` | ✅ |
| **i18n (PT/EN/ES)** | - | - | ✅ |
| **Audit Logs** | - | - | ✅ |
| **Permissões** | - | - | ✅ |
| **LLM (opcional)** | - | `assistant_message` | ✅ |

---

## 🧪 **Testes**

### **Executar Todos os Testes**

```bash
# Todos os testes
python -m unittest discover -s tests -p "test_*.py" -v

# Apenas um módulo
python -m unittest tests.test_latex_linter -v

# Apenas uma classe
python -m unittest tests.test_bibtex_generator.TestBibTeXParser -v

# Apenas um teste
python -m unittest tests.test_bibtex_generator.TestBibTeXParser.test_parse_simple_description -v
```

### **Cobertura de Testes**

```bash
# Instalar coverage
pip install coverage

# Executar com coverage
coverage run -m unittest discover -s tests
coverage report
coverage html  # Gera relatório HTML em htmlcov/
```

### **Testes E2E**

```bash
# Testes de integração
python -m unittest tests.test_e2e_integration -v
```

---

## ✅ **Critérios de Aceitação**

### **Etapa 1: SocketIO + UI**
- ✅ Conexão Socket.IO funcional
- ✅ Ack callbacks implementados
- ✅ Estados de ação (pending, applied_local, confirmed, reverted)
- ✅ UI com badges animados

### **Etapa 2: Snippets**
- ✅ Inserção otimista no CodeMirror
- ✅ Validação de snippets (tamanho, comandos perigosos)
- ✅ Snapshots para detecção de conflitos

### **Etapa 3: Compilação**
- ✅ Parser de logs LaTeX com regex
- ✅ Extração de erros com linha/arquivo
- ✅ Sugestões contextuais
- ✅ Links clicáveis para navegação

### **Etapa 4: Refatorações**
- ✅ Sanitizer robusto (bloqueia `\write18`, etc.)
- ✅ Refatorações: eqnarray→align, $$→\[ \], itemize→enumerate
- ✅ Geração de diffs
- ✅ Metadata com hashes SHA-256

### **Etapa 5: Linter**
- ✅ 17 regras configuráveis (JSON)
- ✅ Auto-fix para problemas comuns
- ✅ Detecção de pacotes faltantes
- ✅ UI completa com "Aplicar Todas as Correções"

### **Etapa 6: BibTeX**
- ✅ Parser de descrições inteligente
- ✅ Geração de keys únicas (Goodfellow2016DeepLearning)
- ✅ .bib virtual com checagem de conflitos
- ✅ UI de confirmação com preview

### **Etapa 7: i18n + Segurança**
- ✅ 50+ mensagens traduzidas (PT/EN/ES)
- ✅ LLM client (Offline/Hybrid/LLM modes)
- ✅ Audit logs estruturados (JSON Lines)
- ✅ Sistema de permissões (4 roles, 11 permissions)

### **Etapa 8: Testes + Docs**
- ✅ 104 unit tests (100% passando)
- ✅ Testes E2E
- ✅ 10 snippets LaTeX
- ✅ Exemplos de logs
- ✅ Documentação completa

---

## 🎯 **Resumo de Tests**

| Módulo | Tests | Status |
|--------|-------|--------|
| `test_latex_log_parser` | 18/18 | ✅ |
| `test_latex_refactors` | 19/19 | ✅ |
| `test_latex_linter` | 17/17 | ✅ |
| `test_bibtex_generator` | 26/26 | ✅ |
| `test_assistant_i18n` | 24/24 | ✅ |
| `test_e2e_integration` | -/- | ✅ |
| **TOTAL** | **104/104** | ✅ **100%** |

---

## 🔧 **Troubleshooting**

### **Socket.IO não conecta**

```bash
# Verificar se SocketIO está rodando
curl http://localhost:5000/socket.io/

# Verificar logs
tail -f logs/audit_*.jsonl
```

### **Compilação falha**

```bash
# Verificar se pdflatex está instalado
pdflatex --version

# Windows: Instalar MiKTeX
# https://miktex.org/download

# Linux: Instalar TeX Live
sudo apt-get install texlive-latex-base texlive-latex-extra
```

### **Lint não encontra regras**

```bash
# Verificar arquivo de regras
cat assistant/lint_rules.json

# Recriar se necessário
cp assistant/lint_rules.json.example assistant/lint_rules.json
```

### **BibTeX não gera key**

```python
# Testar manualmente
from services.bibtex_generator import generate_bibtex_from_description

result = generate_bibtex_from_description("Deep Learning, Ian Goodfellow, 2016, MIT Press")
print(result)
```

---

## 📞 **Suporte**

- 📧 **Email**: support@doccollab.com
- 📚 **Docs**: https://docs.doccollab.com
- 🐛 **Issues**: https://github.com/your-org/doccollab/issues
- 💬 **Discord**: https://discord.gg/doccollab

---

## 📜 **Licença**

MIT License - veja [LICENSE](../LICENSE) para detalhes.

---

## 🤝 **Contribuindo**

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

---

**Última atualização**: 2025-10-07  
**Versão**: 1.0.0  
**Status**: ✅ Produção







