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
    
    def lint(self, content: str) -> Dict[str, List[Dict]]:
        """
        Lint LaTeX content
        
        Args:
            content: LaTeX content to lint
            
        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        self.warnings = []
        self.errors = []
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self._check_line(line, line_num)
        
        self._check_global(content)
        
        return {
            'errors': self.errors,
            'warnings': self.warnings
        }
    
    def _check_line(self, line: str, line_num: int):
        """Check a single line for issues"""
        
        # Check for unescaped special characters
        special_chars = ['&', '%', '$', '#', '_', '{', '}']
        for char in special_chars:
            if char in line and f'\\{char}' not in line:
                # Check if it's in a command or environment
                if not self._is_in_command(line, char):
                    self.warnings.append({
                        'line': line_num,
                        'message': f'Potentially unescaped special character: {char}',
                        'type': 'special_char'
                    })
        
        # Check for common quote mistakes
        if '"' in line:
            self.warnings.append({
                'line': line_num,
                'message': 'Use `` and \'\' instead of " for quotes in LaTeX',
                'type': 'quote_style'
            })
        
        # Check for trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            self.warnings.append({
                'line': line_num,
                'message': 'Trailing whitespace',
                'type': 'whitespace'
            })
        
        # Check for very long lines
        if len(line) > 120:
            self.warnings.append({
                'line': line_num,
                'message': f'Line too long ({len(line)} characters)',
                'type': 'line_length'
            })
    
    def _check_global(self, content: str):
        """Check global document issues"""
        
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
