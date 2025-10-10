"""
Script de Verificação da Instalação
Verifica se todos os componentes do DocCollab Assistant estão funcionando
"""

import os
import sys

def print_header(text):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_result(test_name, passed, message=""):
    """Imprime resultado de um teste"""
    status = "[OK] PASS" if passed else "[!!] FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"       {message}")

def check_python_version():
    """Verifica versão do Python"""
    print_header("1. Python Version")
    version = sys.version_info
    required = (3, 9)
    passed = version >= required
    print_result(
        "Python 3.9+",
        passed,
        f"Versão detectada: {version.major}.{version.minor}.{version.micro}"
    )
    return passed

def check_dependencies():
    """Verifica dependências"""
    print_header("2. Dependencies")
    
    dependencies = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'flask_login': 'Flask-Login',
        'flask_babel': 'Flask-Babel',
        'flask_socketio': 'Flask-SocketIO',
        'werkzeug': 'Werkzeug',
    }
    
    all_passed = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print_result(name, True)
        except ImportError:
            print_result(name, False, f"Execute: pip install {name}")
            all_passed = False
    
    return all_passed

def check_services():
    """Verifica módulos de serviços"""
    print_header("3. Service Modules")
    
    services = [
        'assistant_i18n',
        'llm_client',
        'audit_log',
        'permissions',
        'latex_log_parser',
        'latex_refactors',
        'latex_linter',
        'bibtex_generator'
    ]
    
    all_passed = True
    sys.path.insert(0, os.path.dirname(__file__))
    
    for service in services:
        try:
            __import__(f'services.{service}')
            print_result(f"services/{service}.py", True)
        except ImportError as e:
            print_result(f"services/{service}.py", False, str(e))
            all_passed = False
    
    return all_passed

def check_snippets():
    """Verifica snippets LaTeX"""
    print_header("4. LaTeX Snippets")
    
    snippets_dir = os.path.join(os.path.dirname(__file__), 'assistant', 'snippets')
    expected_snippets = [
        '01_table.tex',
        '02_figure.tex',
        '03_align_equations.tex',
        '04_bibtex_template.tex',
        '05_enumerate.tex',
        '06_footnote.tex',
        '07_theorem_proof.tex',
        '08_algorithm.tex',
        '09_matrix.tex',
        '10_subfigure.tex'
    ]
    
    all_passed = True
    for snippet in expected_snippets:
        path = os.path.join(snippets_dir, snippet)
        exists = os.path.exists(path)
        print_result(snippet, exists)
        if not exists:
            all_passed = False
    
    return all_passed

def check_config_files():
    """Verifica arquivos de configuração"""
    print_header("5. Configuration Files")
    
    config_files = {
        'assistant/lint_rules.json': 'Lint Rules',
        'babel.cfg': 'Babel Config',
    }
    
    all_passed = True
    base_dir = os.path.dirname(__file__)
    
    for file_path, name in config_files.items():
        path = os.path.join(base_dir, file_path)
        exists = os.path.exists(path)
        print_result(name, exists, file_path)
        if not exists:
            all_passed = False
    
    return all_passed

def check_documentation():
    """Verifica documentação"""
    print_header("6. Documentation")
    
    docs = {
        'docs/ASSISTANT_README.md': 'Assistant README',
        'docs/LLM_CONFIGURATION.md': 'LLM Configuration Guide',
        'docs/PROJECT_SUMMARY.md': 'Project Summary',
        'assistant/snippets/README.md': 'Snippets Catalog'
    }
    
    all_passed = True
    base_dir = os.path.dirname(__file__)
    
    for file_path, name in docs.items():
        path = os.path.join(base_dir, file_path)
        exists = os.path.exists(path)
        print_result(name, exists)
        if not exists:
            all_passed = False
    
    return all_passed

def check_examples():
    """Verifica arquivos de exemplo"""
    print_header("7. Example Files")
    
    examples = {
        'examples/compile_log.txt': 'Compilation Log Example',
        'examples/compile_log_parsed.json': 'Parsed Log Example'
    }
    
    all_passed = True
    base_dir = os.path.dirname(__file__)
    
    for file_path, name in examples.items():
        path = os.path.join(base_dir, file_path)
        exists = os.path.exists(path)
        print_result(name, exists)
        if not exists:
            all_passed = False
    
    return all_passed

def run_unit_tests():
    """Executa testes unitários"""
    print_header("8. Unit Tests")
    
    try:
        import unittest
        loader = unittest.TestLoader()
        start_dir = os.path.join(os.path.dirname(__file__), 'tests')
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=0)
        result = runner.run(suite)
        
        passed = result.wasSuccessful()
        total = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        
        print_result(
            f"Unit Tests ({total} total)",
            passed,
            f"Failures: {failures}, Errors: {errors}"
        )
        
        return passed
    except Exception as e:
        print_result("Unit Tests", False, str(e))
        return False

def check_latex():
    """Verifica se LaTeX está instalado"""
    print_header("9. LaTeX Installation (Optional)")
    
    try:
        import subprocess
        result = subprocess.run(
            ['pdflatex', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        passed = result.returncode == 0
        
        if passed:
            version_line = result.stdout.split('\n')[0]
            print_result("pdflatex", True, version_line)
        else:
            print_result("pdflatex", False, "Não encontrado (necessário para compilação)")
        
        return passed
    except FileNotFoundError:
        print_result(
            "pdflatex",
            False,
            "Não instalado. Instale MiKTeX (Windows), TeX Live (Linux) ou MacTeX (macOS)"
        )
        return False
    except Exception as e:
        print_result("pdflatex", False, str(e))
        return False

def main():
    """Executa todas as verificações"""
    print("\n" + "=" * 60)
    print("   DocCollab Assistant - Verificação de Instalação")
    print("=" * 60)
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Service Modules': check_services(),
        'LaTeX Snippets': check_snippets(),
        'Configuration Files': check_config_files(),
        'Documentation': check_documentation(),
        'Example Files': check_examples(),
        'Unit Tests': run_unit_tests(),
        'LaTeX Installation': check_latex()
    }
    
    print_header("SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"\nTotal Checks: {total}")
    print(f"[OK] Passed: {passed}")
    print(f"[!!] Failed: {failed}")
    
    if failed == 0:
        print("\n*** INSTALACAO COMPLETA E FUNCIONAL! ***")
        print("\nPróximos passos:")
        print("1. Execute: python app.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Leia: docs/ASSISTANT_README.md")
        return 0
    elif failed == 1 and not results['LaTeX Installation']:
        print("\n*** INSTALACAO FUNCIONAL (LaTeX opcional) ***")
        print("\nO sistema funcionará sem LaTeX, mas a compilação de documentos não estará disponível.")
        print("\nPara habilitar compilação:")
        print("- Windows: Instale MiKTeX (https://miktex.org/)")
        print("- Linux: sudo apt-get install texlive-latex-base")
        print("- macOS: Instale MacTeX (https://www.tug.org/mactex/)")
        return 0
    else:
        print("\n*** INSTALACAO INCOMPLETA ***")
        print("\nCorreja os problemas acima e execute novamente:")
        print("python verify_installation.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())

