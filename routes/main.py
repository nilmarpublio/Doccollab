from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, abort, jsonify
from flask_login import login_required, current_user
from models import db
from models.project import Project
from utils.file_ops import ensure_project_dir, create_main_tex, rename_project_dir, trash_project_dir
from utils.permissions import require_paid_plan, require_project_limit, require_file_limit, check_plan_limits
from services.latex import compile_latex_to_pdf
from services.latex_compiler import compile_with_pdflatex
import os
import json
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id, is_active=True).order_by(Project.updated_at.desc()).all()
    return render_template('dashboard.html', projects=projects)

@main_bp.route('/create-project', methods=['POST'])
@login_required
@require_project_limit
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        flash('Nome do projeto é obrigatório.', 'warning')
        return redirect(url_for('main.dashboard'))

    if Project.query.filter_by(user_id=current_user.id, name=name, is_active=True).first():
        flash('Já existe um projeto com esse nome.', 'warning')
        return redirect(url_for('main.dashboard'))

    p = Project(name=name, description=description, user_id=current_user.id)
    db.session.add(p)
    db.session.commit()

    # filesystem
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, name)
    create_main_tex(project_path)

    flash('Projeto criado com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/delete-project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('main.dashboard'))

    ok, err = trash_project_dir(current_app.config['PROJECTS_ROOT'], current_app.config['TRASH_ROOT'], current_user.id, project.name)
    if not ok:
        flash('Erro ao mover diretório do projeto.', 'danger')
        return redirect(url_for('main.dashboard'))

    project.is_active = False
    db.session.commit()
    flash('Projeto excluído.', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/rename-project/<int:project_id>', methods=['POST'])
@login_required
def rename_project(project_id):
    new_name = request.form.get('new_name')
    if not new_name:
        flash('Novo nome é obrigatório.', 'warning')
        return redirect(url_for('main.dashboard'))

    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('main.dashboard'))

    if Project.query.filter_by(user_id=current_user.id, name=new_name, is_active=True).first():
        flash('Já existe um projeto com esse nome.', 'warning')
        return redirect(url_for('main.dashboard'))

    ok, err = rename_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name, new_name)
    if not ok:
        if err == 'old_not_found':
            flash('Diretório do projeto não encontrado.', 'danger')
        elif err == 'new_already_exists':
            flash('Diretório de destino já existe.', 'danger')
        else:
            flash('Erro ao renomear diretório do projeto.', 'danger')
        return redirect(url_for('main.dashboard'))

    project.name = new_name
    db.session.commit()
    flash('Projeto renomeado com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/editor/<int:project_id>')
