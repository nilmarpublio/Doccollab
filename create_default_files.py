#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar arquivo main.tex padrão em projetos existentes
"""

from app import app, db, Project, ProjectFile
import os

def create_default_main_tex():
    """Cria arquivo main.tex padrão em todos os projetos que não têm"""
    
    with app.app_context():
        projects = Project.query.all()
        
        for project in projects:
            # Verificar se já tem um main.tex
            existing = ProjectFile.query.filter_by(
                project_id=project.id,
                name='main.tex'
            ).first()
            
            if existing:
                print(f"Projeto {project.id} ({project.name}) já tem main.tex")
                continue
            
            # Criar main.tex padrão
            content = f"""% {project.name}
\\documentclass[12pt,a4paper]{{article}}

% Pacotes essenciais
\\usepackage[utf8]{{inputenc}}
\\usepackage[portuguese]{{babel}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}

% Informações do documento
\\title{{{project.name}}}
\\author{{Seu Nome}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section{{Introdução}}

Este é o documento principal do projeto {project.name}.

\\section{{Desenvolvimento}}

Escreva seu conteúdo aqui.

\\section{{Conclusão}}

Conclusão do documento.

\\end{{document}}"""
            
            # Criar arquivo no banco
            main_file = ProjectFile(
                project_id=project.id,
                name='main.tex',
                path='/main.tex',
                file_type='tex',
                size=len(content.encode('utf-8')),
                content=content
            )
            
            db.session.add(main_file)
            db.session.commit()
            
            print(f"[OK] Criado main.tex para projeto {project.id} ({project.name})")

if __name__ == '__main__':
    print("Criando arquivos main.tex padrão...")
    create_default_main_tex()
    print("Concluído!")
