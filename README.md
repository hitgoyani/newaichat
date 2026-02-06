# AI-Powered Multilingual University Helpdesk System

A complete, production-ready university helpdesk assistant powered by OpenAI GPT-3.5-turbo with knowledge base integration and multilingual support.

## 🎯 Project Overview

This system provides an intelligent chatbot interface for students to ask questions about:
- **Admissions** - Procedures, deadlines, eligibility, required documents
- **Fees** - Fee structure, payment methods, installments, refunds
- **Examinations** - Academic calendar, grading, attendance, backlog policies
- **Scholarships** - Merit-based, need-based, category-based programs

**Key Features:**
- ✅ Multilingual support (English, Hindi, Gujarati, Hinglish)
- ✅ Automatic language detection
- ✅ Domain-specific knowledge base
- ✅ Strict domain enforcement (rejects off-topic queries)
- ✅ No hallucination (grounded in university knowledge)
- ✅ Professional web interface
- ✅ Responsive design (desktop + mobile)

---

## 🏗️ Architecture

```
university-helpdesk/
├── backend/               # Flask API server
│   ├── app.py            # Main application
│   ├── config/           # Configuration & system prompt
│   ├── services/         # OpenAI, knowledge, context services
│   ├── knowledge/        # University knowledge base
│   │   ├── text/        # Text files (admissions, fees, etc.)
│   │   └── pdfs/        # PDF documents
│   └── requirements.txt
│
├── frontend/             # Web UI
│   ├── index.html       # Main page
│   ├── css/style.css    # Styling
│   └── js/app.js        # Frontend logic
│
└── README.md            # This file
```

**Technology Stack:**
- **Backend**: Python, Flask, OpenAI API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Model**: GPT-3.5-turbo
- **Knowledge**: Text files + PDF parsing (pdfplumber, PyPDF2)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

**1. Clone the repository:**
```bash
cd university-helpdesk
```

**2. Set up backend:**
```bash
cd backend
pip install -r requirements.txt
```

**3. Configure environment:**
```bash
# Copy example .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

**4. Start the backend:**
```bash
python app.py
```

You should see:
```
✓ Knowledge base loaded: 4 text files, 0 PDFs, 4 total
 * Running on http://0.0.0.0:5000
```

**5. Open the frontend:**

Simply open `frontend/index.html` in your web browser.

Or use a local server:
```bash
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

---

## 💡 Usage

1. **Open the frontend** in your browser
2. **Type your question** in any language (English/Hindi/Gujarati/Hinglish)
3. **Press Enter** or click "Send"
4. **Get instant answers** with accurate information from the knowledge base

**Example Queries:**

**English:**
- "What are the admission deadlines for engineering?"
- "How much is the tuition fee for MBA?"
- "Are there any scholarships for SC/ST students?"

**Hindi/Hinglish:**
- "engineering ki fees kitni hai?"
- "scholarship ke liye kaise apply karen?"
- "admission kab se start hoga?"

**Gujarati:**
- "admission માટે શું જરૂરી છે?"
- "fees કેટલી છે?"

**Language Toggle:**
- Click **EN** / **हिं** / **ગુ** buttons to change UI language
- Queries auto-detected regardless of UI language

---

## 📚 Knowledge Base

The system includes comprehensive university information:

**Text Files:**
- `admissions.txt` - Admission procedures, eligibility, deadlines (~1,800 words)
- `fees.txt` - Fee structure, payment methods, refunds (~1,600 words)
- `scholarships.txt` - 12 scholarship programs (~2,200 words)
- `exam_policies.txt` - Academic calendar, grading, policies (~2,000 words)

**Total Knowledge**: ~7,600 words of university-specific information

**Adding Knowledge:**
1. Add `.txt` files to `backend/knowledge/text/`
2. Add `.pdf` files to `backend/knowledge/pdfs/`
3. Restart backend server to reload

---

## 🎨 Features

### 1. Intelligent Context Retrieval
- Keyword-based search with relevance ranking
- Extracts most relevant paragraphs from knowledge base
- Token-optimized (stays within GPT limits)

### 2. Domain Enforcement
- **Allowed topics**: Admissions, Fees, Exams, Scholarships
- **Rejected topics**: Programming, entertainment, politics, personal advice
- Polite rejection with suggestions for non-university queries

### 3. Multilingual Support
- **Auto-detection**: No language selector needed for queries
- **UI switching**: Toggle between EN/HI/GU interface labels
- **Mixed responses**: Can respond in Hinglish (Hindi-English mix)

### 4. No Hallucination
- Grounded in knowledge base content
- States "I don't have this information" when knowledge is unavailable
- Low temperature (0.3) for deterministic responses

### 5. Professional UI
- Modern gradient design
- Responsive layout (desktop/tablet/mobile)
- Smooth animations
- Auto-scroll to latest message
- Loading indicators

