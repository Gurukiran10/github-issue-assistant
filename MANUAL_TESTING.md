# 📋 Manual Testing Checklist - Step by Step

## ✅ Tests Completed So Far

- ✅ Python 3.9.13 installed
- ✅ Virtual environment created
- ✅ All dependencies installed (FastAPI, Streamlit, Google API, requests, Pytest)
- ✅ All imports working
- ✅ All Python files have valid syntax
- ✅ IssueAnalyzer class imports correctly
- ✅ Error handling works (detects missing API key)

---

## 📝 Next Manual Tests (What You Need to Do)

### Step 1: Get Your Google API Key
**Time: 2 minutes**

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Open `backend\.env`
5. Replace `test_key_placeholder` with your actual key

### Step 2: Start the Backend Server
**Time: 5 seconds**

Open Terminal 1 and run:
```powershell
cd d:\seedlinglabs-issue-assistant
.\venv\Scripts\activate
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test it's working:**
- Open browser: http://localhost:8000/health
- You should see JSON response with status "healthy"

### Step 3: Start the Frontend
**Time: 5 seconds**

Open Terminal 2 and run:
```powershell
cd d:\seedlinglabs-issue-assistant
.\venv\Scripts\activate
cd frontend
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Browser should open automatically to http://localhost:8501

### Step 4: Test Analysis with Real GitHub Issue
**Time: 30 seconds**

1. In the Streamlit app:
   - Repository URL: `https://github.com/facebook/react`
   - Issue Number: `1`

2. Click "🚀 Analyze Issue"

3. Wait 5-10 seconds for analysis

4. You should see results with:
   - Summary (one line)
   - Type (bug/feature/etc)
   - Priority Score (1-5)
   - Suggested Labels (array)
   - Potential Impact (sentence)

### Step 5: Verify JSON Output
**Time: 30 seconds**

Click the "JSON" tab and verify:
```json
{
  "summary": "...",
  "type": "bug|feature_request|documentation|question|other",
  "priority_score": "X/5: ...",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "..."
}
```

All 5 fields must be present and non-empty.

### Step 6: Test Another Issue
**Time: 30 seconds**

Try a different repository:
- Repository: `https://github.com/nodejs/node`
- Issue Number: `1`

Verify it works for a different repo.

### Step 7: Test Edge Cases
**Time: 1 minute**

Try these to verify error handling:

1. **Invalid repository URL:**
   - URL: `https://gitlab.com/owner/repo`
   - Should show error: "Invalid GitHub URL"

2. **Non-existent issue:**
   - Repository: `https://github.com/facebook/react`
   - Issue: `9999999`
   - Should show error: "Issue not found"

3. **Empty inputs:**
   - Leave URL empty
   - Click analyze
   - Should show error: "Repository URL is required"

### Step 8: Test Caching
**Time: 1 minute**

1. Analyze a repository (e.g., facebook/react #1)
   - Takes 5-10 seconds first time

2. Analyze the SAME repository again
   - Should be instant (<1 second) - this is caching!

3. Check cache stats:
   - Open: http://localhost:8000/stats
   - Should show `cached_items` > 0

---

## ✨ What You're Testing

| Component | Test | Expected Result |
|-----------|------|-----------------|
| **Backend** | http://localhost:8000 | FastAPI running |
| **Frontend** | http://localhost:8501 | Streamlit running |
| **API Endpoint** | POST /analyze | Returns JSON |
| **Analysis** | Facebook React issue #1 | Analyzes successfully |
| **JSON Format** | 5 required fields | All fields present |
| **Error Handling** | Invalid repo URL | Shows error message |
| **Error Handling** | Non-existent issue | Shows error message |
| **Caching** | Same issue twice | 2nd is instant |
| **Cache Stats** | /stats endpoint | Shows count |

---

## 🔍 How to Check If Everything Works

### ✅ Backend is working if:
- You see "Application startup complete"
- http://localhost:8000/health shows JSON
- No error messages in console

### ✅ Frontend is working if:
- http://localhost:8501 opens automatically
- You see input fields for repo URL and issue number
- "🚀 Analyze Issue" button appears

### ✅ Analysis works if:
- After clicking "Analyze", you see a spinner
- Results appear after 5-10 seconds
- All 5 JSON fields are filled
- Text content makes sense

### ✅ Everything is correct if:
- No Python errors in either terminal
- Results are consistent across runs
- Caching works (2nd analysis is instant)
- Error handling shows proper messages

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Run: `pip install -r requirements.txt` |
| "Port 8000 already in use" | Kill process or restart computer |
| "Port 8501 already in use" | Kill Streamlit process or restart |
| "API key not found" | Add GOOGLE_API_KEY to backend/.env |
| "Analysis returns error" | Check API key is valid |
| "Timeout waiting for response" | GitHub API might be slow, try again |
| "JSON parsing error" | LLM might return malformed JSON, retry |

---

## 📊 Test Results Summary

After completing all tests, fill in:

```
Backend Status:     [ ] Working
Frontend Status:    [ ] Working  
Analysis Works:     [ ] Yes
JSON Format OK:     [ ] Correct
Error Handling:     [ ] Working
Caching Works:      [ ] Yes
Ready to Submit:    [ ] Yes
```

---

## ⏱️ Total Time Required

- Setup: 2 minutes (API key)
- Backend start: 1 minute
- Frontend start: 1 minute
- Full testing: 5 minutes

**Total: ~10 minutes**

---

**After completing these tests, your project is verified and ready to submit! ✅**
