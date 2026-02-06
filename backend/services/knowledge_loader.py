"""
Knowledge Loader Service
Loads text files and PDFs from knowledge base directory.
Caches content in memory for fast retrieval.
"""

import os
from services.pdf_parser import PDFParser

class KnowledgeLoader:
    """Service for loading and caching knowledge base files."""
    
    def __init__(self):
        """Initialize knowledge loader."""
        self.text_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'text')
        self.pdf_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'pdfs')
        self.pdf_parser = PDFParser()
        self.knowledge_base = {}
        
        # Load all knowledge on initialization
        self.load_all()
    
    def load_all(self):
        """Load all knowledge files into memory."""
        print("Loading knowledge base...")
        
        # Load text files
        text_count = self._load_text_files()
        
        # Load PDF files
        pdf_count = self._load_pdf_files()
        
        total_files = text_count + pdf_count
        print(f"✓ Knowledge base loaded: {text_count} text files, {pdf_count} PDFs, {total_files} total")
        
        return total_files
    
    def _load_text_files(self):
        """Load all .txt files from knowledge/text/ directory."""
        count = 0
        
        if not os.path.exists(self.text_dir):
            print(f"Text knowledge directory not found: {self.text_dir}")
            return count
        
        for filename in os.listdir(self.text_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.text_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Store with filename as key (without .txt extension)
                    key = filename[:-4]
                    self.knowledge_base[key] = {
                        'type': 'text',
                        'filename': filename,
                        'content': content,
                        'source': filepath
                    }
                    count += 1
                    print(f"  Loaded: {filename}")
                
                except Exception as e:
                    print(f"  Error loading {filename}: {str(e)}")
        
        return count
    
    def _load_pdf_files(self):
        """Load all .pdf files from knowledge/pdfs/ directory."""
        count = 0
        
        if not os.path.exists(self.pdf_dir):
            print(f"PDF knowledge directory not found: {self.pdf_dir}")
            return count
        
        for filename in os.listdir(self.pdf_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(self.pdf_dir, filename)
                try:
                    # Extract text from PDF
                    content = self.pdf_parser.extract_text(filepath)
                    content = self.pdf_parser.clean_text(content)
                    
                    # Store with filename as key (without .pdf extension)
                    key = filename[:-4]
                    self.knowledge_base[key] = {
                        'type': 'pdf',
                        'filename': filename,
                        'content': content,
                        'source': filepath
                    }
                    count += 1
                    print(f"  Loaded: {filename}")
                
                except Exception as e:
                    print(f"  Error loading {filename}: {str(e)}")
        
        return count
    
    def get_all_files(self):
        """Get list of all loaded knowledge files."""
        return list(self.knowledge_base.keys())
    
    def get_file_content(self, key):
        """
        Get content of a specific knowledge file.
        
        Args:
            key (str): Filename without extension
        
        Returns:
            str: File content or None if not found
        """
        if key in self.knowledge_base:
            return self.knowledge_base[key]['content']
        return None
    
    def get_all_content(self):
        """
        Get all knowledge base content as a dictionary.
        
        Returns:
            dict: Dictionary with filename keys and content values
        """
        return {key: data['content'] for key, data in self.knowledge_base.items()}
    
    def search_content(self, query_keywords):
        """
        Search for content containing keywords.
        
        Args:
            query_keywords (list): List of keywords to search
        
        Returns:
            dict: Dictionary with matching files and their content
        """
        matching_files = {}
        
        for key, data in self.knowledge_base.items():
            content = data['content'].lower()
            score = 0
            
            # Count keyword matches
            for keyword in query_keywords:
                keyword_lower = keyword.lower()
                score += content.count(keyword_lower)
            
            if score > 0:
                matching_files[key] = {
                    'content': data['content'],
                    'score': score,
                    'type': data['type']
                }
        
        # Sort by score (descending)
        matching_files = dict(sorted(
            matching_files.items(),
            key=lambda item: item[1]['score'],
            reverse=True
        ))
        
        return matching_files
    
    def reload(self):
        """Reload all knowledge files (useful if files are updated)."""
        self.knowledge_base = {}
        return self.load_all()
