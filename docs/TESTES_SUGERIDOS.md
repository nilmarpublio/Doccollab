# 🧪 Guia de Testes - Sistema de Grupos

> **Data**: 11/10/2025  
> **Objetivo**: Sugestões de testes para garantir qualidade do sistema de grupos

---

## ✅ **TESTES JÁ IMPLEMENTADOS**

### **1. Testes de Modelos** (`test_groups.py`)

- ✅ `test_create_group` - Criar grupo
- ✅ `test_add_member` - Adicionar membro
- ✅ `test_unique_member_constraint` - Constraint único
- ✅ `test_share_document` - Compartilhar documento
- ✅ `test_send_message` - Enviar mensagem
- ✅ `test_soft_delete_message` - Soft delete de mensagem

### **2. Testes de API** (`test_groups.py`)

- ✅ `test_create_group_api` - Criar grupo via API
- ✅ `test_list_groups_api` - Listar grupos
- ✅ `test_get_group_details` - Obter detalhes
- ✅ `test_update_group` - Atualizar grupo
- ✅ `test_delete_group` - Deletar grupo (soft delete)
- ✅ `test_add_member_api` - Adicionar membro
- ✅ `test_non_admin_cannot_add_member` - Permissão de admin

**Total**: **13 testes implementados**

---

## 📋 **TESTES SUGERIDOS (A IMPLEMENTAR)**

### **3. Testes de Permissões** (Prioridade: ALTA 🔴)

```python
def test_admin_can_edit_group():
    """Admin pode editar nome e descrição do grupo"""
    # Criar grupo
    # Admin deve conseguir editar
    
def test_member_cannot_edit_group():
    """Member não pode editar grupo"""
    # Criar grupo e adicionar member
    # Member não deve conseguir editar
    
def test_viewer_can_only_view():
    """Viewer só pode visualizar"""
    # Criar grupo e adicionar viewer
    # Viewer não deve conseguir editar, adicionar membros, etc.
    
def test_member_can_share_documents():
    """Member pode compartilhar documentos"""
    # Member deve poder compartilhar seus próprios documentos
    
def test_viewer_cannot_share_documents():
    """Viewer não pode compartilhar documentos"""
    # Viewer não deve poder compartilhar
    
def test_admin_can_remove_any_member():
    """Admin pode remover qualquer membro"""
    # Admin deve poder remover qualquer membro (exceto último admin)
    
def test_cannot_remove_last_admin():
    """Não pode remover o último admin"""
    # Deve falhar ao tentar remover o único admin
    
def test_admin_can_change_roles():
    """Admin pode alterar roles de membros"""
    # Admin deve poder promover/rebaixar membros
    
def test_member_cannot_change_roles():
    """Member não pode alterar roles"""
    # Member não deve conseguir alterar roles
```

---

### **4. Testes de Socket.IO / Chat** (Prioridade: ALTA 🔴)

```python
def test_join_group_socketio():
    """Testar entrada em sala do grupo"""
    # Conectar via Socket.IO
    # Emitir join_group
    # Verificar histórico de mensagens
    
def test_send_message_socketio():
    """Testar envio de mensagem"""
    # Entrar no grupo
    # Enviar mensagem
    # Verificar broadcast para outros membros
    
def test_typing_indicator():
    """Testar indicador de digitação"""
    # Emitir group_typing
    # Verificar broadcast para sala
    
def test_delete_message_socketio():
    """Testar deleção de mensagem"""
    # Enviar mensagem
    # Deletar como autor
    # Verificar soft delete
    
def test_admin_can_delete_any_message():
    """Admin pode deletar qualquer mensagem"""
    # Outro usuário envia mensagem
    # Admin deve poder deletar
    
def test_member_cannot_delete_others_messages():
    """Member só pode deletar suas próprias mensagens"""
    # Outro usuário envia mensagem
    # Member não deve poder deletar
    
def test_non_member_cannot_join_room():
    """Não-membro não pode entrar na sala"""
    # Tentar entrar sem ser membro
    # Deve retornar erro
```

---

### **5. Testes de Compartilhamento de Documentos** (Prioridade: MÉDIA 🟡)

```python
def test_share_own_document():
    """Compartilhar documento próprio"""
    # Criar documento
    # Compartilhar no grupo
    # Verificar que aparece na lista
    
def test_cannot_share_others_document():
    """Não pode compartilhar documento de outro usuário"""
    # Tentar compartilhar documento de outro
    # Deve retornar erro 403
    
def test_duplicate_share_fails():
    """Não pode compartilhar documento duplicado"""
    # Compartilhar documento
    # Tentar compartilhar novamente
    # Deve retornar erro
    
def test_unshare_document():
    """Remover documento compartilhado"""
    # Compartilhar documento
    # Remover compartilhamento
    # Verificar que não aparece mais
    
def test_admin_can_unshare_any_document():
    """Admin pode remover qualquer documento"""
    # Outro usuário compartilha
    # Admin deve poder remover
    
def test_member_can_only_unshare_own():
    """Member só pode remover seus próprios documentos"""
    # Outro usuário compartilha
    # Member não deve poder remover
    
def test_document_permissions():
    """Testar diferentes níveis de permissão (read/write/admin)"""
    # Compartilhar com permissão 'read'
    # Verificar que usuário não pode editar
```

---

### **6. Testes de Integração E2E** (Prioridade: MÉDIA 🟡)

