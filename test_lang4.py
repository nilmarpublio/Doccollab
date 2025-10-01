#!/usr/bin/env python3
"""
Teste para verificar configuração do Flask-Babel
"""

from app import create_app
from flask_babel import gettext as _, force_locale, get_locale as babel_get_locale

def test_babel_config():
    """Testa a configuração do Flask-Babel"""
    
    app = create_app()
    
    with app.app_context():
        # Teste 1: Verificar locale atual
        with app.test_request_context('/?lang=en'):
            print("=== TESTE 1: VERIFICAR LOCALE ===")
            print(f"app.get_locale(): {app.get_locale()}")
            print(f"babel_get_locale(): {babel_get_locale()}")
            print(f"Home: {_('Home')}")
        
        # Teste 2: Forçar locale
        with app.test_request_context('/?lang=en'):
            with force_locale('en'):
                print("\n=== TESTE 2: FORÇAR LOCALE EN ===")
                print(f"babel_get_locale(): {babel_get_locale()}")
                print(f"Home: {_('Home')}")
        
        # Teste 3: Verificar se arquivos .mo existem
        import os
        project_dir = os.path.dirname(os.path.abspath(__file__))
        en_mo = os.path.join(project_dir, 'translations', 'en', 'LC_MESSAGES', 'messages.mo')
        pt_mo = os.path.join(project_dir, 'translations', 'pt', 'LC_MESSAGES', 'messages.mo')
        
        print(f"\n=== TESTE 3: VERIFICAR ARQUIVOS .mo ===")
        print(f"EN .mo existe: {os.path.exists(en_mo)}")
        print(f"PT .mo existe: {os.path.exists(pt_mo)}")
        
        # Teste 4: Verificar conteúdo dos arquivos .mo
        if os.path.exists(en_mo):
            import polib
            po = polib.pofile(en_mo)
            home_entry = po.find('Home')
            if home_entry:
                print(f"EN Home: '{home_entry.msgstr}'")
            else:
                print("EN Home: não encontrado")
        
        if os.path.exists(pt_mo):
            import polib
            po = polib.pofile(pt_mo)
            home_entry = po.find('Home')
            if home_entry:
                print(f"PT Home: '{home_entry.msgstr}'")
            else:
                print("PT Home: não encontrado")

if __name__ == "__main__":
    test_babel_config()
