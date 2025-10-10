"""
Unit tests para LaTeX Linter
"""

import unittest
import os
from services.latex_linter import LaTeXLinter, LintIssue

class TestLaTeXLinter(unittest.TestCase):
    
    def setUp(self):
        """Inicializa linter antes de cada teste"""
        self.linter = LaTeXLinter()
    
    def test_forbidden_write18(self):
        """Deve detectar \\write18 como comando proibido"""
        content = "\\write18{rm -rf /}"
        issues = self.linter.lint_content(content)
        
        forbidden_issues = [i for i in issues if 'write18' in i.rule_id]
        self.assertGreater(len(forbidden_issues), 0)
        self.assertEqual(forbidden_issues[0].severity, 'error')
    
    def test_forbidden_absolute_path(self):
        """Deve detectar caminhos absolutos em \\input"""
        content = "\\input{/etc/passwd}"
        issues = self.linter.lint_content(content)
        
        self.assertTrue(any(i.severity == 'error' for i in issues))
    
    def test_deprecated_eqnarray(self):
        """Deve detectar eqnarray obsoleto"""
        content = """
\\begin{eqnarray}
  x &=& 1 \\\\
  y &=& 2
\\end{eqnarray}
"""
        issues = self.linter.lint_content(content)
        
        eqnarray_issues = [i for i in issues if i.rule_id == 'deprecated_eqnarray']
        self.assertGreater(len(eqnarray_issues), 0)
        self.assertEqual(eqnarray_issues[0].severity, 'warning')
        self.assertTrue(eqnarray_issues[0].auto_fix)
    
    def test_deprecated_dollar_display(self):
        """Deve detectar $$ obsoleto"""
        content = "Equação: $$x^2 = 1$$"
        issues = self.linter.lint_content(content)
        
        dollar_issues = [i for i in issues if i.rule_id == 'deprecated_dollar_display']
        self.assertGreater(len(dollar_issues), 0)
        self.assertTrue(dollar_issues[0].auto_fix)
    
    def test_old_font_commands(self):
        """Deve detectar comandos de fonte obsoletos"""
        content = "Texto em {\\bf negrito} e {\\it itálico}"
        issues = self.linter.lint_content(content)
        
        font_issues = [i for i in issues if i.rule_id == 'old_font_commands']
        self.assertGreater(len(font_issues), 0)
    
    def test_missing_label_in_figure(self):
        """Deve detectar figura sem \\label"""
        content = """
\\begin{figure}
  \\includegraphics{image.png}
  \\caption{Uma imagem}
\\end{figure}
"""
        issues = self.linter.lint_content(content)
        
        label_issues = [i for i in issues if i.rule_id == 'missing_label_in_figure']
        self.assertGreater(len(label_issues), 0)
        self.assertTrue(label_issues[0].auto_fix)
        self.assertEqual(label_issues[0].fix_type, 'insert')
    
    def test_missing_label_in_table(self):
        """Deve detectar tabela sem \\label"""
        content = """
\\begin{table}
  \\caption{Uma tabela}
  \\begin{tabular}{|c|c|}
    A & B
  \\end{tabular}
\\end{table}
"""
        issues = self.linter.lint_content(content)
        
        label_issues = [i for i in issues if i.rule_id == 'missing_label_in_table']
        self.assertGreater(len(label_issues), 0)
    
    def test_missing_package_graphicx(self):
        """Deve detectar uso de \\includegraphics sem pacote graphicx"""
        content = """
\\documentclass{article}
\\begin{document}
\\includegraphics{test.png}
\\end{document}
"""
        issues = self.linter.lint_content(content)
        
        pkg_issues = [i for i in issues if 'missing_package_graphicx' in i.rule_id]
        self.assertGreater(len(pkg_issues), 0)
        self.assertTrue(pkg_issues[0].auto_fix)
        self.assertEqual(pkg_issues[0].fix_type, 'insert_package')
    
    def test_missing_package_amsmath(self):
        """Deve detectar uso de align sem pacote amsmath"""
        content = """
\\documentclass{article}
\\begin{document}
\\begin{align}
  x = 1
\\end{align}
\\end{document}
"""
        issues = self.linter.lint_content(content)
        
        pkg_issues = [i for i in issues if 'missing_package_amsmath' in i.rule_id]
        self.assertGreater(len(pkg_issues), 0)
    
    def test_package_already_loaded(self):
        """Não deve reportar pacote faltante se já estiver carregado"""
        content = """
\\documentclass{article}
\\usepackage{graphicx}
\\begin{document}
\\includegraphics{test.png}
\\end{document}
"""
        issues = self.linter.lint_content(content)
        
        pkg_issues = [i for i in issues if 'missing_package_graphicx' in i.rule_id]
        self.assertEqual(len(pkg_issues), 0)
    
    def test_non_breaking_space_before_ref(self):
        """Deve sugerir ~ antes de \\ref"""
        content = "Ver Figura \\ref{fig:test}"
        issues = self.linter.lint_content(content)
        
        space_issues = [i for i in issues if i.rule_id == 'non_breaking_space']
        self.assertGreater(len(space_issues), 0)
        self.assertTrue(space_issues[0].auto_fix)
    
    def test_trailing_whitespace(self):
        """Deve detectar espaços no final da linha"""
        content = "Texto com espaços    \nOutra linha"
        issues = self.linter.lint_content(content)
        
        trailing_issues = [i for i in issues if i.rule_id == 'trailing_whitespace']
        self.assertGreater(len(trailing_issues), 0)
        self.assertTrue(trailing_issues[0].auto_fix)
    
    def test_multiple_blank_lines(self):
        """Deve detectar múltiplas linhas vazias"""
        content = "Parágrafo 1\n\n\n\nParágrafo 2"
        issues = self.linter.lint_content(content)
        
        para_issues = [i for i in issues if i.rule_id == 'paragraph_spacing']
        self.assertGreater(len(para_issues), 0)
    
    def test_generate_fixes(self):
        """Deve gerar patches de correção automática"""
        content = """
\\begin{eqnarray}
  x = 1
\\end{eqnarray}
"""
        issues = self.linter.lint_content(content)
        fixes = self.linter.generate_fixes(content)
        
        self.assertGreater(len(fixes), 0)
        self.assertTrue(any(f['type'] == 'refactor' for f in fixes))
    
    def test_summary(self):
        """Deve gerar resumo correto dos issues"""
        content = """
\\write18{bad}
\\begin{eqnarray}
x = 1
\\end{eqnarray}
$$y = 2$$
"""
        issues = self.linter.lint_content(content)
        summary = self.linter.get_summary()
        
        self.assertGreater(summary['total'], 0)
        self.assertGreater(summary['errors'], 0)
        self.assertGreater(summary['warnings'], 0)
        self.assertGreater(summary['auto_fixable'], 0)
    
    def test_line_column_detection(self):
        """Deve detectar linha e coluna corretamente"""
        content = "Linha 1\nLinha 2\n\\write18{test}\nLinha 4"
        issues = self.linter.lint_content(content)
        
        write18_issue = next(i for i in issues if 'write18' in i.rule_id)
        self.assertEqual(write18_issue.line, 3)
    
    def test_multiple_issues_same_line(self):
        """Deve detectar múltiplos issues na mesma linha"""
        content = "Texto {\\bf negrito} e {\\it itálico}"
        issues = self.linter.lint_content(content)
        
        font_issues = [i for i in issues if i.rule_id == 'old_font_commands']
        self.assertGreaterEqual(len(font_issues), 2)

if __name__ == '__main__':
    unittest.main()



