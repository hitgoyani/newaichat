"""
University Helpdesk Backend API
Flask application providing AI-powered helpdesk assistance.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from config.config import Config
from services.openai_service import OpenAIService
from services.context_service import ContextService

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend integration
CORS(app)

# Validate configuration on startup
try:
    Config.validate()
    print("✓ Configuration validated successfully")
except Exception as e:
    print(f"✗ Configuration error: {str(e)}")
    exit(1)

# Load system prompt
try:
    SYSTEM_PROMPT = Config.load_system_prompt()
    print("✓ System prompt loaded successfully")
except Exception as e:
    print(f"✗ Failed to load system prompt: {str(e)}")
    exit(1)

# Initialize services
try:
    # Try to initialize OpenAI service (requires API key)
    openai_service = OpenAIService()
    USE_LOCAL_MODE = False
    print("✓ OpenAI service initialized (Online mode)")
except Exception as e:
    # Fallback to local mode if OpenAI key not available
    from services.local_response_generator import LocalResponseGenerator
    openai_service = LocalResponseGenerator()
    USE_LOCAL_MODE = True
    print("⚠️ OpenAI API key not found - Using LOCAL MODE (offline)")
    print("  Answers will be generated from knowledge base only")

context_service = ContextService()

print("✓ Services initialized")
if not USE_LOCAL_MODE:
    print(f"✓ Using model: {Config.GPT_MODEL}")
    print(f"✓ Temperature: {Config.GPT_TEMPERATURE}")
    print(f"✓ Max tokens: {Config.GPT_MAX_TOKENS}")
else:
    print(f"✓ Mode: LOCAL (No external API)")
    print(f"✓ Knowledge files loaded: {len(context_service.knowledge_loader.get_all_files())}")

@app.route('/ask', methods=['POST'])
def ask():
    """
    Handle user queries and return AI-generated responses.
    
    Expected JSON payload:
    {
        "query": "user's question here"
    }
    
    Returns JSON response:
    {
        "status": "success" or "error",
        "response": "AI response text",
        "message": "error message (if error)"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON"
            }), 400
        
        # Extract query
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({
                "status": "error",
                "message": "Query cannot be empty"
            }), 400
        
        # Get relevant context from knowledge base (Phase 3 enhancement)
        context = context_service.get_relevant_context(user_query)
        
        # Get AI response
        response = openai_service.get_response(
            system_prompt=SYSTEM_PROMPT,
            user_query=user_query,
            context=context
        )
        
        # Return success response
        return jsonify({
            "status": "success",
            "response": response
        }), 200
    
    except Exception as e:
        # Handle errors gracefully
        print(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return "OK", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload a text or PDF file to the knowledge base.
    File will be processed and available immediately.
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Get file extension
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # Validate file type
        if file_ext not in ['txt', 'pdf']:
            return jsonify({
                'status': 'error',
                'message': 'Only .txt and .pdf files are allowed'
            }), 400
        
        # Determine save path
        if file_ext == 'txt':
            save_dir = os.path.join(os.path.dirname(__file__), 'knowledge', 'text')
        else:  # pdf
            save_dir = os.path.join(os.path.dirname(__file__), 'knowledge', 'pdfs')
        
        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Save file
        filepath = os.path.join(save_dir, filename)
        file.save(filepath)
        
        # Reload knowledge base to include new file
        files_loaded = context_service.reload_knowledge()
        
        return jsonify({
            'status': 'success',
            'message': f'File "{filename}" uploaded successfully',
            'filename': filename,
            'type': file_ext,
            'total_files_loaded': files_loaded
        }), 200
        
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/knowledge/list', methods=['GET'])
def list_knowledge():
    """List all files in the knowledge base."""
    try:
        files = context_service.knowledge_loader.get_all_files()
        return jsonify({
            'status': 'success',
            'files': files,
            'total': len(files)
        }), 200
    except Exception as e:
        print(f"Error listing knowledge files: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("University Helpdesk API Server")
    print("="*50)
    print(f"Environment: {Config.FLASK_ENV}")
    print(f"Debug mode: {Config.FLASK_DEBUG}")
    print("Server starting on http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.FLASK_DEBUG
    )
