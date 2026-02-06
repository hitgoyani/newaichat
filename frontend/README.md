# University Helpdesk - Frontend

Clean, professional web interface for the AI-Powered University Helpdesk Assistant.

## Features

✅ **Modern Chat Interface**
- Clean, minimal design
- Chat-like message display
- User messages (right, green) vs AI messages (left, gray)
- Smooth animations and transitions

✅ **Multilingual UI**
- English, Hindi, Gujarati support
- Language toggle buttons in header
- Auto-translated UI labels
- (Queries auto-detected by backend)

✅ **Responsive Design**
- Works on desktop, tablet, mobile
- Adapts to all screen sizes
- Touch-friendly controls

✅ **Seamless Backend Integration**
- Real-time communication with Flask API
- Loading indicators
- Error handling
- Auto-scroll to latest message

## File Structure

```
frontend/
├── index.html          # Main HTML page
├── css/
│   └── style.css       # All styling
├── js/
│   └── app.js          # Frontend logic
└── README.md           # This file
```

## How to Run

### Prerequisites

1. **Backend must be running**:
   ```bash
   cd backend
   python app.py
   ```
   Backend should be running on `http://localhost:5000`

2. **Open frontend**:
   - Simply open `index.html` in your browser
   - Or use a local server:
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Then open: http://localhost:8000
     ```

## Usage

1. **Start the Application**:
   - Open `index.html` in Chrome/Firefox/Edge

2. **Ask Questions**:
   - Type your question in the input box
   - Click "Send" or press Enter
   - Wait for AI response

3. **Switch Language**:
   - Click language buttons (EN/हिं/ગુ) in header
   - UI labels change to selected language
   - Queries auto-detected (no need to match UI language)

4. **Clear Chat**:
   - Click "Clear Chat" button to remove all messages
   - Welcome message remains

## Example Queries

**English**:
- "What are the admission deadlines for engineering?"
- "How much is the tuition fee?"
- "Are there any scholarships available?"

**Hindi/Hinglish**:
- "engineering ki fees kitni hai?"
- "scholarship ke liye kaise apply karen?"
- "admission kab se start hoga?"

**Gujarati**:
- "admission માટે શું જરૂરી છે?"
- "fees કેટલી છે?"

## Design Details

### Color Scheme
- **Primary**: Blue gradient (#1e40af → #3b82f6)
- **User Messages**: Green gradient (#10b981 → #059669)
- **Bot Messages**: White with gray border
- **Background**: Purple gradient (#667eea → #764ba2)

### Typography
- **Font**: System fonts (San Francisco, Segoe UI, Roboto)
- **Header**: 24px, bold
- **Body**: 16px, regular
- **Small**: 14px for metadata

### Layout
- **Max Width**: 800px (readable)
- **Height**: 90vh (centered on screen)
- **Responsive breakpoints**: 768px (tablet), 480px (mobile)

## Technical Details

### API Integration

**Endpoint**: `POST http://localhost:5000/ask`

**Request**:
```json
{
  "query": "user's question"
}
```

**Response**:
```json
{
  "status": "success",
  "response": "AI-generated answer"
}
```

### Browser Support
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ❌ IE (not supported)

### Performance
- **Page Load**: <1 second
- **API Response**: 2-5 seconds (GPT-3.5-turbo)
- **Animations**: 60fps
- **File Size**: ~15KB total (HTML+CSS+JS)

## Troubleshooting

**Problem**: "Unable to connect to server"
- **Solution**: Ensure backend is running on `http://localhost:5000`
- Check: `curl http://localhost:5000/health` should return "OK"

**Problem**: Messages not appearing
- **Solution**: Check browser console (F12) for errors
- Ensure CORS is enabled in backend (already configured)

**Problem**: UI labels in wrong language
- **Solution**: Click language toggle buttons in header
- Default is English (EN)

**Problem**: Layout broken on mobile
- **Solution**: Ensure viewport meta tag is present (already included)
- Try hard refresh (Ctrl+Shift+R)

## For Developers

### Adding New Languages

1. Add translation in `js/app.js`:
   ```javascript
   const TRANSLATIONS = {
       // ... existing languages
       fr: {
           title: 'Assistant du Bureau d\'Aide',
           subtitle: '...',
           // ... other labels
       }
   };
   ```

2. Add language button in `index.html`:
   ```html
   <button class="lang-btn" data-lang="fr">FR</button>
   ```

3. Add placeholder attribute:
   ```html
   data-placeholder-fr="Tapez votre question ici..."
   ```

### Customizing Design

- **Colors**: Edit CSS variables in `css/style.css`
- **Layout**: Change `.container` max-width/height
- **Fonts**: Update `body` font-family
- **Animations**: Modify `@keyframes` rules

### Production Deployment

1. **Update API URL** in `js/app.js`:
   ```javascript
   const API_URL = 'https://your-backend-domain.com/ask';
   ```

2. **Deploy frontend**:
   - GitHub Pages (free)
   - Netlify (free)
   - Vercel (free)
   - Any static hosting

3. **Deploy backend** separately (Heroku, AWS, Azure)

## Academic Context

This frontend is built as part of a college project demonstrating:
- **Clean UI/UX design**
- **Responsive web development**
- **RESTful API integration**
- **Multilingual support**
- **Modern JavaScript (ES6+)**
- **Professional coding practices**

No frameworks used (React/Vue/Angular) to demonstrate core web skills.

---

## License

Educational/Academic use only.

## Contact

For issues or questions, contact the development team or raise an issue in the project repository.
