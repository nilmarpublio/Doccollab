"""
Testes para o sistema de grupos
"""
import unittest
import sys
import os

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.user import User
from models.group import Group
from models.group_member import GroupMember
from models.group_document import GroupDocument
from models.group_message import GroupMessage
from models.project import Project


class TestGroupModels(unittest.TestCase):
    """Testes dos modelos de grupo"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Criar usuários de teste
            self.user1 = User(name='User 1', email='user1@test.com')
            self.user1.set_password('password123')
            
            self.user2 = User(name='User 2', email='user2@test.com')
            self.user2.set_password('password123')
            
            db.session.add_all([self.user1, self.user2])
            db.session.commit()
    
    def tearDown(self):
        """Cleanup após cada teste"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_group(self):
        """Teste de criação de grupo"""
        with app.app_context():
            group = Group(
                name='Test Group',
                description='Test Description',
                created_by=self.user1.id
            )
            db.session.add(group)
            db.session.commit()
            
            self.assertIsNotNone(group.id)
            self.assertEqual(group.name, 'Test Group')
            self.assertEqual(group.description, 'Test Description')
            self.assertEqual(group.created_by, self.user1.id)
            self.assertTrue(group.is_active)
    
    def test_add_member(self):
        """Teste de adicionar membro ao grupo"""
        with app.app_context():
            group = Group(name='Test Group', created_by=self.user1.id)
            db.session.add(group)
            db.session.flush()
            
            member = GroupMember(
                group_id=group.id,
                user_id=self.user1.id,
                role='admin'
            )
            db.session.add(member)
            db.session.commit()
            
            self.assertEqual(member.role, 'admin')
            self.assertEqual(len(group.members), 1)
    
    def test_unique_member_constraint(self):
        """Teste de constraint único de membro"""
        with app.app_context():
            group = Group(name='Test Group', created_by=self.user1.id)
            db.session.add(group)
            db.session.flush()
            
            member1 = GroupMember(group_id=group.id, user_id=self.user1.id, role='admin')
            db.session.add(member1)
            db.session.commit()
            
            # Tentar adicionar o mesmo usuário novamente
            member2 = GroupMember(group_id=group.id, user_id=self.user1.id, role='member')
            db.session.add(member2)
            
            with self.assertRaises(Exception):
                db.session.commit()
    
    def test_share_document(self):
        """Teste de compartilhar documento"""
        with app.app_context():
            # Criar projeto
            project = Project(
                name='Test Project',
                user_id=self.user1.id,
                content='Test content'
            )
            db.session.add(project)
            db.session.flush()
            
            # Criar grupo
            group = Group(name='Test Group', created_by=self.user1.id)
            db.session.add(group)
            db.session.flush()
            
            # Compartilhar documento
            doc = GroupDocument(
                group_id=group.id,
                project_id=project.id,
                shared_by=self.user1.id,
                permissions='read'
            )
            db.session.add(doc)
            db.session.commit()
            
            self.assertEqual(doc.permissions, 'read')
            self.assertEqual(len(group.documents), 1)
    
    def test_send_message(self):
        """Teste de enviar mensagem"""
        with app.app_context():
            group = Group(name='Test Group', created_by=self.user1.id)
            db.session.add(group)
            db.session.flush()
            
            message = GroupMessage(
                group_id=group.id,
                user_id=self.user1.id,
                content='Hello, world!',
                message_type='text'
            )
            db.session.add(message)
            db.session.commit()
            
            self.assertEqual(message.content, 'Hello, world!')
            self.assertEqual(message.message_type, 'text')
            self.assertFalse(message.is_deleted)
            self.assertEqual(len(group.messages), 1)
    
    def test_soft_delete_message(self):
        """Teste de soft delete de mensagem"""
        with app.app_context():
            group = Group(name='Test Group', created_by=self.user1.id)
            db.session.add(group)
            db.session.flush()
            
            message = GroupMessage(
                group_id=group.id,
                user_id=self.user1.id,
                content='Test message'
            )
            db.session.add(message)
            db.session.commit()
            
            # Deletar mensagem
            message.is_deleted = True
            db.session.commit()
            
            # Verificar que a mensagem ainda existe mas está marcada como deletada
            msg = GroupMessage.query.get(message.id)
            self.assertTrue(msg.is_deleted)
            self.assertEqual(msg.to_dict()['content'], '[Mensagem deletada]')


