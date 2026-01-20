# API Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Analyze Issue
**POST** `/analyze`

Analyzes a GitHub issue using AI and returns structured insights.

#### Request
```json
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 12345
}
```

#### Response
```json
{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "bug",
  "priority_score": "3/5: Medium priority due to limited user impact",
  "suggested_labels": ["bug", "ui", "regression"],
  "potential_impact": "Affects users who are experiencing XYZ behavior"
}
```

#### Error Response
```json
{
  "detail": "Issue #12345 not found in facebook/react"
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/facebook/react",
    "issue_number": 12345
  }'
```

#### Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "repo_url": "https://github.com/facebook/react",
        "issue_number": 12345
    }
)

analysis = response.json()
print(analysis["summary"])
```

---

### 2. Health Check
**GET** `/health`

Returns detailed API status and version information.

#### Response
```json
{
  "status": "healthy",
  "service": "GitHub Issue Assistant API",
  "version": "1.0.0"
}
```

#### cURL Example
```bash
curl http://localhost:8000/health
```

---

### 3. Root Endpoint
**GET** `/`

Basic health check endpoint.

#### Response
```json
{
  "status": "healthy",
  "message": "GitHub Issue Assistant API is running"
}
```

---

### 4. API Statistics
**GET** `/stats`

Returns cache statistics and API status.

#### Response
```json
{
  "cached_items": 5,
  "version": "1.0.0",
  "status": "operational"
}
```

#### cURL Example
```bash
curl http://localhost:8000/stats
```

---

### 5. Clear Cache
**POST** `/cache/clear`

Clears all cached analysis results.

#### Response
```json
{
  "message": "Cache cleared successfully"
}
```

#### cURL Example
```bash
curl -X POST http://localhost:8000/cache/clear
```

---

## Error Codes

| Status Code | Meaning | Example |
|-------------|---------|---------|
| 200 | Success | Analysis completed |
| 400 | Bad Request | Invalid repository URL format |
| 404 | Not Found | Issue doesn't exist |
| 500 | Server Error | LLM API failed |

## Common Errors

### Invalid Repository URL
```json
{
  "detail": "Invalid GitHub URL format. Expected: https://github.com/owner/repo"
}
```

### Issue Not Found
```json
{
  "detail": "Issue #12345 not found in facebook/react"
}
```

### API Connection Error
```json
{
  "detail": "Cannot connect to API at http://localhost:8000. Is the backend running?"
}
```

### LLM API Error
```json
{
  "detail": "Failed to generate analysis: API key is invalid"
}
```

---

## Rate Limits

- No hard rate limits on the API itself
- Subject to GitHub API rate limits (60 req/hour unauthenticated, 5000 req/hour authenticated)
- Google Gemini API rate limits apply (60 requests per minute on free tier)

---

## Authentication

Currently, the API is unauthenticated. To use it with private GitHub repositories:

1. Set `GITHUB_TOKEN` environment variable with a GitHub personal access token
2. The token will be automatically used in GitHub API requests

```bash
export GITHUB_TOKEN=your_github_token_here
```

---

## API Testing

### Using Swagger UI
Navigate to: http://localhost:8000/docs

### Using ReDoc
Navigate to: http://localhost:8000/redoc

### Using Postman
1. Import the API endpoint
2. Create a POST request to `/analyze`
3. Set body to JSON:
```json
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 1
}
```

---

## Performance

- Average response time: 5-10 seconds
- Cached results return in <100ms
- Maximum issue body size: ~100KB
- Maximum comments to analyze: 5 most recent

---

## Examples

### Example 1: Analyze React Issue
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/facebook/react", "issue_number": 25000}'
```

### Example 2: Analyze Node.js Issue
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/nodejs/node", "issue_number": 45000}'
```

### Example 3: Check Cache Status
```bash
curl http://localhost:8000/stats
```

---

## Changelog

### Version 1.0.0
- Initial release
- GitHub issue analysis
- JSON output formatting
- Caching support
- Health check endpoints
