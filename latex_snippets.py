"""
LaTeX Snippets Module
Provides predefined LaTeX code snippets for the editor
"""

SNIPPETS = {
    'section': {
        'name': 'Section',
        'description': 'Create a new section',
        'category': 'structure',
        'content': '\\section{${1:Section Title}}\n\n${2:Content here...}'
    },
    'subsection': {
        'name': 'Subsection',
        'description': 'Create a new subsection',
        'category': 'structure',
        'content': '\\subsection{${1:Subsection Title}}\n\n${2:Content here...}'
    },
    'equation': {
        'name': 'Equation',
        'description': 'Create an equation',
        'category': 'math',
        'content': '\\begin{equation}\n\t${1:equation}\n\\end{equation}'
    },
    'align': {
        'name': 'Align',
        'description': 'Create aligned equations',
        'category': 'math',
        'content': '\\begin{align}\n\t${1:equation1} &= ${2:value1} \\\\\n\t${3:equation2} &= ${4:value2}\n\\end{align}'
    },
    'itemize': {
        'name': 'Itemize List',
        'description': 'Create a bullet list',
        'category': 'lists',
        'content': '\\begin{itemize}\n\t\\item ${1:First item}\n\t\\item ${2:Second item}\n\\end{itemize}'
    },
    'enumerate': {
        'name': 'Enumerate List',
        'description': 'Create a numbered list',
        'category': 'lists',
        'content': '\\begin{enumerate}\n\t\\item ${1:First item}\n\t\\item ${2:Second item}\n\\end{enumerate}'
    },
    'table': {
        'name': 'Table',
        'description': 'Create a table',
        'category': 'tables',
        'content': '\\begin{table}[h]\n\t\\centering\n\t\\begin{tabular}{|c|c|}\n\t\t\\hline\n\t\t${1:Header 1} & ${2:Header 2} \\\\\n\t\t\\hline\n\t\t${3:Cell 1} & ${4:Cell 2} \\\\\n\t\t\\hline\n\t\\end{tabular}\n\t\\caption{${5:Table caption}}\n\t\\label{tab:${6:label}}\n\\end{table}'
    },
    'figure': {
        'name': 'Figure',
        'description': 'Insert a figure',
        'category': 'figures',
        'content': '\\begin{figure}[h]\n\t\\centering\n\t\\includegraphics[width=0.8\\textwidth]{${1:image.png}}\n\t\\caption{${2:Figure caption}}\n\t\\label{fig:${3:label}}\n\\end{figure}'
    },
    'bold': {
        'name': 'Bold',
        'description': 'Make text bold',
        'category': 'formatting',
        'content': '\\textbf{${1:text}}'
    },
    'italic': {
        'name': 'Italic',
        'description': 'Make text italic',
        'category': 'formatting',
        'content': '\\textit{${1:text}}'
    },
    'underline': {
        'name': 'Underline',
        'description': 'Underline text',
        'category': 'formatting',
        'content': '\\underline{${1:text}}'
    }
}

CATEGORIES = {
    'structure': 'Document Structure',
    'math': 'Mathematics',
    'lists': 'Lists',
    'tables': 'Tables',
    'figures': 'Figures',
    'formatting': 'Text Formatting'
}


def get_snippet(snippet_id):
    """Get a specific snippet by ID"""
    return SNIPPETS.get(snippet_id)


def get_snippets_by_category(category=None):
    """Get all snippets, optionally filtered by category"""
    if category:
        return {k: v for k, v in SNIPPETS.items() if v.get('category') == category}
    return SNIPPETS


def get_categories():
    """Get all available categories"""
    return CATEGORIES


def process_snippet_placeholders(content, values=None):
    """
    Process snippet placeholders
    
    Args:
        content: Snippet content with placeholders like ${1:default}
        values: Dictionary of placeholder values {1: 'value1', 2: 'value2'}
    
    Returns:
        Processed content with placeholders replaced
    """
    if not values:
        # Remove placeholder syntax, keep default values
        import re
        return re.sub(r'\$\{(\d+):([^}]+)\}', r'\2', content)
    
    # Replace with provided values
    result = content
    for key, value in values.items():
        import re
        result = re.sub(rf'\$\{{{key}:[^}}]+\}}', value, result)
    
    return result