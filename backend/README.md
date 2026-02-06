# University Helpdesk System - Backend

This is the Flask backend for the AI-Powered University Helpdesk System.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST `/ask`

Submit a query to the helpdesk.

**Request:**
```json
{
  "query": "What are the admission deadlines?"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "AI-generated response here..."
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "University Helpdesk API",
  "model": "gpt-3.5-turbo"
}
```

## Testing

Test the API using curl:

```bash
# Test English query
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What are the admission requirements?\"}"

# Test Hindi/Hinglish query
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"fees kitni hai?\"}"

# Test out-of-scope query (should be rejected)
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"How to code in Python?\"}"
```

## Project Structure

```
backend/
├── app.py                  # Main Flask application
├── config/
│   ├── config.py           # Configuration management
│   └── system_prompt.txt   # AI system prompt
├── services/
│   ├── openai_service.py   # OpenAI API integration
│   └── context_service.py  # Knowledge base integration
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (not in git)
```

## Configuration

All configuration is managed through environment variables in `.env`:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `GPT_MODEL` - Model to use (default: gpt-3.5-turbo)
- `GPT_TEMPERATURE` - Response randomness (default: 0.3)
- `GPT_MAX_TOKENS` - Max response length (default: 500)
- `FLASK_ENV` - Environment (development/production)
- `FLASK_DEBUG` - Debug mode (True/False)
