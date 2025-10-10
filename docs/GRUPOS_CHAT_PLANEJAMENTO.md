# 📋 Planejamento: Grupos de Chat/Colaboração

> **Data**: 11/10/2025  
> **Objetivo**: Implementar sistema completo de grupos de colaboração com chat em tempo real

---

## 🎯 VISÃO GERAL

Adicionar ao DocCollab um sistema de **grupos de colaboração** onde:
- Usuários podem criar grupos
- Adicionar/remover membros
- Compartilhar documentos LaTeX
- Chat em tempo real específico do grupo
- Permissões granulares (admin, membro, visualizador)

---

## 📊 ARQUITETURA

### **Novos Modelos (SQLAlchemy)**

```python
# models/group.py
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relacionamentos
    members = db.relationship('GroupMember', backref='group', lazy=True)
    documents = db.relationship('GroupDocument', backref='group', lazy=True)
    messages = db.relationship('GroupMessage', backref='group', lazy=True)

# models/group_member.py
class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(20))  # 'admin', 'member', 'viewer'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('group_id', 'user_id'),)

# models/group_document.py
class GroupDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    shared_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    permissions = db.Column(db.String(20))  # 'read', 'write', 'admin'

# models/group_message.py
class GroupMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(20))  # 'text', 'file', 'system'
```

---

## 🛠️ IMPLEMENTAÇÃO

### **ETAPA 1: Modelos e Banco de Dados** (1-2h)

#### **Arquivos a Criar**
- `DocCollab/models/group.py`
- `DocCollab/models/group_member.py`
- `DocCollab/models/group_document.py`
- `DocCollab/models/group_message.py`

#### **Tarefas**
1. ✅ Criar modelos SQLAlchemy
2. ✅ Adicionar relacionamentos
3. ✅ Criar migrations (se usar Alembic)
4. ✅ Atualizar `app.py` para importar modelos
5. ✅ Criar tabelas no banco

#### **Script de Migração**
```python
# scripts/create_groups_tables.py
from app import app, db
from models.group import Group
from models.group_member import GroupMember
from models.group_document import GroupDocument
from models.group_message import GroupMessage

with app.app_context():
    db.create_all()
    print("✅ Tabelas de grupos criadas!")
```

---

### **ETAPA 2: Rotas REST API** (2-3h)

#### **Endpoints a Criar**

```python
# app.py

# ===== GRUPOS =====
@app.route('/api/groups', methods=['GET'])
@login_required
def list_groups():
    """Listar grupos do usuário"""
    pass

@app.route('/api/groups', methods=['POST'])
@login_required
def create_group():
    """Criar novo grupo"""
    pass

@app.route('/api/groups/<int:group_id>', methods=['GET'])
@login_required
def get_group(group_id):
    """Obter detalhes do grupo"""
    pass

@app.route('/api/groups/<int:group_id>', methods=['PUT'])
@login_required
def update_group(group_id):
    """Atualizar grupo (admin only)"""
    pass

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    """Deletar grupo (admin only)"""
    pass

# ===== MEMBROS =====
@app.route('/api/groups/<int:group_id>/members', methods=['GET'])
@login_required
def list_members(group_id):
    """Listar membros do grupo"""
    pass

@app.route('/api/groups/<int:group_id>/members', methods=['POST'])
@login_required
def add_member(group_id):
    """Adicionar membro (admin only)"""
    pass

@app.route('/api/groups/<int:group_id>/members/<int:user_id>', methods=['DELETE'])
@login_required
def remove_member(group_id, user_id):
    """Remover membro (admin only)"""
    pass

@app.route('/api/groups/<int:group_id>/members/<int:user_id>/role', methods=['PUT'])
@login_required
def update_member_role(group_id, user_id):
    """Atualizar role do membro (admin only)"""
    pass

# ===== DOCUMENTOS =====
@app.route('/api/groups/<int:group_id>/documents', methods=['GET'])
@login_required
def list_group_documents(group_id):
    """Listar documentos do grupo"""
    pass

@app.route('/api/groups/<int:group_id>/documents', methods=['POST'])
@login_required
def share_document(group_id):
    """Compartilhar documento no grupo"""
    pass

@app.route('/api/groups/<int:group_id>/documents/<int:doc_id>', methods=['DELETE'])
@login_required
def unshare_document(group_id, doc_id):
    """Remover documento do grupo"""
    pass
```

---

### **ETAPA 3: Socket.IO para Chat** (2-3h)

#### **Eventos Socket.IO**

