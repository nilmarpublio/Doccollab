#!/usr/bin/env python3
"""
Script para compilar traduções usando Python
"""

import os
import polib

def compile_translations():
    """Compila as traduções do projeto"""
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(project_dir, 'translations')
    
    print("Compilando traducoes...")
    
    for lang in ['pt', 'en', 'es']:
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        mo_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')
        
        if os.path.exists(po_file):
            try:
                # Carregar arquivo .po
                po = polib.pofile(po_file)
                
                # Salvar como .mo
                po.save_as_mofile(mo_file)
                
                print(f"Traducao {lang} compilada com sucesso")
            except Exception as e:
                print(f"Erro ao compilar {lang}: {e}")
        else:
            print(f"Arquivo {po_file} nao encontrado")
    
    print("Compilacao concluida!")

if __name__ == "__main__":
    compile_translations()
