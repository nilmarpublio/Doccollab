import os
import subprocess
from typing import Tuple, Optional

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

    pdf_path = os.path.join(project_dir, "main.pdf")
    if not os.path.exists(pdf_path):
        return False, None, "PDF not generated"

    return True, pdf_path, None