```python
# app.py

@socketio.on('join_group')
def handle_join_group(data):
    """Entrar em sala do grupo"""
    group_id = data.get('group_id')
    
    # Verificar permissão
    member = GroupMember.query.filter_by(
        group_id=group_id,
        user_id=current_user.id
    ).first()
    
    if not member:
        return {'success': False, 'error': 'Você não é membro deste grupo'}
    
    # Entrar na sala
    room = f'group_{group_id}'
    join_room(room)
    
    # Notificar outros membros
    emit('user_joined_group', {
        'user_name': current_user.name,
        'user_id': current_user.id
    }, room=room, skip_sid=request.sid)
    
    # Carregar histórico
    messages = GroupMessage.query.filter_by(group_id=group_id)\
        .order_by(GroupMessage.timestamp.desc())\
        .limit(50)\
        .all()
    
    return {
        'success': True,
        'messages': [msg.to_dict() for msg in reversed(messages)]
    }

@socketio.on('leave_group')
def handle_leave_group(data):
    """Sair da sala do grupo"""
    group_id = data.get('group_id')
    room = f'group_{group_id}'
    leave_room(room)
    
    emit('user_left_group', {
        'user_name': current_user.name,
        'user_id': current_user.id
    }, room=room)

@socketio.on('send_group_message')
def handle_group_message(data):
    """Enviar mensagem no grupo"""
    group_id = data.get('group_id')
    content = data.get('content')
    
    # Verificar permissão
    member = GroupMember.query.filter_by(
        group_id=group_id,
        user_id=current_user.id
    ).first()
    
    if not member:
        return {'success': False, 'error': 'Você não é membro deste grupo'}
    
    # Salvar mensagem
    message = GroupMessage(
        group_id=group_id,
        user_id=current_user.id,
        content=content,
        message_type='text'
    )
    db.session.add(message)
    db.session.commit()
    
    # Broadcast para sala
    room = f'group_{group_id}'
    emit('new_group_message', {
        'id': message.id,
        'user_name': current_user.name,
        'user_id': current_user.id,
        'content': content,
        'timestamp': message.timestamp.isoformat()
    }, room=room)
    
    return {'success': True, 'message_id': message.id}

@socketio.on('group_typing')
def handle_group_typing(data):
    """Indicar que está digitando"""
    group_id = data.get('group_id')
    is_typing = data.get('is_typing', False)
    
    room = f'group_{group_id}'
    emit('user_typing_group', {
        'user_name': current_user.name,
        'user_id': current_user.id,
        'is_typing': is_typing
    }, room=room, skip_sid=request.sid)
```

---

### **ETAPA 4: Interface Frontend** (3-4h)

#### **Páginas a Criar**

1. **`templates/groups.html`** - Lista de grupos
2. **`templates/group_detail.html`** - Detalhes do grupo + chat
3. **`templates/create_group.html`** - Criar novo grupo

#### **Componentes JavaScript**

```javascript
// static/js/groups.js

class GroupManager {
  constructor() {
    this.currentGroup = null;
    this.socket = io();
    this.setupSocketListeners();
  }
  
  async loadGroups() {
    const response = await fetch('/api/groups');
    const groups = await response.json();
    this.renderGroupsList(groups);
  }
  
  async createGroup(name, description) {
    const response = await fetch('/api/groups', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name, description})
    });
    const data = await response.json();
    if (data.success) {
      this.loadGroups();
      return data.group;
    }
    throw new Error(data.error);
  }
  
  async joinGroup(groupId) {
    this.currentGroup = groupId;
    
    // Socket.IO
    this.socket.emit('join_group', {group_id: groupId}, (response) => {
      if (response.success) {
        this.renderMessages(response.messages);
      }
    });
    
    // Carregar membros e documentos
    await this.loadMembers(groupId);
    await this.loadDocuments(groupId);
  }
  
  sendMessage(content) {
    if (!this.currentGroup) return;
    
    this.socket.emit('send_group_message', {
      group_id: this.currentGroup,
      content: content
    });
  }
  
  setupSocketListeners() {
    this.socket.on('new_group_message', (data) => {
      this.appendMessage(data);
    });
    
    this.socket.on('user_joined_group', (data) => {
      this.showNotification(`${data.user_name} entrou no grupo`);
      this.addUserToList(data);
    });
    
    this.socket.on('user_left_group', (data) => {
      this.showNotification(`${data.user_name} saiu do grupo`);
      this.removeUserFromList(data);
    });
    
    this.socket.on('user_typing_group', (data) => {
      this.showTypingIndicator(data);
    });
  }
  
  // ... métodos auxiliares
}

// Inicializar
const groupManager = new GroupManager();
```

---

### **ETAPA 5: UI/UX Design** (2-3h)

#### **Layout da Página de Grupos**

