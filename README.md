# GitHub Issue Assistant

AI-powered analysis of GitHub issues with a Streamlit frontend and FastAPI backend. Generates concise summaries, type, priority, suggested labels, impact, and a ready-to-use JSON blob.

**🌐 Live Demo**
- **Frontend**: https://github-issue-assistant-frontend.onrender.com
- **Backend API**: https://github-issue-assistant-backend.onrender.com
  - Health check: https://github-issue-assistant-backend.onrender.com/health

> **💡 For recruiters**: The live frontend is pre-configured with the deployed backend URL (`https://github-issue-assistant-backend.onrender.com`). You can start analyzing GitHub issues immediately—just enter a repo URL (like `https://github.com/facebook/react`) and an issue number, then click Analyze. No setup required!

---

## ✅ Assessment Requirements Met

This project fulfills all SeedlingLabs requirements:

- ✅ **Input UI**: GitHub repository URL and issue number fields
- ✅ **Backend API**: FastAPI endpoint at `/analyze` 
- ✅ **GitHub Integration**: Fetches title, body, and comments via GitHub API
- ✅ **LLM Core**: Uses Groq (Llama 3.3 70B) for intelligent analysis
- ✅ **Structured JSON Output**: Exact required format with summary, type, priority_score, suggested_labels, potential_impact
- ✅ **Output Display**: Beautiful Streamlit UI with multiple tabs
- ✅ **Production-Ready**: Error handling, validation, edge case management
- ✅ **Deployed to Cloud**: Both services live on Render with auto-deploy from GitHub

**🚀 Extra Features Added**:
- In-memory TTL cache (~1 hour) for fast repeated queries
- `/health`, `/stats`, `/cache/clear` endpoints
- JSON copy helper in UI
- Sidebar configuration with usage instructions
- Comprehensive error messages and validation

---

## 🏗️ Tech Stack

- **Backend**: Python 3.11.7, FastAPI, Pydantic, Uvicorn
- **Frontend**: Streamlit
- **LLM**: Groq Llama 3.3 70B via `groq` SDK
- **Data Source**: GitHub REST API
- **Caching**: In-memory TTL cache (3600s)
- **Deployment**: Render (free tier, auto-deploy from GitHub)

---

## 📁 Project Structure

```
github-issue-assistant/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── issue_analyzer.py    # Core LLM + GitHub logic
│   ├── cache.py             # In-memory TTL cache
│   └── requirements.txt     # Backend dependencies
├── frontend/
│   ├── app.py               # Streamlit UI
│   └── requirements.txt     # Frontend dependencies
├── render.yaml              # Render deployment config
└── README.md                # This file
```

---

## ⚡ Quickstart (Local Development)

