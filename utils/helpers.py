"""
Funções auxiliares e utilitárias
"""
import os
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'zip'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """
    Salva um arquivo enviado pelo usuário
    
    Returns:
        tuple: (success, file_path or error_message)
    """
    if not file or file.filename == '':
        return False, 'Nenhum arquivo selecionado'
    
    if not allowed_file(file.filename):
        return False, 'Tipo de arquivo não permitido'
    
    # Gerar nome único
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    # Salvar arquivo
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    return True, unique_filename

def format_timestamp(timestamp_str):
    """Formata timestamp para exibição"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        
        # Se for hoje
        if dt.date() == now.date():
            return dt.strftime('%H:%M')
        
        # Se foi ontem
        if dt.date() == (now - timedelta(days=1)).date():
            return f'Ontem {dt.strftime("%H:%M")}'
        
        # Se foi esta semana
        if (now - dt).days < 7:
            dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            return f'{dias[dt.weekday()]} {dt.strftime("%H:%M")}'
        
        # Data completa
        return dt.strftime('%d/%m/%Y %H:%M')
    
    except:
        return timestamp_str

def get_file_icon(filename):
    """Retorna o ícone FontAwesome para o tipo de arquivo"""
    if not filename:
        return 'fa-file'
    
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    icons = {
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'txt': 'fa-file-alt',
        'zip': 'fa-file-archive',
        'png': 'fa-file-image',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'gif': 'fa-file-image'
    }
    
    return icons.get(ext, 'fa-file')

def is_image(filename):
    """Verifica se o arquivo é uma imagem"""
    if not filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in {'png', 'jpg', 'jpeg', 'gif'}

def clean_old_messages(days=365):
    """Remove mensagens antigas do banco de dados"""
    from utils.db import execute_query
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Buscar arquivos das mensagens antigas
    old_messages = execute_query(
        'SELECT file_path FROM messages WHERE timestamp < ? AND file_path IS NOT NULL',
        (cutoff_date,),
        fetch_all=True
    )
    
    # Deletar arquivos
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    for msg in old_messages:
        file_path = os.path.join(upload_folder, msg['file_path'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Deletar mensagens do banco
    execute_query(
        'DELETE FROM messages WHERE timestamp < ?',
        (cutoff_date,),
        commit=True
    )

def truncate_text(text, max_length=50):
    """Trunca texto longo"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + '...'

