"""
Phase 2: Text Extraction and Integration
Extracts text from HTML and PDFs, cleans it, and integrates into knowledge base.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re
from datetime import datetime

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    
try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class TextExtractor:
    """Extract and clean text from HTML and PDF files."""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.raw_dir = self.base_dir / "data" / "raw"
        self.text_raw_dir = self.base_dir / "data" / "text" / "raw"
        self.text_meta_dir = self.base_dir / "data" / "text" / "meta"
        # Project root is parent of crawler directory
        project_root = self.base_dir.parent
        self.knowledge_text_dir = project_root / "backend" / "knowledge" / "text"
        self.knowledge_pdf_dir = project_root / "backend" / "knowledge" / "pdfs"
        
        # Create directories
        for dir_path in [self.text_raw_dir, self.text_meta_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def extract_text_from_html(self, html_path):
        """Extract main content from HTML file."""
        try:
            with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script, style, nav, header, footer elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find main content by common tags
            main_content = None
            for tag in ['main', 'article', '#content', '.content', '.main-content']:
                if tag.startswith('#'):
                    main_content = soup.find(id=tag[1:])
                elif tag.startswith('.'):
                    main_content = soup.find(class_=tag[1:])
                else:
                    main_content = soup.find(tag)
                
                if main_content:
                    break
            
            # If no main content found, use body
            if not main_content:
                main_content = soup.find('body') or soup
            
            # Extract text
            text = main_content.get_text(separator='\n', strip=True)
            
            # Get title
            title_tag = soup.find('title')
            title = title_tag.get_text(strip=True) if title_tag else html_path.stem
            
            # Clean text
            text = self.clean_text(text)
            
            return {
                'text': text,
                'title': title,
                'word_count': len(text.split())
            }
            
        except Exception as e:
            print(f"Error extracting from HTML {html_path}: {str(e)}")
            return None
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file."""
        text = ""
        title = pdf_path.stem
        
        try:
            # Try pdfplumber first (better quality)
            if PDFPLUMBER_AVAILABLE:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n\n"
            
            # Fallback to PyPDF2
            elif PYPDF2_AVAILABLE:
                reader = PdfReader(str(pdf_path))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            
            else:
                print("No PDF library available. Install pdfplumber or PyPDF2")
                return None
            
            # Clean text
            text = self.clean_text(text)
            
            return {
                'text': text,
                'title': title,
                'word_count': len(text.split())
            }
            
        except Exception as e:
            print(f"Error extracting from PDF {pdf_path}: {str(e)}")
            return None
    
    def clean_text(self, text):
        """Clean extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove repeated navigation/menu items
        lines = text.split('\n')
        cleaned_lines = []
        seen = set()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip very short lines (likely navigation)
            if len(line) < 10:
                continue
            
            # Skip repeated lines
            if line in seen:
                continue
            
            seen.add(line)
            cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Fix common encoding issues
        text = text.replace('â€™', "'")
        text = text.replace('â€œ', '"')
        text = text.replace('â€', '"')
        text = text.replace('â€"', '–')
        
        # Remove URLs (optional, keeps content clean)
        # text = re.sub(r'http\S+', '', text)
        
        return text.strip()
    
    def process_all_files(self):
        """Process all files from raw directory."""
        # Load manifest
        manifest_path = self.raw_dir / "discovery_manifest.json"
        
        if not manifest_path.exists():
            print("Error: discovery_manifest.json not found. Run Phase 1 first.")
            return
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        print(f"\nProcessing {len(manifest)} files...")
        
        processed_count = 0
        categorized_content = {
            'admissions': [],
            'scholarship': [],
            'policies': [],
            'research': [],
            'calendar': [],
            'general': []
        }
        
        for entry in manifest:
            slug = entry['slug']
            content_type = entry.get('content_type', '')
            url = entry['url']
            
            print(f"\nProcessing: {slug}")
            
            # Determine file path
            file_path = self.raw_dir / entry['file_path'].split('\\')[-1]
            
            if not file_path.exists():
                print(f"  File not found: {file_path}")
                continue
            
            # Extract text based on type
            extracted = None
            if 'html' in content_type or file_path.suffix == '.html':
                extracted = self.extract_text_from_html(file_path)
            elif 'pdf' in content_type or file_path.suffix == '.pdf':
                extracted = self.extract_text_from_pdf(file_path)
            
            if not extracted or not extracted['text']:
                print(f"  No text extracted")
                continue
            
            # Save extracted text
            text_file = self.text_raw_dir / f"{slug}.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(extracted['text'])
            
            # Save metadata
            meta = {
                'url': url,
                'title': extracted['title'],
                'retrieved_at': entry['retrieved_at'],
                'source_file': str(file_path),
                'content_type': content_type,
                'word_count': extracted['word_count'],
                'processed_at': datetime.now().isoformat()
            }
            
            meta_file = self.text_meta_dir / f"{slug}.json"
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2)
            
            # Categorize content
            url_lower = url.lower()
            text_lower = extracted['text'].lower()
            
            if 'admission' in url_lower or 'admission' in text_lower[:500]:
                category = 'admissions'
            elif 'scholarship' in url_lower or 'scholarship' in text_lower[:500]:
                category = 'scholarship'
            elif 'research' in url_lower or 'policy' in url_lower:
                category = 'research'
            elif 'calendar' in url_lower:
                category = 'calendar'
            elif any(word in url_lower for word in ['code', 'conduct', 'ragging', 'rule']):
                category = 'policies'
            else:
                category = 'general'
            
            categorized_content[category].append({
                'slug': slug,
                'title': extracted['title'],
                'text': extracted['text'],
                'url': url,
                'word_count': extracted['word_count']
            })
            
            processed_count += 1
            print(f"  ✓ Extracted {extracted['word_count']} words → {text_file.name}")
        
        print(f"\n{'='*60}")
        print(f"Phase 2 Complete: Processed {processed_count} files")
        print(f"{'='*60}")
        
        # Create consolidated knowledge files for each category
        print("\nCreating consolidated knowledge files...")
        self.create_knowledge_files(categorized_content)
    
    def create_knowledge_files(self, categorized_content):
        """Create consolidated knowledge files for the helpdesk."""
        
        for category, items in categorized_content.items():
            if not items:
                continue
            
            # Create knowledge file
            knowledge_file = self.knowledge_text_dir / f"charusat_{category}.txt"
            
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                f.write(f"CHARUSAT UNIVERSITY - {category.upper()}\n")
                f.write(f"Compiled from official website: charusat.ac.in\n")
                f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"Total documents: {len(items)}\n")
                f.write("="*80 + "\n\n")
                
                for item in items:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"Source: {item['title']}\n")
                    f.write(f"URL: {item['url']}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(item['text'])
                    f.write("\n\n")
            
            print(f"  ✓ Created: {knowledge_file.name} ({len(items)} documents, {sum(i['word_count'] for i in items)} words)")
        
        print(f"\n{'='*60}")
        print(f"Knowledge files created in: {self.knowledge_text_dir}")
        print(f"Your helpdesk can now answer questions about CHARUSAT!")
        print(f"{'='*60}")


def main():
    """Run text extraction and integration."""
    base_dir = Path(__file__).parent
    extractor = TextExtractor(base_dir)
    
    print("="*60)
    print("PHASE 2: TEXT EXTRACTION & INTEGRATION")
    print("="*60)
    
    extractor.process_all_files()


if __name__ == "__main__":
    main()