---

## 🧪 Testing

### Backend API Testing

**Health Check:**
```bash
curl http://localhost:5000/health
# Expected: "OK"
```

**Query Test:**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the admission deadlines?"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "response": "For the 2024-25 academic year, admission deadlines are..."
}
```

### Frontend Testing

1. **Open `frontend/index.html`**
2. **Test message sending**: Type and send a query
3. **Test multilingual UI**: Click language toggle buttons
4. **Test responsive design**: Resize browser window
5. **Test error handling**: Stop backend and try sending

---

## 📖 Documentation

**Detailed Documentation:**
- **[Backend README](backend/README.md)** - API details, configuration, architecture
- **[Frontend README](frontend/README.md)** - UI features, customization, deployment
- **[System Prompt](backend/config/system_prompt.txt)** - AI behavior definition
- **[Complete Walkthrough](../brain/.../walkthrough.md)** - All phases, testing, academic prep

**Artifacts (Academic Context):**
Located in `C:\Users\Hit\.gemini\antigravity\brain\05f4315c-8ce9-4bd9-84ad-ae59113ac86b\`:
- `task.md` - Development task breakdown
- `implementation_plan.md` - Technical planning document
- `system_prompt.md` - Detailed prompt engineering
- `prompt_explanation.md` - Academic justification
- `walkthrough.md` - Complete implementation walkthrough

---

## 🎓 Academic Context

This project demonstrates:
- **Prompt Engineering**: Controlling AI behavior without fine-tuning
- **Knowledge Integration**: Grounding LLMs with domain-specific data
- **Multilingual NLP**: Cross-language query handling
- **Full-Stack Development**: Backend API + Frontend UI
- **System Design**: Scalable, modular architecture

**Technologies Learned:**
- Flask REST API development
- OpenAI API integration
- PDF parsing and text extraction
- Semantic search and ranking
- Responsive web design
- JavaScript async/await patterns

**Suitable For:**
- College/university final year projects
- AI/ML course projects
- Web development portfolios
- NLP demonstrations

---

## 🔧 Configuration

### Backend Configuration

**Environment Variables** (`.env` file):
```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
FLASK_DEBUG=True
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=500
```

### Frontend Configuration

**API URL** (`frontend/js/app.js`):
```javascript
const API_URL = 'http://localhost:5000/ask';
```

For production, update to your backend URL:
```javascript
const API_URL = 'https://your-backend.com/ask';
```

---

## 🚀 Deployment

### Backend (Heroku Example)

```bash
cd backend
heroku create university-helpdesk-api
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Frontend (Netlify/Vercel)

1. Update `API_URL` in `app.js` to your backend URL
2. Drag `frontend/` folder to Netlify
3. Deploy

**OR** use GitHub Pages:
```bash
cd frontend
# Push to GitHub repository
# Enable GitHub Pages in repo settings
```

---

## 🛠️ Troubleshooting

**Issue**: "Unable to connect to server"
- **Fix**: Ensure backend is running on `http://localhost:5000`
- Test: `curl http://localhost:5000/health`

**Issue**: "OPENAI_API_KEY is not set"
- **Fix**: Create `.env` file in `backend/` with your API key

**Issue**: Empty or incorrect responses
- **Fix**: Check knowledge base files are loaded
- Look for "Knowledge base loaded" message on backend startup

**Issue**: UI not updating language
- **Fix**: Hard refresh browser (Ctrl+Shift+R)
- Check browser console (F12) for errors

---

## 📊 Project Statistics

- **Total Files**: 20+
- **Lines of Code**: ~1,500
- **Knowledge Base**: ~7,600 words
- **Languages Supported**: 4 (EN, HI, GU, Hinglish)
- **Backend**: ~600 lines Python
- **Frontend**: ~500 lines HTML+CSS+JS
- **Dependencies**: 6 Python packages

---

## 🔐 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Rotate API keys regularly
- Use environment variables for production
- Implement rate limiting for public deployment
- Add authentication for production use

---

## 📝 License

Educational/Academic use only.

---

## 👥 Contributing

This is an academic project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🙏 Acknowledgments

- **OpenAI** - GPT-3.5-turbo API
- **Flask** - Web framework
- **pdfplumber** - PDF text extraction

---

## 📞 Support

For issues or questions:
- Check `backend/README.md` and `frontend/README.md`
- Review `walkthrough.md` for detailed implementation
- Raise an issue in the repository

---

## 🎯 Project Status

✅ **Phase 1**: Core AI Behavior & System Prompt Design  
✅ **Phase 2**: Backend Implementation (Flask + OpenAI)  
✅ **Phase 3**: Knowledge Base Integration  
✅ **Phase 4**: Frontend UI Development  

**Status**: Production-ready ✨

---

**Built with ❤️ for educational purposes**
