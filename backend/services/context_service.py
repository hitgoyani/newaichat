"""
Context service for knowledge base integration.
Retrieves relevant context from knowledge base using keyword-based search.
"""

import re
from services.knowledge_loader import KnowledgeLoader

class ContextService:
    """Service class for retrieving relevant context from knowledge base."""
    
    def __init__(self):
        """Initialize context service and load knowledge base."""
        self.knowledge_loader = KnowledgeLoader()
        self.max_context_length = 2000  # Maximum characters for context
    
    def get_relevant_context(self, query):
        """
        Retrieve relevant context from knowledge base based on user query.
        
        Args:
            query (str): The user's question
        
        Returns:
            str: Relevant context from knowledge base
        """
        # Extract keywords from query
        keywords = self._extract_keywords(query)
        
        if not keywords:
            return ""
        
        # Search for matching content
        matching_files = self.knowledge_loader.search_content(keywords)
        
        if not matching_files:
            return ""
        
        # Build context from top matching files
        context = self._build_context(matching_files, keywords)
        
        return context
    
    def _extract_keywords(self, query):
        """
        Extract meaningful keywords from user query.
        
        Args:
            query (str): User's question
        
        Returns:
            list: List of keywords
        """
        # Convert to lowercase
        query_lower = query.lower()
        
        # Remove common stop words (basic set for demo)
        stop_words = {
            'what', 'when', 'where', 'who', 'how', 'why', 'is', 'are', 'the',
            'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'kya', 'hai', 'hain', 'ki', 'ka', 'ke', 'ko', 'se', 'me', 'mein'
        }
        
        # Split into words and remove punctuation
        words = re.findall(r'\b\w+\b', query_lower)
        
        # Filter out stop words and short words
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _build_context(self, matching_files, keywords):
        """
        Build context string from matching files.
        
        Args:
            matching_files (dict): Dictionary of matching files with scores
            keywords (list): Search keywords
        
        Returns:
            str: Formatted context string
        """
        context_parts = []
        total_length = 0
        
        # Process top 2 files (most relevant)
        for file_key, file_data in list(matching_files.items())[:2]:
            content = file_data['content']
            
            # Extract relevant snippets
            snippets = self._extract_relevant_snippets(content, keywords)
            
            if snippets:
                file_context = f"=== From {file_key.upper()} ===\n{snippets}\n"
                
                # Check if adding this would exceed limit
                if total_length + len(file_context) < self.max_context_length:
                    context_parts.append(file_context)
                    total_length += len(file_context)
                else:
                    # Add as much as possible
                    remaining = self.max_context_length - total_length
                    context_parts.append(file_context[:remaining])
                    break
        
        return '\n'.join(context_parts)
    
    def _extract_relevant_snippets(self, content, keywords, snippet_size=500):
        """
        Extract relevant snippets from content containing keywords.
        
        Args:
            content (str): File content
            keywords (list): Search keywords
            snippet_size (int): Maximum size of each snippet
        
        Returns:
            str: Relevant snippets
        """
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        
        # Score each paragraph
        scored_paragraphs = []
        for para in paragraphs:
            score = 0
            para_lower = para.lower()
            for keyword in keywords:
                score += para_lower.count(keyword.lower())
            
            if score > 0:
                scored_paragraphs.append((score, para))
        
        # Sort by score
        scored_paragraphs.sort(reverse=True, key=lambda x: x[0])
        
        # Take top paragraphs
        snippets = []
        current_length = 0
        
        for score, para in scored_paragraphs[:5]:  # Top 5 paragraphs
            if current_length + len(para) < snippet_size * 3:
                snippets.append(para)
                current_length += len(para)
            else:
                break
        
        return '\n\n'.join(snippets)
    
    def reload_knowledge(self):
        """Reload knowledge base (useful if files are updated)."""
        return self.knowledge_loader.reload()