**Prerequisites**: Python 3.11+, Git, Groq API key (free at [console.groq.com](https://console.groq.com))

```bash
# Clone repository
git clone https://github.com/Gurukiran10/github-issue-assistant.git
cd github-issue-assistant

# Create virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\activate          # Windows
# source .venv/bin/activate        # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Set environment variables
set GROQ_API_KEY=gsk_your_key_here          # use export on macOS/Linux
set BACKEND_URL=http://localhost:8000       # optional for local dev
set GITHUB_TOKEN=ghp_your_token_optional    # optional; increases rate limits

# Start backend (terminal 1)
uvicorn backend.main:app --reload --port 8000

# Start frontend (terminal 2)
streamlit run frontend/app.py --server.port 8501
```

**Local URLs**:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- Health check: http://localhost:8000/health

---

## 📡 API Documentation

### POST /analyze

Analyzes a GitHub issue using AI.

**Request**:
```json
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 1
}
```

**Response**:
```json
{
  "summary": "Run each test in its own iframe to improve test isolation",
  "type": "feature_request",
  "priority_score": "2/5: Low priority due to non-blocking nature and existing workaround",
  "suggested_labels": ["test-improvement", "performance", "refactoring"],
  "potential_impact": "Improved test reliability and isolation for users",
  "reasoning": "I chose feature_request because the issue proposes a new approach..."
}
```

### Other Endpoints

- **GET /health** – Service liveness check
- **GET /stats** – Basic service statistics  
- **POST /cache/clear** – Clear cached analyses

---

## 🎨 Frontend Features

The Streamlit UI includes:

### Sidebar Configuration

**API Endpoint Field**:
- Pre-filled with `https://github-issue-assistant-backend.onrender.com` (deployed backend)
- **For local development**: Change to `http://localhost:8000`
- **For testing**: You can paste any backend API URL here
- The frontend will use whatever URL you specify in this field

**Usage Instructions**:
- Step-by-step guide on how to use the tool
- Tips for entering GitHub URLs correctly

### Main Interface

- **Repository URL**: Enter full GitHub URL (e.g., `https://github.com/facebook/react`)
- **Issue Number**: Numeric ID of the issue to analyze
- **Analyze Button**: Triggers analysis with loading state
- **Results Tabs**:
  - **Summary**: One-sentence issue overview
  - **Metrics**: Type, priority score, potential impact
  - **Labels**: AI-suggested GitHub labels
  - **JSON**: Full response with copy button

---

## 🔧 Backend Implementation

**Core Flow**:
1. Parse repository URL (supports HTTPS, SSH formats)
2. Fetch issue data from GitHub API (title, body, comments)
3. Build intelligent prompt for LLM with context
4. Call Groq API (Llama 3.3 70B)
5. Parse and validate JSON response
6. Return structured output

**Caching Strategy**:
- **Key**: MD5 hash of repo URL + issue number
- **TTL**: 3600 seconds (1 hour) for analysis results
- **Storage**: In-memory via [backend/cache.py](backend/cache.py)
- **Benefit**: Instant responses for repeated queries

**Error Handling**:
- 400 for invalid inputs (malformed URL, missing issue)
- Descriptive errors for GitHub API failures (404, rate limits)
- Graceful fallback for LLM parsing errors
- Timeout protection on API calls

---

## 🚀 Deployment (Render)

Both services are deployed on Render's free tier with auto-deploy from GitHub.

**Backend Configuration**:
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
- Environment variables (set in Render dashboard):
  - `GROQ_API_KEY` (required)
  - `GITHUB_TOKEN` (optional; increases rate limits)

**Frontend Configuration**:
- Start command: `streamlit run frontend/app.py --server.port 10000 --server.address 0.0.0.0`
- Environment variables:
  - `BACKEND_URL` (optional; defaults to deployed backend)
  - `PYTHONUNBUFFERED=1` (for better logging)

**Live URLs**:
- Frontend: https://github-issue-assistant-frontend.onrender.com
- Backend: https://github-issue-assistant-backend.onrender.com

---

## ✅ Testing & Validation

**Manual End-to-End Tests**:

Verified with multiple real-world repositories:
- ✅ **facebook/react** (React issues) - Feature requests and bugs
- ✅ **microsoft/vscode** (VS Code issues) - Complex technical issues
- ✅ **python/cpython** (Python core) - Language improvement proposals
- ✅ **nodejs/node** (Node.js issues) - Performance and API issues
- ✅ **Invalid repository** - Error handling verification

All tests returned proper JSON structure with required fields.

**Health Monitoring**:
- `/health` endpoint monitored by Render
- Returns service status and version info

**Cache Validation**:
- TTL-based expiration tested locally
- Hit/miss behavior verified with repeated requests
- Cache clear endpoint tested for manual invalidation

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **400 Bad Request** | Verify repo URL includes `github.com` and issue number ≥ 1 |
| **GitHub rate limit exceeded** | Add `GITHUB_TOKEN` environment variable |
| **LLM timeout or error** | Retry the request; cached results return instantly on subsequent tries |
| **Wrong backend URL in UI** | Update API endpoint in sidebar to `https://github-issue-assistant-backend.onrender.com` (deployed) or `http://localhost:8000` (local) |
| **Cold start delay (first request slow)** | Normal on Render free tier; takes 30-60s for first request after inactivity |
| **Frontend shows old API endpoint** | Refresh browser with Ctrl+Shift+R (hard refresh) after deployment updates |

---

## 🎯 Future Enhancements (Roadmap)

Potential features to add:

- [ ] **Theme customization**: Light/dark mode toggle with custom accent colors
- [ ] **Persistent settings**: Remember API endpoint and last analyzed repo/issue
- [ ] **Batch analysis**: Analyze multiple issues from same repo at once
- [ ] **Export options**: Download results as CSV or Markdown
- [ ] **Direct issue links**: Paste full GitHub issue URL (auto-extract repo and number)
- [ ] **Analytics dashboard**: Show request latency, cache hit/miss rates
- [ ] **Version endpoint**: Display build version and commit hash
- [ ] **Retry logic**: Automatic retries with exponential backoff for transient failures
- [ ] **Private repos**: OAuth support for analyzing private repository issues
- [ ] **Custom prompts**: Allow users to customize analysis focus areas

---

## 📄 License

MIT

---

## 🙏 Acknowledgments

- Built for **SeedlingLabs** – AI-Native Product Development Internship
- Powered by **Groq (Llama 3.3 70B)** for fast LLM inference
- Leveraging **GitHub REST API** for issue data
- Developed with **FastAPI** and **Streamlit**

---

**Ready to ship! 🚀**

*Created with dedication to "faster, smarter, and radically more efficient" AI-powered development.*
