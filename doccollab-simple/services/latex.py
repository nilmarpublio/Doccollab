import os
import subprocess
import tempfile
from typing import Tuple, Optional
from flask import current_app


def compile_latex_to_pdf(project_path: str, main_tex_name: str = "main.tex") -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Compile main.tex inside project_path using pdflatex.
    Returns (ok, pdf_path, error_message)
    """
    main_tex_path = os.path.join(project_path, main_tex_name)
    if not os.path.exists(main_tex_path):
        return False, None, "main.tex not found"

    # Run pdflatex directly in the project directory to allow relative assets
    # Decide binary path before running, so we can include it on errors
    pdflatex_bin = (
        (current_app and current_app.config.get('PDFLATEX'))
        or os.getenv('PDFLATEX')
        or 'pdflatex'
    )
    try:
        full_log = []
        # Debug line to help diagnose path issues (printed only in dev server)
        try:
            print(f"[pdflatex] using: {pdflatex_bin} | cwd={project_path}")
        except Exception:
            pass
        for _ in range(2):
            proc = subprocess.run(
                [pdflatex_bin, "-interaction=nonstopmode", main_tex_name],
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=True,
            )
            full_log.append(proc.stdout.decode(errors='ignore'))
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        out = getattr(e, 'stdout', b'').decode(errors='ignore') or str(e)
        return False, None, f"pdflatex error: {out} | bin={pdflatex_bin} | cwd={project_path}"

    pdf_out_path = os.path.join(project_path, "main.pdf")
    if not os.path.exists(pdf_out_path):
        return False, None, "PDF not generated"

    return True, pdf_out_path, None


