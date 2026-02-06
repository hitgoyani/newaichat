# Testing Guide - University Helpdesk System

## Prerequisites Checklist

Before testing, ensure:
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ OpenAI API key added to `backend/.env` file
- ✅ Knowledge files present in `backend/knowledge/text/` and `backend/knowledge/pdfs/`

---

## Step 1: Start the Backend

**Navigate to backend directory:**
```bash
cd backend
```

**Start the server:**
```bash
python app.py
```

**Expected Output:**
```
Loading knowledge base...
  Loaded: admissions.txt
  Loaded: fees.txt
  Loaded: scholarships.txt
  Loaded: exam_policies.txt
  Loaded: academic_programs.txt
  Loaded: campus_facilities.txt
✓ Knowledge base loaded: 6 text files, 0 PDFs, 6 total

==================================================
🎓 University Helpdesk Assistant
==================================================
✓ Configuration validated
✓ System prompt loaded
✓ OpenAI service initialized (gpt-3.5-turbo)
✓ Knowledge base loaded (6 files)

Starting Flask server...
 * Running on http://0.0.0.0:5000
==================================================
```

**If this fails**, check:
- `.env` file exists and has valid OpenAI API key
- All dependencies installed
- Port 5000 not already in use

---

## Step 2: Test Backend API

**Open new terminal** (keep backend running in first terminal)

**Test 1: Health Check**
```bash
curl http://localhost:5000/health
```
**Expected:** `OK`

**Test 2: List Knowledge Files**
```bash
curl http://localhost:5000/knowledge/list
```
**Expected:** JSON with list of 6 files

**Test 3: Simple Query (English)**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What are the admission deadlines?\"}"
```
**Expected:** JSON response with specific dates from admissions.txt

**Test 4: Hinglish Query**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"engineering ki fees kitni hai?\"}"
```
**Expected:** Response in Hindi/Hinglish with fee details

**Test 5: Knowledge Query (New Files)**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What courses are offered in Engineering?\"}"
```
**Expected:** Response listing CSE, ECE, ME, CE, EE from academic_programs.txt

**Test 6: Facilities Query**
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Tell me about hostel facilities\"}"
```
**Expected:** Response with hostel info from campus_facilities.txt

---

## Step 3: Test Frontend Chat Interface

**Open in browser:**
```
file:///C:/Users/Hit/Desktop/New folder/university-helpdesk/frontend/index.html
```

**Or use local server:**
```bash
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000
```

**Visual Test Checklist:**

1. **UI Loads Correctly**
   - ✅ Header with "University Helpdesk Assistant" title
   - ✅ Language toggle buttons (EN/हिं/ગુ) visible
   - ✅ Welcome message displayed
   - ✅ Input box and send button at bottom

2. **Language Toggle**
   - Click "हिं" button
   - ✅ Title changes to Hindi
   - ✅ Subtitle in Hindi
   - ✅ Buttons show Hindi text
   - ✅ Placeholder in Hindi

3. **Send Message**
   - Type: "What are the admission deadlines for B.Tech?"
   - Click Send (or press Enter)
   - ✅ User message appears on right (green)
   - ✅ Loading indicator briefly shows
   - ✅ AI response appears on left (gray)
   - ✅ Response contains specific dates

4. **Multilingual Query**
   - Type: "library mein kitne books hain?"
   - Send
   - ✅ AI responds in Hindi/Hinglish
   - ✅ Answer based on campus_facilities.txt (50,000+ books)

5. **New Knowledge Test**
   - Type: "What specializations are available in MBA?"
   - Send
   -✅ Response mentions Finance, Marketing, HR, Operations, IT from academic_programs.txt

6. **Responsive Design**
   - Resize browser window
   - ✅ Layout adapts smoothly
   - ✅ No horizontal scrolling
   - ✅ Readable on all sizes

7. **Clear Chat**
   - Click "Clear Chat" button
   - ✅ All messages removed except welcome message

---

## Step 4: Test File Upload Feature

**Open upload interface:**
```
file:///C:/Users/Hit/Desktop/New folder/university-helpdesk/frontend/upload.html
```

**Or:**
```bash
cd frontend
python -m http.server 8000
# Then visit: http://localhost:8000/upload.html
```

**Upload Test Checklist:**

1. **View Current Files**
   - Page loads
   - ✅ Stats show correct counts (6 total, 6 text, 0 PDF)
   - ✅ All 6 files listed

2. **Create Test File**
   - Create `test_file.txt` with content:
   ```
   CAMPUS WIFI INFORMATION
   
   WiFi Network: UniversityNet
   Password: Welcome2024
   Coverage: All academic buildings and hostels
   Speed: 100 Mbps
   Support: it-helpdesk@university.edu
   ```

3. **Upload via Click**
   - Click upload area
   - Select `test_file.txt`
   - ✅ Loading indicator shows
   - ✅ Success message appears
   - ✅ File count updates to 7
   - ✅ New file appears in list

