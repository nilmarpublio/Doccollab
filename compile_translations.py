#!/usr/bin/env python
"""Compile translation files."""
import os
from babel.messages import pofile, mofile

def compile_translations():
    languages = ['en', 'es', 'pt']
    
    for lang in languages:
        po_file = f'translations/{lang}/LC_MESSAGES/messages.po'
        mo_file = f'translations/{lang}/LC_MESSAGES/messages.mo'
        
        print(f'Compilando {lang}...')
        
        with open(po_file, 'rb') as f:
            catalog = pofile.read_po(f, locale=lang)
        
        with open(mo_file, 'wb') as f:
            mofile.write_mo(f, catalog)
        
        print(f'✓ {lang} compilado: {mo_file}')
    
    print('\n✅ Todas as traduções compiladas!')

if __name__ == '__main__':
    compile_translations()
