"""
Unit tests para internacionalização do assistente
"""

import unittest
from services.assistant_i18n import get_message, detect_language, get_available_languages
from services.llm_client import LLMClient, LLMMode, LLMProvider

class TestAssistantI18n(unittest.TestCase):
    
    def test_get_message_portuguese(self):
        """Deve retornar mensagem em português"""
        msg = get_message('action_confirmed', 'pt', action_type='compile')
        self.assertIn('confirmada', msg)
        self.assertIn('compile', msg)
    
    def test_get_message_english(self):
        """Deve retornar mensagem em inglês"""
        msg = get_message('action_confirmed', 'en', action_type='compile')
        self.assertIn('confirmed', msg)
        self.assertIn('compile', msg)
    
    def test_get_message_spanish(self):
        """Deve retornar mensagem em espanhol"""
        msg = get_message('action_confirmed', 'es', action_type='compile')
        self.assertIn('confirmada', msg)
        self.assertIn('compile', msg)
    
    def test_get_message_fallback_to_portuguese(self):
        """Deve usar português como fallback para idioma inválido"""
        msg = get_message('action_confirmed', 'fr', action_type='test')
        self.assertIn('confirmada', msg)  # Português
    
    def test_get_message_with_parameters(self):
        """Deve formatar mensagem com parâmetros"""
        msg = get_message('snippet_too_large', 'en', max_size=10)
        self.assertIn('10', msg)
        self.assertIn('KB', msg)
    
    def test_get_message_missing_key(self):
        """Deve retornar mensagem de erro para chave inexistente"""
        msg = get_message('nonexistent_key', 'pt')
        self.assertIn('Missing translation', msg)
    
    def test_detect_language_from_payload(self):
        """Deve detectar idioma do payload"""
        payload = {'lang': 'es'}
        lang = detect_language(payload)
        self.assertEqual(lang, 'es')
    
    def test_detect_language_fallback(self):
        """Deve usar fallback se idioma inválido"""
        payload = {'lang': 'invalid'}
        lang = detect_language(payload, default='en')
        self.assertEqual(lang, 'en')
    
    def test_available_languages(self):
        """Deve retornar idiomas disponíveis"""
        langs = get_available_languages()
        self.assertIn('pt', langs)
        self.assertIn('en', langs)
        self.assertIn('es', langs)
    
    def test_security_messages_all_languages(self):
        """Deve ter mensagens de segurança em todos os idiomas"""
        keys = ['dangerous_command', 'user_not_authenticated', 'no_permission']
        
        for key in keys:
            for lang in ['pt', 'en', 'es']:
                msg = get_message(key, lang)
                self.assertNotIn('Missing translation', msg)
                self.assertNotIn('[', msg)

class TestLLMClient(unittest.TestCase):
    
    def test_offline_mode_default(self):
        """Deve estar em modo offline por padrão"""
        client = LLMClient()
        self.assertEqual(client.mode, LLMMode.OFFLINE)
        self.assertFalse(client.is_enabled())
    
    def test_rules_based_response_portuguese(self):
        """Deve gerar resposta em português"""
        client = LLMClient()
        response = client.generate_response("olá", language='pt')
        
        self.assertIn('text', response)
        self.assertIn('Olá', response['text'])
        self.assertEqual(response['source'], 'rules')
    
    def test_rules_based_response_english(self):
        """Deve gerar resposta em inglês"""
        client = LLMClient()
        response = client.generate_response("hello", language='en')
        
        self.assertIn('Hello', response['text'])
        self.assertEqual(response['source'], 'rules')
    
    def test_rules_based_response_spanish(self):
        """Deve gerar resposta em espanhol"""
        client = LLMClient()
        response = client.generate_response("hola", language='es')
        
        self.assertIn('Hola', response['text'])
        self.assertEqual(response['source'], 'rules')
    
    def test_help_command_portuguese(self):
        """Deve responder comando de ajuda em português"""
        client = LLMClient()
        response = client.generate_response("ajuda", language='pt')
        
        self.assertIn('Posso ajudar', response['text'])
        self.assertIn('snippets', response['text'].lower())
    
    def test_help_command_english(self):
        """Deve responder comando de ajuda em inglês"""
        client = LLMClient()
        response = client.generate_response("help", language='en')
        
        self.assertIn('can help', response['text'])
        self.assertIn('snippets', response['text'].lower())
    
    def test_compile_suggestion_portuguese(self):
        """Deve sugerir compilação em português"""
        client = LLMClient()
        response = client.generate_response("como compilar?", language='pt')
        
        self.assertIn('compilar', response['text'].lower())
        self.assertEqual(len(response['actions']), 1)
        self.assertEqual(response['actions'][0]['type'], 'suggest_compile')
    
    def test_bibtex_suggestion_english(self):
        """Deve sugerir BibTeX em inglês"""
        client = LLMClient()
        response = client.generate_response("how to add citation?", language='en')
        
        self.assertIn('bibtex', response['text'].lower())
        self.assertEqual(response['actions'][0]['type'], 'suggest_bibtex')
    
    def test_lint_suggestion_spanish(self):
        """Deve sugerir lint em espanhol"""
        client = LLMClient()
        response = client.generate_response("verificar errores", language='es')
        
        self.assertIn('lint', response['text'].lower())
        self.assertEqual(response['actions'][0]['type'], 'suggest_lint')
    
    def test_unknown_command_fallback(self):
        """Deve ter fallback para comandos desconhecidos"""
        client = LLMClient()
        response = client.generate_response("xyzabc123", language='pt')
        
        self.assertIn('não entendi', response['text'].lower())
        self.assertEqual(len(response['actions']), 0)
        self.assertLess(response['confidence'], 0.5)
    
    def test_confidence_scores(self):
        """Deve retornar scores de confiança apropriados"""
        client = LLMClient()
        
        # Alta confiança para saudação
        response1 = client.generate_response("olá", language='pt')
        self.assertEqual(response1['confidence'], 1.0)
        
        # Baixa confiança para desconhecido
        response2 = client.generate_response("asdfghjkl", language='pt')
        self.assertLess(response2['confidence'], 0.5)
    
    def test_context_ignored_in_offline_mode(self):
        """Modo offline deve funcionar sem contexto"""
        client = LLMClient()
        response = client.generate_response(
            "help",
            context={'file': 'test.tex', 'project': 123},
            language='en'
        )
        
        self.assertIn('can help', response['text'])
        # Não deve dar erro mesmo com contexto

class TestPermissionsI18n(unittest.TestCase):
    
    def test_permission_denied_messages(self):
        """Mensagens de permissão negada em todos os idiomas"""
        for lang in ['pt', 'en', 'es']:
            msg = get_message('no_permission', lang)
            self.assertNotIn('Missing', msg)
            
            if lang == 'pt':
                self.assertIn('permissão', msg)
            elif lang == 'en':
                self.assertIn('permission', msg)
            elif lang == 'es':
                self.assertIn('permiso', msg)
    
    def test_compilation_error_messages(self):
        """Mensagens de erro de compilação em todos os idiomas"""
        for lang in ['pt', 'en', 'es']:
            msg = get_message('compilation_failed', lang, count=5)
            self.assertIn('5', msg)
            
            if lang == 'pt':
                self.assertIn('falhou', msg)
            elif lang == 'en':
                self.assertIn('failed', msg)
            elif lang == 'es':
                self.assertIn('falló', msg)

if __name__ == '__main__':
    unittest.main()



