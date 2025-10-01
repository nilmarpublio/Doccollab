#!/usr/bin/env python3
"""
Script para corrigir as traduções do DocCollab
"""

import os
import subprocess

def fix_translations():
    """Corrige as traduções do projeto"""
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(project_dir, 'translations')
    
    print("Corrigindo traducoes do DocCollab...")
    
    # Traduções em português
    pt_translations = {
        "Home": "Início",
        "Sign in": "Entrar", 
        "Sign up": "Cadastrar",
        "Language": "Idioma",
        "Sign out": "Sair",
        "Dashboard": "Painel",
        "Upgrade Plan": "Upgrade do Plano",
        "Email": "E-mail",
        "Password": "Senha",
        "Full name": "Nome completo",
        "Confirm password": "Confirmar senha",
        "Create account": "Criar conta",
        "Already have an account?": "Já tem uma conta?",
        "No account?": "Não tem conta?",
        "My Projects": "Meus Projetos",
        "Create New Project": "Criar Novo Projeto",
        "Project Name": "Nome do Projeto",
        "Description": "Descrição",
        "Create": "Criar",
        "Edit": "Editar",
        "Delete": "Excluir",
        "Open": "Abrir",
        "Free Plan": "Plano Gratuito",
        "Paid Plan": "Plano Pago",
        "Files": "Arquivos",
        "Save": "Salvar",
        "Compile PDF": "Compilar PDF",
        "Auto-save:": "Salvamento automático:",
        "Enabled": "Habilitado",
        "Disabled": "Desabilitado"
    }
    
    # Atualizar arquivo .po em português
    pt_po_file = os.path.join(translations_dir, 'pt', 'LC_MESSAGES', 'messages.po')
    
    if os.path.exists(pt_po_file):
        with open(pt_po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar traduções que estão faltando
        for msgid, msgstr in pt_translations.items():
            if f'msgid "{msgid}"' in content and f'msgstr "{msgstr}"' not in content:
                # Encontrar a linha msgid e adicionar msgstr
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == f'msgid "{msgid}"':
                        # Verificar se já tem msgstr
                        if i + 1 < len(lines) and lines[i + 1].startswith('msgstr'):
                            lines[i + 1] = f'msgstr "{msgstr}"'
                        else:
                            lines.insert(i + 1, f'msgstr "{msgstr}"')
                        break
                content = '\n'.join(lines)
        
        with open(pt_po_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Traducoes em portugues atualizadas")
    
    # Compilar traduções
    try:
        for lang in ['pt', 'en', 'es']:
            po_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.po')
            mo_file = os.path.join(translations_dir, lang, 'LC_MESSAGES', 'messages.mo')
            
            if os.path.exists(po_file):
                # Compilar usando msgfmt
                result = subprocess.run(['msgfmt', po_file, '-o', mo_file], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Traducao {lang} compilada")
                else:
                    print(f"Erro ao compilar {lang}: {result.stderr}")
    except FileNotFoundError:
        print("msgfmt nao encontrado. Instale gettext para compilar traducoes.")
    
    print("Traducoes corrigidas!")

if __name__ == "__main__":
    fix_translations()
