"""
Unit tests para gerador de BibTeX
"""

import unittest
from services.bibtex_generator import (
    BibTeXParser, BibTeXKeyGenerator, BibTeXManager, 
    BibTeXEntry, generate_bibtex_from_description
)

class TestBibTeXParser(unittest.TestCase):
    
    def test_parse_simple_description(self):
        """Testa parsing de descrição simples"""
        desc = "Deep Learning, Ian Goodfellow, 2016, MIT Press"
        fields = BibTeXParser.parse_description(desc)
        
        self.assertEqual(fields['title'], 'Deep Learning')
        self.assertEqual(fields['author'], 'Ian Goodfellow')
        self.assertEqual(fields['year'], '2016')
        self.assertEqual(fields['publisher'], 'MIT Press')
    
    def test_parse_multiple_authors(self):
        """Testa parsing com múltiplos autores"""
        desc = "Neural Networks, Ian Goodfellow, Yoshua Bengio, Aaron Courville, 2016"
        fields = BibTeXParser.parse_description(desc)
        
        self.assertIn('Goodfellow', fields['author'])
        self.assertIn('and', fields['author'])
    
    def test_parse_author_year_title_format(self):
        """Testa formato: Author (Year). Title. Publisher"""
        desc = "Ian Goodfellow (2016). Deep Learning. MIT Press"
        fields = BibTeXParser.parse_description(desc)
        
        self.assertEqual(fields['title'], 'Deep Learning')
        self.assertEqual(fields['author'], 'Ian Goodfellow')
        self.assertEqual(fields['year'], '2016')
    
    def test_parse_with_journal_keyword(self):
        """Testa detecção de tipo por keyword"""
        desc = "Article in Nature journal, Smith et al, 2020"
        fields = BibTeXParser.parse_description(desc)
        entry_type = BibTeXParser.detect_entry_type({'journal': 'Nature'})
        
        self.assertEqual(entry_type, 'article')
    
    def test_format_authors_with_and(self):
        """Testa formatação de autores"""
        author = "Ian Goodfellow, Yoshua Bengio, Aaron Courville"
        formatted = BibTeXParser.format_authors(author)
        
        self.assertIn(' and ', formatted)
        self.assertEqual(formatted.count(' and '), 2)
    
    def test_format_authors_already_formatted(self):
        """Testa que não altera autores já formatados"""
        author = "Ian Goodfellow and Yoshua Bengio"
        formatted = BibTeXParser.format_authors(author)
        
        self.assertEqual(formatted, author)
    
    def test_detect_entry_type_article(self):
        """Testa detecção de tipo article"""
        fields = {'journal': 'Nature', 'title': 'Test'}
        entry_type = BibTeXParser.detect_entry_type(fields)
        
        self.assertEqual(entry_type, 'article')
    
    def test_detect_entry_type_book(self):
        """Testa detecção de tipo book"""
        fields = {'publisher': 'MIT Press', 'title': 'Test'}
        entry_type = BibTeXParser.detect_entry_type(fields)
        
        self.assertEqual(entry_type, 'book')

class TestBibTeXKeyGenerator(unittest.TestCase):
    
    def test_generate_simple_key(self):
        """Testa geração de key simples"""
        fields = {
            'author': 'Ian Goodfellow',
            'year': '2016',
            'title': 'Deep Learning'
        }
        key = BibTeXKeyGenerator.generate_key(fields)
        
        self.assertEqual(key, 'Goodfellow2016DeepLearning')
    
    def test_generate_key_with_multiple_authors(self):
        """Testa key com múltiplos autores (usa primeiro)"""
        fields = {
            'author': 'Ian Goodfellow and Yoshua Bengio',
            'year': '2016',
            'title': 'Deep Learning Book'
        }
        key = BibTeXKeyGenerator.generate_key(fields)
        
        self.assertTrue(key.startswith('Goodfellow'))
        self.assertIn('2016', key)
    
    def test_generate_unique_key_with_conflict(self):
        """Testa geração de key única com conflito"""
        fields = {
            'author': 'Ian Goodfellow',
            'year': '2016',
            'title': 'Deep Learning'
        }
        existing = ['Goodfellow2016DeepLearning']
        key = BibTeXKeyGenerator.generate_key(fields, existing)
        
        self.assertNotEqual(key, 'Goodfellow2016DeepLearning')
        self.assertTrue(key.startswith('Goodfellow2016DeepLearning'))
    
    def test_clean_string_removes_accents(self):
        """Testa remoção de acentos"""
        clean = BibTeXKeyGenerator.clean_string('José García')
        
        self.assertEqual(clean, 'JoseGarcia')
    
    def test_extract_title_words(self):
        """Testa extração de palavras do título"""
        title = "The Deep Learning Revolution in AI"
        words = BibTeXKeyGenerator.extract_title_words(title)
        
        self.assertEqual(words, 'DeepLearning')
    
    def test_extract_title_words_removes_stop_words(self):
        """Testa que remove stop words"""
        title = "A Study on the Impact of AI"
        words = BibTeXKeyGenerator.extract_title_words(title)
        
        self.assertNotIn('the', words.lower())
        self.assertNotIn('of', words.lower())

