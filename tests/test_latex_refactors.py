"""
Unit tests para refatorações e patches LaTeX
"""

import unittest
from services.latex_refactors import (
    PatchSanitizer, LaTeXRefactor, PatchApplier
)

class TestPatchSanitizer(unittest.TestCase):
    
    def test_block_write18(self):
        """Deve bloquear \\write18"""
        content = "\\write18{rm -rf /}"
        is_safe, error = PatchSanitizer.sanitize_content(content)
        self.assertFalse(is_safe)
        self.assertIn('write18', error.lower())
    
    def test_block_absolute_input(self):
        """Deve bloquear \\input com caminho absoluto"""
        content = "\\input{/etc/passwd}"
        is_safe, error = PatchSanitizer.sanitize_content(content)
        self.assertFalse(is_safe)
    
    def test_block_absolute_include(self):
        """Deve bloquear \\include com caminho absoluto"""
        content = "\\include{C:\\\\Windows\\\\system32\\\\config}"
        is_safe, error = PatchSanitizer.sanitize_content(content)
        self.assertFalse(is_safe)
    
    def test_allow_safe_content(self):
        """Deve permitir conteúdo seguro"""
        content = "\\section{Test}\n\\begin{equation}\nx^2\n\\end{equation}"
        is_safe, error = PatchSanitizer.sanitize_content(content)
        self.assertTrue(is_safe)
        self.assertIsNone(error)
    
    def test_block_large_patch(self):
        """Deve bloquear patches muito grandes"""
        content = "A" * 102401  # > 100KB
        is_safe, error = PatchSanitizer.sanitize_content(content)
        self.assertFalse(is_safe)
        self.assertIn('muito grande', error.lower())
    
    def test_sanitize_patch_data(self):
        """Deve validar dados completos do patch"""
        patch_data = {
            'file': 'main.tex',
            'range': {'start': 0, 'end': 10},
            'content': '\\section{Test}'
        }
        is_safe, error = PatchSanitizer.sanitize_patch(patch_data)
        self.assertTrue(is_safe)
    
    def test_block_invalid_filename(self):
        """Deve bloquear filenames com .."""
        patch_data = {
            'file': '../../../etc/passwd',
            'content': 'test'
        }
        is_safe, error = PatchSanitizer.sanitize_patch(patch_data)
        self.assertFalse(is_safe)
        self.assertIn('inválido', error.lower())

class TestLaTeXRefactor(unittest.TestCase):
    
    def test_eqnarray_to_align(self):
        """Deve converter eqnarray para align"""
        content = """
\\begin{eqnarray}
  x + y &=& 10 \\\\
  2x - y &=& 5
\\end{eqnarray}
"""
        modified, changes = LaTeXRefactor.eqnarray_to_align(content)
        
        self.assertIn('\\begin{align}', modified)
        self.assertIn('\\end{align}', modified)
        self.assertNotIn('eqnarray', modified)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['type'], 'refactor')
    
    def test_eqnarray_starred_to_align_starred(self):
        """Deve converter eqnarray* para align*"""
        content = "\\begin{eqnarray*}\nx = 1\n\\end{eqnarray*}"
        modified, changes = LaTeXRefactor.eqnarray_to_align(content)
        
        self.assertIn('\\begin{align*}', modified)
        self.assertIn('\\end{align*}', modified)
    
    def test_itemize_to_enumerate(self):
        """Deve converter itemize para enumerate"""
        content = """\\begin{itemize}
  \\item Item 1
  \\item Item 2
\\end{itemize}"""
        
        modified, changes = LaTeXRefactor.itemize_to_enumerate(content)
        
        self.assertIn('\\begin{enumerate}', modified)
        self.assertIn('\\end{enumerate}', modified)
        self.assertNotIn('itemize', modified)
        self.assertEqual(len(changes), 2)  # begin + end
    
    def test_dollar_to_displaymath(self):
        """Deve converter $$ para \\[ \\]"""
        content = "Equação: $$x^2 + y^2 = z^2$$"
        modified, changes = LaTeXRefactor.dollar_to_displaymath(content)
        
        self.assertIn('\\[', modified)
        self.assertIn('\\]', modified)
        self.assertNotIn('$$', modified)
        self.assertEqual(len(changes), 1)
    
    def test_suggest_refactors_eqnarray(self):
        """Deve sugerir refatoração de eqnarray"""
        content = "\\begin{eqnarray}\nx = 1\n\\end{eqnarray}"
        suggestions = LaTeXRefactor.suggest_refactors(content)
        
        self.assertGreater(len(suggestions), 0)
        eqnarray_suggestion = next(
            (s for s in suggestions if s['type'] == 'eqnarray_to_align'),
            None
        )
        self.assertIsNotNone(eqnarray_suggestion)
    
    def test_suggest_refactors_dollar(self):
        """Deve sugerir refatoração de $$"""
        content = "$$x^2$$"
        suggestions = LaTeXRefactor.suggest_refactors(content)
        
        dollar_suggestion = next(
            (s for s in suggestions if s['type'] == 'dollar_to_displaymath'),
            None
        )
        self.assertIsNotNone(dollar_suggestion)

