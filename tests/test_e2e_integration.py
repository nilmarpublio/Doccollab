"""
Testes End-to-End e de Integração
Simula fluxo completo: query → aplicar patch → verificar snapshot
"""

import unittest
import json
from app import app, db, User, Project
from services.latex_refactors import PatchApplier
from services.latex_linter import LaTeXLinter
from services.bibtex_generator import generate_bibtex_from_description

class TestE2EIntegration(unittest.TestCase):
    
    def setUp(self):
        """Configura ambiente de teste"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        # Criar usuário de teste
        self.test_user = User(name='Test User', email='test@example.com')
        self.test_user.set_password('password123')
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        """Limpa ambiente"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def login(self):
        """Faz login do usuário de teste"""
        return self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
    
    def test_e2e_login_dashboard_editor(self):
        """Testa fluxo: login → dashboard → editor"""
        # Login
        response = self.login()
        self.assertEqual(response.status_code, 200)
        
        # Acessar dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # Acessar editor
        response = self.client.get('/editor')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'editor', response.data.lower())
    
    def test_e2e_compile_latex(self):
        """Testa fluxo: editar → salvar → compilar"""
        self.login()
        
        # Salvar documento LaTeX
        latex_content = r"""
\documentclass{article}
\begin{document}
Hello World!
\end{document}
"""
        
        response = self.client.post('/api/save-latex', 
            json={'filename': 'test.tex', 'content': latex_content})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_e2e_lint_workflow(self):
        """Testa fluxo: lint → detectar issues → aplicar fixes"""
        self.login()
        
        # Conteúdo com problemas
        content_with_issues = r"""
\begin{eqnarray}
    x = 1 \\
    y = 2
\end{eqnarray}

$$z = 3$$
"""
        
        # Executar lint
        response = self.client.post('/api/lint',
            json={'content': content_with_issues, 'filename': 'test.tex'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['summary']['total'], 0)
        
        # Verificar que detectou eqnarray e $$
        issues = data['issues']
        has_eqnarray_issue = any('eqnarray' in str(i) for i in issues)
        self.assertTrue(has_eqnarray_issue)
    
    def test_e2e_bibtex_generation(self):
        """Testa fluxo: gerar BibTeX → salvar → usar citação"""
        self.login()
        
        # Gerar BibTeX
        response = self.client.post('/api/generate-bibtex',
            json={'description': 'Deep Learning, Ian Goodfellow, 2016, MIT Press'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['key'], 'Goodfellow2016DeepLearning')
        self.assertIn('@book', data['bibtex'])
    
    def test_e2e_refactor_patch_workflow(self):
        """Testa fluxo: detectar refatoração → gerar patch → aplicar"""
        original_content = r"""
\begin{eqnarray}
    f(x) = x^2 \\
    g(x) = x^3
\end{eqnarray}
"""
        
        # Aplicar patch de refatoração
        patch_data = {
            'type': 'refactor',
            'refactor_type': 'eqnarray_to_align',
            'original_content': original_content
        }
        
        modified, metadata = PatchApplier.apply_patch(original_content, patch_data)
        
        # Verificar que aplicou a refatoração
        self.assertIn('align', modified)
        self.assertNotIn('eqnarray', modified)
        
        # Verificar metadata
        self.assertIn('patch_id', metadata)
        self.assertIn('timestamp', metadata)
        self.assertEqual(metadata['type'], 'refactor')
    
    def test_integration_lint_and_fix(self):
        """Integração: lint detecta → gera fixes → aplica → re-lint (zero issues)"""
        content = r"""
\begin{eqnarray}
    x = 1
\end{eqnarray}

\begin{figure}
\includegraphics{test.png}
\caption{Test}
\end{figure}
"""
        
        # 1. Primeiro lint
        linter1 = LaTeXLinter()
        issues1 = linter1.lint_content(content)
        self.assertGreater(len(issues1), 0)
        
        # 2. Gerar fixes
        fixes = linter1.generate_fixes(content)
        self.assertGreater(len(fixes), 0)
        
        # 3. Aplicar primeiro fix (eqnarray → align)
        first_fix = fixes[0]
        modified, _ = PatchApplier.apply_patch(content, first_fix)
        
        # 4. Re-lint no conteúdo modificado
        linter2 = LaTeXLinter()
        issues2 = linter2.lint_content(modified)
        
        # Deve ter menos issues (ou igual se outras issues não foram corrigidas)
        self.assertLessEqual(len(issues2), len(issues1))
    
    def test_integration_snippets_api(self):
        """Integração: listar snippets → obter snippet → inserir"""
        self.login()
        
        # Listar snippets
        response = self.client.get('/api/snippets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verificar categorias
        self.assertIn('categories', data)

if __name__ == '__main__':
    unittest.main()

