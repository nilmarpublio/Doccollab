#!/usr/bin/env python3
"""
Script para atualizar as traduções do DocCollab
Execute este script para extrair strings e compilar traduções
"""

import os
import sys
from babel.messages.frontend import extract_messages, update_catalog, compile_catalog

def update_translations():
    """Atualiza as traduções do projeto"""
    
    # Configurações
    project_name = 'DocCollab'
    version = '1.0'
    copyright_holder = 'DocCollab Team'
    email = 'team@doccollab.com'
    
    # Diretórios
    project_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(project_dir, 'translations')
    pot_file = os.path.join(translations_dir, 'messages.pot')
    
    print("🌐 Atualizando traduções do DocCollab...")
    
    # 1. Extrair mensagens do código
    print("📝 Extraindo mensagens...")
    extract_messages(
        input_dirs=[project_dir],
        output_file=pot_file,
        project=project_name,
        version=version,
        copyright_holder=copyright_holder,
        msgid_bugs_address=email,
        mapping_file=os.path.join(project_dir, 'babel.cfg')
    )
    
    # 2. Atualizar catálogos para cada idioma
    languages = ['pt', 'en', 'es']
    for lang in languages:
        print(f"🔄 Atualizando catálogo para {lang}...")
        po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
        
        update_catalog(
            input_file=pot_file,
            output_dir=translations_dir,
            locale=lang,
            domain='messages'
        )
    
    # 3. Compilar catálogos
    for lang in languages:
        print(f"🔨 Compilando catálogo para {lang}...")
        compile_catalog(
            directory=translations_dir,
            locale=lang,
            domain='messages'
        )
    
    print("✅ Traduções atualizadas com sucesso!")

if __name__ == "__main__":
    update_translations()
