"""
PDF Parser Service
Extracts text from PDF files using pdfplumber and PyPDF2 as fallback.
"""

import pdfplumber
from PyPDF2 import PdfReader
import os

class PDFParser:
    """Service for extracting text from PDF files."""
    
    def __init__(self):
        """Initialize PDF parser."""
        pass
    
    def extract_text(self, pdf_path):
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
        
        Returns:
            str: Extracted text from the PDF
        
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            Exception: If PDF parsing fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Try pdfplumber first (better text extraction)
            return self._extract_with_pdfplumber(pdf_path)
        except Exception as e:
            print(f"pdfplumber failed: {str(e)}, trying PyPDF2...")
            try:
                # Fallback to PyPDF2
                return self._extract_with_pypdf2(pdf_path)
            except Exception as e2:
                raise Exception(f"Both PDF parsers failed. Errors: {str(e)}, {str(e2)}")
    
    def _extract_with_pdfplumber(self, pdf_path):
        """Extract text using pdfplumber (primary method)."""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    
    def _extract_with_pypdf2(self, pdf_path):
        """Extract text using PyPDF2 (fallback method)."""
        text = ""
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
        return text.strip()
    
    def clean_text(self, text):
        """
        Clean extracted text.
        
        Args:
            text (str): Raw extracted text
        
        Returns:
            str: Cleaned text
        """
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        # Join with single newline
        cleaned = '\n'.join(lines)
        
        # Replace multiple spaces with single space
        import re
        cleaned = re.sub(r' +', ' ', cleaned)
        
        return cleaned
