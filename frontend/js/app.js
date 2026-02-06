// ===== CONFIGURATION =====
const API_URL = 'http://localhost:5000/ask';

// ===== MULTILINGUAL UI LABELS =====
const TRANSLATIONS = {
    en: {
        title: '🎓 CHARUSAT Helpdesk Assistant',
        subtitle: 'Ask about admissions, scholarships, research, and campus information',
        sendBtn: 'Send',
        clearBtn: 'Clear Chat',
        welcome: 'Welcome to CHARUSAT! I\'m here to help you with questions about Charotar University of Science and Technology - admissions, scholarships, research policies, and campus information. Ask in English, Hindi, or Gujarati.'
    },
    hi: {
        title: '🎓 चारुसैट हेल्पडेस्क सहायक',
        subtitle: 'प्रवेश, छात्रवृत्ति, अनुसंधान और परिसर जानकारी के बारे में पूछें',
        sendBtn: 'भेजें',
        clearBtn: 'चैट साफ़ करें',
        welcome: 'चारुसैट में आपका स्वागत है! मैं चारोतर विज्ञान और प्रौद्योगिकी विश्वविद्यालय के बारे में आपकी सहायता के लिए यहाँ हूँ - प्रवेश, छात्रवृत्ति, अनुसंधान नीतियाँ और परिसर जानकारी।'
    },
    gu: {
        title: '🎓 ચારુસેટ હેલ્પડેસ્ક સહાયક',
        subtitle: 'પ્રવેશ, શિષ્યવૃત્તિ, સંશોધન અને કેમ્પસ માહિતી વિશે પૂછો',
        sendBtn: 'મોકલો',
        clearBtn: 'ચેટ સાફ કરો',
        welcome: 'ચારુસેટમાં સ્વાગત છે! હું ચારોતર વિજ્ઞાન અને ટેકનોલોજી યુનિવર્સિટી વિશે તમારી મદદ માટે અહીં છું - પ્રવેશ, શિષ્યવૃત્તિ, સંશોધન નીતિઓ અને કેમ્પસ માહિતી.'
    }
};

// ===== STATE =====
let currentLanguage = 'en';

// ===== DOM ELEMENTS =====
const elements = {
    chatContainer: document.getElementById('chatContainer'),
    userInput: document.getElementById('userInput'),
    sendBtn: document.getElementById('sendBtn'),
    clearBtn: document.getElementById('clearBtn'),
    loadingIndicator: document.getElementById('loadingIndicator'),
    title: document.getElementById('title'),
    subtitle: document.getElementById('subtitle'),
    sendBtnText: document.getElementById('sendBtnText'),
    clearBtnText: document.getElementById('clearBtnText'),
    welcomeText: document.getElementById('welcomeText'),
    langBtns: document.querySelectorAll('.lang-btn')
};

// ===== INITIALIZATION =====
function init() {
    // Event listeners
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.clearBtn.addEventListener('click', clearChat);
    elements.userInput.addEventListener('keydown', handleKeyPress);

    // Auto-resize textarea
    elements.userInput.addEventListener('input', autoResizeTextarea);

    // Language toggle buttons
    elements.langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            switchLanguage(lang);
        });
    });

    // Set initial active language button
    updateActiveLanguageButton();

    console.log('✅ University Helpdesk Assistant initialized');
}

// ===== LANGUAGE SWITCHING =====
function switchLanguage(lang) {
    if (!TRANSLATIONS[lang]) return;

    currentLanguage = lang;

    // Update UI labels
    elements.title.textContent = TRANSLATIONS[lang].title;
    elements.subtitle.textContent = TRANSLATIONS[lang].subtitle;
    elements.sendBtnText.textContent = TRANSLATIONS[lang].sendBtn;
    elements.clearBtnText.textContent = TRANSLATIONS[lang].clearBtn;
    elements.welcomeText.textContent = TRANSLATIONS[lang].welcome;

    // Update placeholder
    const placeholderAttr = `data-placeholder-${lang}`;
    elements.userInput.placeholder = elements.userInput.getAttribute(placeholderAttr);

    // Update active button
    updateActiveLanguageButton();

    console.log(`Language switched to: ${lang}`);
}

function updateActiveLanguageButton() {
    elements.langBtns.forEach(btn => {
        if (btn.dataset.lang === currentLanguage) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// ===== AUTO-RESIZE TEXTAREA =====
function autoResizeTextarea() {
    elements.userInput.style.height = 'auto';
    elements.userInput.style.height = elements.userInput.scrollHeight + 'px';
}

// ===== HANDLE ENTER KEY =====
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ===== SEND MESSAGE =====
async function sendMessage() {
    const message = elements.userInput.value.trim();

    if (!message) return;

    // Display user message
    addMessage(message, 'user');

    // Clear input
    elements.userInput.value = '';
    elements.userInput.style.height = 'auto';

    // Disable send button
    elements.sendBtn.disabled = true;

    // Show loading indicator
    showLoading();

    try {
        // Send to backend
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: message })
        });

        // Handle specific error status codes
        if (response.status === 401 || response.status === 403) {
            hideLoading();
            addMessage('⚠️ Authentication Error: Please check your OpenAI API key in backend/.env file', 'error');
            return;
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading
        hideLoading();

        // Display AI response
        if (data.status === 'success' && data.response) {
            addMessage(data.response, 'bot');
        } else {
            addMessage('Sorry, I could not generate a response. Please try again.', 'error');
        }

    } catch (error) {
        console.error('Error:', error);
        hideLoading();
        addMessage('Unable to connect to the server. Please ensure the backend is running on http://localhost:5000', 'error');
    } finally {
        // Re-enable send button
        elements.sendBtn.disabled = false;
        elements.userInput.focus();
    }
}

// ===== ADD MESSAGE TO CHAT =====
function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type === 'user' ? 'user-message' : type === 'error' ? 'bot-message error-message' : 'bot-message'}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textP = document.createElement('p');
    textP.textContent = text;

    contentDiv.appendChild(textP);

    // Add timestamp
    const timeSpan = document.createElement('div');
    timeSpan.className = 'message-time';
    timeSpan.textContent = getCurrentTime();
    contentDiv.appendChild(timeSpan);

    messageDiv.appendChild(contentDiv);
    elements.chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

// ===== CLEAR CHAT =====
function clearChat() {
    // Remove all messages except welcome message
    const messages = elements.chatContainer.querySelectorAll('.message');
    messages.forEach((msg, index) => {
        if (index > 0) { // Skip first message (welcome)
            msg.remove();
        }
    });

    console.log('Chat cleared');
}

// ===== UTILITY FUNCTIONS =====
function showLoading() {
    elements.loadingIndicator.classList.add('active');
}

function hideLoading() {
    elements.loadingIndicator.classList.remove('active');
}

function scrollToBottom() {
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// ===== START APPLICATION =====
document.addEventListener('DOMContentLoaded', init);