4. **Upload via Drag-Drop**
   - Create another file (or PDF)
   - Drag and drop onto upload area
   - ✅ Upload succeeds
   - ✅ Count updates

5. **Test Uploaded Knowledge**
   - Go back to main chat interface
   - Type: "What is the WiFi password?"
   - Send
   - ✅ AI responds with "Welcome2024" from uploaded file
   - ✅ No server restart needed!

6. **Invalid File Test**
   - Try uploading .jpg or .doc file
   - ✅ Error message shows: "Only .txt and .pdf files allowed"

---

## Step 5: Comprehensive Query Tests

**Test queries across all knowledge areas:**

### Admissions
```
Q: "What documents are required for admission?"
Expected: List of 10 documents from admissions.txt
```

### Fees
```
Q: "What is the refund policy?"
Expected: Refund percentages based on timing
```

### Scholarships
```
Q: "Are there scholarships for sports students?"
Expected: Sports Excellence Scholarship details (75% or 50% waiver)
```

### Exams
```
Q: "What is the passing criteria?"
Expected: Minimum 40% overall + 20/60 in end-semester
```

### Academic Programs (NEW)
```
Q: "How many seats are there in Computer Science?"
Expected: 120 seats for CSE B.Tech
```

### Campus Facilities (NEW)
```
Q: "What are the hostel timings?"
Expected: Boys 10 PM, Girls 9 PM entry deadline
```

### Uploaded File (NEW)
```
Q: "How do I connect to campus WiFi?"
Expected: Network name and password from uploaded file
```

---

## Step 6: Error Handling Tests

**Test 1: Backend Down**
- Stop backend server (Ctrl+C)
- Try sending message in frontend
- ✅ Error message: "Unable to connect to the server..."

**Test 2: Empty Query**
- Try sending empty message
- ✅ Nothing happens (validation prevents sending)

**Test 3: Out-of-Scope Query**
```
Q: "How do I learn Python programming?"
Expected: Polite rejection, not hallucination
```

**Test 4: Unknown Information**
```
Q: "What is the president's phone number?"
Expected: "I don't have this information" response
```

---

## Step 7: Performance Tests

**Response Time:**
- Simple query: Should respond in 2-5 seconds
- Complex query: Should respond in 3-7 seconds

**Knowledge Loading:**
- First backend startup: <2 seconds to load 6 files
- File upload reload: <1 second

**Concurrent Queries:**
- Open 2 browser tabs
- Send queries from both simultaneously
- ✅ Both should work (Flask handles concurrent requests)

---

## Expected Results Summary

✅ **6 Knowledge Files Loaded** (admissions, fees, scholarships, exams, academic_programs, campus_facilities)  
✅ **Backend Running** on http://localhost:5000  
✅ **Frontend Working** with multilingual UI  
✅ **File Upload** functional (no restart needed)  
✅ **Queries Answered** accurately from knowledge base  
✅ **Multilingual** responses (EN/HI/GU/Hinglish)  
✅ **Domain Enforcement** working (rejects off-topic)  
✅ **No Hallucination** (states when info unavailable)  

---

## Troubleshooting Common Issues

**Issue: "ModuleNotFoundError: No module named 'flask'"**
```bash
cd backend
pip install -r requirements.txt
```

**Issue: "OPENAI_API_KEY is not set"**
- Check `.env` file exists in `backend/`
- Ensure it contains: `OPENAI_API_KEY=sk-...`
- No quotes needed around the key

**Issue: "Knowledge base loaded: 0 text files"**
- Check files exist in `backend/knowledge/text/`
- Verify file extensions are `.txt`
- Check file permissions (readable)

**Issue: "Unable to connect to server" in frontend**
- Verify backend is running
- Check `curl http://localhost:5000/health` returns OK
- Ensure no firewall blocking port 5000

**Issue: File upload fails**
- Check backend is running
- Verify CORS enabled (already configured)
- Check file size < 10MB
- File type must be .txt or .pdf

**Issue: AI gives wrong answers**
- Verify correct knowledge file contains the information
- Check if context retrieval is working (keywords matching)
- Try rewording the query with more specific keywords

---

## Next Steps After Testing

Once testing is complete:

1. **Add More Knowledge**
   - Create more .txt files or PDFs
   - Upload via upload.html interface
   - Test new knowledge immediately

2. **Customize**
   - Update university name in system prompt
   - Change color scheme in frontend CSS
   - Add university logo

3. **Deploy**
   - Deploy backend to Heroku/AWS
   - Deploy frontend to Netlify/GitHub Pages
   - Update API_URL in frontend JavaScript

4. **Production Enhancements**
   - Add rate limiting
   - Implement user authentication
   - Add usage analytics
   - Set up monitoring

---

## Conclusion

If all tests pass, you have a fully functional:
- ✅ AI-powered helpdesk system
- ✅ Multilingual support
- ✅ Knowledge base with 6+ files
- ✅ File upload capability
- ✅ Professional web interface

**System is production-ready!** 🎉
