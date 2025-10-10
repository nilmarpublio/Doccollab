"""
LaTeX Log Parser
Parses LaTeX compilation logs and extracts error messages
"""

import re
from typing import List, Dict, Optional


def parse_latex_log(log_content: str) -> List[Dict[str, any]]:
    """
    Parse LaTeX log file and extract errors
    
    Args:
        log_content: Content of the LaTeX log file
        
    Returns:
        List of error dictionaries with line, file, and message
    """
    errors = []
    lines = log_content.split('\n')
    
    for i, line in enumerate(lines):
        # Look for error patterns
        if line.startswith('!'):
            error = {
                'type': 'error',
                'line': None,
                'file': None,
                'message': line[1:].strip()
            }
            
            # Try to find line number in next few lines
            for j in range(i+1, min(i+5, len(lines))):
                line_match = re.search(r'l\.(\d+)', lines[j])
                if line_match:
                    error['line'] = int(line_match.group(1))
                    break
            
            errors.append(error)
        
        # Look for warnings
        elif 'Warning' in line:
            error = {
                'type': 'warning',
                'line': None,
                'file': None,
                'message': line.strip()
            }
            errors.append(error)
    
    return errors


def format_error_message(errors: List[Dict[str, any]]) -> str:
    """
    Format error list into human-readable message
    
    Args:
        errors: List of error dictionaries
        
    Returns:
        Formatted error message string
    """
    if not errors:
        return "Compilation successful!"
    
    message_parts = []
    
    for error in errors:
        error_type = error.get('type', 'error').upper()
        line_num = error.get('line')
        msg = error.get('message', 'Unknown error')
        
        if line_num:
            message_parts.append(f"{error_type} (line {line_num}): {msg}")
        else:
            message_parts.append(f"{error_type}: {msg}")
    
    return '\n'.join(message_parts)


def extract_missing_packages(log_content: str) -> List[str]:
    """
    Extract list of missing LaTeX packages from log
    
    Args:
        log_content: Content of the LaTeX log file
        
    Returns:
        List of missing package names
    """
    packages = []
    pattern = r"File `([^']+)\.sty' not found"
    
    matches = re.finditer(pattern, log_content)
    for match in matches:
        packages.append(match.group(1))
    
    return packages


def get_error_context(log_content: str, error_line: int, context_lines: int = 3) -> Optional[str]:
    """
    Get context around an error line
    
    Args:
        log_content: Content of the LaTeX log file
        error_line: Line number of the error
        context_lines: Number of lines before/after to include
        
    Returns:
        Context string or None
    """
    lines = log_content.split('\n')
    
    if error_line < 1 or error_line > len(lines):
        return None
    
    start = max(0, error_line - context_lines - 1)
    end = min(len(lines), error_line + context_lines)
    
    context = lines[start:end]
    return '\n'.join(context)
