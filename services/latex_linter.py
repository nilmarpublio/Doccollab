"""
LaTeX Linter
Provides linting and style checking for LaTeX documents
"""

import re
from typing import List, Dict, Optional, Tuple


class LaTeXLinter:
    """Lint LaTeX documents for common issues"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.suggestions = []
    
    def lint(self, content: str) -> Dict[str, List[Dict]]:
        """
        Lint LaTeX content
        
        Args:
            content: LaTeX content to lint
        
        Returns:
            Dictionary with 'errors', 'warnings', and 'suggestions' lists
        """
        self.warnings = []
        self.errors = []
        self.suggestions = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self._check_line(line, line_num, lines)
        
        self._check_global(content)
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }
    
    def _check_line(self, line: str, line_num: int, all_lines: List[str]):
        """Check a single line for issues"""
        
        # Skip comments
        if line.strip().startswith('%'):
            return
        
        # Check for unmatched braces on single line
        line_no_comments = re.sub(r'%.*$', '', line)
        open_braces = line_no_comments.count('{')
        close_braces = line_no_comments.count('}')
        if open_braces != close_braces:
            self.warnings.append({
                'line': line_num,
                'message': f'Unmatched braces on this line: {open_braces} opening, {close_braces} closing',
                'type': 'braces_line',
                'suggestion': 'Check if you forgot to close or open a brace'
            })
        
        # Check for common command typos
        typos = {
            r'\\begind{': r'\\begin{',
            r'\\endd{': r'\\end{',
            r'\\docmentclass': r'\\documentclass',
            r'\\uspackage': r'\\usepackage',
            r'\\includ graphics': r'\\includegraphics',
            r'\\lable{': r'\\label{',
            r'\\rf{': r'\\ref{',
        }
        for typo, correct in typos.items():
            if re.search(typo, line):
                self.errors.append({
                    'line': line_num,
                    'message': f'Possible typo: found "{typo.replace("\\\\", "\\")}"',
                    'type': 'typo',
                    'suggestion': f'Did you mean "{correct.replace("\\\\", "\\")}"?',
                    'fix': line.replace(typo.replace('\\\\', '\\'), correct.replace('\\\\', '\\'))
                })
        
        # Check for missing $ in math mode
        if re.search(r'[^$\\]_[^{]', line) or re.search(r'[^$\\]\^[^{]', line):
            self.errors.append({
                'line': line_num,
                'message': 'Subscript (_) or superscript (^) outside math mode',
                'type': 'math_mode',
                'suggestion': 'Wrap in $ $ for inline math or use \\[ \\] for display math'
            })
        
        # Check for common quote mistakes
        if '"' in line_no_comments:
            self.warnings.append({
                'line': line_num,
                'message': 'Use `` and \'\' instead of " for quotes in LaTeX',
                'type': 'quote_style',
                'suggestion': 'Replace " with `` (opening) or \'\' (closing)',
                'fix': line.replace('"', '``', 1).replace('"', "''", 1)
            })
        
        # Check for \\ at end of line (common mistake)
        if line.strip().endswith('\\\\') and not any(env in line for env in ['tabular', 'array', 'align']):
            self.warnings.append({
                'line': line_num,
                'message': 'Double backslash (\\\\) at end of line',
                'type': 'line_break',
                'suggestion': 'Use blank line for paragraph break, or remove if unintended'
            })
        
        # Check for missing packages
        if '\\includegraphics' in line and line_num < 20:
            # Check if graphicx is loaded (rough heuristic)
            preamble = ''.join(all_lines[:line_num])
            if 'graphicx' not in preamble:
                self.errors.append({
                    'line': line_num,
                    'message': '\\includegraphics requires \\usepackage{graphicx}',
                    'type': 'missing_package',
                    'suggestion': 'Add \\usepackage{graphicx} to preamble'
                })
        
        # Check for trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            self.warnings.append({
                'line': line_num,
                'message': 'Trailing whitespace',
                'type': 'whitespace',
                'fix': line.rstrip()
            })
        
        # Check for very long lines
        if len(line) > 120:
            self.warnings.append({
                'line': line_num,
                'message': f'Line too long ({len(line)} characters)',
                'type': 'line_length',
                'suggestion': 'Consider breaking into multiple lines for readability'
            })
    
    def _check_global(self, content: str):
        """Check global document issues"""
        
        # Check for multiple \documentclass
        documentclass_matches = list(re.finditer(r'\\documentclass', content))
        if len(documentclass_matches) > 1:
            self.errors.append({
                'line': None,
                'message': f'Multiple \\documentclass found ({len(documentclass_matches)} times). Only one is allowed per document.',
                'type': 'multiple_documentclass'
            })
        
        # Check for multiple \begin{document}
        begin_doc_matches = list(re.finditer(r'\\begin\{document\}', content))
        if len(begin_doc_matches) > 1:
            self.errors.append({
                'line': None,
                'message': f'Multiple \\begin{{document}} found ({len(begin_doc_matches)} times). Only one is allowed.',
                'type': 'multiple_begin_document'
            })
        
        # Check for multiple \end{document}
        end_doc_matches = list(re.finditer(r'\\end\{document\}', content))
        if len(end_doc_matches) > 1:
            self.errors.append({
                'line': None,
                'message': f'Multiple \\end{{document}} found ({len(end_doc_matches)} times). Only one is allowed.',
                'type': 'multiple_end_document'
            })
        
        # Check for content after \end{document}
        if end_doc_matches:
            last_end_doc = end_doc_matches[-1]
            content_after = content[last_end_doc.end():].strip()
            # Remove comments
            content_after_no_comments = re.sub(r'%.*', '', content_after).strip()
            if content_after_no_comments:
                # Get first 50 chars of content after
                preview = content_after_no_comments[:50]
                if len(content_after_no_comments) > 50:
                    preview += '...'
                self.errors.append({
                    'line': None,
                    'message': f'Content found after \\end{{document}}: "{preview}"',
                    'type': 'content_after_end_document'
                })
        
        # Check for duplicate labels
        labels = re.findall(r'\\label\{([^}]+)\}', content)
        label_counts = {}
        for label in labels:
            label_counts[label] = label_counts.get(label, 0) + 1
        
        for label, count in label_counts.items():
            if count > 1:
                self.errors.append({
                    'line': None,
                    'message': f'Duplicate label "{label}" found {count} times',
                    'type': 'duplicate_label'
                })
        
        # Check for missing referenced files
        cite_matches = re.findall(r'\\cite\{([^}]+)\}', content)
        if cite_matches and '\\bibliography{' not in content and '\\begin{thebibliography}' not in content:
            self.warnings.append({
                'line': None,
                'message': f'Found \\cite commands but no \\bibliography or thebibliography environment',
                'type': 'missing_bibliography'
            })
        
        # Check for bibliography without file
        bib_matches = re.findall(r'\\bibliography\{([^}]+)\}', content)
        if bib_matches:
            for bib_file in bib_matches:
                self.warnings.append({
                    'line': None,
                    'message': f'Bibliography file "{bib_file}.bib" referenced - ensure it exists',
                    'type': 'bibliography_file'
                })
        
        # Check for text after \end{environment}
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '\\end{' in line:
                # Check if there's non-whitespace text after \end{...}
                match = re.search(r'\\end\{[^}]+\}(.+)', line)
                if match and match.group(1).strip() and not match.group(1).strip().startswith('%'):
                    self.errors.append({
                        'line': i,
                        'message': f'Text found after \\end command: "{match.group(1).strip()}"',
                        'type': 'text_after_end'
                    })
        
        # Check for balanced braces
        brace_count = content.count('{') - content.count('}')
        if brace_count != 0:
            self.errors.append({
                'line': None,
                'message': f'Unbalanced braces: {abs(brace_count)} {"extra opening" if brace_count > 0 else "extra closing"}',
                'type': 'braces'
            })
        
        # Check for balanced environments
        begin_matches = re.findall(r'\\begin\{([^}]+)\}', content)
        end_matches = re.findall(r'\\end\{([^}]+)\}', content)
        
        begin_counts = {}
        for env in begin_matches:
            begin_counts[env] = begin_counts.get(env, 0) + 1
        
        end_counts = {}
        for env in end_matches:
            end_counts[env] = end_counts.get(env, 0) + 1
        
        for env in set(list(begin_counts.keys()) + list(end_counts.keys())):
            begin = begin_counts.get(env, 0)
            end = end_counts.get(env, 0)
            if begin != end:
                self.errors.append({
                    'line': None,
                    'message': f'Unbalanced environment "{env}": {begin} begin vs {end} end',
                    'type': 'environment'
                })
        
        # Check for documentclass
        if '\\documentclass' not in content:
            self.warnings.append({
                'line': None,
                'message': 'No \\documentclass found',
                'type': 'structure'
            })
        
        # Check for begin/end document
        if '\\begin{document}' not in content:
            self.errors.append({
                'line': None,
                'message': 'No \\begin{document} found',
                'type': 'structure'
            })
        
        if '\\end{document}' not in content:
            self.errors.append({
                'line': None,
                'message': 'No \\end{document} found',
                'type': 'structure'
            })
    
    def _is_in_command(self, line: str, char: str) -> bool:
        """Check if character is part of a LaTeX command"""
        # Simple heuristic: check if preceded by backslash
        escaped = f'\\{char}'
        return escaped in line
    
    @staticmethod
    def check_package_exists(content: str, package_name: str) -> bool:
        """
        Check if a package is included in the document
        
        Args:
            content: LaTeX content
            package_name: Name of package to check
            
        Returns:
            True if package is included
        """
        pattern = rf'\\usepackage(?:\[[^\]]*\])?\{{{package_name}\}}'
        return bool(re.search(pattern, content))
    
    @staticmethod
    def find_undefined_references(content: str) -> List[str]:
        """
        Find potentially undefined references
        
        Args:
            content: LaTeX content
            
        Returns:
            List of undefined reference labels
        """
        # Find all \ref{} and \cite{} commands
        ref_pattern = r'\\(?:ref|cite|eqref)\{([^}]+)\}'
        refs = set(re.findall(ref_pattern, content))
        
        # Find all \label{} commands
        label_pattern = r'\\label\{([^}]+)\}'
        labels = set(re.findall(label_pattern, content))
        
        # Find refs without corresponding labels
        undefined = refs - labels
        
        return list(undefined)
    
    def auto_fix(self, content: str) -> str:
        """
        Automatically fix common issues
        
        Args:
            content: LaTeX content
            
        Returns:
            Fixed content
        """
        fixed = content
        
        # Fix trailing whitespace
        lines = fixed.split('\n')
        lines = [line.rstrip() for line in lines]
        fixed = '\n'.join(lines)
        
        # Fix common quote mistakes
        # This is simplistic - real implementation would need better logic
        fixed = re.sub(r'"([^"]+)"', r'``\1' + "''", fixed)
        
        # Remove duplicate \end{document}
        end_doc_count = fixed.count('\\end{document}')
        if end_doc_count > 1:
            # Keep only the first occurrence
            parts = fixed.split('\\end{document}')
            fixed = parts[0] + '\\end{document}'
        
        # Remove content after \end{document}
        if '\\end{document}' in fixed:
            idx = fixed.rfind('\\end{document}')
            fixed = fixed[:idx + len('\\end{document}')]
        
        # Remove duplicate \documentclass
        documentclass_matches = list(re.finditer(r'\\documentclass[^\n]*\n', fixed))
        if len(documentclass_matches) > 1:
            # Keep only the first one
            first_match = documentclass_matches[0]
            for match in documentclass_matches[1:]:
                fixed = fixed[:match.start()] + fixed[match.end():]
        
        return fixed
    
    @staticmethod
    def suggest_packages(content: str) -> List[Tuple[str, str]]:
        """
        Suggest packages based on content
        
        Args:
            content: LaTeX content
        
        Returns:
            List of (package_name, reason) tuples
        """
        suggestions = []
        
        # Check for math mode without amsmath
        if ('$' in content or '\\[' in content) and not LaTeXLinter.check_package_exists(content, 'amsmath'):
            suggestions.append(('amsmath', 'For enhanced math support'))
        
        # Check for graphics without graphicx
        if '\\includegraphics' in content and not LaTeXLinter.check_package_exists(content, 'graphicx'):
            suggestions.append(('graphicx', 'Required for \\includegraphics'))
        
        # Check for colors without xcolor
        if ('\\color' in content or '\\textcolor' in content) and not LaTeXLinter.check_package_exists(content, 'xcolor'):
            suggestions.append(('xcolor', 'Required for color commands'))
        
        # Check for hyperlinks without hyperref
        if ('\\href' in content or '\\url' in content) and not LaTeXLinter.check_package_exists(content, 'hyperref'):
            suggestions.append(('hyperref', 'Required for hyperlinks'))
        
        return suggestions