class TestPatchApplier(unittest.TestCase):
    
    def test_apply_replace_patch(self):
        """Deve aplicar patch de substituição"""
        original = "Hello World"
        patch_data = {
            'type': 'replace',
            'range': {'start': 6, 'end': 11},
            'content': 'Universe'
        }
        
        modified, metadata = PatchApplier.apply_patch(original, patch_data)
        
        self.assertEqual(modified, "Hello Universe")
        self.assertIn('patch_id', metadata)
        self.assertEqual(metadata['type'], 'replace')
    
    def test_apply_insert_patch(self):
        """Deve aplicar patch de inserção"""
        original = "Hello World"
        patch_data = {
            'type': 'insert',
            'position': 5,
            'content': ' Beautiful'
        }
        
        modified, metadata = PatchApplier.apply_patch(original, patch_data)
        
        self.assertEqual(modified, "Hello Beautiful World")
    
    def test_apply_delete_patch(self):
        """Deve aplicar patch de deleção"""
        original = "Hello Beautiful World"
        patch_data = {
            'type': 'delete',
            'range': {'start': 5, 'end': 15}
        }
        
        modified, metadata = PatchApplier.apply_patch(original, patch_data)
        
        self.assertEqual(modified, "Hello World")
    
    def test_apply_refactor_patch(self):
        """Deve aplicar patch de refatoração"""
        original = "\\begin{eqnarray}\nx = 1\n\\end{eqnarray}"
        patch_data = {
            'type': 'refactor',
            'refactor_type': 'eqnarray_to_align'
        }
        
        modified, metadata = PatchApplier.apply_patch(original, patch_data)
        
        self.assertIn('align', modified)
        self.assertNotIn('eqnarray', modified)
    
    def test_generate_diff(self):
        """Deve gerar diff entre original e modificado"""
        original = "Line 1\nLine 2\nLine 3"
        modified = "Line 1\nLine 2 Modified\nLine 3"
        
        diff = PatchApplier.generate_diff(original, modified)
        
        self.assertGreater(len(diff), 0)
    
    def test_patch_metadata_includes_hashes(self):
        """Deve incluir hashes no metadata"""
        original = "Test content"
        patch_data = {
            'type': 'replace',
            'range': {'start': 0, 'end': 4},
            'content': 'Best'
        }
        
        modified, metadata = PatchApplier.apply_patch(original, patch_data)
        
        self.assertIn('original_hash', metadata)
        self.assertIn('modified_hash', metadata)
        self.assertNotEqual(metadata['original_hash'], metadata['modified_hash'])

if __name__ == '__main__':
    unittest.main()







