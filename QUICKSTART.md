# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites Check
```bash
python --version  # Should be 3.9+
git --version
```

### 2. Setup
```bash
# Clone/navigate to project
cd d:\seedlinglabs-issue-assistant

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
# Copy example environment
cp backend\.env.example backend\.env

# Edit backend/.env and add:
# GOOGLE_API_KEY=your_key_here
# GITHUB_TOKEN=your_token_here (optional)
```

Get free Google Gemini API key at: https://makersuite.google.com/app/apikey

### 4. Start Backend (Terminal 1)
```bash
cd backend
python main.py
```
✅ Backend running at http://localhost:8000

### 5. Start Frontend (Terminal 2)
```bash
cd frontend
streamlit run app.py
```
✅ Frontend running at http://localhost:8501

### 6. Use the App
1. Enter repository: `https://github.com/facebook/react`
2. Enter issue number: `1`
3. Click "Analyze Issue"
4. View results!

---

## 📚 What You Can Do

- Analyze any public GitHub issue
- Get AI-powered insights on priority, type, labels
- Copy results as JSON
- See cache statistics
- Analyze multiple issues (cached results are fast!)

---

## 🧪 Test It

Try these popular repositories:

| Repository | Issue | Description |
|------------|-------|-------------|
| facebook/react | 1 | React core issue |
| nodejs/node | 1 | Node.js core issue |
| torvalds/linux | 1 | Linux kernel issue |

---

## 🔗 Useful URLs

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Status**: http://localhost:8000/stats

---

## 📖 Documentation

- [README.md](README.md) - Full project documentation
- [API.md](API.md) - API reference
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide

---

## ✨ Key Features

✅ AI-powered GitHub issue analysis
✅ Fast & cached responses
✅ Beautiful Streamlit UI
✅ Production-ready code
✅ Comprehensive error handling
✅ Full documentation

---

## 🆘 Troubleshooting

**API won't connect?**
- Ensure backend is running: `python backend/main.py`
- Check http://localhost:8000 in browser

**Missing API key?**
- Get free key at: https://makersuite.google.com/app/apikey
- Add to backend/.env file

**Timeout errors?**
- Try a smaller issue
- GitHub API might be slow
- Retry after a moment

**Need more help?**
- Check [DEVELOPMENT.md](DEVELOPMENT.md)
- Review backend logs
- Verify .env configuration

---

## 📝 Next Steps

1. ✅ Try analyzing some issues
2. ✅ Explore the API documentation
3. ✅ Review the code structure
4. ✅ Customize prompts if needed
5. ✅ Deploy to cloud (optional)

---

## 🎓 Learning Points

This project demonstrates:
- FastAPI backend architecture
- Prompt engineering for consistent LLM output
- GitHub API integration
- Streamlit frontend development
- Error handling & validation
- Caching strategies
- Git workflow & clean commits

---

**Ready to analyze? Start the application and explore! 🚀**
