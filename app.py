from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, send_from_directory, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import tempfile
import subprocess
import shutil

# Função simples de tradução
def _(text):
    return text

# Criar app Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configurações
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doccollab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Criar instância única do SQLAlchemy
db = SQLAlchemy(app)

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

@app.route('/editor-page')
def editor_page():
    """Editor LaTeX"""
    return render_template('editor_page.html')

# ===== ROTAS DE PROJETOS =====

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
                    '-interaction=nonstopmode',
                    '-output-directory', temp_dir,
                    tex_file
                ], capture_output=True, text=True, timeout=30)
                
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
                    'error': 'Timeout na compilação (máximo 30 segundos)'
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

# Criar banco de dados e usuário admin
with app.app_context():
    db.create_all()
    
    # Criar usuário admin se não existir
    admin_user = User.query.filter_by(email='admin@doccollab.com').first()
    if not admin_user:
        admin = User(name='Administrador', email='admin@doccollab.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado: admin@doccollab.com / admin123")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)