from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, abort
from flask_login import login_required, current_user
from models import db
from models.project import Project
from utils.file_ops import ensure_project_dir, create_main_tex, rename_project_dir, trash_project_dir
from services.latex import compile_latex_to_pdf
import os

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
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')

    if not name:
        flash('Nome do projeto é obrigatório.', 'warning')
        return redirect(url_for('main.dashboard'))

    if not current_user.can_create_project():
        flash('Limite de projetos atingido no plano gratuito. Faça upgrade.', 'warning')
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
        return {'ok': False, 'error': 'not_found'}, 404
    project_path = ensure_project_dir(current_app.config['PROJECTS_ROOT'], current_user.id, project.name)
    ok, pdf_path, err = compile_latex_to_pdf(project_path)
    if not ok:
        # Log server-side for troubleshooting
        try:
            print(f"[pdflatex] compile error: {err}")
        except Exception:
            pass
        return {'success': False, 'error': err}, 400
    return {'success': True}


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
