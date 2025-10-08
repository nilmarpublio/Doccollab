from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, send_from_directory, send_file, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext as _
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import re
import tempfile
import subprocess
import shutil
import uuid
import hashlib
import time
from collections import defaultdict
from latex_snippets import get_snippet, get_snippets_by_category, get_categories, process_snippet_placeholders
from services.latex_log_parser import parse_latex_log, format_error_message
from services.latex_refactors import PatchSanitizer, LaTeXRefactor, PatchApplier
from services.latex_linter import LaTeXLinter
from services.bibtex_generator import generate_bibtex_from_description
from services.file_manager import FileManager

# Criar app Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Configuração do Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en', 'es']

def get_locale():
    # Tentar pegar da sessão
    lang = session.get('language')
    print(f"[DEBUG] Idioma na sessão: {lang}")
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        print(f"[DEBUG] Usando idioma: {lang}")
        return lang
    # Se não tiver na sessão, usar o idioma do navegador
    default = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES']) or 'pt'
    print(f"[DEBUG] Usando idioma padrão: {default}")
    return default

babel = Babel(app, locale_selector=get_locale)

# Adicionar função _ ao contexto do Jinja2
app.jinja_env.globals.update(_=_)

# Configurações
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doccollab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância única do SQLAlchemy
db = SQLAlchemy(app)

# Configurar FileManager
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
file_manager = FileManager(UPLOAD_FOLDER)

# Definir modelos
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    files = db.relationship('ProjectFile', backref='project', lazy=True, cascade='all, delete-orphan')
    folders = db.relationship('ProjectFolder', backref='project', lazy=True, cascade='all, delete-orphan')

class ProjectFolder(db.Model):
    __tablename__ = 'project_folders'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('project_folders.id'), nullable=True)
    path = db.Column(db.String(500), nullable=False)  # Caminho completo: /imagens/figuras
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    children = db.relationship('ProjectFolder', backref=db.backref('parent', remote_side=[id]), lazy=True)
    files = db.relationship('ProjectFile', backref='folder', lazy=True)

class ProjectFile(db.Model):
    __tablename__ = 'project_files'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('project_folders.id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(500), nullable=False)  # Caminho completo: /imagens/logo.png
    file_type = db.Column(db.String(50))  # tex, png, jpg, pdf, bib, etc.
    size = db.Column(db.Integer, default=0)  # Tamanho em bytes
    content = db.Column(db.Text, nullable=True)  # Para arquivos de texto (.tex, .bib)
    file_path = db.Column(db.String(500), nullable=True)  # Caminho no sistema de arquivos (para binários)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    versions = db.relationship('FileVersion', backref='file', lazy=True, cascade='all, delete-orphan')

class FileVersion(db.Model):
    __tablename__ = 'file_versions'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('project_files.id'), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    size = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(500))  # Comentário da versão

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===== ROTAS PRINCIPAIS =====

