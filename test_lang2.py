#!/usr/bin/env python3
"""
Teste mais específico para verificar traduções
"""

from app import create_app
from flask_babel import gettext as _, force_locale

def test_translations():
    """Testa as traduções com contexto específico"""
    
    app = create_app()
    
    with app.app_context():
        with app.test_request_context():
            print("=== TESTE SEM SESSÃO ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
            
            # Testar com locale forçado
            print("\n=== TESTE COM LOCALE FORÇADO ===")
            with force_locale('en'):
                print(f"Home (EN): {_('Home')}")
                print(f"Sign in (EN): {_('Sign in')}")
            
            with force_locale('pt'):
                print(f"Home (PT): {_('Home')}")
                print(f"Sign in (PT): {_('Sign in')}")
            
            # Testar mudança de sessão
            print("\n=== TESTE COM MUDANÇA DE SESSÃO ===")
            from flask import session
            session['lang'] = 'en'
            
            # Recriar contexto para forçar reload
            with app.test_request_context():
                print(f"Home (sessão EN): {_('Home')}")
                print(f"Sign in (sessão EN): {_('Sign in')}")

if __name__ == "__main__":
    test_translations()
