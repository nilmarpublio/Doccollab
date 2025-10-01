import os
import subprocess
from typing import Tuple, Optional
from datetime import datetime

from flask import current_app


def _resolve_pdflatex_binary() -> str:
    """Resolve the pdflatex binary path from config/env or fallback to 'pdflatex'."""
    configured = None
    try:
        if current_app:  # pragma: no cover
            configured = current_app.config.get('PDFLATEX')
    except Exception:
        configured = None
    return configured or os.getenv('PDFLATEX') or 'pdflatex'


def compile_with_pdflatex(main_tex_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Compile the provided main.tex file using pdflatex in its directory.

    Returns: (ok, pdf_path, error_message)
    """
    if not os.path.exists(main_tex_path):
        return False, None, f"File not found: {main_tex_path}"

    project_dir = os.path.dirname(os.path.abspath(main_tex_path))
    tex_filename = os.path.basename(main_tex_path)
    pdflatex_bin = _resolve_pdflatex_binary()

    try:
        # Run twice for references
        for _ in range(2):
            subprocess.run(
                [pdflatex_bin, "-interaction=nonstopmode", tex_filename],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
            )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        out = getattr(e, 'stdout', b'').decode(errors='ignore') or str(e)
        return False, None, f"pdflatex error: {out} | bin={pdflatex_bin} | cwd={project_dir}"

    # Generate PDF with same name as tex file
    pdf_filename = os.path.splitext(tex_filename)[0] + '.pdf'
    pdf_path = os.path.join(project_dir, pdf_filename)
    if not os.path.exists(pdf_path):
        return False, None, "PDF not generated"

    return True, pdf_path, None


def get_main_file(project_path: str) -> str:
    """Get the main file for compilation from project directory"""
    main_file_path = os.path.join(project_path, '.mainfile')
    if os.path.exists(main_file_path):
        try:
            with open(main_file_path, 'r') as f:
                main_file = f.read().strip()
                if main_file and os.path.exists(os.path.join(project_path, main_file)):
                    return main_file
        except Exception:
            pass
    
    # Fallback to main.tex
    return 'main.tex'


def save_version_snapshot(project_id: int, main_file_path: str, description: str = None) -> bool:
    """
    Save a snapshot of the main file content as a new version.
    
    Returns: True if successful, False otherwise
    """
    try:
        from models import Version, db
        
        # Read the current content
        if not os.path.exists(main_file_path):
            return False
            
        with open(main_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get the next version number
        last_version = Version.query.filter_by(project_id=project_id).order_by(Version.version_number.desc()).first()
        next_version = (last_version.version_number + 1) if last_version else 1
        
        # Create new version
        version = Version(
            project_id=project_id,
            version_number=next_version,
            content=content,
            file_name=os.path.basename(main_file_path),
            description=description or f"Compilation snapshot - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        )
        
        db.session.add(version)
        db.session.commit()
        
        return True
        
    except Exception as e:
        print(f"Error saving version snapshot: {e}")
        return False