@app.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    """Trocar idioma"""
    session['language'] = lang_code
    return redirect(request.referrer or url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'error')
            return render_template('auth/register.html')

        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do usuário"""
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard_simple.html', projects=projects)

@app.route('/pricing')
def pricing():
    """Página de preços"""
    return render_template('pricing.html')



# ===== ROTAS DE PROJETOS =====

# Página do editor LaTeX
@app.route('/editor')
@app.route('/editor/<int:project_id>')
@login_required
def editor_page(project_id=None):
    project = None
    if project_id:
        project = Project.query.get_or_404(project_id)
        # Verificar permissão
        if project.user_id != current_user.id:
            flash('Você não tem permissão para acessar este projeto.', 'error')
            return redirect(url_for('dashboard'))
    
    return render_template('editor_page.html', project=project)

@app.route('/view_pdf/<filename>')
@login_required
def view_pdf(filename):
    """Render PDF viewer page"""
    pdf_url = f'/uploads/{filename}'
    return render_template('pdf_viewer.html', pdf_url=pdf_url, filename=filename)

@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    """Criar novo projeto"""
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Nome do projeto é obrigatório!', 'error')
        return redirect(url_for('dashboard'))
    
    project = Project(name=name, description=description, user_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    
    flash('Projeto criado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    """Deletar projeto"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    
    if project:
        db.session.delete(project)
        db.session.commit()
        flash('Projeto deletado com sucesso!', 'success')
    else:
        flash('Projeto não encontrado!', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/rename_project/<int:project_id>', methods=['POST'])
@login_required
def rename_project(project_id):
    """Renomear projeto"""
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first()
    new_name = request.form.get('new_name')
    
    if project and new_name:
        project.name = new_name
        db.session.commit()
        flash('Projeto renomeado com sucesso!', 'success')
    else:
        flash('Erro ao renomear projeto!', 'error')
    
    return redirect(url_for('dashboard'))

# ===== API ROUTES FOR LATEX EDITOR =====

@app.route('/api/save-latex', methods=['POST'])
def save_latex():
    """Save LaTeX document"""
    try:
        data = request.get_json()
        filename = data.get('filename', 'document.tex')
        content = data.get('content', '')
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(app.root_path, 'uploads')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Save file
        file_path = os.path.join(uploads_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': 'Documento salvo com sucesso',
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/compile-latex', methods=['POST'])
def compile_latex():
    """Compile LaTeX document using pdflatex"""
    try:
        data = request.get_json()
        filename = data.get('filename', 'document')
        content = data.get('content', '')
        
        # Create temp directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write LaTeX file
            tex_file = os.path.join(temp_dir, f'{filename}.tex')
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Compile with pdflatex
            try:
                result = subprocess.run([
                    'pdflatex',
                    '-interaction=batchmode',
                    '-halt-on-error',
                    '-output-directory', temp_dir,
                    tex_file
                ], capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
                
                pdf_file = os.path.join(temp_dir, f'{filename}.pdf')
                
                if os.path.exists(pdf_file):
                    # Copy PDF to uploads directory
                    uploads_dir = os.path.join(app.root_path, 'uploads')
                    if not os.path.exists(uploads_dir):
                        os.makedirs(uploads_dir)
                    
                    final_pdf = os.path.join(uploads_dir, f'{filename}.pdf')
                    shutil.copy2(pdf_file, final_pdf)
                    
                    return jsonify({
                        'success': True,
                        'message': 'Compilação bem-sucedida',
                        'pdf_url': f'/uploads/{filename}.pdf',
                        'log': result.stdout
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'PDF não foi gerado',
                        'log': result.stdout + '\n' + result.stderr
                    })
                    
            except subprocess.TimeoutExpired:
                return jsonify({
                    'success': False,
                    'error': 'Timeout na compilação (máximo 60 segundos)'
                })
            except FileNotFoundError:
                return jsonify({
                    'success': False,
                    'error': 'pdflatex não encontrado. Instale o LaTeX no sistema.'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': f'Erro na compilação: {str(e)}'
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

# ============================================================================
# API - SNIPPETS LATEX
# ============================================================================

@app.route('/api/snippets', methods=['GET'])
@login_required
def get_snippets_api():
    """Retorna lista de snippets disponíveis"""
    try:
        category = request.args.get('category')
        snippets = get_snippets_by_category(category)
        
        # Formatar para resposta JSON
        result = []
        for snippet_id, snippet_data in snippets.items():
            result.append({
                'id': snippet_id,
                'name': snippet_data.get('name'),
                'description': snippet_data.get('description'),
                'category': snippet_data.get('category'),
                'content_preview': snippet_data.get('content', '')[:100] + '...'
            })
        
        return jsonify({
            'success': True,
            'snippets': result,
            'categories': get_categories()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/snippets/<snippet_id>', methods=['GET'])
@login_required
def get_snippet_api(snippet_id):
    """Retorna detalhes de um snippet específico"""
    try:
        snippet_data = get_snippet(snippet_id)
        
        if not snippet_data:
            return jsonify({'success': False, 'error': 'Snippet não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'snippet': {
                'id': snippet_id,
                **snippet_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - LINTER LATEX
# ============================================================================

@app.route('/api/lint', methods=['POST'])
@login_required
def lint_latex_api():
    """Executa lint em conteúdo LaTeX"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        filename = data.get('filename', 'main.tex')
        
        linter = LaTeXLinter()
        issues = linter.lint_content(content, filename)
        fixes = linter.generate_fixes(content)
        summary = linter.get_summary()
        
        return jsonify({
            'success': True,
            'issues': [issue.to_dict() for issue in issues],
            'fixes': fixes,
            'summary': summary,
            'message': f'Lint completo: {summary["total"]} issues encontrados'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Erro ao executar lint: {str(e)}'
        }), 500

@app.route('/api/lint/auto-fix', methods=['POST'])
@login_required
def lint_auto_fix_api():
    """Aplica correções automáticas do lint"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        fix_ids = data.get('fix_ids', [])  # IDs dos fixes a aplicar
        
        linter = LaTeXLinter()
        issues = linter.lint_content(content)
        fixes = linter.generate_fixes(content)
        
        # Filtrar fixes solicitados
        selected_fixes = [f for f in fixes if f.get('issue_id') in fix_ids] if fix_ids else fixes
        
        # Aplicar fixes em ordem reversa (de baixo para cima) para não afetar posições
        modified_content = content
        applied_fixes = []
        
        for fix in reversed(sorted(selected_fixes, key=lambda f: f.get('position', 0))):
            try:
                if fix['type'] == 'refactor':
                    from services.latex_refactors import PatchApplier
                    modified_content, metadata = PatchApplier.apply_patch(modified_content, {
                        'type': 'refactor',
                        'refactor_type': fix.get('refactor_type'),
                        'description': fix.get('description')
                    })
                    applied_fixes.append(fix['issue_id'])
                
                elif fix['type'] == 'insert':
                    pos = fix.get('position', 0)
                    content_to_insert = fix.get('content', '')
                    modified_content = modified_content[:pos] + content_to_insert + modified_content[pos:]
                    applied_fixes.append(fix['issue_id'])
                
                elif fix['type'] == 'replace_pattern':
                    pattern = fix.get('pattern')
                    replacement = fix.get('replacement')
                    modified_content = re.sub(pattern, replacement, modified_content, flags=re.MULTILINE)
                    applied_fixes.append(fix['issue_id'])
                    
            except Exception as e:
                print(f'[API] Erro ao aplicar fix {fix["issue_id"]}: {str(e)}')
        
        return jsonify({
            'success': True,
            'modified_content': modified_content,
            'applied_fixes': applied_fixes,
            'total_applied': len(applied_fixes),
            'message': f'{len(applied_fixes)} correções aplicadas com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Erro ao aplicar correções: {str(e)}'
        }), 500

# ============================================================================
# API - BIBTEX GENERATOR
# ============================================================================

@app.route('/api/generate-bibtex', methods=['POST'])
@login_required
def generate_bibtex_api():
    """Gera entrada BibTeX a partir de descrição"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        entry_type = data.get('entry_type')  # opcional
        existing_bib = data.get('existing_bib', '')  # .bib existente
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'Descrição é obrigatória'
            }), 400
        
        result = generate_bibtex_from_description(description, existing_bib, entry_type)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Erro ao gerar BibTeX: {str(e)}'
        }), 500

@app.route('/api/bib-file', methods=['GET', 'POST'])
@login_required
def bib_file_api():
    """Gerencia arquivo .bib do projeto"""
    try:
        # Caminho do .bib (poderia ser por projeto no futuro)
        bib_path = os.path.join(app.root_path, 'uploads', 'references.bib')
        
        if request.method == 'GET':
            # Ler .bib existente
            if os.path.exists(bib_path):
                with open(bib_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return jsonify({
                    'success': True,
                    'content': content,
                    'exists': True
                })
            else:
                return jsonify({
                    'success': True,
                    'content': '',
                    'exists': False
                })
        
        elif request.method == 'POST':
            # Adicionar entrada ao .bib
            data = request.get_json()
            bibtex_entry = data.get('bibtex_entry', '')
            mode = data.get('mode', 'append')  # 'append' ou 'replace'
            
            if not bibtex_entry:
                return jsonify({
                    'success': False,
                    'error': 'Entrada BibTeX é obrigatória'
                }), 400
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(bib_path), exist_ok=True)
            
            if mode == 'replace':
                # Substituir arquivo
                with open(bib_path, 'w', encoding='utf-8') as f:
                    f.write(bibtex_entry)
            else:
                # Adicionar ao final
                with open(bib_path, 'a', encoding='utf-8') as f:
                    if os.path.getsize(bib_path) > 0:
                        f.write('\n\n')
                    f.write(bibtex_entry)
            
            return jsonify({
                'success': True,
                'message': 'Entrada adicionada ao .bib',
                'path': bib_path
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Erro ao gerenciar .bib: {str(e)}'
        }), 500

@app.route('/api/open-file-manager', methods=['POST'])
def open_file_manager():
    """Abrir gerenciador de arquivos na pasta especificada"""
    try:
        data = request.get_json()
        path = data.get('path', './Arquivos')
        
        # Criar pasta se não existir
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
        # Abrir gerenciador de arquivos
        import subprocess
        import platform
        
        system = platform.system()
        
        if system == "Windows":
            # Windows - usar start para abrir pasta atual
            subprocess.run(['start', '.', '/max'], shell=True, check=True)
        elif system == "Darwin":
            # macOS - usar Finder
            subprocess.run(['open', os.path.abspath(path)], check=True)
        elif system == "Linux":
            # Linux - tentar diferentes gerenciadores
            try:
                subprocess.run(['xdg-open', os.path.abspath(path)], check=True)
            except:
                subprocess.run(['nautilus', os.path.abspath(path)], check=True)
        else:
            return jsonify({
                'success': False,
                'error': f'Sistema operacional não suportado: {system}'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'Gerenciador de arquivos aberto em: {os.path.abspath(path)}'
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao abrir gerenciador: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/static/sample.pdf')
def sample_pdf():
    """Serve sample PDF for demonstration"""
    try:
        # Criar um PDF de exemplo simples
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.colors import black, blue
        import io
        
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Título
        p.setFont("Helvetica-Bold", 18)
        p.setFillColor(blue)
        p.drawString(100, height - 80, "DocCollab - Editor LaTeX")
        
        # Subtítulo
        p.setFont("Helvetica", 14)
        p.setFillColor(black)
        p.drawString(100, height - 110, "Documento de Exemplo")
        
        # Linha separadora
        p.line(100, height - 130, width - 100, height - 130)
        
        # Conteúdo principal
        p.setFont("Helvetica", 12)
        y_pos = height - 160
        
        lines = [
            "Este é um PDF de exemplo gerado pelo DocCollab.",
            "",
            "Para compilar seu documento LaTeX, certifique-se de que:",
            "• O LaTeX está instalado no sistema",
            "• O pdflatex está disponível no PATH", 
            "• O documento LaTeX está bem formado",
            "",
            "Comandos LaTeX básicos:",
            "• \\textbf{texto} - Negrito",
            "• \\textit{texto} - Itálico", 
            "• \\underline{texto} - Sublinhado",
            "• \\section{título} - Seção",
            "• \\subsection{título} - Subseção",
            "• \\begin{equation}...\\end{equation} - Equação",
            "• \\begin{itemize}...\\end{itemize} - Lista",
            "• \\begin{table}...\\end{table} - Tabela",
            "",
            "Dicas importantes:",
            "• Use \\documentclass{article} no início",
            "• Sempre feche os ambientes com \\end{}",
            "• Use \\begin{document} e \\end{document}",
            "• Salve o arquivo com extensão .tex",
            "",
            "Se houver erros de compilação:",
            "• Verifique a sintaxe LaTeX",
            "• Certifique-se de que todos os \\begin{} têm \\end{}",
            "• Instale pacotes necessários com \\usepackage{}"
        ]
        
        for line in lines:
            if line.startswith("•"):
                p.setFont("Helvetica-Bold", 12)
                p.drawString(120, y_pos, line)
            elif line.startswith("Comandos") or line.startswith("Dicas") or line.startswith("Se houver"):
                p.setFont("Helvetica-Bold", 12)
                p.setFillColor(blue)
                p.drawString(100, y_pos, line)
                p.setFillColor(black)
            else:
                p.setFont("Helvetica", 12)
                p.drawString(100, y_pos, line)
            
            y_pos -= 20
            if y_pos < 100:  # Nova página se necessário
                p.showPage()
                y_pos = height - 50
        
        # Rodapé
        p.setFont("Helvetica", 10)
        p.setFillColor(blue)
        p.drawString(100, 50, "DocCollab - Editor LaTeX Profissional")
        p.drawString(100, 35, "Gerado automaticamente em caso de erro de compilação")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return send_file(buffer, as_attachment=False, download_name='sample.pdf', mimetype='application/pdf')
        
    except ImportError:
        # Fallback se reportlab não estiver instalado
        return jsonify({
            'error': 'ReportLab não instalado. Instale com: pip install reportlab',
            'message': 'PDF de exemplo não disponível'
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'Erro ao gerar PDF: {str(e)}',
            'message': 'Tente instalar o LaTeX no sistema'
        }), 500

# ============================================================================
# SOCKET.IO EVENTS - ASSISTENTE VIRTUAL
# ============================================================================

# Armazenar ações pendentes por sessão
pending_actions = {}

# Armazenar snapshots do documento por sessão
document_snapshots = {}

# Debounce de compilações por projeto (evitar spam)
compilation_timestamps = defaultdict(float)
COMPILATION_DEBOUNCE_SECONDS = 3

def generate_snapshot_id(content):
    """Gera ID único para snapshot baseado no conteúdo"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

def validate_snippet_permission(user_id, action_type, payload):
    """
    Valida se o usuário tem permissão para executar a ação
    
    Args:
        user_id: ID do usuário
        action_type: Tipo de ação
        payload: Dados da ação
    
    Returns:
        (bool, str): (é_válido, mensagem_erro)
    """
    # Validações básicas
    if not user_id:
        return False, "Usuário não autenticado"
    
        # Validar tipo de ação
        allowed_actions = ['insert_snippet', 'correct_latex', 'format', 'compile', 'analyze_errors', 'apply_patch', 'suggest_refactors', 'lint', 'generate_bibtex']
        if action_type not in allowed_actions:
            return False, f"Ação '{action_type}' não permitida"
    
    # Validar payload
    if action_type == 'insert_snippet':
        if 'snippet' not in payload and 'snippet_id' not in payload:
            return False, "Snippet não especificado"
        
        # Validar tamanho do snippet (max 10KB)
        snippet_content = payload.get('snippet', '')
        if len(snippet_content) > 10240:
            return False, "Snippet muito grande (máx 10KB)"
        
        # Validar caracteres perigosos
        dangerous_patterns = ['\\input{', '\\include{', '\\write18']
        for pattern in dangerous_patterns:
            if pattern in snippet_content:
                return False, f"Comando perigoso detectado: {pattern}"
    
    return True, ""

def verify_snapshot_integrity(client_snapshot_id, server_snapshot_id):
    """
    Verifica se o snapshot do cliente está sincronizado com o servidor
    
    Args:
        client_snapshot_id: ID do snapshot do cliente
        server_snapshot_id: ID do snapshot atual do servidor
    
    Returns:
        bool: True se sincronizado, False se há conflito
    """
    if not client_snapshot_id or not server_snapshot_id:
        return True  # Primeira edição, sem snapshot anterior
    
    return client_snapshot_id == server_snapshot_id

# ============================================================================
# API - GERENCIAMENTO DE ARQUIVOS E PASTAS
# ============================================================================

@app.route('/api/project/<int:project_id>/files', methods=['GET'])
@login_required
def get_project_files(project_id):
    """Lista todos os arquivos do projeto (formato simplificado para o editor)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Verificar permissão
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        # Buscar arquivos
        files = ProjectFile.query.filter_by(project_id=project_id).all()
        
        # Retornar no formato esperado pelo frontend
        return jsonify([{
            'id': f.id,
            'filename': f.name,
            'file_type': f.file_type,
            'size': f.size,
            'folder_id': f.folder_id,
            'version': f.version,
            'created_at': f.created_at.isoformat(),
            'updated_at': f.updated_at.isoformat()
        } for f in files])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/folder', methods=['POST'])
@login_required
def create_folder(project_id):
    """Cria uma nova pasta no projeto"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        data = request.get_json()
        folder_name = data.get('name', '').strip()
        parent_id = data.get('parent_id')
        
        if not folder_name:
            return jsonify({'success': False, 'error': 'Nome da pasta é obrigatório'}), 400
        
        # Construir caminho
        if parent_id:
            parent = ProjectFolder.query.get(parent_id)
            if not parent or parent.project_id != project_id:
                return jsonify({'success': False, 'error': 'Pasta pai inválida'}), 400
            folder_path = f"{parent.path}/{folder_name}"
        else:
            folder_path = f"/{folder_name}"
        
        # Verificar se já existe
        existing = ProjectFolder.query.filter_by(
            project_id=project_id,
            path=folder_path
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Pasta já existe'}), 400
        
        # Criar pasta no sistema de arquivos
        success, message = file_manager.create_folder(project_id, folder_path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        # Criar no banco de dados
        folder = ProjectFolder(
            project_id=project_id,
            name=folder_name,
            parent_id=parent_id,
            path=folder_path
        )
        db.session.add(folder)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'folder': {
                'id': folder.id,
                'name': folder.name,
                'path': folder.path,
                'parent_id': folder.parent_id,
                'created_at': folder.created_at.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/file', methods=['POST'])
@login_required
def create_file(project_id):
    """Cria um novo arquivo no projeto"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        data = request.get_json()
        file_name = data.get('name', '').strip()
        folder_id = data.get('folder_id')
        content = data.get('content', '')
        
        if not file_name:
            return jsonify({'success': False, 'error': 'Nome do arquivo é obrigatório'}), 400
        
        # Construir caminho
        if folder_id:
            folder = ProjectFolder.query.get(folder_id)
            if not folder or folder.project_id != project_id:
                return jsonify({'success': False, 'error': 'Pasta inválida'}), 400
            file_path = f"{folder.path}/{file_name}"
        else:
            file_path = f"/{file_name}"
        
        # Verificar se já existe
        existing = ProjectFile.query.filter_by(
            project_id=project_id,
            path=file_path
        ).first()
        
        if existing:
            return jsonify({'success': False, 'error': 'Arquivo já existe'}), 400
        
        # Salvar arquivo no sistema de arquivos
        content_bytes = content.encode('utf-8')
        success, message, size = file_manager.save_file(project_id, file_path, content_bytes)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        # Criar no banco de dados
        file_type = file_manager.get_file_type(file_name)
        is_text = file_manager.is_text_file(file_name)
        
        new_file = ProjectFile(
            project_id=project_id,
            folder_id=folder_id,
            name=file_name,
            path=file_path,
            file_type=file_type,
            size=size,
            content=content if is_text else None,
            file_path=file_path if not is_text else None,
            version=1
        )
        db.session.add(new_file)
        db.session.commit()
        
        # Criar primeira versão
        version = FileVersion(
            file_id=new_file.id,
            version=1,
            content=content if is_text else None,
            file_path=file_path if not is_text else None,
            size=size,
            created_by=current_user.id,
            comment='Versão inicial'
        )
        db.session.add(version)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file': {
                'id': new_file.id,
                'name': new_file.name,
                'path': new_file.path,
                'type': new_file.file_type,
                'size': new_file.size,
                'folder_id': new_file.folder_id,
                'version': new_file.version,
                'created_at': new_file.created_at.isoformat()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/file/<int:file_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_file(project_id, file_id):
    """Gerencia arquivo (ler, atualizar, excluir)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.get_or_404(file_id)
        
        if file.project_id != project_id:
            return jsonify({'success': False, 'error': 'Arquivo não pertence ao projeto'}), 400
        
        if request.method == 'GET':
            # Ler arquivo
            if file_manager.is_text_file(file.name):
                content = file.content or ''
            else:
                success, content_bytes, message = file_manager.read_file(project_id, file.path)
                if not success:
                    return jsonify({'success': False, 'error': message}), 500
                content = content_bytes.decode('utf-8', errors='ignore')
            
            return jsonify({
                'success': True,
                'file': {
                    'id': file.id,
                    'name': file.name,
                    'path': file.path,
                    'type': file.file_type,
                    'size': file.size,
                    'content': content,
                    'version': file.version,
                    'created_at': file.created_at.isoformat(),
                    'updated_at': file.updated_at.isoformat()
                }
            })
        
        elif request.method == 'PUT':
            # Atualizar arquivo
            data = request.get_json()
            new_content = data.get('content')
            new_name = data.get('name')
            comment = data.get('comment', 'Atualização')
            
            if new_name and new_name != file.name:
                # Renomear arquivo
                old_path = file.path
                new_path = old_path.rsplit('/', 1)[0] + '/' + new_name
                
                success, message = file_manager.rename_file(project_id, old_path, new_path)
                if not success:
                    return jsonify({'success': False, 'error': message}), 500
                
                file.name = new_name
                file.path = new_path
                file.file_type = file_manager.get_file_type(new_name)
            
            if new_content is not None:
                # Atualizar conteúdo
                content_bytes = new_content.encode('utf-8')
                success, message, size = file_manager.save_file(project_id, file.path, content_bytes)
                
                if not success:
                    return jsonify({'success': False, 'error': message}), 500
                
                # Incrementar versão
                file.version += 1
                file.size = size
                file.updated_at = datetime.utcnow()
                
                if file_manager.is_text_file(file.name):
                    file.content = new_content
                
                # Criar nova versão
                version = FileVersion(
                    file_id=file.id,
                    version=file.version,
                    content=new_content if file_manager.is_text_file(file.name) else None,
                    file_path=file.path if not file_manager.is_text_file(file.name) else None,
                    size=size,
                    created_by=current_user.id,
                    comment=comment
                )
                db.session.add(version)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'file': {
                    'id': file.id,
                    'name': file.name,
                    'path': file.path,
                    'type': file.file_type,
                    'size': file.size,
                    'version': file.version,
                    'updated_at': file.updated_at.isoformat()
                }
            })
        
        elif request.method == 'DELETE':
            # Excluir arquivo
            success, message = file_manager.delete_file(project_id, file.path)
            
            if not success:
                return jsonify({'success': False, 'error': message}), 500
            
            db.session.delete(file)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Arquivo excluído com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/upload', methods=['POST'])
@login_required
def upload_file_to_project(project_id):
    """Upload de arquivo binário (imagem, PDF, etc.)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        uploaded_file = request.files['file']
        
        if uploaded_file.filename == '':
            return jsonify({'success': False, 'error': 'Nome do arquivo vazio'}), 400
        
        if not file_manager.is_allowed_file(uploaded_file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'}), 400
        
        # Ler conteúdo
        content = uploaded_file.read()
        
        folder_id = request.form.get('folder_id')
        file_name = uploaded_file.filename
        
        # Construir caminho
        if folder_id:
            folder = ProjectFolder.query.get(folder_id)
            if not folder or folder.project_id != project_id:
                return jsonify({'success': False, 'error': 'Pasta inválida'}), 400
            file_path = f"{folder.path}/{file_name}"
        else:
            file_path = f"/{file_name}"
        
        # Salvar arquivo
        success, message, size = file_manager.save_file(project_id, file_path, content)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        # Criar no banco de dados
        file_type = file_manager.get_file_type(file_name)
        is_text = file_manager.is_text_file(file_name)
        
        new_file = ProjectFile(
            project_id=project_id,
            folder_id=int(folder_id) if folder_id else None,
            name=file_name,
            path=file_path,
            file_type=file_type,
            size=size,
            content=content.decode('utf-8', errors='ignore') if is_text else None,
            file_path=file_path if not is_text else None,
            version=1
        )
        db.session.add(new_file)
        db.session.commit()
        
        # Criar primeira versão
        version = FileVersion(
            file_id=new_file.id,
            version=1,
            content=content.decode('utf-8', errors='ignore') if is_text else None,
            file_path=file_path if not is_text else None,
            size=size,
            created_by=current_user.id,
            comment='Upload inicial'
        )
        db.session.add(version)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file': {
                'id': new_file.id,
                'name': new_file.name,
                'path': new_file.path,
                'type': new_file.file_type,
                'size': new_file.size
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/file/<int:file_id>/copy', methods=['POST'])
@login_required
def copy_file_in_project(project_id, file_id):
    """Copia um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.get_or_404(file_id)
        
        if file.project_id != project_id:
            return jsonify({'success': False, 'error': 'Arquivo não pertence ao projeto'}), 400
        
        data = request.get_json()
        new_name = data.get('name', f"{file.name.rsplit('.', 1)[0]}_copy.{file.name.rsplit('.', 1)[1]}")
        dest_folder_id = data.get('folder_id', file.folder_id)
        
        # Construir novo caminho
        if dest_folder_id:
            folder = ProjectFolder.query.get(dest_folder_id)
            if not folder or folder.project_id != project_id:
                return jsonify({'success': False, 'error': 'Pasta de destino inválida'}), 400
            new_path = f"{folder.path}/{new_name}"
        else:
            new_path = f"/{new_name}"
        
        # Copiar arquivo no sistema de arquivos
        success, message = file_manager.copy_file(project_id, file.path, new_path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        # Criar no banco de dados
        new_file = ProjectFile(
            project_id=project_id,
            folder_id=dest_folder_id,
            name=new_name,
            path=new_path,
            file_type=file.file_type,
            size=file.size,
            content=file.content,
            file_path=new_path if file.file_path else None,
            version=1
        )
        db.session.add(new_file)
        db.session.commit()
        
        # Criar primeira versão
        version = FileVersion(
            file_id=new_file.id,
            version=1,
            content=file.content,
            file_path=new_path if file.file_path else None,
            size=file.size,
            created_by=current_user.id,
            comment=f'Cópia de {file.name}'
        )
        db.session.add(version)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'file': {
                'id': new_file.id,
                'name': new_file.name,
                'path': new_file.path,
                'type': new_file.file_type,
                'size': new_file.size
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/file/<int:file_id>/versions', methods=['GET'])
@login_required
def get_file_versions(project_id, file_id):
    """Lista todas as versões de um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.get_or_404(file_id)
        
        if file.project_id != project_id:
            return jsonify({'success': False, 'error': 'Arquivo não pertence ao projeto'}), 400
        
        versions = FileVersion.query.filter_by(file_id=file_id).order_by(FileVersion.version.desc()).all()
        
        return jsonify({
            'success': True,
            'versions': [{
                'id': v.id,
                'version': v.version,
                'size': v.size,
                'created_by': v.created_by,
                'created_at': v.created_at.isoformat(),
                'comment': v.comment
            } for v in versions]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/download', methods=['GET'])
@login_required
def download_project_zip(project_id):
    """Download do projeto completo em ZIP"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        # Criar arquivo ZIP temporário
        zip_path = os.path.join(tempfile.gettempdir(), f'project_{project_id}_{int(time.time())}.zip')
        
        success, message = file_manager.create_zip(project_id, zip_path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{project.name}.zip'
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/folder/<int:folder_id>', methods=['DELETE'])
@login_required
def delete_folder(project_id, folder_id):
    """Exclui uma pasta e todos os seus arquivos"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Sem permissão'}), 403
        
        folder = ProjectFolder.query.get_or_404(folder_id)
        
        if folder.project_id != project_id:
            return jsonify({'success': False, 'error': 'Pasta não pertence ao projeto'}), 400
        
        # Excluir do sistema de arquivos
        success, message = file_manager.delete_folder(project_id, folder.path)
        
        if not success:
            return jsonify({'success': False, 'error': message}), 500
        
        # Excluir do banco de dados (cascade vai excluir arquivos e subpastas)
        db.session.delete(folder)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Pasta excluída com sucesso'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API SIMPLIFICADA PARA O EDITOR (formato esperado pelo frontend)
# ============================================================================

@app.route('/api/project/<int:project_id>/files', methods=['POST'])
@login_required
def api_create_file(project_id):
    """Cria um novo arquivo (formato simplificado)"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        data = request.get_json()
        filename = data.get('filename', '').strip()
        content = data.get('content', '')
        
        if not filename:
            return jsonify({'error': 'Nome do arquivo é obrigatório'}), 400
        
        # Construir caminho
        file_path = f"/{filename}"
        
        # Verificar se já existe
        existing = ProjectFile.query.filter_by(
            project_id=project_id,
            path=file_path
        ).first()
        
        if existing:
            return jsonify({'error': 'Arquivo já existe'}), 400
        
        # Salvar arquivo
        content_bytes = content.encode('utf-8')
        success, message, size = file_manager.save_file(project_id, file_path, content_bytes)
        
        if not success:
            return jsonify({'error': message}), 500
        
        # Criar no banco
        file_type = file_manager.get_file_type(filename)
        is_text = file_manager.is_text_file(filename)
        
        new_file = ProjectFile(
            project_id=project_id,
            name=filename,
            path=file_path,
            file_type=file_type,
            size=size,
            content=content if is_text else None
        )
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({
            'id': new_file.id,
            'filename': new_file.name,
            'file_type': new_file.file_type,
            'size': new_file.size,
            'content': new_file.content,
            'created_at': new_file.created_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/files/<int:file_id>', methods=['GET'])
@login_required
def api_get_file(project_id, file_id):
    """Obtém um arquivo específico"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.filter_by(id=file_id, project_id=project_id).first_or_404()
        
        return jsonify({
            'id': file.id,
            'filename': file.name,
            'file_type': file.file_type,
            'size': file.size,
            'content': file.content,
            'created_at': file.created_at.isoformat(),
            'updated_at': file.updated_at.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/files/<int:file_id>', methods=['PUT'])
@login_required
def api_update_file(project_id, file_id):
    """Atualiza o conteúdo de um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.filter_by(id=file_id, project_id=project_id).first_or_404()
        
        data = request.get_json()
        content = data.get('content', '')
        
        # Atualizar arquivo no sistema
        content_bytes = content.encode('utf-8')
        success, message, size = file_manager.save_file(project_id, file.path, content_bytes)
        
        if not success:
            return jsonify({'error': message}), 500
        
        # Atualizar no banco
        file.content = content
        file.size = size
        file.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Arquivo atualizado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/files/<int:file_id>', methods=['DELETE'])
@login_required
def api_delete_file(project_id, file_id):
    """Exclui um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.filter_by(id=file_id, project_id=project_id).first_or_404()
        
        # Excluir do sistema de arquivos
        file_manager.delete_file(project_id, file.path)
        
        # Excluir do banco
        db.session.delete(file)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Arquivo excluído'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/files/<int:file_id>/rename', methods=['POST'])
@login_required
def api_rename_file(project_id, file_id):
    """Renomeia um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.filter_by(id=file_id, project_id=project_id).first_or_404()
        
        data = request.get_json()
        new_filename = data.get('filename', '').strip()
        
        if not new_filename:
            return jsonify({'error': 'Nome do arquivo é obrigatório'}), 400
        
        # Construir novo caminho
        old_path = file.path
        path_parts = old_path.rsplit('/', 1)
        new_path = f"{path_parts[0]}/{new_filename}" if len(path_parts) > 1 else f"/{new_filename}"
        
        # Renomear no sistema de arquivos
        success, message = file_manager.rename_file(project_id, old_path, new_path)
        
        if not success:
            return jsonify({'error': message}), 500
        
        # Atualizar no banco
        file.name = new_filename
        file.path = new_path
        file.file_type = file_manager.get_file_type(new_filename)
        file.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Arquivo renomeado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<int:project_id>/files/<int:file_id>/download')
@login_required
def api_download_file(project_id, file_id):
    """Download de um arquivo"""
    try:
        project = Project.query.get_or_404(project_id)
        
        if project.user_id != current_user.id:
            return jsonify({'error': 'Sem permissão'}), 403
        
        file = ProjectFile.query.filter_by(id=file_id, project_id=project_id).first_or_404()
        
        # Se for arquivo de texto, retornar o conteúdo
        if file.content:
            from io import BytesIO
            return send_file(
                BytesIO(file.content.encode('utf-8')),
                as_attachment=True,
                download_name=file.name,
                mimetype='text/plain'
            )
        
        # Se for binário, buscar do sistema de arquivos
        file_path = os.path.join(UPLOAD_FOLDER, f'project_{project_id}', file.path.lstrip('/'))
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=file.name)
        
        return jsonify({'error': 'Arquivo não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# SOCKET.IO - ASSISTENTE VIRTUAL
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Cliente conectado ao Socket.IO"""
    print(f'[SocketIO] Cliente conectado: {request.sid}')
    emit('connection_status', {'status': 'connected', 'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    print(f'[SocketIO] Cliente desconectado: {request.sid}')
    # Limpar ações pendentes desta sessão
    if request.sid in pending_actions:
        del pending_actions[request.sid]

@socketio.on('join_project')
def handle_join_project(data):
    """Entrar em uma sala de projeto para colaboração"""
    project_id = data.get('project_id')
    if project_id:
        join_room(f'project_{project_id}')
        emit('project_joined', {'project_id': project_id, 'sid': request.sid})
        print(f'[SocketIO] Cliente {request.sid} entrou no projeto {project_id}')

@socketio.on('leave_project')
def handle_leave_project(data):
    """Sair de uma sala de projeto"""
    project_id = data.get('project_id')
    if project_id:
        leave_room(f'project_{project_id}')
        emit('project_left', {'project_id': project_id})
        print(f'[SocketIO] Cliente {request.sid} saiu do projeto {project_id}')

@socketio.on('assistant_action')
def handle_assistant_action(data):
    """
    Processar ação do assistente virtual com validação e snapshots
    
    Estados possíveis:
    - pending: Ação enviada, aguardando processamento
    - applied_local: Aplicada localmente (optimistic UI)
    - confirmed: Confirmada pelo servidor
    - reverted: Revertida pelo servidor (erro/conflito)
    
    data = {
        'action_id': str,
        'action_type': 'insert_snippet' | 'correct_latex' | 'format' | 'compile',
        'payload': {
            'snippet' or 'snippet_id': str,
            'file': str (opcional),
            'range': {start, end} (opcional),
            'content': str (opcional),
            'client_snapshot_id': str (opcional)
        },
        'state': 'applied_local'
    }
    """
    try:
        action_id = data.get('action_id', str(uuid.uuid4()))
        action_type = data.get('action_type')
        payload = data.get('payload', {})
        state = data.get('state', 'pending')
        client_snapshot_id = payload.get('client_snapshot_id')
        
        print(f'[SocketIO] Ação recebida: {action_id} | Tipo: {action_type} | Estado: {state}')
        
        # Obter user_id da sessão (TODO: integrar com Flask-Login)
        user_id = getattr(current_user, 'id', None) if current_user.is_authenticated else None
        
        # VALIDAÇÃO DE PERMISSÕES
        is_valid, error_msg = validate_snippet_permission(user_id, action_type, payload)
        
        if not is_valid:
            print(f'[SocketIO] Ação REJEITADA: {error_msg}')
            response = {
                'action_id': action_id,
                'state': 'reverted',
                'message': f'Ação rejeitada: {error_msg}',
                'error': error_msg,
                'should_revert': True
            }
            emit('assistant_action_reverted', response)
            return response
        
        # VERIFICAR SNAPSHOT (detecção de conflito)
        session_key = f"{request.sid}_{payload.get('file', 'main.tex')}"
        server_snapshot_id = document_snapshots.get(session_key)
        
        has_conflict = not verify_snapshot_integrity(client_snapshot_id, server_snapshot_id)
        
        if has_conflict:
            print(f'[SocketIO] CONFLITO detectado: client={client_snapshot_id[:8]} != server={server_snapshot_id[:8] if server_snapshot_id else "None"}')
            response = {
                'action_id': action_id,
                'state': 'conflict',
                'message': 'Conflito detectado: documento foi modificado',
                'error': 'Snapshot mismatch',
                'should_revert': False,  # Usuário pode escolher
                'server_snapshot_id': server_snapshot_id,
                'merge_options': {
                    'keep_local': 'Manter alteração local',
                    'use_server': 'Usar versão do servidor',
                    'manual_merge': 'Resolver manualmente'
                }
            }
            emit('assistant_action_conflict', response)
            return response
        
        # PROCESSAR SNIPPET SE USAR snippet_id
        if action_type == 'insert_snippet' and 'snippet_id' in payload:
            snippet_id = payload['snippet_id']
            snippet_data = get_snippet(snippet_id)
            
            if not snippet_data:
                response = {
                    'action_id': action_id,
                    'state': 'reverted',
                    'message': f'Snippet "{snippet_id}" não encontrado',
                    'error': 'Snippet not found',
                    'should_revert': True
                }
                return response
            
            # Processar placeholders
            snippet_content = process_snippet_placeholders(
                snippet_data['content'],
                payload.get('placeholder_values')
            )
            payload['snippet'] = snippet_content
        
        # Armazenar ação pendente
        if request.sid not in pending_actions:
            pending_actions[request.sid] = {}
        
        pending_actions[request.sid][action_id] = {
            'type': action_type,
            'payload': payload,
            'state': 'confirmed',
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id
        }
        
        # PROCESSAR PATCHES / REFATORAÇÕES
        patch_result = None
        if action_type == 'apply_patch':
            # Sanitizar patch
            is_safe, error_msg = PatchSanitizer.sanitize_patch(payload)
            
            if not is_safe:
                print(f'[SocketIO] PATCH REJEITADO: {error_msg}')
                response = {
                    'action_id': action_id,
                    'state': 'reverted',
                    'message': f'Patch rejeitado: {error_msg}',
                    'error': error_msg,
                    'should_revert': True
                }
                return response
            
            # Aplicar patch
            original_content = payload.get('original_content', '')
            
            try:
                modified_content, metadata = PatchApplier.apply_patch(original_content, payload)
                
                # Gerar diff para preview
                diff = PatchApplier.generate_diff(original_content, modified_content)
                
                patch_result = {
                    'success': True,
                    'modified_content': modified_content,
                    'metadata': metadata,
                    'diff': diff,
                    'message': metadata.get('description', 'Patch aplicado com sucesso')
                }
                
                print(f'[SocketIO] PATCH APLICADO: {metadata["patch_id"]} | {metadata["description"]}')
                
            except Exception as e:
                patch_result = {
                    'success': False,
                    'error': str(e),
                    'message': f'Erro ao aplicar patch: {str(e)}'
                }
        
        elif action_type == 'suggest_refactors':
            # Analisar código e sugerir refatorações
            content = payload.get('content', '')
            
            suggestions = LaTeXRefactor.suggest_refactors(content)
            
            patch_result = {
                'success': True,
                'suggestions': suggestions,
                'message': f'{len(suggestions)} sugestões de refatoração encontradas'
            }
            
            print(f'[SocketIO] SUGESTÕES GERADAS: {len(suggestions)} refatorações')
        
        elif action_type == 'lint':
            # Executar linter LaTeX
            content = payload.get('content', '')
            filename = payload.get('filename', 'main.tex')
            
            try:
                linter = LaTeXLinter()
                issues = linter.lint_content(content, filename)
                fixes = linter.generate_fixes(content)
                summary = linter.get_summary()
                
                patch_result = {
                    'success': True,
                    'issues': [issue.to_dict() for issue in issues],
                    'fixes': fixes,
                    'summary': summary,
                    'message': f'Lint completo: {summary["total"]} issues encontrados'
                }
                
                print(f'[SocketIO] LINT EXECUTADO: {summary["total"]} issues | {summary["auto_fixable"]} auto-fixable')
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                patch_result = {
                    'success': False,
                    'error': str(e),
                    'message': f'Erro ao executar lint: {str(e)}'
                }
        
        elif action_type == 'generate_bibtex':
            # Gerar entrada BibTeX
            description = payload.get('description', '')
            entry_type = payload.get('entry_type')
            existing_bib = payload.get('existing_bib', '')
            
            if not description:
                patch_result = {
                    'success': False,
                    'error': 'Descrição é obrigatória',
                    'message': 'Forneça uma descrição para gerar BibTeX'
                }
            else:
                try:
                    result = generate_bibtex_from_description(description, existing_bib, entry_type)
                    
                    patch_result = {
                        'success': result['success'],
                        'bibtex': result['bibtex'],
                        'key': result['key'],
                        'fields': result['fields'],
                        'entry_type': result['entry_type'],
                        'has_conflict': result['has_conflict'],
                        'conflict_entry': result.get('conflict_entry'),
                        'message': f'BibTeX gerado com sucesso: {result["key"]}'
                    }
                    
                    print(f'[SocketIO] BIBTEX GERADO: {result["key"]} | Tipo: {result["entry_type"]}')
                    
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    patch_result = {
                        'success': False,
                        'error': str(e),
                        'message': f'Erro ao gerar BibTeX: {str(e)}'
                    }
        
        # PROCESSAR COMPILAÇÃO se for action_type == 'compile'
        compilation_result = None
        if action_type == 'compile':
            project_key = payload.get('file', 'main.tex')
            current_time = time.time()
            last_compilation = compilation_timestamps.get(project_key, 0)
            
            # Debounce: evitar compilações muito frequentes
            if current_time - last_compilation < COMPILATION_DEBOUNCE_SECONDS:
                response = {
                    'action_id': action_id,
                    'state': 'rate_limited',
                    'message': f'Aguarde {COMPILATION_DEBOUNCE_SECONDS} segundos entre compilações',
                    'wait_seconds': COMPILATION_DEBOUNCE_SECONDS - (current_time - last_compilation)
                }
                return response
            
            compilation_timestamps[project_key] = current_time
            
            # Compilar LaTeX
            content = payload.get('content', '')
            filename = payload.get('filename', 'document')
            
            if not content:
                response = {
                    'action_id': action_id,
                    'state': 'reverted',
                    'message': 'Conteúdo vazio para compilação',
                    'should_revert': False
                }
                return response
            
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    tex_file = os.path.join(temp_dir, f'{filename}.tex')
                    with open(tex_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Executar pdflatex
                    result = subprocess.run([
                        'pdflatex',
                        '-interaction=batchmode',
                        '-halt-on-error',
                        '-output-directory', temp_dir,
                        tex_file
                    ], capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
                    
                    log_output = result.stdout + '\n' + result.stderr
                    
                    # Parsear log para encontrar erros
                    errors = parse_latex_log(log_output)
                    
                    pdf_file = os.path.join(temp_dir, f'{filename}.pdf')
                    
                    if os.path.exists(pdf_file):
                        # Compilação bem-sucedida
                        uploads_dir = os.path.join(app.root_path, 'uploads')
                        if not os.path.exists(uploads_dir):
                            os.makedirs(uploads_dir)
                        
                        final_pdf = os.path.join(uploads_dir, f'{filename}.pdf')
                        shutil.copy2(pdf_file, final_pdf)
                        
                        compilation_result = {
                            'success': True,
                            'pdf_url': f'/uploads/{filename}.pdf',
                            'errors': errors,  # Pode ter warnings mesmo com sucesso
                            'message': 'Compilação bem-sucedida' + (f' com {len(errors)} avisos' if errors else '')
                        }
                    else:
                        # Compilação falhou
                        compilation_result = {
                            'success': False,
                            'errors': errors,
                            'log': log_output[-1000:],  # Últimos 1000 chars do log
                            'message': f'Compilação falhou com {len(errors)} erros'
                        }
            
            except subprocess.TimeoutExpired:
                compilation_result = {
                    'success': False,
                    'errors': [],
                    'message': 'Timeout na compilação (máximo 60 segundos)'
                }
            except FileNotFoundError:
                compilation_result = {
                    'success': False,
                    'errors': [],
                    'message': 'pdflatex não encontrado. Instale o LaTeX no sistema.'
                }
            except Exception as e:
                compilation_result = {
                    'success': False,
                    'errors': [],
                    'message': f'Erro na compilação: {str(e)}'
                }
        
        # GERAR NOVO SNAPSHOT após aplicar ação
        if 'content' in payload:
            new_snapshot_id = generate_snapshot_id(payload['content'])
            document_snapshots[session_key] = new_snapshot_id
        else:
            new_snapshot_id = None
        
        # CONFIRMAR AÇÃO
        response = {
            'action_id': action_id,
            'state': 'confirmed',
            'message': f'Ação {action_type} confirmada com sucesso',
            'server_snapshot_id': new_snapshot_id
        }
        
        # Adicionar resultado de compilação se houver
        if compilation_result:
            response['compilation'] = compilation_result
        
        # Adicionar resultado de patch/refatoração se houver
        if patch_result:
            response['patch'] = patch_result
        
        print(f'[SocketIO] Ação CONFIRMADA: {action_id} | Snapshot: {new_snapshot_id[:8] if new_snapshot_id else "None"}')
        
        # Emitir para todos na sala do projeto (colaboração)
        project_id = payload.get('project_id')
        if project_id:
            emit('assistant_action_confirmed', response, room=f'project_{project_id}', skip_sid=request.sid)
        
        return response
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f'[SocketIO] ERRO ao processar ação: {str(e)}\n{error_trace}')
        
        error_response = {
            'action_id': data.get('action_id', 'unknown'),
            'state': 'error',
            'message': f'Erro ao processar ação: {str(e)}',
            'error': str(e),
            'should_revert': True
        }
        
        emit('assistant_error', error_response)
        return error_response

@socketio.on('assistant_message')
def handle_assistant_message(data):
    """Processar mensagem de chat do assistente"""
    try:
        from services.llm_client import get_llm_client
        from services.assistant_i18n import detect_language
        
        message_id = data.get('message_id', str(uuid.uuid4()))
        content = data.get('content', '')
        
        # Detectar idioma
        lang = detect_language(data, default=session.get('language', 'pt'))
        
        print(f'[SocketIO] Mensagem do assistente: {message_id} | Idioma: {lang} | {content[:50]}...')
        
        # Obter resposta inteligente do LLM client (offline/hybrid/llm)
        llm_client = get_llm_client()
        llm_response = llm_client.generate_response(
            user_message=content,
            context={
                'user_id': current_user.id if current_user.is_authenticated else None,
                'language': lang
            },
            language=lang
        )
        
        # Construir resposta
        response = {
            'message_id': message_id,
            'content': llm_response['text'],
            'timestamp': datetime.utcnow().isoformat(),
            'state': 'delivered',
            'source': llm_response.get('source', 'rules'),  # 'rules' ou 'llm'
            'actions': llm_response.get('actions', [])  # Ações sugeridas
        }
        
        # Emitir resposta para o cliente
        emit('assistant_response', response)
        
        # Retornar também via callback
        return response
        
    except Exception as e:
        error_response = {
            'message_id': data.get('message_id', 'unknown'),
            'error': str(e)
        }
        
        print(f'[SocketIO] Erro ao processar mensagem: {str(e)}')
        return error_response

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Criar banco de dados e usuário admin
with app.app_context():
    db.create_all()
    
    # Criar usuário admin se não existir
    try:
        admin_user = User.query.filter_by(email='admin@doccollab.com').first()
        if not admin_user:
            admin = User(name='Administrador', email='admin@doccollab.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado: admin@doccollab.com / admin123")
        else:
            print("Usuário admin já existe")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)