class TestBibTeXEntry(unittest.TestCase):
    
    def test_to_bibtex_format(self):
        """Testa conversão para formato BibTeX"""
        entry = BibTeXEntry(
            'book',
            'Goodfellow2016',
            {
                'title': 'Deep Learning',
                'author': 'Ian Goodfellow',
                'year': '2016',
                'publisher': 'MIT Press'
            }
        )
        bibtex = entry.to_bibtex()
        
        self.assertIn('@book{Goodfellow2016,', bibtex)
        self.assertIn('title = {Deep Learning}', bibtex)
        self.assertIn('author = {Ian Goodfellow}', bibtex)
        self.assertIn('year = {2016}', bibtex)
    
    def test_field_ordering(self):
        """Testa ordenação de campos (title, author, year primeiro)"""
        entry = BibTeXEntry(
            'book',
            'Test2024',
            {
                'publisher': 'Press',
                'year': '2024',
                'author': 'Smith',
                'title': 'Title'
            }
        )
        bibtex = entry.to_bibtex()
        lines = bibtex.split('\n')
        
        # title, author, year devem vir antes de publisher
        title_idx = next(i for i, line in enumerate(lines) if 'title' in line)
        author_idx = next(i for i, line in enumerate(lines) if 'author' in line)
        year_idx = next(i for i, line in enumerate(lines) if 'year' in line)
        publisher_idx = next(i for i, line in enumerate(lines) if 'publisher' in line)
        
        self.assertTrue(title_idx < publisher_idx)
        self.assertTrue(author_idx < publisher_idx)
        self.assertTrue(year_idx < publisher_idx)

class TestBibTeXManager(unittest.TestCase):
    
    def test_parse_existing_bib(self):
        """Testa parsing de .bib existente"""
        bib_content = """
@book{Goodfellow2016,
  title = {Deep Learning},
  author = {Ian Goodfellow},
  year = {2016}
}
"""
        manager = BibTeXManager(bib_content)
        
        self.assertEqual(len(manager.entries), 1)
        self.assertEqual(manager.entries[0].key, 'Goodfellow2016')
    
    def test_get_existing_keys(self):
        """Testa obtenção de keys existentes"""
        bib_content = """
@book{Key1,
  title = {Title 1}
}
@article{Key2,
  title = {Title 2}
}
"""
        manager = BibTeXManager(bib_content)
        keys = manager.get_existing_keys()
        
        self.assertIn('Key1', keys)
        self.assertIn('Key2', keys)
        self.assertEqual(len(keys), 2)
    
    def test_add_entry_success(self):
        """Testa adição de entrada com sucesso"""
        manager = BibTeXManager()
        entry = BibTeXEntry('book', 'NewKey', {'title': 'New Book'})
        
        result = manager.add_entry(entry)
        
        self.assertTrue(result)
        self.assertEqual(len(manager.entries), 1)
    
    def test_add_entry_conflict(self):
        """Testa rejeição de entrada com key duplicada"""
        manager = BibTeXManager('@book{ExistingKey,\n  title = {Test}\n}')
        entry = BibTeXEntry('book', 'ExistingKey', {'title': 'Duplicate'})
        
        result = manager.add_entry(entry)
        
        self.assertFalse(result)
        self.assertEqual(len(manager.entries), 1)
    
    def test_find_entry(self):
        """Testa busca de entrada por key"""
        bib_content = '@book{FindMe,\n  title = {Test}\n}'
        manager = BibTeXManager(bib_content)
        
        entry = manager.find_entry('FindMe')
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.key, 'FindMe')

class TestGenerateBibTeXFromDescription(unittest.TestCase):
    
    def test_generate_from_simple_description(self):
        """Testa geração completa a partir de descrição"""
        desc = "Deep Learning, Ian Goodfellow, 2016, MIT Press"
        result = generate_bibtex_from_description(desc)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['key'], 'Goodfellow2016DeepLearning')
        self.assertIn('@book', result['bibtex'])
    
    def test_generate_with_existing_bib(self):
        """Testa geração com .bib existente"""
        existing = '@book{Goodfellow2016DeepLearning,\n  title = {Test}\n}'
        desc = "Deep Learning, Ian Goodfellow, 2016, MIT Press"
        result = generate_bibtex_from_description(desc, existing)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['has_conflict'] or result['key'] != 'Goodfellow2016DeepLearning')
    
    def test_generate_with_conflict(self):
        """Testa detecção de conflito"""
        existing = '@book{Goodfellow2016DeepLearning,\n  title = {Old Title}\n}'
        desc = "Deep Learning, Ian Goodfellow, 2016, MIT Press"
        result = generate_bibtex_from_description(desc, existing)
        
        # Deve gerar key alternativa (com sufixo)
        self.assertTrue(result['success'])
        self.assertNotEqual(result['key'], 'Goodfellow2016DeepLearning')
    
    def test_generate_article_type(self):
        """Testa geração de artigo"""
        desc = "Article in Nature, John Smith, 2023"
        result = generate_bibtex_from_description(desc, entry_type='article')
        
        self.assertEqual(result['entry_type'], 'article')
        self.assertIn('@article', result['bibtex'])
    
    def test_multiple_authors_in_description(self):
        """Testa descrição com múltiplos autores"""
        desc = "Neural Networks, Goodfellow, Bengio, Courville, 2016, MIT Press"
        result = generate_bibtex_from_description(desc)
        
        self.assertTrue(result['success'])
        self.assertIn(' and ', result['fields']['author'])

if __name__ == '__main__':
    unittest.main()