class TestGroupAPI(unittest.TestCase):
    """Testes das rotas da API de grupos"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Criar usuário de teste
            self.user = User(name='Test User', email='test@test.com')
            self.user.set_password('password123')
            db.session.add(self.user)
            db.session.commit()
            
            # Fazer login
            self.app.post('/login', data={
                'email': 'test@test.com',
                'password': 'password123'
            }, follow_redirects=True)
    
    def tearDown(self):
        """Cleanup após cada teste"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_group_api(self):
        """Teste de criar grupo via API"""
        response = self.app.post('/api/groups', json={
            'name': 'API Test Group',
            'description': 'Created via API'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['group']['name'], 'API Test Group')
    
    def test_list_groups_api(self):
        """Teste de listar grupos via API"""
        # Criar grupo primeiro
        self.app.post('/api/groups', json={
            'name': 'Test Group 1'
        })
        
        # Listar grupos
        response = self.app.get('/api/groups')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(len(data['groups']), 0)
    
    def test_get_group_details(self):
        """Teste de obter detalhes do grupo"""
        # Criar grupo
        create_response = self.app.post('/api/groups', json={
            'name': 'Detail Test Group'
        })
        group_id = create_response.get_json()['group']['id']
        
        # Obter detalhes
        response = self.app.get(f'/api/groups/{group_id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['group']['name'], 'Detail Test Group')
    
    def test_update_group(self):
        """Teste de atualizar grupo"""
        # Criar grupo
        create_response = self.app.post('/api/groups', json={
            'name': 'Original Name'
        })
        group_id = create_response.get_json()['group']['id']
        
        # Atualizar
        response = self.app.put(f'/api/groups/{group_id}', json={
            'name': 'Updated Name',
            'description': 'Updated Description'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['group']['name'], 'Updated Name')
    
    def test_delete_group(self):
        """Teste de deletar grupo (soft delete)"""
        # Criar grupo
        create_response = self.app.post('/api/groups', json={
            'name': 'To Be Deleted'
        })
        group_id = create_response.get_json()['group']['id']
        
        # Deletar
        response = self.app.delete(f'/api/groups/{group_id}')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        
        # Verificar soft delete
        with app.app_context():
            group = Group.query.get(group_id)
            self.assertFalse(group.is_active)
    
    def test_add_member_api(self):
        """Teste de adicionar membro via API"""
        # Criar segundo usuário
        with app.app_context():
            user2 = User(name='User 2', email='user2@test.com')
            user2.set_password('password123')
            db.session.add(user2)
            db.session.commit()
            user2_id = user2.id
        
        # Criar grupo
        create_response = self.app.post('/api/groups', json={
            'name': 'Member Test Group'
        })
        group_id = create_response.get_json()['group']['id']
        
        # Adicionar membro
        response = self.app.post(f'/api/groups/{group_id}/members', json={
            'user_id': user2_id,
            'role': 'member'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    def test_non_admin_cannot_add_member(self):
        """Teste que não-admin não pode adicionar membro"""
        # Criar dois usuários
        with app.app_context():
            user2 = User(name='User 2', email='user2@test.com')
            user2.set_password('password123')
            user3 = User(name='User 3', email='user3@test.com')
            user3.set_password('password123')
            db.session.add_all([user2, user3])
            db.session.commit()
            user2_id = user2.id
            user3_id = user3.id
        
        # Criar grupo
        create_response = self.app.post('/api/groups', json={
            'name': 'Permission Test Group'
        })
        group_id = create_response.get_json()['group']['id']
        
        # Adicionar user2 como member (não admin)
        self.app.post(f'/api/groups/{group_id}/members', json={
            'user_id': user2_id,
            'role': 'member'
        })
        
        # Fazer logout e login como user2
        self.app.get('/logout')
        self.app.post('/login', data={
            'email': 'user2@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Tentar adicionar user3 (deve falhar)
        response = self.app.post(f'/api/groups/{group_id}/members', json={
            'user_id': user3_id,
            'role': 'member'
        })
        
        self.assertEqual(response.status_code, 403)
        data = response.get_json()
        self.assertFalse(data['success'])


class TestGroupPermissions(unittest.TestCase):
    """Testes de permissões de grupos"""
    
    def setUp(self):
        """Setup antes de cada teste"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Cleanup após cada teste"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_admin_can_edit_group(self):
        """Teste que admin pode editar grupo"""
        # TODO: Implementar
        pass
    
    def test_member_cannot_edit_group(self):
        """Teste que member não pode editar grupo"""
        # TODO: Implementar
        pass
    
    def test_viewer_can_only_view(self):
        """Teste que viewer só pode visualizar"""
        # TODO: Implementar
        pass


if __name__ == '__main__':
    # Executar testes
    unittest.main(verbosity=2)