```
┌─────────────────────────────────────────────────────────────┐
│ DocCollab - Grupos                                    [+]    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 📁 Grupo 1  │  │ 📁 Grupo 2  │  │ 📁 Grupo 3  │         │
│  │ 5 membros   │  │ 3 membros   │  │ 8 membros   │         │
│  │ 2 docs      │  │ 1 doc       │  │ 5 docs      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ 📁 Grupo 4  │  │ 📁 Grupo 5  │                           │
│  │ 2 membros   │  │ 4 membros   │                           │
│  │ 0 docs      │  │ 3 docs      │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### **Layout da Página de Detalhes do Grupo**

```
┌─────────────────────────────────────────────────────────────┐
│ 📁 Grupo de Trabalho - TCC                                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────────────────────┐  │
│  │ 👥 MEMBROS (5)  │  │ 💬 CHAT                         │  │
│  ├─────────────────┤  ├─────────────────────────────────┤  │
│  │ ● João (Admin)  │  │ João: Olá pessoal!              │  │
│  │ ● Maria (Memb.) │  │ Maria: Oi! Como vai o TCC?      │  │
│  │ ○ Pedro (View.) │  │ João: Estou terminando cap. 3   │  │
│  │ ● Ana (Member)  │  │ ...                             │  │
│  │ ○ Carlos (View.)│  │                                 │  │
│  │                 │  │ [Digite sua mensagem...]        │  │
│  │ [+ Adicionar]   │  └─────────────────────────────────┘  │
│  └─────────────────┘                                         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 📄 DOCUMENTOS COMPARTILHADOS (2)                     │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ 📝 capitulo1.tex          [Abrir] [Editar]          │   │
│  │    Compartilhado por João em 10/10/2025             │   │
│  │                                                       │   │
│  │ 📝 referencias.bib        [Abrir] [Editar]          │   │
│  │    Compartilhado por Maria em 09/10/2025            │   │
│  │                                                       │   │
│  │ [+ Compartilhar Documento]                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

### **ETAPA 6: Permissões e Segurança** (1-2h)

#### **Sistema de Permissões**

```python
# services/group_permissions.py

class GroupPermissions:
    """Gerenciador de permissões de grupo"""
    
    ROLES = {
        'admin': {
            'can_edit_group': True,
            'can_delete_group': True,
            'can_add_members': True,
            'can_remove_members': True,
            'can_change_roles': True,
            'can_share_documents': True,
            'can_unshare_documents': True,
            'can_send_messages': True,
            'can_view_documents': True
        },
        'member': {
            'can_edit_group': False,
            'can_delete_group': False,
            'can_add_members': False,
            'can_remove_members': False,
            'can_change_roles': False,
            'can_share_documents': True,
            'can_unshare_documents': False,
            'can_send_messages': True,
            'can_view_documents': True
        },
        'viewer': {
            'can_edit_group': False,
            'can_delete_group': False,
            'can_add_members': False,
            'can_remove_members': False,
            'can_change_roles': False,
            'can_share_documents': False,
            'can_unshare_documents': False,
            'can_send_messages': True,
            'can_view_documents': True
        }
    }
    
    @staticmethod
    def user_can(user_id, group_id, permission):
        """Verificar se usuário tem permissão"""
        member = GroupMember.query.filter_by(
            user_id=user_id,
            group_id=group_id
        ).first()
        
        if not member:
            return False
        
        role_perms = GroupPermissions.ROLES.get(member.role, {})
        return role_perms.get(permission, False)
    
    @staticmethod
    def require_group_permission(permission):
        """Decorator para verificar permissão"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                group_id = kwargs.get('group_id')
                if not GroupPermissions.user_can(current_user.id, group_id, permission):
                    return jsonify({
                        'success': False,
                        'error': 'Você não tem permissão para esta ação'
                    }), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

#### **Uso nos Endpoints**

```python
@app.route('/api/groups/<int:group_id>/members', methods=['POST'])
@login_required
@require_group_permission('can_add_members')
def add_member(group_id):
    """Adicionar membro (admin only)"""
    # ... implementação
```

---

### **ETAPA 7: Testes** (2-3h)

#### **Testes Unitários**

```python
# tests/test_groups.py

import unittest
from app import app, db
from models.group import Group
from models.group_member import GroupMember
from models.user import User

