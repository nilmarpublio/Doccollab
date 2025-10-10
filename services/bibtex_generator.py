"""
BibTeX Generator
Generates BibTeX entries from descriptions or metadata
"""

import re
from typing import Dict, Optional


def generate_bibtex_from_description(description: str, entry_type: str = 'article') -> str:
    """
    Generate a BibTeX entry from a description
    
    Args:
        description: Description or metadata about the reference
        entry_type: Type of BibTeX entry (article, book, etc.)
        
    Returns:
        BibTeX entry as string
    """
    # Extract common fields from description
    fields = extract_fields_from_description(description)
    
    # Generate citation key
    cite_key = generate_cite_key(fields)
    
    # Build BibTeX entry
    bibtex = f"@{entry_type}{{{cite_key},\n"
    
    # Add fields
    if 'author' in fields:
        bibtex += f"  author = {{{fields['author']}}},\n"
    if 'title' in fields:
        bibtex += f"  title = {{{fields['title']}}},\n"
    if 'year' in fields:
        bibtex += f"  year = {{{fields['year']}}},\n"
    if 'journal' in fields:
        bibtex += f"  journal = {{{fields['journal']}}},\n"
    if 'volume' in fields:
        bibtex += f"  volume = {{{fields['volume']}}},\n"
    if 'pages' in fields:
        bibtex += f"  pages = {{{fields['pages']}}},\n"
    if 'publisher' in fields:
        bibtex += f"  publisher = {{{fields['publisher']}}},\n"
    
    bibtex += "}\n"
    
    return bibtex


def extract_fields_from_description(description: str) -> Dict[str, str]:
    """
    Extract BibTeX fields from a description
    
    Args:
        description: Description text
        
    Returns:
        Dictionary of field names to values
    """
    fields = {}
    
    # Try to extract year (4 digits)
    year_match = re.search(r'\b(19|20)\d{2}\b', description)
    if year_match:
        fields['year'] = year_match.group(0)
    
    # Try to extract author (look for patterns like "by Author Name" or "Author Name,")
    author_patterns = [
        r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+),',
    ]
    for pattern in author_patterns:
        author_match = re.search(pattern, description)
        if author_match:
            fields['author'] = author_match.group(1)
            break
    
    # Try to extract title (text in quotes or after colon)
    title_patterns = [
        r'"([^"]+)"',
        r"'([^']+)'",
        r':\s*([^,\n]+)',
    ]
    for pattern in title_patterns:
        title_match = re.search(pattern, description)
        if title_match:
            fields['title'] = title_match.group(1)
            break
    
    # If no specific fields found, use description as title
    if not fields:
        fields['title'] = description[:100]  # First 100 chars
    
    return fields


def generate_cite_key(fields: Dict[str, str]) -> str:
    """
    Generate a citation key from fields
    
    Args:
        fields: Dictionary of BibTeX fields
        
    Returns:
        Citation key string
    """
    parts = []
    
    # Add author last name
    if 'author' in fields:
        author = fields['author'].split()[-1]  # Last word (last name)
        parts.append(author.lower())
    
    # Add year
    if 'year' in fields:
        parts.append(fields['year'])
    
    # If no parts, use generic
    if not parts:
        parts = ['ref', '2025']
    
    return '_'.join(parts)


def create_article_entry(author: str, title: str, year: str, 
                        journal: str, volume: Optional[str] = None,
                        pages: Optional[str] = None) -> str:
    """
    Create a BibTeX article entry
    
    Args:
        author: Author name(s)
        title: Article title
        year: Publication year
        journal: Journal name
        volume: Volume number (optional)
        pages: Page numbers (optional)
        
    Returns:
        BibTeX entry as string
    """
    cite_key = generate_cite_key({'author': author, 'year': year})
    
    entry = f"@article{{{cite_key},\n"
    entry += f"  author = {{{author}}},\n"
    entry += f"  title = {{{title}}},\n"
    entry += f"  year = {{{year}}},\n"
    entry += f"  journal = {{{journal}}},\n"
    
    if volume:
        entry += f"  volume = {{{volume}}},\n"
    if pages:
        entry += f"  pages = {{{pages}}},\n"
    
    entry += "}\n"
    
    return entry


def create_book_entry(author: str, title: str, year: str,
                     publisher: str, address: Optional[str] = None) -> str:
    """
    Create a BibTeX book entry
    
    Args:
        author: Author name(s)
        title: Book title
        year: Publication year
        publisher: Publisher name
        address: Publisher address (optional)
        
    Returns:
        BibTeX entry as string
    """
    cite_key = generate_cite_key({'author': author, 'year': year})
    
    entry = f"@book{{{cite_key},\n"
    entry += f"  author = {{{author}}},\n"
    entry += f"  title = {{{title}}},\n"
    entry += f"  year = {{{year}}},\n"
    entry += f"  publisher = {{{publisher}}},\n"
    
    if address:
        entry += f"  address = {{{address}}},\n"
    
    entry += "}\n"
    
    return entry


def create_inproceedings_entry(author: str, title: str, year: str,
                               booktitle: str, pages: Optional[str] = None) -> str:
    """
    Create a BibTeX inproceedings entry
    
    Args:
        author: Author name(s)
        title: Paper title
        year: Publication year
        booktitle: Conference/proceedings name
        pages: Page numbers (optional)
        
    Returns:
        BibTeX entry as string
    """
    cite_key = generate_cite_key({'author': author, 'year': year})
    
    entry = f"@inproceedings{{{cite_key},\n"
    entry += f"  author = {{{author}}},\n"
    entry += f"  title = {{{title}}},\n"
    entry += f"  year = {{{year}}},\n"
    entry += f"  booktitle = {{{booktitle}}},\n"
    
    if pages:
        entry += f"  pages = {{{pages}}},\n"
    
    entry += "}\n"
    
    return entry
