#!/usr/bin/env python3
"""
Teste específico para verificar detecção de idioma
"""

from app import create_app
from flask_babel import gettext as _, force_locale

def test_language_detection():
    """Testa a detecção de idioma"""
    
    app = create_app()
    
    with app.app_context():
        # Teste 1: Sem parâmetros
        with app.test_request_context():
            print("=== TESTE 1: SEM PARÂMETROS ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
        
        # Teste 2: Com parâmetro na URL
        with app.test_request_context('/?lang=en'):
            print("\n=== TESTE 2: COM PARÂMETRO ?lang=en ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
        
        # Teste 3: Com parâmetro na URL pt
        with app.test_request_context('/?lang=pt'):
            print("\n=== TESTE 3: COM PARÂMETRO ?lang=pt ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
        
        # Teste 4: Com sessão
        with app.test_request_context() as ctx:
            from flask import session
            session['lang'] = 'en'
            print("\n=== TESTE 4: COM SESSÃO lang=en ===")
            print(f"Home: {_('Home')}")
            print(f"Sign in: {_('Sign in')}")
        
        # Teste 5: Verificar função get_locale
        with app.test_request_context('/?lang=en'):
            from flask import request
            print(f"\n=== TESTE 5: get_locale() com ?lang=en ===")
            print(f"get_locale(): {app.get_locale()}")
            print(f"request.args.get('lang'): {request.args.get('lang')}")

if __name__ == "__main__":
    test_language_detection()