class TestGroups(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_create_group(self):
        """Teste de criação de grupo"""
        # Criar usuário
        user = User(name='Test', email='test@test.com')
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        
        # Login
        self.app.post('/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })
        
        # Criar grupo
        response = self.app.post('/api/groups', json={
            'name': 'Grupo Teste',
            'description': 'Descrição teste'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['group']['name'], 'Grupo Teste')
    
    def test_add_member(self):
        """Teste de adicionar membro"""
        # ... implementação
    
    def test_permissions(self):
        """Teste de permissões"""
        # ... implementação
    
    def test_chat_message(self):
        """Teste de mensagem no chat"""
        # ... implementação

if __name__ == '__main__':
    unittest.main()
```

---

## 📅 CRONOGRAMA

### **Dia 1 (11/10/2025) - Manhã**
- ✅ ETAPA 1: Modelos e Banco (1-2h)
- ✅ ETAPA 2: Rotas REST API (2-3h)

### **Dia 1 (11/10/2025) - Tarde**
- ✅ ETAPA 3: Socket.IO para Chat (2-3h)
- ✅ ETAPA 4: Interface Frontend - Parte 1 (2h)

### **Dia 1 (11/10/2025) - Noite**
- ✅ ETAPA 4: Interface Frontend - Parte 2 (2h)
- ✅ ETAPA 5: UI/UX Design (2h)

### **Dia 2 (12/10/2025) - Manhã** (se necessário)
- ✅ ETAPA 6: Permissões e Segurança (1-2h)
- ✅ ETAPA 7: Testes (2-3h)
- ✅ Deploy e Documentação (1h)

---

## 🎯 OBJETIVOS DE CADA ETAPA

### **ETAPA 1: Modelos**
- ✅ Estrutura de dados completa
- ✅ Relacionamentos corretos
- ✅ Constraints e validações

### **ETAPA 2: API REST**
- ✅ CRUD completo de grupos
- ✅ Gerenciamento de membros
- ✅ Compartilhamento de documentos
- ✅ Validações e tratamento de erros

### **ETAPA 3: Socket.IO**
- ✅ Chat em tempo real
- ✅ Notificações de entrada/saída
- ✅ Indicador de digitação
- ✅ Histórico de mensagens

### **ETAPA 4: Frontend**
- ✅ Interface intuitiva
- ✅ Responsiva (mobile-friendly)
- ✅ Integração Socket.IO
- ✅ Feedback visual

### **ETAPA 5: Design**
- ✅ UI moderna e limpa
- ✅ UX fluida
- ✅ Acessibilidade
- ✅ Consistência visual

### **ETAPA 6: Segurança**
- ✅ Permissões granulares
- ✅ Validações server-side
- ✅ Proteção contra ataques
- ✅ Audit logs

### **ETAPA 7: Testes**
- ✅ Cobertura 100%
- ✅ Testes de integração
- ✅ Testes de permissões
- ✅ Testes de Socket.IO

---

## 🚀 FEATURES ADICIONAIS (FUTURO)

### **v1.2 - Melhorias**
- [ ] Notificações push
- [ ] Busca de grupos
- [ ] Tags/categorias
- [ ] Grupos públicos/privados
- [ ] Convites por email

### **v1.3 - Avançado**
- [ ] Videochamada (WebRTC)
- [ ] Compartilhamento de tela
- [ ] Edição colaborativa em tempo real (CRDT)
- [ ] Integração com Google Drive/Dropbox

### **v2.0 - Enterprise**
- [ ] SSO (Single Sign-On)
- [ ] LDAP/Active Directory
- [ ] Auditoria avançada
- [ ] Backup automático
- [ ] SLA e suporte 24/7

---

## 📝 NOTAS TÉCNICAS

### **Escalabilidade**
- Usar Redis para Socket.IO em produção
- Implementar cache de grupos/membros
- Pagination para mensagens antigas
- CDN para arquivos estáticos

### **Performance**
- Lazy loading de mensagens
- Compressão de WebSocket
- Índices no banco de dados
- Query optimization

### **Segurança**
- Rate limiting por IP
- CSRF protection
- XSS sanitization
- SQL injection prevention
- Audit logs completos

---

## ✅ CHECKLIST FINAL

### **Backend**
- [ ] Modelos criados e testados
- [ ] Rotas REST implementadas
- [ ] Socket.IO events funcionando
- [ ] Permissões configuradas
- [ ] Testes passando (100%)

### **Frontend**
- [ ] Página de grupos
- [ ] Página de detalhes
- [ ] Chat em tempo real
- [ ] Gerenciamento de membros
- [ ] Compartilhamento de docs

### **Deploy**
- [ ] Migrations aplicadas
- [ ] Redis configurado (produção)
- [ ] Supervisor atualizado
- [ ] Testes em produção
- [ ] Documentação atualizada

---

**Estimativa Total**: 12-16 horas (1-2 dias)

**Prioridade**: Alta 🔴

**Status**: 📋 Planejamento Completo

---

**Preparado por**: Claude Sonnet 4.5  
**Data**: 10/10/2025  
**Versão**: 1.0

