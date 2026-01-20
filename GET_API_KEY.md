# 🔑 How to Get Google Gemini API Key (FREE)

## Step-by-Step Guide

### 1. Go to Google AI Studio
Visit: https://makersuite.google.com/app/apikey

### 2. Click "Create API Key"
- You'll see a blue button "Create API Key"
- Click it

### 3. Copy Your Key
- Your API key will appear in a popup
- Click "Copy" to copy it to clipboard
- Save it somewhere safe

### 4. Add to .env File
Open `backend/.env` and replace:
```
GOOGLE_API_KEY=test_key_placeholder
```

With your actual key:
```
GOOGLE_API_KEY=your_actual_key_here
```

### 5. That's It!
Your backend is now ready to use with the LLM.

---

## ⚠️ Important Notes

- The API key is FREE (no credit card required for limited use)
- Keep it private, don't share it
- The key is already in .gitignore, so it won't be committed to Git

## Getting GitHub Token (Optional)

For higher rate limits on GitHub API:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select "repo" scope
4. Generate and copy
5. Add to `backend/.env`:
   ```
   GITHUB_TOKEN=your_token_here
   ```

But this is optional - the project works without it!