@login_required
def editor(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        flash('Projeto não encontrado.', 'danger')
        return redirect(url_for('main.dashboard'))
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    main_tex_path = os.path.join(project_path, 'main.tex')
    content = ''
    if os.path.exists(main_tex_path):
        with open(main_tex_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    return render_template('editor.html', project=project, content=content)


@main_bp.route('/project/<int:project_id>/save', methods=['POST'])
@login_required
def api_save(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return {'ok': False, 'error': 'not_found'}, 404
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    main_tex_path = os.path.join(project_path, 'main.tex')
    with open(main_tex_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return {'success': True}


@main_bp.route('/project/<int:project_id>/compile', methods=['POST'])
@login_required
def api_compile(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return {'success': False, 'error': 'not_found'}, 404
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    
    # Get the main file for compilation
    from services.latex_compiler import get_main_file
    main_file = get_main_file(project_path)
    main_tex_path = os.path.join(project_path, main_file)
    
    # Prefer local pdflatex binary if available; fallback to existing service
    ok, pdf_path, err = compile_with_pdflatex(main_tex_path)
    if not ok:
        # fallback to previous implementation (uses config/env too)
        ok, pdf_path, err = compile_latex_to_pdf(project_path)
    if not ok:
        # Log server-side for troubleshooting
        try:
            print(f"[pdflatex] compile error: {err}")
        except Exception:
            pass
        return {'success': False, 'error': err}, 400
    return {'success': True}


@main_bp.route('/project/<int:project_id>/content')
@login_required
def get_project_content(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return {'success': False, 'error': 'Project not found'}, 404
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    main_tex_path = os.path.join(project_path, 'main.tex')
    
    content = ''
    if os.path.exists(main_tex_path):
        try:
            with open(main_tex_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'success': False, 'error': f'Error reading file: {str(e)}'}, 500
    
    return {'success': True, 'content': content}


@main_bp.route('/project/<int:project_id>/pdf')
@login_required
def get_pdf(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        abort(404)
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    pdf_path = os.path.join(project_path, 'main.pdf')
    if not os.path.exists(pdf_path):
        abort(404)
    return send_file(pdf_path, mimetype='application/pdf')


# File Management Endpoints
@main_bp.route('/project/<int:project_id>/files')
@login_required
def get_project_files(project_id):
    """Get list of files in project directory"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    
    files = []
    try:
        for item in os.listdir(project_path):
            item_path = os.path.join(project_path, item)
            if os.path.isfile(item_path):
                file_info = {
                    'name': item,
                    'type': 'file',
                    'extension': os.path.splitext(item)[1].lower(),
                    'size': os.path.getsize(item_path),
                    'modified': os.path.getmtime(item_path)
                }
                files.append(file_info)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
    # Sort files: .tex first, then others
    tex_files = [f for f in files if f['extension'] == '.tex']
    other_files = [f for f in files if f['extension'] != '.tex']
    files = tex_files + other_files
    
    return jsonify({'success': True, 'files': files})


@main_bp.route('/project/<int:project_id>/files/create', methods=['POST'])
@login_required
@require_file_limit('project_id')
def create_file(project_id):
    """Create a new file in project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    data = request.get_json()
    filename = data.get('filename', '').strip()
    file_type = data.get('type', 'tex')  # tex, image, bib
    
    if not filename:
        return jsonify({'success': False, 'error': 'Filename is required'}), 400
    
    # Add extension if not provided
    if file_type == 'tex' and not filename.endswith('.tex'):
        filename += '.tex'
    elif file_type == 'bib' and not filename.endswith('.bib'):
        filename += '.bib'
    
    # Secure filename
    filename = secure_filename(filename)
    if not filename:
        return jsonify({'success': False, 'error': 'Invalid filename'}), 400
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, filename)
    
    if os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File already exists'}), 400
    
    try:
        # Create file with default content based on type
        if file_type == 'tex':
            content = '\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\n\\begin{document}\n\n\\end{document}'
        elif file_type == 'bib':
            content = '@article{example,\n  title={Example Article},\n  author={Author Name},\n  journal={Journal Name},\n  year={2024}\n}'
        else:
            content = ''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/files/rename', methods=['POST'])
@login_required
@require_paid_plan
def rename_file(project_id):
    """Rename a file in project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    data = request.get_json()
    old_name = data.get('old_name', '').strip()
    new_name = data.get('new_name', '').strip()
    
    if not old_name or not new_name:
        return jsonify({'success': False, 'error': 'Both old and new names are required'}), 400
    
    old_name = secure_filename(old_name)
    new_name = secure_filename(new_name)
    
    if not old_name or not new_name:
        return jsonify({'success': False, 'error': 'Invalid filename'}), 400
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    old_path = os.path.join(project_path, old_name)
    new_path = os.path.join(project_path, new_name)
    
    if not os.path.exists(old_path):
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    if os.path.exists(new_path):
        return jsonify({'success': False, 'error': 'File with new name already exists'}), 400
    
    try:
        os.rename(old_path, new_path)
        return jsonify({'success': True, 'new_name': new_name})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/files/delete', methods=['POST'])
@login_required
@require_paid_plan
def delete_file(project_id):
    """Delete a file from project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    data = request.get_json()
    filename = data.get('filename', '').strip()
    
    if not filename:
        return jsonify({'success': False, 'error': 'Filename is required'}), 400
    
    filename = secure_filename(filename)
    if not filename:
        return jsonify({'success': False, 'error': 'Invalid filename'}), 400
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    try:
        os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/files/upload', methods=['POST'])
@login_required
@require_paid_plan
def upload_file(project_id):
    """Upload a file to project"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({'success': False, 'error': 'Invalid filename'}), 400
    
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, filename)
    
    if os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File already exists'}), 400
    
    try:
        file.save(file_path)
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/files/<filename>')
@login_required
def get_file_content(project_id, filename):
    """Get content of a specific file"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    filename = secure_filename(filename)
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, filename)
    
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File not found'}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return jsonify({'success': True, 'content': content, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/files/<filename>/save', methods=['POST'])
@login_required
def save_file_content(project_id, filename):
    """Save content to a specific file"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    data = request.get_json()
    content = data.get('content', '')
    
    filename = secure_filename(filename)
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, filename)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/project/<int:project_id>/main-file', methods=['POST'])
@login_required
def set_main_file(project_id):
    """Set which .tex file is the main file for compilation"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id, is_active=True).first()
    if not project:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    data = request.get_json()
    main_file = data.get('main_file', 'main.tex')
    
    # Validate that the file exists and is a .tex file
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    file_path = os.path.join(project_path, main_file)
    
    if not os.path.exists(file_path) or not main_file.endswith('.tex'):
        return jsonify({'success': False, 'error': 'Invalid main file'}), 400
    
    # Store main file in project metadata (you might want to add this to Project model)
    # For now, we'll use a simple approach
    try:
        # Create a .mainfile file to store the main file name
        main_file_path = os.path.join(project_path, '.mainfile')
        with open(main_file_path, 'w') as f:
            f.write(main_file)
        
        return jsonify({'success': True, 'main_file': main_file})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@main_bp.route('/plan-info')
@login_required
def get_plan_info():
    """Get current user's plan information and limits"""
    limits = check_plan_limits()
    subscription = current_user.get_subscription()
    
    return jsonify({
        'success': True,
        'plan_type': subscription.plan_type.value,
        'is_paid': subscription.is_paid,
        'limits': limits
    })
