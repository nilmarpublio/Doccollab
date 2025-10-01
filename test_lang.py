#!/usr/bin/env python3
"""
Teste para verificar se as traduções estão funcionando
"""

from app import create_app
from flask_babel import gettext as _

def test_translations():
    """Testa as traduções"""
    
    app = create_app()
    
    with app.app_context():
        # Testar diferentes idiomas
        with app.test_request_context():
            # Português (padrão)
            print("=== PORTUGUES ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
            print(f"Sign up: {_('Sign up')}")
            print(f"Language: {_('Language')}")
            
            # Simular mudança para inglês
            from flask import session
            session['lang'] = 'en'
            
            print("\n=== ENGLISH ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
            print(f"Sign up: {_('Sign up')}")
            print(f"Language: {_('Language')}")

if __name__ == "__main__":
    test_translations()
