# GitHub Issue Assistant - Development Guide

## Local Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment tool (venv)

### Step 1: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

### Step 4: Run Backend
```bash
cd backend
python main.py
```

### Step 5: Run Frontend (in another terminal)
```bash
cd frontend
streamlit run app.py
```

## API Development

### Adding New Endpoints
1. Define Pydantic models in `backend/main.py`
2. Create route in `backend/main.py`
3. Add handler logic in `backend/issue_analyzer.py`
4. Test with curl or Postman

Example:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/facebook/react", "issue_number": 1}'
```

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=backend
```

### Add New Tests
Create test functions in `tests/test_analyzer.py`:
```python
def test_new_feature():
    # Test code here
    assert result == expected
```

## Debugging

### Enable Debug Logging
Edit `backend/main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### View API Documentation
- Open http://localhost:8000/docs (Swagger UI)
- Open http://localhost:8000/redoc (ReDoc)

## Performance Optimization

### Caching
Implement Redis or in-memory caching for:
- Issue data (5 minute TTL)
- Analysis results (1 hour TTL)

### Rate Limiting
Add rate limiting middleware to FastAPI

### Async Processing
Use Celery for background analysis of large issues

## Deployment

### Docker Deployment
```bash
docker build -t github-issue-assistant .
docker run -p 8000:8000 -p 8501:8501 github-issue-assistant
```

### Cloud Deployment
- **Backend**: Deploy to AWS Lambda, Google Cloud Functions, or Railway
- **Frontend**: Deploy to Streamlit Cloud, Vercel, or Netlify

## Troubleshooting

### Issues
- Check logs in backend and frontend terminals
- Verify environment variables are set
- Ensure API keys are valid
- Check network connectivity

### Common Errors
| Error | Solution |
|-------|----------|
| `Port 8000 already in use` | Kill process: `lsof -i :8000` |
| `API key not found` | Set GOOGLE_API_KEY in .env |
| `CORS error` | Check CORS middleware in main.py |

## Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Limit line length to 88 characters

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: Add caching for GitHub API responses

Implement Redis caching with 5-minute TTL for issue data
to improve performance and reduce API calls.

Closes #123
```