```python
def test_full_group_workflow():
    """Fluxo completo: criar grupo → adicionar membros → chat → compartilhar doc"""
    # 1. Criar grupo
    # 2. Adicionar 2 membros
    # 3. Enviar mensagens no chat
    # 4. Compartilhar documento
    # 5. Verificar que todos veem
    
def test_multiple_groups_isolation():
    """Verificar isolamento entre grupos"""
    # Criar grupo A e B
    # Enviar mensagem em A
    # Verificar que não aparece em B
    
def test_user_leaves_group():
    """Usuário sai do grupo"""
    # Adicionar usuário
    # Remover usuário
    # Verificar que não tem mais acesso
    
def test_group_deletion_cascade():
    """Deletar grupo cascata para mensagens/documentos"""
    # Criar grupo com mensagens e documentos
    # Deletar grupo (soft delete)
    # Verificar que não aparece mais nas listagens
```

---

### **7. Testes de Validação** (Prioridade: BAIXA 🟢)

```python
def test_empty_group_name():
    """Nome vazio não é permitido"""
    # Tentar criar grupo sem nome
    # Deve retornar erro 400
    
def test_very_long_group_name():
    """Nome muito longo (>100 chars)"""
    # Tentar criar com nome de 101+ chars
    # Deve truncar ou retornar erro
    
def test_empty_message():
    """Mensagem vazia não é permitida"""
    # Tentar enviar mensagem vazia
    # Deve retornar erro
    
def test_invalid_role():
    """Role inválido não é aceito"""
    # Tentar adicionar membro com role 'superadmin'
    # Deve retornar erro
    
def test_sql_injection_prevention():
    """Prevenir SQL injection"""
    # Tentar injetar SQL no nome do grupo
    # Deve escapar corretamente
```

---

### **8. Testes de Performance** (Prioridade: BAIXA 🟢)

```python
def test_list_many_groups():
    """Listar muitos grupos"""
    # Criar 100 grupos
    # Listar todos
    # Verificar tempo de resposta < 2s
    
def test_chat_with_many_messages():
    """Chat com muitas mensagens"""
    # Criar 1000 mensagens
    # Carregar histórico (últimas 50)
    # Verificar tempo de resposta < 1s
    
def test_concurrent_messages():
    """Múltiplos usuários enviando mensagens simultaneamente"""
    # 10 usuários enviando mensagens ao mesmo tempo
    # Verificar que todas são salvas corretamente
```

---

## 🎯 **COMO EXECUTAR OS TESTES**

### **Todos os testes**
```bash
python -m unittest tests.test_groups -v
```

### **Apenas uma classe**
```bash
python -m unittest tests.test_groups.TestGroupModels -v
```

### **Um teste específico**
```bash
python -m unittest tests.test_groups.TestGroupModels.test_create_group -v
```

### **Com pytest (se instalado)**
```bash
pytest tests/test_groups.py -v
pytest tests/test_groups.py::TestGroupModels -v
pytest tests/test_groups.py::TestGroupModels::test_create_group -v
```

---

## 📊 **COBERTURA ATUAL**

| Categoria | Testes | Status |
|-----------|--------|--------|
| **Modelos** | 6/6 | ✅ 100% |
| **API REST** | 7/15 | 🟡 47% |
| **Socket.IO** | 0/7 | 🔴 0% |
| **Permissões** | 1/9 | 🔴 11% |
| **Documentos** | 1/7 | 🔴 14% |
| **E2E** | 0/4 | 🔴 0% |
| **Validação** | 0/5 | 🔴 0% |
| **Performance** | 0/3 | 🔴 0% |
| **TOTAL** | **15/56** | **🟡 27%** |

---

## 🎯 **PRIORIDADES**

### **Imediato (Antes do Deploy)** 🔴
1. Testes de permissões (9 testes)
2. Testes de Socket.IO (7 testes)
3. Testes de compartilhamento de documentos (7 testes)

**Total**: ~23 testes essenciais

### **Antes do MVP** 🟡
4. Testes de integração E2E (4 testes)
5. Testes de validação (5 testes)

**Total**: ~9 testes importantes

### **Nice to Have** 🟢
6. Testes de performance (3 testes)

---

## 💡 **DICAS PARA TESTAR**

### **1. Socket.IO Testing**

Para testar Socket.IO, use a biblioteca `python-socketio` com test client:

```python
from socketio import SimpleClient

def test_socketio_example():
    client = SimpleClient()
    client.connect('http://localhost:5000')
    client.emit('join_group', {'group_id': 1})
    response = client.receive()
    assert response['success'] == True
```

### **2. Testar com Múltiplos Usuários**

Crie contextos separados para cada usuário:

```python
# Usuário 1
with self.app.session_transaction() as sess:
    sess['user_id'] = user1.id

# Fazer ações como usuário 1

# Usuário 2
with self.app.session_transaction() as sess:
    sess['user_id'] = user2.id

# Fazer ações como usuário 2
```

### **3. Testar Permissões**

Use decorators ou contexts personalizados:

```python
def as_admin(func):
    def wrapper(*args, **kwargs):
        # Login como admin
        return func(*args, **kwargs)
    return wrapper
```

---

## 📝 **CHECKLIST DE TESTES**

Antes de marcar uma feature como "completa":

- [ ] Testes unitários dos modelos
- [ ] Testes da API REST
- [ ] Testes de permissões
- [ ] Testes de Socket.IO
- [ ] Testes de validação de entrada
- [ ] Pelo menos 1 teste E2E
- [ ] Cobertura > 80%
- [ ] Todos os testes passando

---

## 🚀 **NEXT STEPS**

1. **Implementar testes prioritários (🔴)**
   - Executar: `~2-3 horas`
   
2. **Testar manualmente no navegador**
   - Criar grupo
   - Adicionar membros
   - Enviar mensagens
   - Compartilhar documentos
   
3. **Deploy para staging/produção**
   - Executar todos os testes
   - Verificar logs
   - Monitorar performance

---

**Última atualização**: 11/10/2025  
**Versão**: 1.0  
**Status**: 📋 Planejamento Completo

