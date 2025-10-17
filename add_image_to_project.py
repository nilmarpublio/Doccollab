#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para adicionar imagem ao projeto
"""

from app import app, db, Project, ProjectFile
import os

def add_image_to_project(project_id, image_filename):
    """Adiciona uma imagem ao projeto no banco de dados"""
    
    with app.app_context():
        project = Project.query.get(project_id)
        
        if not project:
            print(f"[ERRO] Projeto {project_id} nao encontrado")
            return
        
        # Verificar se imagem já existe no banco
        existing = ProjectFile.query.filter_by(
            project_id=project_id,
            name=image_filename
        ).first()
        
        if existing:
            print(f"[INFO] Imagem {image_filename} ja existe no banco")
            return
        
        # Caminho da imagem
        image_path = f"/imagens/{image_filename}"
        full_path = os.path.join('uploads', f'project_{project_id}', 'imagens', image_filename)
        
        # Verificar se arquivo existe
        if not os.path.exists(full_path):
            print(f"[ERRO] Arquivo nao encontrado: {full_path}")
            return
        
        # Obter tamanho
        size = os.path.getsize(full_path)
        
        # Criar registro no banco
        image_file = ProjectFile(
            project_id=project_id,
            name=image_filename,
            path=image_path,
            file_type='image',
            size=size,
            content=None,  # Imagens não têm conteúdo de texto
            file_path=image_path  # Caminho relativo
        )
        
        db.session.add(image_file)
        db.session.commit()
        
        print(f"[OK] Imagem {image_filename} adicionada ao projeto {project_id} ({project.name})")
        print(f"     Caminho: {image_path}")
        print(f"     Tamanho: {size} bytes")

if __name__ == '__main__':
    print("Adicionando imagem ao projeto...")
    add_image_to_project(1, 'frog.png')
    print("Concluido!")






