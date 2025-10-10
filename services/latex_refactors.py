"""
LaTeX Refactoring Tools
Provides tools for sanitizing and refactoring LaTeX code
"""

import re
from typing import List, Dict, Tuple, Optional


class PatchSanitizer:
    """Sanitize LaTeX patches before applying"""
    
    @staticmethod
    def sanitize_patch(patch_content: str) -> str:
        """
        Sanitize a LaTeX patch
        
        Args:
            patch_content: Raw patch content
            
        Returns:
            Sanitized patch content
        """
        # Remove dangerous commands
        dangerous_patterns = [
            r'\\write18',
            r'\\input\{[^}]*\|',
            r'\\immediate\\write',
        ]
        
        sanitized = patch_content
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def validate_patch(patch_content: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a LaTeX patch
        
        Args:
            patch_content: Patch content to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for balanced braces
        brace_count = patch_content.count('{') - patch_content.count('}')
        if brace_count != 0:
            return False, f"Unbalanced braces: {brace_count} extra opening braces"
        
        # Check for balanced environments
        begin_count = len(re.findall(r'\\begin\{', patch_content))
        end_count = len(re.findall(r'\\end\{', patch_content))
        if begin_count != end_count:
            return False, f"Unbalanced environments: {begin_count} begin vs {end_count} end"
        
        return True, None


class LaTeXRefactor:
    """Refactor LaTeX code"""
    
    @staticmethod
    def normalize_whitespace(content: str) -> str:
        """
        Normalize whitespace in LaTeX content
        
        Args:
            content: LaTeX content
            
        Returns:
            Normalized content
        """
        # Remove trailing whitespace
        lines = [line.rstrip() for line in content.split('\n')]
        
        # Remove multiple blank lines
        result = []
        prev_blank = False
        for line in lines:
            is_blank = line.strip() == ''
            if not (is_blank and prev_blank):
                result.append(line)
            prev_blank = is_blank
        
        return '\n'.join(result)
    
    @staticmethod
    def fix_common_errors(content: str) -> str:
        """
        Fix common LaTeX errors
        
        Args:
            content: LaTeX content
            
        Returns:
            Fixed content
        """
        fixed = content
        
        # Fix common quote issues
        fixed = re.sub(r'(?<!\`)\"([^\"]+)\"', r"``\1''", fixed)
        
        # Fix common dash issues
        fixed = re.sub(r'(?<!-)-(?!-)', r'--', fixed)  # Convert single dash to en-dash
        
        # Fix spacing around math mode
        fixed = re.sub(r'\$\s+', r'$', fixed)
        fixed = re.sub(r'\s+\$', r'$', fixed)
        
        return fixed
    
    @staticmethod
    def extract_preamble(content: str) -> Tuple[str, str]:
        """
        Extract preamble from LaTeX document
        
        Args:
            content: Full LaTeX content
            
        Returns:
            Tuple of (preamble, body)
        """
        match = re.search(r'\\begin\{document\}', content)
        if match:
            preamble = content[:match.start()].strip()
            body = content[match.start():].strip()
            return preamble, body
        
        return '', content
    
    @staticmethod
    def add_package(content: str, package_name: str, options: Optional[str] = None) -> str:
        """
        Add a package to LaTeX preamble if not already present
        
        Args:
            content: LaTeX content
            package_name: Name of package to add
            options: Optional package options
            
        Returns:
            Content with package added
        """
        # Check if package already exists
        pattern = rf'\\usepackage(?:\[[^\]]*\])?\{{{package_name}\}}'
        if re.search(pattern, content):
            return content
        
        # Find documentclass line
        doc_match = re.search(r'\\documentclass.*?\n', content)
        if not doc_match:
            return content
        
        # Insert after documentclass
        insert_pos = doc_match.end()
        if options:
            package_line = f'\\usepackage[{options}]{{{package_name}}}\n'
        else:
            package_line = f'\\usepackage{{{package_name}}}\n'
        
        return content[:insert_pos] + package_line + content[insert_pos:]


class PatchApplier:
    """Apply patches to LaTeX documents"""
    
    @staticmethod
    def apply_patch(original: str, patch: str, line_number: Optional[int] = None) -> str:
        """
        Apply a patch to LaTeX content
        
        Args:
            original: Original LaTeX content
            patch: Patch to apply
            line_number: Optional line number to apply patch at
            
        Returns:
            Patched content
        """
        if line_number is not None:
            lines = original.split('\n')
            if 0 <= line_number < len(lines):
                lines.insert(line_number, patch)
                return '\n'.join(lines)
        
        # If no line number, append to end of preamble
        preamble, body = LaTeXRefactor.extract_preamble(original)
        if preamble:
            return preamble + '\n' + patch + '\n' + body
        else:
            return patch + '\n' + original
    
    @staticmethod
    def replace_text(content: str, old_text: str, new_text: str, count: int = -1) -> str:
        """
        Replace text in LaTeX content
        
        Args:
            content: LaTeX content
            old_text: Text to replace
            new_text: Replacement text
            count: Maximum number of replacements (-1 for all)
            
        Returns:
            Content with replacements
        """
        if count == -1:
            return content.replace(old_text, new_text)
        else:
            return content.replace(old_text, new_text, count)
    
    @staticmethod
    def insert_at_line(content: str, line_number: int, text: str) -> str:
        """
        Insert text at specific line number
        
        Args:
            content: LaTeX content
            line_number: Line number (0-indexed)
            text: Text to insert
            
        Returns:
            Content with text inserted
        """
        lines = content.split('\n')
        if 0 <= line_number <= len(lines):
            lines.insert(line_number, text)
        return '\n'.join(lines)
    
    @staticmethod
    def delete_lines(content: str, start_line: int, end_line: int) -> str:
        """
        Delete lines from content
        
        Args:
            content: LaTeX content
            start_line: Start line (0-indexed, inclusive)
            end_line: End line (0-indexed, exclusive)
            
        Returns:
            Content with lines deleted
        """
        lines = content.split('\n')
        if 0 <= start_line < end_line <= len(lines):
            del lines[start_line:end_line]
        return '\n'.join(lines)
