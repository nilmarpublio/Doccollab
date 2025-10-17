#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para sincronizar main.tex com o banco de dados
"""

from app import app, db, Project, ProjectFile
import os

def sync_main_tex(project_id):
    """Sincroniza main.tex do sistema de arquivos com o banco"""
    
    with app.app_context():
        project = Project.query.filter_by(id=project_id).first()
        
        if not project:
            print(f"[ERRO] Projeto {project_id} nao encontrado")
            return
        
        # Caminho do arquivo
        file_path = os.path.join('uploads', f'project_{project_id}', 'main.tex')
        
        if not os.path.exists(file_path):
            print(f"[ERRO] Arquivo nao encontrado: {file_path}")
            return
        
        # Ler conteúdo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        size = os.path.getsize(file_path)
        
        # Verificar se já existe no banco
        existing = ProjectFile.query.filter_by(
            project_id=project_id,
            name='main.tex'
        ).first()
        
        if existing:
            # Atualizar
            existing.content = content
            existing.size = size
            print(f"[OK] main.tex atualizado no banco de dados")
        else:
            # Criar novo
            main_file = ProjectFile(
                project_id=project_id,
                name='main.tex',
                path='/main.tex',
                file_type='tex',
                size=size,
                content=content
            )
            db.session.add(main_file)
            print(f"[OK] main.tex criado no banco de dados")
        
        db.session.commit()
        print(f"     Projeto: {project.name}")
        print(f"     Tamanho: {size} bytes")
        print(f"     Linhas: {len(content.splitlines())}")

if __name__ == '__main__':
    print("Sincronizando main.tex...")
    sync_main_tex(1)
    print("Concluido!")






