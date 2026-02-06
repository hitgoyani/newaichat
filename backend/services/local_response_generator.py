"""
Local Response Generator
Generates answers from knowledge base WITHOUT any external API.
Works completely offline - no OpenAI key needed!
"""

import re
from services.context_service import ContextService

class LocalResponseGenerator:
    """Generate responses from knowledge base without external AI."""
    
    def __init__(self):
        """Initialize local response generator."""
        self.context_service = ContextService()
    
    def get_response(self, system_prompt, user_query, context=""):
        """
        Generate response using only local knowledge base.
        
        Args:
            system_prompt (str): System instructions (for compatibility)
            user_query (str): User's question
            context (str): Knowledge base context
        
        Returns:
            str: Generated answer from knowledge base
        """
        # If no context provided, get it
        if not context:
            context = self.context_service.get_relevant_context(user_query)
        
        # If still no context, return default message
        if not context:
            return self._generate_fallback_response(user_query)
        
        # Extract and format answer from context
        answer = self._extract_answer_from_context(user_query, context)
        
        return answer
    
    def _extract_answer_from_context(self, query, context):
        """
        Extract relevant answer from context based on query.
        
        Args:
            query (str): User's question
            context (str): Knowledge base context
        
        Returns:
            str: Formatted answer
        """
        # Extract keywords from query
        keywords = self._extract_keywords(query)
        
        # Split context by file sections
        sections = context.split('=== From ')
        
        # Build answer
        answer_parts = []
        
        for section in sections[1:]:  # Skip empty first element
            if not section.strip():
                continue
            
            # Extract file name and content
            lines = section.split('\n', 1)
            if len(lines) < 2:
                continue
            
            file_name = lines[0].replace(' ===', '').strip()
            content = lines[1].strip()
            
            # Get most relevant paragraphs
            relevant_text = self._get_relevant_paragraphs(content, keywords, max_paragraphs=3)
            
            if relevant_text:
                answer_parts.append(f"**From {file_name}:**\n\n{relevant_text}")
        
        if answer_parts:
            # Format final answer
            intro = self._generate_intro(query, keywords)
            body = "\n\n---\n\n".join(answer_parts)
            outro = "\n\n*Note: This information is from our knowledge base. For more details, please contact the university office.*"
            
            return f"{intro}\n\n{body}{outro}"
        else:
            return self._generate_fallback_response(query)
    
    def _get_relevant_paragraphs(self, content, keywords, max_paragraphs=3):
        """Get most relevant paragraphs from content."""
        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # Score each paragraph
        scored = []
        for para in paragraphs:
            score = 0
            para_lower = para.lower()
            
            # Count keyword matches
            for keyword in keywords:
                score += para_lower.count(keyword.lower())
            
            # Bonus for questions/answers
            if any(word in para_lower for word in ['?', 'answer', 'information', 'details']):
                score += 0.5
            
            if score > 0:
                scored.append((score, para))
        
        # Sort by score and take top N
        scored.sort(reverse=True, key=lambda x: x[0])
        top_paras = [para for score, para in scored[:max_paragraphs]]
        
        return '\n\n'.join(top_paras) if top_paras else ""
    
    def _extract_keywords(self, query):
        """Extract meaningful keywords from query."""
        query_lower = query.lower()
        
        # Stop words
        stop_words = {
            'what', 'when', 'where', 'who', 'how', 'why', 'is', 'are', 'the',
            'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'kya', 'hai', 'hain', 'ki', 'ka', 'ke', 'ko', 'se', 'me', 'mein',
            'tell', 'me', 'about', 'can', 'you', 'please', 'i', 'want', 'know'
        }
        
        # Extract words
        words = re.findall(r'\b\w+\b', query_lower)
        
        # Filter keywords
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _generate_intro(self, query, keywords):
        """Generate introductory sentence for answer."""
        # Determine question type
        query_lower = query.lower()
        
        if 'what' in query_lower:
            return "Here's what I found about your question:"
        elif 'how' in query_lower:
            return "Here's information on how to proceed:"
        elif 'when' in query_lower:
            return "Here are the relevant details about timing/dates:"
        elif 'where' in query_lower:
            return "Here's location information:"
        elif any(word in query_lower for word in ['scholarship', 'छात्रवृत्ति', 'શિષ્યવૃત્તિ']):
            return "📚 **Scholarship Information:**"
        elif any(word in query_lower for word in ['admission', 'प्रवेश', 'પ્રવેશ']):
            return "🎓 **Admission Information:**"
        elif any(word in query_lower for word in ['fee', 'fees', 'शुल्क', 'ફી']):
            return "💰 **Fee Information:**"
        elif any(word in query_lower for word in ['exam', 'परीक्षा', 'પરીક્ષા']):
            return "📝 **Examination Information:**"
        else:
            return "Here's what I found in our knowledge base:"
    
    def _generate_fallback_response(self, query):
        """Generate fallback response when no relevant information found."""
        query_lower = query.lower()
        
        # Check for common topics
        topics = {
            'admission': "I don't have specific information about admissions in my current knowledge base. Please check the admissions section or contact the university office.",
            'scholarship': "I don't have specific scholarship information available. Please contact the scholarship office or check the university website.",
            'fee': "Fee information is not available in my current knowledge base. Please contact the accounts department.",
            'exam': "Examination details are not in my knowledge base. Please refer to the examination office.",
        }
        
        for topic, response in topics.items():
            if topic in query_lower:
                return f"⚠️ **Limited Information**\n\n{response}"
        
        # Generic fallback
        return """⚠️ **No Matching Information Found**

I couldn't find specific information about your query in the knowledge base.

**Suggestions:**
- Try rephrasing your question with different keywords
- Ask about: admissions, fees, scholarships, exams, facilities
- Contact the university office directly for detailed information

**Topics I can help with:**
- 🎓 Admission procedures
- 💰 Fee structure
- 📚 Scholarship programs  
- 📝 Examination policies
- 🏛️ Campus facilities
- 🔬 Academic programs"""
