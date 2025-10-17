"""
Unit tests para o parser de logs LaTeX
"""

import unittest
from services.latex_log_parser import parse_latex_log, extract_line_number, get_suggestion

class TestLatexLogParser(unittest.TestCase):
    
    def test_extract_line_number_l_pattern(self):
        """Testa extração de linha no padrão l.<n>"""
        text = "l.42 \\foo"
        self.assertEqual(extract_line_number(text), 42)
    
    def test_extract_line_number_line_pattern(self):
        """Testa extração de linha no padrão 'line <n>'"""
        text = "Error on line 123"
        self.assertEqual(extract_line_number(text), 123)
    
    def test_extract_line_number_input_line_pattern(self):
        """Testa extração de linha no padrão 'on input line <n>'"""
        text = "Error on input line 56"
        self.assertEqual(extract_line_number(text), 56)
    
    def test_extract_line_number_no_match(self):
        """Testa quando não há número de linha"""
        text = "Some error without line number"
        self.assertIsNone(extract_line_number(text))
    
    def test_undefined_control_sequence(self):
        """Testa parsing de Undefined control sequence"""
        log = """
! Undefined control sequence.
l.42 \\foo
     {bar}
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['type'], 'error')
        self.assertEqual(errors[0]['line'], 42)
        self.assertIn('\\foo', errors[0]['message'])
    
    def test_missing_dollar(self):
        """Testa parsing de Missing $ inserted"""
        log = """
! Missing $ inserted.
<inserted text> 
                $
l.15 x
      ^2 + y^2 = z^2
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['type'], 'error')
        self.assertEqual(errors[0]['line'], 15)
    
    def test_latex_error(self):
        """Testa parsing de LaTeX Error"""
        log = """
! LaTeX Error: Environment equation undefined.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...                                              
                                                  
l.23 \\begin{equation}
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['type'], 'error')
        self.assertEqual(errors[0]['line'], 23)
    
    def test_package_error(self):
        """Testa parsing de Package Error"""
        log = """
! Package graphicx Error: File `image.png' not found.

See the graphicx package documentation for explanation.
Type  H <return>  for immediate help.
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['error_type'], 'Package graphicx Error')
    
    def test_warning(self):
        """Testa parsing de Warning"""
        log = """
LaTeX Warning: Citation `ref1' on page 1 undefined on input line 45.
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['type'], 'warning')
        self.assertEqual(errors[0]['line'], 45)
    
    def test_overfull_hbox(self):
        """Testa parsing de Overfull hbox"""
        log = """
Overfull \\hbox (12.34567pt too wide) in paragraph at lines 89--91
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['type'], 'info')
        self.assertEqual(errors[0]['line'], 89)
    
    def test_multiple_errors(self):
        """Testa parsing de múltiplos erros"""
        log = """
! Undefined control sequence.
l.10 \\foo
     
! Missing $ inserted.
l.20 x^2
        
LaTeX Warning: Reference `fig:test' on page 2 undefined on input line 30.
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0]['line'], 10)
        self.assertEqual(errors[1]['line'], 20)
        self.assertEqual(errors[2]['line'], 30)
    
    def test_no_errors(self):
        """Testa log sem erros"""
        log = """
This is pdfTeX, Version 3.14159265-2.6-1.40.21 (TeX Live 2020)
Output written on main.pdf (1 page, 12345 bytes).
Transcript written on main.log.
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 0)
    
    def test_suggestion_for_undefined_includegraphics(self):
        """Testa sugestão para \\includegraphics"""
        suggestion = get_suggestion('Undefined control sequence', 'Comando indefinido: \\includegraphics', '\\includegraphics')
        self.assertIsNotNone(suggestion)
        self.assertIn('graphicx', suggestion)
    
    def test_suggestion_for_undefined_cite(self):
        """Testa sugestão para \\cite"""
        suggestion = get_suggestion('Undefined control sequence', 'Comando indefinido: \\cite', '\\cite')
        self.assertIsNotNone(suggestion)
        self.assertIn('bibliografia', suggestion.lower())
    
    def test_suggestion_for_missing_dollar(self):
        """Testa sugestão para Missing $ inserted"""
        suggestion = get_suggestion('Missing $ inserted', 'Missing $ inserted')
        self.assertIsNotNone(suggestion)
        self.assertIn('$', suggestion)
    
    def test_edge_case_empty_log(self):
        """Testa edge case: log vazio"""
        errors = parse_latex_log("")
        self.assertEqual(len(errors), 0)
    
    def test_edge_case_malformed_log(self):
        """Testa edge case: log malformado"""
        log = "Random text\nwithout\nany\nstructure"
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 0)
    
    def test_filename_extraction(self):
        """Testa extração de nome de arquivo"""
        log = """
(./main.tex
! Undefined control sequence.
l.42 \\foo
"""
        errors = parse_latex_log(log)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]['filename'], 'main.tex')

if __name__ == '__main__':
    unittest.main()







